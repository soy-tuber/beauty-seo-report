# -*- coding: utf-8 -*-
"""Instagram競合投稿データ(instagram_posts.csv)を分析し、
docs/instagram-analysis.html(教育用レポート)を生成する。

データ: 美容・フィットネス系の公開アカウント48件・399投稿のスクレイプ結果
(timestamp / username / likes / caption / comments / url)。
likes = -1 は取得不可(非公開カウント)なので集計から除外する。
"""
import csv, re, json, os, sqlite3, collections, statistics, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(BASE, "docs")
os.makedirs(DOCS, exist_ok=True)

# ---------------- load posts ----------------
posts = []
with open(os.path.join(BASE, "instagram_posts.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ts = r["timestamp"]
        try:
            dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
            jst = dt + datetime.timedelta(hours=9)
        except ValueError:
            continue
        likes = float(r["likes"] or -1)
        posts.append({
            "user": (r["username"] or "").strip(),
            "likes": int(likes) if likes >= 0 else None,  # -1 = 非公開
            "caption": r["caption"] or "",
            "comments": int(float(r["comments"] or 0)),
            "url": r["url"],
            "jst": jst,
        })

def med(vals):
    vals = [v for v in vals if v is not None]
    return round(statistics.median(vals)) if vals else 0

period = (min(p["jst"] for p in posts).strftime("%Y-%m"),
          max(p["jst"] for p in posts).strftime("%Y-%m"))

# ---------------- account stats ----------------
by_user = collections.defaultdict(list)
for p in posts:
    if p["user"]:
        by_user[p["user"]].append(p)

accounts = []
for u, ps in by_user.items():
    likes = [p["likes"] for p in ps if p["likes"] is not None]
    accounts.append({
        "user": u, "n": len(ps),
        "med_likes": med(likes),
        "max_likes": max(likes) if likes else 0,
        "med_com": med([p["comments"] for p in ps]),
        "sum_com": sum(p["comments"] for p in ps),
    })
accounts.sort(key=lambda a: (-a["n"], -a["med_likes"]))

# ---------------- hashtags ----------------
tag_re = re.compile(r"[#＃]([^\s#＃　]+)")
tag_count = collections.Counter()
tag_likes = collections.defaultdict(list)
posts_with_tags = 0
tags_per_post = []
for p in posts:
    tags = tag_re.findall(p["caption"])
    tags_per_post.append(len(tags))
    if tags:
        posts_with_tags += 1
    for t in set(tags):
        tag_count[t] += 1
        if p["likes"] is not None:
            tag_likes[t].append(p["likes"])
top_tags = [{"tag": t, "n": n, "med": med(tag_likes[t])} for t, n in tag_count.most_common(40)]

# ---------------- time-of-day / weekday ----------------
hour_count = [0] * 24
hour_likes = [[] for _ in range(24)]
dow_count = [0] * 7
dow_likes = [[] for _ in range(7)]
for p in posts:
    h, d = p["jst"].hour, p["jst"].weekday()
    hour_count[h] += 1
    dow_count[d] += 1
    if p["likes"] is not None:
        hour_likes[h].append(p["likes"])
        dow_likes[d].append(p["likes"])
hours = [{"h": h, "n": hour_count[h], "med": med(hour_likes[h])} for h in range(24)]
dows = [{"d": ["月", "火", "水", "木", "金", "土", "日"][d], "n": dow_count[d],
         "med": med(dow_likes[d])} for d in range(7)]

# ---------------- caption length & CTA ----------------
buckets = [(0, 100, "〜100字"), (100, 300, "100〜300字"), (300, 600, "300〜600字"),
           (600, 1000, "600〜1000字"), (1000, 10**9, "1000字〜")]
len_stats = []
for lo, hi, label in buckets:
    sel = [p for p in posts if lo <= len(p["caption"]) < hi]
    len_stats.append({"label": label, "n": len(sel),
                      "med": med([p["likes"] for p in sel])})

CTA = ["フォロー", "保存", "いいね", "コメント", "プロフィール", "DM", "LINE", "予約", "無料"]
cta_stats = []
for c in CTA:
    sel = [p for p in posts if c.lower() in p["caption"].lower()]
    cta_stats.append({"cta": c, "n": len(sel),
                      "med": med([p["likes"] for p in sel])})
med_all = med([p["likes"] for p in posts])

# ---------------- SEO keyword cross analysis ----------------
KW = {
  "悩み・症状": ["腰痛", "肩こり", "猫背", "反り腰", "巻き肩", "ぽっこり", "むくみ", "冷え", "便秘",
             "自律神経", "睡眠", "側弯", "ヘルニア", "坐骨神経", "ストレートネック", "頭痛", "膝", "股関節",
             "産後", "更年期", "生理"],
  "なりたい姿": ["ダイエット", "痩身", "痩せ", "くびれ", "美脚", "美尻", "二の腕", "小顔", "姿勢改善", "姿勢",
             "体幹", "インナーマッスル", "柔軟", "可動域", "引き締め", "脚やせ"],
  "手法": ["マシンピラティス", "ピラティス", "ヨガ", "整体", "ストレッチ", "エステ", "加圧", "骨盤矯正",
         "骨盤", "マッサージ", "鍼", "パーソナル", "筋トレ", "トレーニング"],
  "検索意図": ["効果", "初心者", "違い", "とは", "おすすめ", "頻度", "回数", "体験", "口コミ", "比較",
           "選び方", "自宅", "方法", "原因", "改善", "解消", "メリット", "デメリット", "料金"],
}
DROP_SLUGS = {"column", "author", "blog", "tag", "category", "news", "page", "", "questionnaire15"}

def clean_title(t):
    if not t:
        return ""
    t = re.split(r"[｜|]", t)[0]
    t = re.sub(r"(エステサロン GINZA BLV.*|シンビ.*|Rintosull.*|CLUB PILATES.*|Nピラティス.*|pilates K.*)$", "", t)
    return t.strip("　 ・-")

seo_counts = collections.Counter()
seo_total = 0
db_path = os.path.join(BASE, "seo.db")
if os.path.exists(db_path):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    for r in db.execute("select * from articles where error=''"):
        slug = (r["slug"] or "").lower().replace(".html", "")
        if slug in DROP_SLUGS or not (r["title"] or "").strip():
            continue
        seo_total += 1
        body = f"{clean_title(r['title'])} {r['h2']}"
        for ks in KW.values():
            for k in ks:
                if k in body:
                    seo_counts[k] += 1

ig_counts = collections.Counter()
for p in posts:
    for ks in KW.values():
        for k in ks:
            if k in p["caption"]:
                ig_counts[k] += 1

cross = []
for theme, ks in KW.items():
    for k in ks:
        s, g = seo_counts[k], ig_counts[k]
        if s or g:
            cross.append({"theme": theme, "kw": k,
                          "seo": s, "seo_pct": round(100 * s / seo_total, 1) if seo_total else 0,
                          "ig": g, "ig_pct": round(100 * g / len(posts), 1)})

# ---------------- top posts ----------------
def snippet(t, n=90):
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n] + ("…" if len(t) > n else "")

top_posts = sorted([p for p in posts if p["likes"] is not None],
                   key=lambda p: -p["likes"])[:12]
top_posts = [{"user": p["user"], "likes": p["likes"], "com": p["comments"],
              "cap": snippet(p["caption"]), "url": p["url"],
              "date": p["jst"].strftime("%Y-%m-%d")} for p in top_posts]

# ---------------- takeaways (教育用まとめ) ----------------
best_hour = max(hours, key=lambda x: x["n"])
best_dow = max(dows, key=lambda x: x["n"])
gap_seo = sorted([c for c in cross if c["seo_pct"] >= 3 and c["ig_pct"] < c["seo_pct"] / 3],
                 key=lambda c: -c["seo_pct"])[:6]
gap_ig = sorted([c for c in cross if c["ig_pct"] >= 3 and c["seo_pct"] < c["ig_pct"] / 3],
                key=lambda c: -c["ig_pct"])[:6]

data = {
    "generated": datetime.date.today().isoformat(),
    "total": len(posts), "n_users": len(by_user),
    "period": period, "med_all": med_all,
    "unavailable": sum(1 for p in posts if p["likes"] is None),
    "avg_tags": round(statistics.mean(tags_per_post), 1),
    "pct_tags": round(100 * posts_with_tags / len(posts)),
    "seo_total": seo_total,
    "accounts": accounts, "top_tags": top_tags,
    "hours": hours, "dows": dows,
    "len_stats": len_stats, "cta": cta_stats,
    "cross": cross, "top_posts": top_posts,
    "best_hour": best_hour["h"], "best_dow": best_dow["d"],
    "gap_seo": [c["kw"] for c in gap_seo], "gap_ig": [c["kw"] for c in gap_ig],
}

HTML = """<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Instagram競合投稿分析｜美容・フィットネス系48アカウント</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
:root{--bg:#0f1419;--card:#1a2129;--ink:#e6edf3;--mut:#8b98a5;--ac:#4cc9f0;--ac2:#f72585;--line:#2a333d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:"Helvetica Neue",-apple-system,"Hiragino Kaku Gothic ProN","Meiryo",sans-serif;line-height:1.6}
.wrap{max-width:1080px;margin:0 auto;padding:24px 18px 80px}
h1{font-size:1.7rem;margin:.2em 0}h2{font-size:1.25rem;border-left:4px solid var(--ac2);padding-left:10px;margin-top:2.2em}
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
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media(max-width:760px){.grid2{grid-template-columns:1fr}}
details{margin-top:8px}summary{cursor:pointer;color:var(--mut)}
.chartbox{position:relative;height:300px}
.foot{color:var(--mut);font-size:.8rem;margin-top:40px;border-top:1px solid var(--line);padding-top:16px}
.tag{font-size:.75rem;color:var(--bg);background:var(--ac2);border-radius:4px;padding:1px 6px;margin-left:6px}
.nav{font-size:.88rem;margin-bottom:14px}.nav a{margin-right:16px}
.edu{background:#1d2a20;border:1px solid #2e4a35;color:#a8d5b0;font-size:.84rem;border-radius:8px;padding:10px 14px;margin:14px 0}
.take li{margin:.45em 0}
.gap{color:var(--ac2)}
.hm td{text-align:center;font-variant-numeric:tabular-nums}
blockquote{margin:0;color:#cdd9e5;font-size:.85rem}
</style></head><body><div class="wrap">
<div class="nav"><a href="./index.html">← SEO分析トップ</a><a href="./content/index.html">コンテンツ教育サンプル</a></div>
<h1>Instagram競合投稿分析 <span class="tag">教育用</span></h1>
<p class="sub">美容・フィットネス・ピラティス系の公開 <b id="nu"></b> アカウント・<b id="tot"></b> 投稿（<b id="pd"></b>）のキャプション/エンゲージメント分析。
SEO記事分析（<a href="./index.html">8サイト・記事テーマ比較</a>）と対をなす「SNS側のお題研究」。生成日 <b id="gen"></b></p>
<div class="edu">📚 <b>教育用資料</b>: 公開投稿のメタ情報（いいね・コメント数・キャプション）のみを集計した学習用レポートです。
いいね数は各アカウントのフォロワー規模に依存するため、絶対値の比較ではなく「同一アカウント内・カテゴリ内の傾向」を読むのが目的です。likes が非公開の投稿（<span id="unav"></span>件）は集計から除外。</div>

<h2>1. アカウント別サマリ</h2>
<div class="card"><div class="chartbox"><canvas id="acc"></canvas></div>
<p class="sub">投稿数上位15アカウント。棒＝収集投稿数、線＝いいね中央値（右軸・対数）。</p></div>
<div class="card"><details open><summary>全アカウント表（投稿数順）</summary><table id="acctbl"></table></details></div>

<h2>2. ハッシュタグ分析</h2>
<p class="sub">キャプション内の #タグ を集計。付与率 <b id="ptag"></b>%・1投稿あたり平均 <b id="atag"></b> 個。</p>
<div class="card"><div class="chartbox"><canvas id="tags"></canvas></div></div>
<div class="card" id="tagcloud"></div>

<h2>3. 投稿タイミング（日本時間）</h2>
<div class="grid2">
<div class="card"><h3>時間帯別</h3><div class="chartbox"><canvas id="hr"></canvas></div></div>
<div class="card"><h3>曜日別</h3><div class="chartbox"><canvas id="dw"></canvas></div></div>
</div>

<h2>4. キャプションの型（長さ・CTA）</h2>
<div class="grid2">
<div class="card"><h3>文字数といいね中央値</h3><div class="chartbox"><canvas id="len"></canvas></div></div>
<div class="card"><h3>CTA（行動喚起）語の使用率</h3><table id="ctatbl"></table>
<p class="sub">全体のいいね中央値 = <b id="medall"></b>。CTA を含む投稿の中央値との比較。</p></div>
</div>

<h2>5. SEO記事 × Instagram クロス分析</h2>
<p class="sub">同じキーワード辞書（SEO分析と共通）で、<b>SEO記事 <span id="seototal"></span>本</b> と <b>Instagram投稿</b> の出現率(%)を比較。
「検索では戦っているのに SNS では語られていない」テーマ＝コンテンツの空白地帯がわかる。</p>
<div class="card" style="overflow-x:auto"><table class="hm" id="crosstbl"></table></div>

<h2>6. 高エンゲージメント投稿 Top12</h2>
<div class="card"><table id="toptbl"></table></div>

<h2>7. 学びのポイント（教育用まとめ）</h2>
<div class="card"><ul class="take" id="take"></ul></div>

<div class="foot">
<p>データは公開アカウントの公開投稿メタ情報（取得時点のスナップショット）に基づく教育用の集計です。
キャプションは要旨のみ抜粋し、全文は元投稿リンクを参照してください。本ページは noindex 設定です。</p>
</div>
</div>
<script>
const D=__DATA__;
const $=id=>document.getElementById(id);
$('gen').textContent=D.generated;$('tot').textContent=D.total;$('nu').textContent=D.n_users;
$('pd').textContent=D.period[0]+' 〜 '+D.period[1];$('unav').textContent=D.unavailable;
$('ptag').textContent=D.pct_tags;$('atag').textContent=D.avg_tags;
$('medall').textContent=D.med_all;$('seototal').textContent=D.seo_total;
const C=getComputedStyle(document.documentElement);
const AC=C.getPropertyValue('--ac').trim(),AC2=C.getPropertyValue('--ac2').trim(),MUT=C.getPropertyValue('--mut').trim();
// ---- tables & text first (Chart.js が読めなくても表は出す) ----
let ah='<tr><th>アカウント</th><th class=num>投稿</th><th class=num>いいね中央値</th><th class=num>いいね最大</th><th class=num>コメント計</th></tr>';
D.accounts.forEach(a=>{ah+=`<tr><td><a href="https://www.instagram.com/${a.user}/" target="_blank" rel="noopener">${a.user}</a></td>
<td class=num>${a.n}</td><td class=num>${a.med_likes.toLocaleString()}</td><td class=num>${a.max_likes.toLocaleString()}</td><td class=num>${a.sum_com.toLocaleString()}</td></tr>`;});
acctbl.innerHTML=ah;
tagcloud.innerHTML=D.top_tags.map(t=>`<span class="pill">#${t.tag} <b>${t.n}</b></span>`).join('');
let ch='<tr><th>CTA語</th><th class=num>投稿数</th><th class=num>使用率</th><th class=num>いいね中央値</th></tr>';
D.cta.sort((a,b)=>b.n-a.n).forEach(c=>{
 ch+=`<tr><td>${c.cta}</td><td class=num>${c.n}</td><td class=num>${Math.round(100*c.n/D.total)}%</td>
 <td class=num>${c.med.toLocaleString()}${c.med>D.med_all?' <span style="color:'+AC2+'">▲</span>':''}</td></tr>`;});
ctatbl.innerHTML=ch;
// 5. cross
const mxp=Math.max(...D.cross.map(c=>Math.max(c.seo_pct,c.ig_pct)));
let xh='<tr><th>テーマ</th><th>キーワード</th><th class=num>SEO記事数</th><th class=num>SEO出現率</th><th class=num>IG投稿数</th><th class=num>IG出現率</th><th>ギャップ</th></tr>';
let lastT='';
D.cross.sort((a,b)=>a.theme.localeCompare(b.theme)||(b.seo_pct+b.ig_pct)-(a.seo_pct+a.ig_pct)).forEach(c=>{
 const tcell=c.theme!==lastT?`<td>${c.theme}</td>`:'<td></td>';lastT=c.theme;
 const cell=(v,col)=>`<td class=num style="background:rgba(${col},${v?0.10+0.85*v/mxp:0})">${v}%</td>`;
 let gap='';
 if(c.seo_pct>=3&&c.ig_pct<c.seo_pct/3)gap='<span class=gap>SNS未開拓</span>';
 else if(c.ig_pct>=3&&c.seo_pct<c.ig_pct/3)gap='<span style="color:#80ffdb">記事化余地</span>';
 xh+=`<tr>${tcell}<td>${c.kw}</td><td class=num>${c.seo}</td>${cell(c.seo_pct,'76,201,240')}<td class=num>${c.ig}</td>${cell(c.ig_pct,'247,37,133')}<td>${gap}</td></tr>`;});
crosstbl.innerHTML=xh;
// 6. top posts
let th='<tr><th>#</th><th>アカウント</th><th class=num>いいね</th><th class=num>コメント</th><th>投稿日</th><th>キャプション要旨</th></tr>';
D.top_posts.forEach((p,i)=>{th+=`<tr><td>${i+1}</td><td>${p.user}</td><td class=num><b>${p.likes.toLocaleString()}</b></td>
<td class=num>${p.com}</td><td>${p.date}</td><td><blockquote>${p.cap.replace(/</g,'&lt;')}</blockquote>
<a href="${p.url}" target="_blank" rel="noopener" class=sub>元投稿 ↗</a></td></tr>`;});
toptbl.innerHTML=th;
// 7. takeaways
const cta_top=D.cta.filter(c=>c.n>=20&&c.med>D.med_all).map(c=>c.cta);
take.innerHTML=[
 `<b>投稿タイミング</b>: 最多は <b>${D.best_hour}時台</b>・<b>${D.best_dow}曜</b>。ターゲット（美容・健康関心層）の生活リズムに合わせた予約投稿が定石。`,
 `<b>ハッシュタグ</b>: 付与率 ${D.pct_tags}%・平均 ${D.avg_tags} 個/投稿。上位タグ（${D.top_tags.slice(0,3).map(t=>'#'+t.tag).join(' ')}…）は「検索キーワード」と「コミュニティタグ」の2層で構成される。`,
 cta_top.length?`<b>CTA</b>: 「${cta_top.join('」「')}」を含む投稿は全体中央値（${D.med_all}いいね）を上回る傾向。保存・フォロー誘導は依然有効。`:`<b>CTA</b>: 明確ないいね押し上げ効果は今回のサンプルでは確認できず。文脈依存が大きい。`,
 D.gap_seo.length?`<b class=gap>SNS未開拓キーワード</b>（SEOでは頻出・IGでは希薄）: ${D.gap_seo.join(' / ')} — リール・カルーセルの新ネタ候補。`:'',
 D.gap_ig.length?`<b style="color:#80ffdb">記事化余地キーワード</b>（IGでは頻出・SEO記事では希薄）: ${D.gap_ig.join(' / ')} — 検索コンテンツへの展開候補。`:'',
 `<b>注意</b>: いいね数はフォロワー規模の影響が支配的。施策の評価は「同一アカウント内の前後比較」か「エンゲージメント率（要フォロワー数）」で行うこと。`,
].filter(Boolean).map(t=>`<li>${t}</li>`).join('');
// ---- charts (CDN 読込失敗時は表のみ表示) ----
if(window.Chart){
Chart.defaults.color=MUT;Chart.defaults.borderColor='#2a333d';
const A=D.accounts.slice(0,15);
new Chart(acc,{data:{labels:A.map(a=>a.user),datasets:[
 {type:'bar',label:'投稿数',data:A.map(a=>a.n),backgroundColor:AC,yAxisID:'y'},
 {type:'line',label:'いいね中央値',data:A.map(a=>Math.max(a.med_likes,1)),borderColor:AC2,yAxisID:'y2',tension:.3}]},
 options:{scales:{y:{beginAtZero:true},y2:{position:'right',type:'logarithmic',grid:{display:false}}}}});
const T=D.top_tags.slice(0,15);
new Chart(tags,{type:'bar',data:{labels:T.map(t=>'#'+t.tag),datasets:[{label:'使用投稿数',data:T.map(t=>t.n),backgroundColor:AC2}]},
 options:{indexAxis:'y',plugins:{legend:{display:false}},scales:{x:{beginAtZero:true}}}});
new Chart(hr,{data:{labels:D.hours.map(h=>h.h+'時'),datasets:[
 {type:'bar',label:'投稿数',data:D.hours.map(h=>h.n),backgroundColor:AC},
 {type:'line',label:'いいね中央値',data:D.hours.map(h=>h.med),borderColor:AC2,yAxisID:'y2',tension:.3}]},
 options:{scales:{y:{beginAtZero:true},y2:{position:'right',beginAtZero:true,grid:{display:false}}}}});
new Chart(dw,{data:{labels:D.dows.map(d=>d.d),datasets:[
 {type:'bar',label:'投稿数',data:D.dows.map(d=>d.n),backgroundColor:AC},
 {type:'line',label:'いいね中央値',data:D.dows.map(d=>d.med),borderColor:AC2,yAxisID:'y2',tension:.3}]},
 options:{scales:{y:{beginAtZero:true},y2:{position:'right',beginAtZero:true,grid:{display:false}}}}});
new Chart(len,{data:{labels:D.len_stats.map(l=>l.label),datasets:[
 {type:'bar',label:'投稿数',data:D.len_stats.map(l=>l.n),backgroundColor:AC},
 {type:'line',label:'いいね中央値',data:D.len_stats.map(l=>l.med),borderColor:AC2,yAxisID:'y2',tension:.3}]},
 options:{scales:{y:{beginAtZero:true},y2:{position:'right',beginAtZero:true,grid:{display:false}}}}});
}
</script></body></html>"""

html_out = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False))
out = os.path.join(DOCS, "instagram-analysis.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html_out)
print(f"wrote {out} ({len(html_out)} bytes) — {len(posts)} posts / {len(by_user)} accounts, "
      f"{len(cross)} cross-kw rows, seo_total={seo_total}")
