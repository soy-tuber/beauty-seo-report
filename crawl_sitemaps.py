# -*- coding: utf-8 -*-
"""Recursively fetch sitemaps for the 8 sites and dump structure summary."""
import urllib.request, gzip, io, sys, re, json
from xml.etree import ElementTree as ET

UA = "Mozilla/5.0 (compatible; SEO-Analyzer/1.0)"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

SEEDS = {
    "pilates-k":    ["https://pilates-k.jp/sitemap.xml"],
    "clubpilates":  ["https://clubpilates.co.jp/sitemap.xml"],
    "rintosull":    ["https://rintosull.jp/sitemap.xml"],
    "npilates":     ["https://npilates.jp/sitemap.xml"],
    "parler":       ["https://www.parler.co.jp/sitemap.xml"],
    "bikatsu":      ["https://www.bikatsu.jp/sitemap.xml"],
    "shiga-seitai": ["https://shiga-seitai.jp/sitemap.xml"],
    # ginza-blv handled separately (HTML crawl) — no XML sitemap
}

def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    if url.endswith(".gz") or data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data

def parse_xml(data):
    # strip BOM / leading whitespace
    try:
        return ET.fromstring(data)
    except ET.ParseError:
        txt = data.decode("utf-8", "ignore")
        txt = txt[txt.find("<?xml"):] if "<?xml" in txt else txt
        return ET.fromstring(txt.encode("utf-8"))

def walk(site, seeds):
    """Return (sub_sitemaps[list of (url,count)], urls[list of (loc,lastmod)])."""
    seen_sm = set()
    queue = list(seeds)
    leaf_summary = []   # (sitemap_url, url_count)
    all_urls = []       # (loc, lastmod, source_sitemap)
    while queue:
        sm = queue.pop(0)
        if sm in seen_sm:
            continue
        seen_sm.add(sm)
        try:
            root = parse_xml(fetch(sm))
        except Exception as e:
            print(f"  !! {site}: failed {sm}: {e}", file=sys.stderr)
            continue
        tag = root.tag.split('}')[-1]
        if tag == "sitemapindex":
            for s in root.findall(f"{SM_NS}sitemap"):
                loc = s.findtext(f"{SM_NS}loc")
                if loc:
                    queue.append(loc.strip())
        elif tag == "urlset":
            cnt = 0
            for u in root.findall(f"{SM_NS}url"):
                loc = u.findtext(f"{SM_NS}loc")
                lm = u.findtext(f"{SM_NS}lastmod")
                if loc:
                    all_urls.append((loc.strip(), (lm or "").strip(), sm))
                    cnt += 1
            leaf_summary.append((sm, cnt))
    return leaf_summary, all_urls

if __name__ == "__main__":
    result = {}
    for site, seeds in SEEDS.items():
        leaf, urls = walk(site, seeds)
        result[site] = {"total_urls": len(urls), "leaves": leaf}
        print(f"\n===== {site}: {len(urls)} urls across {len(leaf)} leaf sitemaps =====")
        for smurl, c in sorted(leaf, key=lambda x: -x[1]):
            print(f"  {c:6d}  {smurl}")
    with open("C:/Users/q0702/seo-analysis/sitemap_structure.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
