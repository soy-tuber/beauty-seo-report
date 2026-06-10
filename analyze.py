# -*- coding: utf-8 -*-
"""Analyze collected articles: お題(clean titles) + 狙いキーワード matrix -> report.md / keywords.csv"""
import sqlite3, re, csv, collections
BASE = "C:/Users/q0702/seo-analysis"

# non-article rows to drop (index / archive / author / tag pages picked up by crawl)
DROP_SLUGS = {"column", "author", "blog", "tag", "category", "news", "page", "", "questionnaire15"}

SITES = ["pilates-k","npilates","bikatsu","shiga-seitai","ginza-blv","parler","rintosull","clubpilates"]

# 狙いキーワード辞書（テーマ別）。各記事の title+description+h2 に含まれるか。
KW = {
  "悩み・症状": ["腰痛","肩こり","肩凝り","猫背","反り腰","巻き肩","ぽっこり","むくみ","冷え","便秘",
              "自律神経","不眠","睡眠","側弯","ヘルニア","坐骨神経","ストレートネック","頭痛","膝","股関節",
              "産後","妊娠","更年期","生理"],
  "なりたい姿": ["ダイエット","痩身","痩せ","減量","くびれ","美脚","美尻","二の腕","小顔","美姿勢",
              "姿勢改善","姿勢","体幹","インナーマッスル","柔軟","可動域","ボディメイク","引き締め","脚やせ"],
  "手法": ["マシンピラティス","ピラティス","ヨガ","整体","ストレッチ","エステ","加圧","リフォーマー",
          "骨盤矯正","骨盤","マッサージ","鍼","パーソナル","筋トレ","トレーニング","コアトレ"],
  "検索意図": ["効果","初心者","違い","とは","おすすめ","頻度","回数","体験","口コミ","比較",
            "選び方","自宅","方法","原因","改善","解消","メリット","デメリット","料金","値段"],
}
ALL_KW = [(theme,k) for theme,ks in KW.items() for k in ks]

def clean_title(t):
    if not t: return ""
    # サイト名サフィックスを除去（区切り: ｜ | ―）
    t = re.split(r"[｜|]", t)[0]
    return t.strip()

def year_of(lastmod):
    m = re.match(r"(\d{4})", lastmod or "")
    return m.group(1) if m else "?"

def main():
    db = sqlite3.connect(f"{BASE}/seo.db"); db.row_factory = sqlite3.Row
    rows = list(db.execute("select * from articles where error='' "))
    # filter out non-article pages
    arts = collections.defaultdict(list)
    for r in rows:
        slug = (r["slug"] or "").lower().replace(".html","")
        if slug in DROP_SLUGS: continue
        if not (r["title"] or "").strip(): continue
        t = clean_title(r["title"])
        # ginza-blv/parler の title末尾サイト名（｜が無い形）対策: 既知サフィックス除去
        t = re.sub(r"(エステサロン GINZA BLV.*|シンビ／エステ.*|コアラボ.*|Rintosull.*|CLUB PILATES.*|Nピラティス.*|pilates K.*)$","",t).strip("　 ・-")
        arts[r["site"]].append({**dict(r), "ctitle": t})

    lines = []
    P = lines.append
    P("# ピラティス・美容系8サイト SEO分析 ―― お題と狙いキーワード\n")
    P(f"対象: SEO記事の核のみ抽出（店舗お知らせ・お客様の声・テスト記事は除外）\n")

    # ---- 1. サイト別サマリ ----
    P("## 1. サイト別サマリ（記事数・年代分布）\n")
    P("| サイト | 有効記事 | 年代分布(lastmod) |")
    P("|---|---|---|")
    for s in SITES:
        a = arts.get(s, [])
        yrs = collections.Counter(year_of(x["lastmod"]) for x in a)
        ydist = " ".join(f"{y}:{c}" for y,c in sorted(yrs.items()) if y!="?")
        if yrs.get("?"): ydist += f" (日付無:{yrs['?']})"
        P(f"| {s} | {len(a)} | {ydist or '—'} |")
    P("")

    # ---- 2. 狙いキーワード マトリクス（記事数ベース）----
    P("## 2. 狙いキーワード出現マトリクス（その語を含む記事数）\n")
    # per site keyword counts over CLEAN title + h2 only
    # (生titleのサイト名サフィックスやサイト共通metaを除外し、記事固有の狙い語だけ拾う)
    def blob(x): return f"{x['ctitle']} {x['h2']}"
    counts = {s: collections.Counter() for s in SITES}
    for s in SITES:
        for x in arts.get(s, []):
            b = blob(x)
            for theme,k in ALL_KW:
                if k in b: counts[s][k]+=1
    # write full matrix CSV
    with open(f"{BASE}/keywords.csv","w",encoding="utf-8-sig",newline="") as f:
        w=csv.writer(f); w.writerow(["theme","keyword"]+SITES+["合計"])
        for theme,k in ALL_KW:
            row=[counts[s][k] for s in SITES]; tot=sum(row)
            if tot>0: w.writerow([theme,k]+row+[tot])
    # report: top keywords per theme (合計上位)
    for theme,ks in KW.items():
        agg=[(k,sum(counts[s][k] for s in SITES)) for k in ks]
        agg=[x for x in agg if x[1]>0]; agg.sort(key=lambda x:-x[1])
        P(f"**{theme}**: " + ", ".join(f"{k}({c})" for k,c in agg[:12]))
        P("")

    # ---- 3. サイト別の狙いキーワードTop ----
    P("## 3. サイト別 狙いキーワード Top（記事数）\n")
    for s in SITES:
        top = counts[s].most_common(10)
        if not top: continue
        P(f"- **{s}** ({len(arts.get(s,[]))}本): " + ", ".join(f"{k}×{c}" for k,c in top))
    P("")

    # ---- 4. お題リスト（各サイト 代表20件）----
    P("## 4. お題リスト（クリーン化タイトル・各サイト先頭20件）\n")
    for s in SITES:
        a = arts.get(s, [])
        P(f"### {s}（{len(a)}本）")
        for x in a[:20]:
            P(f"- {x['ctitle']}")
        if len(a)>20: P(f"- …他 {len(a)-20}本")
        P("")

    out = "\n".join(lines)
    with open(f"{BASE}/report.md","w",encoding="utf-8") as f:
        f.write(out)
    print(f"wrote report.md ({len(out)} chars), keywords.csv")
    print("valid articles per site:", {s:len(arts.get(s,[])) for s in SITES})

if __name__=="__main__":
    main()
