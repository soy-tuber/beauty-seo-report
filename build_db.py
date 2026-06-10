# -*- coding: utf-8 -*-
"""Collect SEO-core articles for the 8 sites -> SQLite + CSV.
Stdlib only. Fetches title / meta description / meta keywords / h1 per article."""
import urllib.request, urllib.parse, re, sqlite3, csv, sys, html, time
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree as ET

UA = "Mozilla/5.0 (compatible; SEO-Analyzer/1.0)"
NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
BASE = "C:/Users/q0702/seo-analysis"

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def sm_urls(sitemap_url):
    """All <loc> in a leaf sitemap, with lastmod."""
    root = ET.fromstring(fetch(sitemap_url))
    out = []
    for u in root.findall(f"{NS}url"):
        loc = (u.findtext(f"{NS}loc") or "").strip()
        lm = (u.findtext(f"{NS}lastmod") or "").strip()
        if loc:
            out.append((loc, lm))
    return out

# ---- per-site article-URL collectors -> list of (url, lastmod) -------------
def collect():
    arts = {}  # site -> list[(url, lastmod)]

    # pilates-k: /column/ only (EN slugs)
    arts["pilates-k"] = sm_urls("https://pilates-k.jp/column-sitemap.xml")

    # npilates: all posts (EN slugs = body-concern keywords)
    arts["npilates"] = sm_urls("https://npilates.jp/post-sitemap.xml")

    # bikatsu: /blog/ only (post-sitemap = shop news, excluded)
    arts["bikatsu"] = sm_urls("https://www.bikatsu.jp/blog-sitemap.xml")

    # clubpilates: 3 posts
    arts["clubpilates"] = sm_urls("https://clubpilates.co.jp/post-sitemap.xml")

    # rintosull: column only
    arts["rintosull"] = sm_urls("https://rintosull.jp/sitemap_column.xml")

    # shiga-seitai: only "*-column" path posts (drop info/voice/qanda/campaign)
    rows = sm_urls("https://shiga-seitai.jp/post-sitemap.xml")
    arts["shiga-seitai"] = [(u, lm) for (u, lm) in rows
                            if re.search(r"/[a-z\-]*column/", u)]

    # parler: /column/column_NNN.html (drop the /column/ index and news/)
    rows = sm_urls("https://www.parler.co.jp/sitemap.xml")
    arts["parler"] = [(u, lm) for (u, lm) in rows
                      if re.search(r"/column/column_\d+\.html", u)]

    # ginza-blv: crawl /column/ listing pagination (no XML sitemap)
    seen, ga = set(), []
    page = 1
    while page <= 30:
        url = "https://www.ginza-blv.jp/column/" if page == 1 \
              else f"https://www.ginza-blv.jp/column/page/{page}/"
        try:
            doc = fetch(url).decode("utf-8", "ignore")
        except Exception:
            break
        links = set(re.findall(r'href="(https://www\.ginza-blv\.jp/column/[^"]+)"', doc))
        links = {l for l in links if not re.search(r"/column/(page/|category/)", l)}
        new = [l for l in links if l not in seen]
        if not new:
            break
        for l in new:
            seen.add(l); ga.append((l, ""))
        page += 1
    arts["ginza-blv"] = ga
    return arts

# ---- per-article metadata extraction ---------------------------------------
def meta_of(url):
    try:
        raw = fetch(url, timeout=25)
    except Exception as e:
        return {"error": str(e)[:120]}
    doc = raw.decode("utf-8", "ignore")
    def grab(pat):
        m = re.search(pat, doc, re.I | re.S)
        return html.unescape(m.group(1)).strip() if m else ""
    title = grab(r"<title[^>]*>(.*?)</title>")
    desc = grab(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']') \
        or grab(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\'](.*?)["\']')
    kw = grab(r'<meta[^>]+name=["\']keywords["\'][^>]+content=["\'](.*?)["\']')
    h1 = grab(r"<h1[^>]*>(.*?)</h1>")
    h1 = re.sub(r"<[^>]+>", "", h1).strip()
    h2s = [re.sub(r"<[^>]+>", "", x).strip()
           for x in re.findall(r"<h2[^>]*>(.*?)</h2>", doc, re.I | re.S)]
    h2s = [x for x in h2s if x][:8]
    return {"title": title, "description": desc, "keywords": kw,
            "h1": h1, "h2": " | ".join(h2s)}

def slug_of(url):
    p = urllib.parse.urlparse(url).path.rstrip("/")
    seg = p.split("/")[-1]
    return urllib.parse.unquote(seg)

def main():
    arts = collect()
    print("== collected article URLs ==")
    for s, v in arts.items():
        print(f"  {s:14s} {len(v)}")
    tasks = [(s, u, lm) for s, v in arts.items() for (u, lm) in v]
    print(f"  TOTAL {len(tasks)} articles to fetch\n")

    results = []
    def work(t):
        s, u, lm = t
        m = meta_of(u)
        m.update({"site": s, "url": u, "lastmod": lm, "slug": slug_of(u)})
        return m
    done = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(work, tasks):
            results.append(r); done += 1
            if done % 50 == 0:
                print(f"  fetched {done}/{len(tasks)}")

    # SQLite
    db = sqlite3.connect(f"{BASE}/seo.db")
    db.execute("DROP TABLE IF EXISTS articles")
    db.execute("""CREATE TABLE articles(
        site TEXT, url TEXT, slug TEXT, lastmod TEXT,
        title TEXT, description TEXT, keywords TEXT, h1 TEXT, h2 TEXT, error TEXT)""")
    db.executemany("""INSERT INTO articles
        (site,url,slug,lastmod,title,description,keywords,h1,h2,error)
        VALUES (:site,:url,:slug,:lastmod,:title,:description,:keywords,:h1,:h2,:error)""",
        [{**{k: r.get(k, "") for k in
            ["site","url","slug","lastmod","title","description","keywords","h1","h2","error"]}}
         for r in results])
    db.commit()

    # CSV
    with open(f"{BASE}/articles.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["site","url","slug","lastmod","title","description","keywords","h1","h2","error"])
        for r in results:
            w.writerow([r.get(k,"") for k in
                ["site","url","slug","lastmod","title","description","keywords","h1","h2","error"]])

    errs = sum(1 for r in results if r.get("error"))
    print(f"\nDONE: {len(results)} rows -> seo.db / articles.csv  (errors: {errs})")

if __name__ == "__main__":
    main()
