# -*- coding: utf-8 -*-
"""Generate a self-contained GitHub Pages report (docs/index.html) from seo.db."""
import sqlite3, re, json, collections, os, datetime, shutil

BASE = "C:/Users/q0702/seo-analysis"
DOCS = f"{BASE}/docs"
os.makedirs(DOCS, exist_ok=True)

DROP_SLUGS = {"column","author","blog","tag","category","news","page","","questionnaire15"}
SITES = ["npilates","shiga-seitai","bikatsu","ginza-blv","pilates-k","parler","rintosull","clubpilates"]
SITE_LABEL = {
  "npilates":"Nピラティス","shiga-seitai":"滋賀整体HOPE","bikatsu":"美活(ジョビアン)",
  "ginza-blv":"GINZA BLV","pilates-k":"pilates K","parler":"パルレ",
  "rintosull":"Rintosull","clubpilates":"CLUB PILATES"}
SITE_URL = {
  "npilates":"https://npilates.jp/","shiga-seitai":"https://shiga-seitai.jp/",
  "bikatsu":"https://www.bikatsu.jp/","ginza-blv":"https://www.ginza-blv.jp/column/",
  "pilates-k":"https://pilates-k.jp/column/","parler":"https://www.parler.co.jp/column/",
  "rintosull":"https://rintosull.jp/","clubpilates":"https://clubpilates.co.jp/"}

KW = {
  "悩み・症状":["腰痛","肩こり","猫背","反り腰","巻き肩","ぽっこり","むくみ","冷え","便秘",
            "自律神経","睡眠","側弯","ヘルニア","坐骨神経","ストレートネック","頭痛","膝","股関節",
            "産後","更年期","生理"],
  "なりたい姿":["ダイエット","痩身","痩せ","くびれ","美脚","美尻","二の腕","小顔","姿勢改善","姿勢",
            "体幹","インナーマッスル","柔軟","可動域","引き締め","脚やせ"],
  "手法":["マシンピラティス","ピラティス","ヨガ","整体","ストレッチ","エステ","加圧","骨盤矯正",
        "骨盤","マッサージ","鍼","パーソナル","筋トレ","トレーニング"],
  "検索意図":["効果","初心者","違い","とは","おすすめ","頻度","回数","体験","口コミ","比較",
          "選び方","自宅","方法","原因","改善","解消","メリット","デメリット","料金"],
}
ALL_KW=[(t,k) for t,ks in KW.items() for k in ks]

def clean_title(t):
    if not t: return ""
    t=re.split(r"[｜|]",t)[0]
    t=re.sub(r"(エステサロン GINZA BLV.*|シンビ.*|Rintosull.*|CLUB PILATES.*|Nピラティス.*|pilates K.*)$","",t)
    return t.strip("　 ・-")

def year_of(lm):
    m=re.match(r"(\d{4})",lm or ""); return m.group(1) if m else "?"

db=sqlite3.connect(f"{BASE}/seo.db"); db.row_factory=sqlite3.Row
arts=collections.defaultdict(list)
for r in db.execute("select * from articles where error=''"):
    slug=(r["slug"] or "").lower().replace(".html","")
    if slug in DROP_SLUGS or not (r["title"] or "").strip(): continue
    arts[r["site"]].append({**dict(r),"ctitle":clean_title(r["title"])})

# --- per-site stats ---
years=sorted({year_of(x["lastmod"]) for s in SITES for x in arts.get(s,[]) if year_of(x["lastmod"])!="?"})
summary=[]
for s in SITES:
    a=arts.get(s,[]); yc=collections.Counter(year_of(x["lastmod"]) for x in a)
    summary.append({"site":s,"label":SITE_LABEL[s],"url":SITE_URL[s],"n":len(a),
                    "years":{y:yc.get(y,0) for y in years},"nodate":yc.get("?",0)})

# --- keyword counts (clean title + h2) ---
counts={s:collections.Counter() for s in SITES}
for s in SITES:
    for x in arts.get(s,[]):
        b=f"{x['ctitle']} {x['h2']}"
        for _,k in ALL_KW:
            if k in b: counts[s][k]+=1
matrix=[]
for theme,k in ALL_KW:
    row={"theme":theme,"kw":k,"by":{s:counts[s][k] for s in SITES},"tot":sum(counts[s][k] for s in SITES)}
    if row["tot"]>0: matrix.append(row)
topkw={s:counts[s].most_common(12) for s in SITES}
titles={s:[x["ctitle"] for x in arts.get(s,[]) if x["ctitle"]] for s in SITES}

data={"summary":summary,"years":years,"matrix":matrix,"topkw":topkw,"titles":titles,
      "sites":SITES,"label":SITE_LABEL,"generated":"2026-06-10",
      "total":sum(len(arts.get(s,[])) for s in SITES)}

HTML = """<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>ピラティス・美容系8サイト SEO分析</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
:root{--bg:#0f1419;--card:#1a2129;--ink:#e6edf3;--mut:#8b98a5;--ac:#4cc9f0;--ac2:#f72585;--line:#2a333d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:"Helvetica Neue",-apple-system,"Hiragino Kaku Gothic ProN","Meiryo",sans-serif;line-height:1.6}
.wrap{max-width:1080px;margin:0 auto;padding:24px 18px 80px}
h1{font-size:1.7rem;margin:.2em 0}h2{font-size:1.25rem;border-left:4px solid var(--ac);padding-left:10px;margin-top:2.2em}
h3{font-size:1.02rem;color:var(--ac)}
.sub{color:var(--mut);font-size:.9rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{padding:6px 9px;border-bottom:1px solid var(--line);text-align:left}
th{color:var(--mut);font-weight:600}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
a{color:var(--ac)}a:hover{color:var(--ac2)}
.pill{display:inline-block;background:#22303c;border-radius:20px;padding:2px 10px;margin:2px;font-size:.8rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}
details{margin-top:8px}summary{cursor:pointer;color:var(--mut)}
.chartbox{position:relative;height:300px}
.hm td{text-align:center;font-variant-numeric:tabular-nums}
.foot{color:var(--mut);font-size:.8rem;margin-top:40px;border-top:1px solid var(--line);padding-top:16px}
.dl a{margin-right:14px}
.tag{font-size:.75rem;color:var(--bg);background:var(--ac);border-radius:4px;padding:1px 6px;margin-left:6px}
ul.titles{columns:2;font-size:.85rem;color:#cdd9e5;margin:0;padding-left:18px}
@media(max-width:600px){ul.titles{columns:1}}
.nav{font-size:.88rem;margin-bottom:14px}.nav a{margin-right:16px}
.related{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.related .card{margin:0}.related h3{margin:.2em 0 .4em}
.badge{font-size:.72rem;color:var(--bg);background:var(--ac2);border-radius:4px;padding:1px 6px;margin-left:6px;vertical-align:middle}
</style></head><body><div class="wrap">
<div class="nav"><a href="./instagram-analysis.html">Instagram競合投稿分析</a><a href="./content/index.html">コンテンツ教育サンプル</a></div>
<h1>ピラティス・美容系8サイト SEO分析</h1>
<p class="sub">お題（記事テーマ）と狙いキーワードの横断分析 ／ 生成日 <b id="gen"></b> ／ SEO記事の核 <b id="tot"></b> 本（店舗お知らせ・お客様の声・テスト記事は除外）</p>

<div class="related">
<div class="card"><h3><a href="./instagram-analysis.html">📱 Instagram競合投稿分析</a><span class="badge">NEW</span></h3>
<p class="sub">美容・フィットネス系47アカウント・397投稿のハッシュタグ／投稿時間帯／CTA分析。
本レポートと同じキーワード辞書で「SEO記事 × Instagram」の出現率を突き合わせ、SNS未開拓テーマと記事化余地を洗い出す教育用レポート。</p></div>
<div class="card"><h3><a href="./content/index.html">✍️ コンテンツ教育サンプル</a></h3>
<p class="sub">分析で見つかった狙いキーワードをもとに作成した、体験記ブログ5本＋Instagram投稿例30本のサンプル集。</p></div>
</div>

<h2>1. サイト別サマリ</h2>
<div class="card"><div class="chartbox"><canvas id="cnt"></canvas></div></div>
<div class="card"><h3>更新の推移（lastmod 年別記事数）</h3><div class="chartbox"><canvas id="yr"></canvas></div>
<p class="sub">※ GINZA BLV / Rintosull はサイトマップに更新日が無く集計対象外（技術SEOの差）。</p></div>
<div class="card"><table id="sumtbl"></table></div>

<h2>2. 狙いキーワード ヒートマップ</h2>
<p class="sub">記事固有部分（クリーン化タイトル＋H2見出し）に各語を含む記事数。屋号サフィックスは除外。色が濃いほど多い。</p>
<div class="card" style="overflow-x:auto"><table class="hm" id="heat"></table></div>

<h2>3. サイト別 狙いキーワード Top & お題リスト</h2>
<div class="grid" id="cards"></div>

<div class="foot">
<p>注記: shiga-seitai の「整体/ストレッチ」は全ページ共通H2ナビ由来の残留を含む。parler は一部重複記事あり。データは公開サイトマップ・公開ページの公開メタ情報に基づく。</p>
</div>
</div>
<script>
const D=__DATA__;
document.getElementById('gen').textContent=D.generated;
document.getElementById('tot').textContent=D.total;
const C=getComputedStyle(document.documentElement);
const AC=C.getPropertyValue('--ac').trim(),MUT=C.getPropertyValue('--mut').trim();
Chart.defaults.color=MUT;Chart.defaults.borderColor='#2a333d';
// counts bar
new Chart(cnt,{type:'bar',data:{labels:D.summary.map(s=>D.label[s.site]),
 datasets:[{label:'SEO記事数',data:D.summary.map(s=>s.n),backgroundColor:AC}]},
 options:{plugins:{legend:{display:false}},indexAxis:'y',scales:{x:{beginAtZero:true}}}});
// year lines
const pal=['#4cc9f0','#f72585','#b5179e','#7209b7','#3a0ca3','#4361ee','#4895ef','#80ffdb'];
new Chart(yr,{type:'line',data:{labels:D.years,
 datasets:D.summary.filter(s=>s.n-s.nodate>0).map((s,i)=>({label:D.label[s.site],
  data:D.years.map(y=>s.years[y]),borderColor:pal[i%pal.length],tension:.3,fill:false}))},
 options:{scales:{y:{beginAtZero:true}}}});
// summary table
let h='<tr><th>サイト</th><th class=num>SEO記事</th><th>主な狙い(Top5)</th><th>備考</th></tr>';
D.summary.forEach(s=>{const tk=(D.topkw[s.site]||[]).slice(0,5).map(x=>x[0]).join(' / ');
 h+=`<tr><td><a href="${s.url}" target="_blank">${D.label[s.site]}</a></td><td class=num>${s.n}</td><td>${tk}</td><td class=sub>${s.nodate?'更新日なし':''}</td></tr>`;});
sumtbl.innerHTML=h;
// heatmap
const mx=Math.max(...D.matrix.map(r=>Math.max(...D.sites.map(s=>r.by[s]))));
let hh='<tr><th>テーマ</th><th>キーワード</th>'+D.sites.map(s=>`<th class=num>${D.label[s]}</th>`).join('')+'<th class=num>計</th></tr>';
let lastT='';
D.matrix.sort((a,b)=>a.theme.localeCompare(b.theme)||b.tot-a.tot).forEach(r=>{
 const tcell=r.theme!==lastT?`<td>${r.theme}</td>`:'<td></td>';lastT=r.theme;
 hh+=`<tr>${tcell}<td>${r.kw}</td>`+D.sites.map(s=>{const v=r.by[s];
  const a=v? (0.12+0.88*v/mx):0;return `<td style="background:rgba(76,201,240,${a})">${v||''}</td>`;}).join('')+`<td class=num><b>${r.tot}</b></td></tr>`;});
heat.innerHTML=hh;
// cards
let cc='';
D.sites.forEach(s=>{const ts=D.titles[s]||[];
 cc+=`<div class="card"><h3>${D.label[s]} <span class="tag">${ts.length}本</span></h3>`;
 cc+='<div>'+(D.topkw[s]||[]).map(x=>`<span class="pill">${x[0]} <b>${x[1]}</b></span>`).join('')+'</div>';
 cc+=`<details><summary>お題リストを開く（${ts.length}本）</summary><ul class="titles">`+
   ts.map(t=>`<li>${t.replace(/</g,'&lt;')}</li>`).join('')+'</ul></details></div>';});
cards.innerHTML=cc;
</script></body></html>"""

html_out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
with open(f"{DOCS}/index.html","w",encoding="utf-8") as f:
    f.write(html_out)
print(f"wrote {DOCS}/index.html ({len(html_out)} bytes), total {data['total']} articles, {len(matrix)} kw rows")
