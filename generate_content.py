# -*- coding: utf-8 -*-
"""コンテンツ教育用サンプル: 女性ピラティスインストラクターの体験記
ブログ5記事 + Instagram投稿例30 をマルチページHTMLで生成 -> docs/content/
※ペルソナ・エピソードはすべて架空のサンプル。実在の事実に差し替えて使う前提。"""
import os, html
BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "docs", "content")
os.makedirs(OUT, exist_ok=True)

PERSONA = {
  "name": "佐藤 美樹（さとう・みき）",
  "role": "マシンピラティス インストラクター（歴6年）",
  "creds": "全米ヨガアライアンス RYT200 / PHI Pilates Mat & Equipment 取得",
  "bio": "学生時代からの慢性腰痛をピラティスで改善した経験から指導の道へ。一児の母。"
         "「がんばらないのに体が変わる」感覚を一人でも多くの方に届けたいと思っています。",
}

# ===== ブログ5記事 ============================================================
ARTICLES = [
 {
  "id":"postpartum","kw":"産後 ピラティス 骨盤","date":"2026-06-10","read":"約4分",
  "title":"「産後、体型が戻らない…」私がマシンピラティスで骨盤を立て直した産後3ヶ月の記録",
  "lead":"出産から2ヶ月、久しぶりに全身鏡の前に立って正直ぞっとしました。"
         "下腹はぽっこり、腰は反って、なんだか体の軸がぐにゃぐにゃ。"
         "インストラクターの私でも「これは戻らないかも」と一瞬あきらめかけた、そのときの記録です。",
  "sections":[
    {"h":"産後に体が「ゆるむ」のは、あなたのせいじゃない",
     "ps":["妊娠中に分泌されるリラキシンというホルモンは、骨盤まわりの靭帯をゆるめて出産に備えます。"
           "つまり産後しばらくは、骨盤が動きやすく不安定なのが自然な状態。",
           "私もここで「たるんだ自分」を責めそうになりましたが、まず知ってほしいのは"
           "“ゆるんで当たり前、そこから少しずつ戻す”という順番です。"]},
    {"h":"最初の2週間、私がやったのは「呼吸」だけ",
     "ps":["いきなり腹筋運動…ではなく、私が最初にやり直したのは呼吸でした。"
           "息を吐きながらお腹を薄く凹ませ、骨盤底筋をそっと引き上げる。これだけ。",
           "地味ですが、産後ゆるんだインナーユニット（腹横筋・骨盤底筋）に最初にスイッチを入れる大事な一歩でした。"]},
    {"h":"マシンピラティスを再開して、3ヶ月で変わったこと",
     "ps":["1ヶ月健診で問題なしと言われてから、週2回マシンピラティスを再開。"
           "リフォーマーは負荷を細かく調整できるので、ゆるんだ体でも“支えられながら”正しい動きを思い出せます。",
           "1ヶ月目：反っていた腰が落ち着き、立っているのが楽に。"
           "2ヶ月目：下腹に力が入る感覚が戻る。3ヶ月目：パンツのウエストが元に戻りました。"]},
    {"h":"焦らないで。始める時期は必ず体と相談を",
     "ps":["産後すぐの運動は体への負担が大きいもの。一般的には1ヶ月健診で許可が出てからが目安ですが、"
           "出産の経過は人それぞれです。必ずかかりつけの医師に相談してから始めてください。"]},
  ],
  "takeaway":["産後のゆるみは自然な反応。まず呼吸からインナーに火を入れる",
              "再開はマシンの“支え”を借りると安全に動きを思い出せる",
              "開始時期は自己判断せず必ず医師に確認を"],
  "medical":True,
 },
 {
  "id":"sleep","kw":"寝る前 ピラティス 睡眠 不眠","date":"2026-06-08","read":"約3分",
  "title":"寝つきが悪かった私が「寝る前5分ピラティス」で朝すっきり起きられるようになった話",
  "lead":"レッスンが立て込んでいた時期、布団に入っても頭が冴えて眠れない夜が続きました。"
         "睡眠薬には頼りたくない——そんな私が落ち着いたのが、寝る前のたった5分の習慣でした。",
  "sections":[
    {"h":"眠れない夜は、体じゃなく“呼吸”が浅かった",
     "ps":["眠れないとき、私の呼吸は決まって浅く速くなっていました。"
           "交感神経が優位なまま、体が“戦闘モード”で寝ようとしていたんですね。",
           "ピラティスのゆっくりした胸式呼吸は、吐く時間を長くすることで副交感神経side（休息モード）に切り替わりやすくなります。"]},
    {"h":"私が毎晩やっている寝る前ルーティン3つ",
     "ps":["①仰向けで膝を立てて深呼吸を10回。②膝を左右にゆっくり倒す“ロールダウン”で腰をゆるめる。"
           "③猫のように背骨を丸めて反らす（キャット&カウ）を5回。",
           "どれも布団の上でできる、頑張らない動きばかり。3分〜5分で十分です。"]},
    {"h":"2週間で「朝の体の軽さ」が変わった",
     "ps":["続けて2週間ほどで、寝つくまでの時間が明らかに短くなり、"
           "何より朝起きたときの体の重だるさが減りました。激しい運動より、"
           "“ゆるめて呼吸を整える”ほうが私には合っていたようです。"]},
  ],
  "takeaway":["眠れない夜は呼吸が浅い。吐く息を長く","布団の上でできる3つの動きを5分だけ",
              "目的は鍛えることではなく“ゆるめて整える”こと"],
  "medical":False,
 },
 {
  "id":"autonomic","kw":"自律神経 ピラティス 呼吸","date":"2026-06-05","read":"約4分",
  "title":"自律神経が乱れやすかった私を救った「呼吸とピラティス」のはなし",
  "lead":"季節の変わり目になると、めまい・だるさ・気分の浮き沈みに振り回されていました。"
         "病院で大きな異常はなし。でも毎日しんどい。そんな“なんとなく不調”と私がどう付き合ってきたかを書きます。",
  "sections":[
    {"h":"“なんとなく不調”は、自律神経のサインかも",
     "ps":["自律神経は、活動の交感神経と休息の副交感神経のバランスで成り立っています。"
           "睡眠不足やストレスでこのバランスが崩れると、検査では異常がないのに不調が続くことがあります。"]},
    {"h":"ピラティスの呼吸が「切り替えスイッチ」になる",
     "ps":["ピラティスは動きと呼吸をセットで行います。とくに長く吐く呼吸は、"
           "高ぶった神経を落ち着かせる方向に働きます。私は朝に5分、深い呼吸とともに背骨を動かすだけで、"
           "一日のスタートの“ざわつき”が減りました。"]},
    {"h":"背骨を動かすと、気分まで動く",
     "ps":["背骨をしなやかに動かすエクササイズを続けるうち、肩や首のこわばりがほぐれ、"
           "それに連れて気分の波も穏やかに。体と心がつながっているのを実感した瞬間でした。"]},
    {"h":"つらいときは、無理せず専門家に",
     "ps":["ピラティスはあくまでセルフケアの一つ。症状が強い・長く続くときは、"
           "我慢せず医療機関に相談してください。運動が向かない時期もあります。"]},
  ],
  "takeaway":["“検査異常なしの不調”は自律神経のバランスかも","長く吐く呼吸が高ぶりを鎮める",
              "症状が強いときは必ず医療機関へ"],
  "medical":True,
 },
 {
  "id":"swayback","kw":"反り腰 腰痛 マシンピラティス","date":"2026-06-02","read":"約5分",
  "title":"反り腰で慢性腰痛だった私が、マシンピラティスで「立つのが楽」になるまで",
  "lead":"学生時代から腰が痛いのが“普通”でした。原因は反り腰。"
         "マッサージでは一時的に楽になるだけ。根本から変わったきっかけが、マシンピラティスでした。",
  "sections":[
    {"h":"反り腰は「腰が悪い」のではなく「使い方のクセ」",
     "ps":["反り腰は骨盤が前に傾き、腰だけで体を支えてしまっている状態。"
           "腰そのものが悪いというより、お腹やお尻のサボりを腰がカバーしているクセであることが多いんです。"]},
    {"h":"マシンが“正しい位置”を教えてくれた",
     "ps":["リフォーマーやキャデラックは、体を支えながら動けるので、"
           "「骨盤を立てたままお腹で支える」感覚を体に覚えさせやすい。"
           "自己流マットでは反って代償していた動きが、マシンだと正しく入るのを実感しました。"]},
    {"h":"3ヶ月で“立っているだけで痛い”がなくなった",
     "ps":["週1〜2回を3ヶ月。長時間立っているときの腰の張りが減り、"
           "朝起きたときの「うっ」という痛みがほぼなくなりました。"
           "鍛えたというより、サボっていた筋肉が働き始めた感覚です。"]},
    {"h":"※痛みが強いときの注意",
     "ps":["しびれを伴う・安静にしても痛む強い腰痛は、自己判断で運動せず整形外科の受診を。"
           "原因によっては運動を避けるべきケースもあります。"]},
  ],
  "takeaway":["反り腰は“腰の使いすぎ”のクセ","マシンは正しい支え方を体に教えてくれる",
              "しびれ・強い痛みはまず受診"],
  "medical":True,
 },
 {
  "id":"beginner","kw":"ピラティス 初心者 効果 1ヶ月","date":"2026-05-30","read":"約4分",
  "title":"ピラティス初心者だった頃の自分へ。最初の1ヶ月で本当に感じた体の変化",
  "lead":"今でこそ教える側ですが、私にも「マシンって難しそう」「運動苦手なのに大丈夫?」とビビっていた初心者時代がありました。"
         "最初の1ヶ月、何が変わったのかを当時の日記から振り返ります。",
  "sections":[
    {"h":"1回目：筋肉痛より「呼吸の難しさ」に驚いた",
     "ps":["初回でいちばん難しかったのは、実は動きより呼吸。"
           "「吐きながら動く」だけでこんなに集中するのかと。逆に言えば、頭がスッキリして終わった後は妙に爽快でした。"]},
    {"h":"2週間：姿勢を“注意される前に”自分で気づくように",
     "ps":["デスクワーク中、ふと「あ、今背中丸まってる」と自分で気づけるように。"
           "体の地図（ボディマップ）がはっきりしてきた感覚でした。"]},
    {"h":"1ヶ月：体重より先に“見た目”と“軽さ”が変わる",
     "ps":["体重はほぼ変わらず。でも周りから「姿勢よくなった?」と言われ、"
           "階段で息が切れにくくなりました。ピラティスは“数字より先に質が変わる”運動だと、このとき腹落ちしました。"]},
    {"h":"初心者さんへ：最初の一歩のコツ",
     "ps":["完璧を目指さないこと。「呼吸だけ意識できればOK」くらいの気持ちで。"
           "週1でも続ければ、1ヶ月後の自分が必ず教えてくれます。"]},
  ],
  "takeaway":["最初の壁は動きより“呼吸”","2週間で姿勢への気づきが芽生える",
              "体重より先に“見た目と軽さ”が変わる"],
  "medical":False,
 },
]

# ===== Instagram投稿例(旧30本・参考用) ========================================
# ※ instagram.html の生成は generate_instagram_examples.py(300本+秘訣10ルール)に移行済み。
#   以下の30本は初期サンプルのアーカイブとして残している。
# type: feed / reel / carousel
IG = [
 ("reel","産後","【産後ママ必見】骨盤を立て直す“呼吸”だけエクササイズ🤱",
  "出産後、下腹ぽっこりに悩んでいませんか?🥲\nまず鍛えるより“呼吸”から。\n吐きながらお腹を薄く凹ませる、これだけでインナーにスイッチが入ります✨\n※運動再開は1ヶ月健診後・医師に相談してね",
  ["産後ピラティス","産後ダイエット","骨盤矯正","産後ケア","マシンピラティス","ピラティスのある暮らし"]),
 ("carousel","産後","産後3ヶ月の私の体の変化を正直に公開📖",
  "「戻らないかも」と泣きそうだった私が、週2ピラティスで変わるまで。\nスワイプで1→2→3ヶ月の記録を見てね👉",
  ["産後","産後ピラティス","ビフォーアフター","ピラティス女子","骨盤"]),
 ("feed","産後","産後の腰痛、原因は“腹筋のサボり”かも",
  "赤ちゃんを抱っこする毎日で腰が悲鳴…🥲\n反り腰で腰だけが頑張ってるサインかも。\nお腹で支える感覚、レッスンで一緒に取り戻しましょう☺️",
  ["産後腰痛","抱っこ腰痛","反り腰","ピラティス","骨盤ケア"]),
 ("reel","睡眠","眠れない夜の“寝る前5分ピラティス”😴",
  "布団の上でOK✋\n①深呼吸10回 ②膝を左右に倒す ③背骨を丸めて反らす\n吐く息を長く。それだけで休息モードに切り替わります🌙",
  ["寝る前ピラティス","不眠改善","睡眠の質","おうちピラティス","リラックス"]),
 ("feed","睡眠","“朝の体が重い”が減った私の夜習慣",
  "激しい運動より、ゆるめて呼吸を整えるほうが眠りには効く🌙\n2週間で朝のだるさが変わりました。",
  ["睡眠","快眠習慣","ピラティス","セルフケア","おやすみ前"]),
 ("carousel","睡眠","副交感神経を上げる呼吸、図解しました🫁",
  "交感神経=戦闘モード／副交感神経=休息モード。\n吐く時間を長くするだけ。スワイプで呼吸のやり方👉",
  ["自律神経","睡眠","呼吸法","ピラティス呼吸","リラックス"]),
 ("reel","自律神経","季節の変わり目のだるさに、朝5分の背骨ほぐし🌿",
  "なんとなく不調…それ自律神経かも。\n朝に背骨を動かすと一日の“ざわつき”が減ります☀️\nつらい時は無理せず病院へ🏥",
  ["自律神経","朝活","ピラティス","背骨エクササイズ","不調改善"]),
 ("feed","自律神経","体と心はつながってる、という実感の話",
  "肩のこわばりがほぐれると、気分の波まで穏やかに。\n動きと呼吸をセットにするピラティスならではの感覚です☺️",
  ["自律神経","メンタルケア","ピラティス","呼吸","おうち時間"]),
 ("reel","反り腰","反り腰さんの腰痛、犯人は“お尻のサボり”⁉️",
  "腰が痛いのは腰のせいじゃないことも。\nお腹とお尻が働けば、腰はラクになります🍑\nセルフチェック→保存して試してね📌",
  ["反り腰","腰痛改善","ヒップアップ","マシンピラティス","姿勢改善"]),
 ("carousel","反り腰","壁でできる反り腰セルフチェック🧱",
  "壁に背中をつけて、腰の隙間に手は何枚入る?\n2枚以上は反り腰サインかも。スワイプでチェック法👉",
  ["反り腰","セルフチェック","姿勢","ピラティス","腰痛"]),
 ("feed","反り腰","“立ってるだけで腰が痛い”がなくなった話",
  "マッサージは一時しのぎだった私。\nマシンピラティスで支え方を覚えたら、朝の「うっ」が消えました。",
  ["腰痛","反り腰","マシンピラティス","体験談","姿勢"]),
 ("reel","初心者","ピラティス初心者が最初につまずく“あるある”😂",
  "実は動きより「吐きながら動く」が難しい!\nでも大丈夫、最初は呼吸だけ意識すればOK🙆‍♀️\n運動苦手さんこそ来てほしい💛",
  ["ピラティス初心者","運動苦手","マシンピラティス","はじめてのピラティス","ピラティス女子"]),
 ("carousel","初心者","始める前の不安、ぜんぶ答えます🙋",
  "「体が硬くても?」「年齢は?」「ジムと何が違う?」\nよくある質問にスワイプでお答え👉保存推奨📌",
  ["ピラティスQ&A","初心者","マシンピラティス","体験レッスン","ピラティスとは"]),
 ("feed","初心者","体重より先に変わるのは“見た目と軽さ”",
  "1ヶ月で体重はほぼ変わらず。でも「姿勢よくなった?」と言われました✨\nピラティスは質が先に変わる運動です。",
  ["ピラティス効果","初心者","ボディメイク","姿勢改善","1ヶ月"]),
 ("reel","姿勢","スマホ首、その場で30秒リセット📱",
  "気づくと頭が前に…ストレートネックの入口。\n肩を後ろに回して胸を開く30秒、今やってみて☺️",
  ["スマホ首","ストレートネック","姿勢改善","肩こり","ピラティス"]),
 ("feed","姿勢","“姿勢がいい人”は若く見える、はホント",
  "背骨が動く人は、立ち姿が違う。\nピラティスは見た目年齢にいちばん効くと思っています✨",
  ["姿勢改善","美姿勢","アンチエイジング","ピラティス","美意識"]),
 ("carousel","むくみ","脚のむくみ、寝る前ほぐしで翌朝スッキリ🦵",
  "夕方になるとパンパンな脚に。\n足首回し→ふくらはぎポンプ→脚上げ。スワイプで手順👉",
  ["むくみ解消","脚やせ","ふくらはぎ","寝る前ストレッチ","ピラティス"]),
 ("reel","体幹","ぽっこり下腹に効く“ドローイン”のコツ",
  "腹筋運動より先に、これ。\n息を吐ききってお腹を薄く。これが全ての土台です💪",
  ["ぽっこりお腹","ドローイン","体幹トレーニング","インナーマッスル","ピラティス"]),
 ("feed","体幹","“腹筋100回”より呼吸1回が効く理由",
  "回数より質。深い呼吸でインナーが働くと、お腹は内側から引き締まります。",
  ["体幹","インナーマッスル","くびれ","ピラティス","ボディメイク"]),
 ("carousel","食事","レッスン前後、何食べる?を解説🍽",
  "前は軽く・後はたんぱく質。\n空腹すぎても満腹すぎてもNG。スワイプで具体例👉",
  ["ピラティス食事","ダイエット食","たんぱく質","食事管理","ボディメイク"]),
 ("reel","肩こり","デスクワークの肩こり、1分で軽くなる動き💻",
  "肩甲骨、固まってませんか?\n肩を大きく回して、胸を開く。1分でじんわり軽くなります☺️",
  ["肩こり解消","肩甲骨はがし","デスクワーク","ピラティス","セルフケア"]),
 ("feed","モチベ","続かない人へ。週1でいい、を本気で言いたい",
  "毎日じゃなくていい。週1でも、1ヶ月後の体は応えてくれます。\n“ゼロより1”をいっしょに☺️",
  ["継続は力なり","ピラティス習慣","運動習慣","モチベーション","ピラティス女子"]),
 ("reel","モチベ","三日坊主の私でも続いた理由は“頑張らない”こと",
  "ストイックは続かない。\nゆるめて気持ちいいから、また行きたくなる。それでいいんです🌿",
  ["三日坊主","続けるコツ","ピラティス","ゆる運動","セルフケア"]),
 ("feed","スタジオ","今日のレッスン風景☺️（スタッフ撮影）",
  "今日は産後ママクラス。赤ちゃんの話で笑いながら、しっかり骨盤ケア🤱\n一人じゃ続かないことも、ここなら続く。",
  ["ピラティススタジオ","産後クラス","マシンピラティス","スタジオの日常","ピラティス仲間"]),
 ("carousel","スタジオ","マシンピラティスって何?を写真で紹介📸",
  "リフォーマー・キャデラック…名前は難しいけど大丈夫。\nスワイプでマシンの役割を紹介👉",
  ["マシンピラティス","リフォーマー","ピラティスとは","スタジオ紹介","初心者歓迎"]),
 ("reel","季節","梅雨のだる重に効く“背骨ゆらし”☔",
  "気圧でなんだか不調な季節。\n背骨をやさしく揺らして自律神経を整えましょう🌿",
  ["梅雨だるさ","気圧不調","自律神経","ピラティス","背骨"]),
 ("feed","Q&A","「体が硬いんですけど…」←いちばん多い質問です",
  "硬くて大丈夫。むしろ硬い人ほど変化を感じやすい💛\n柔らかくするためにやるものなので、安心して来てね☺️",
  ["体が硬い","ピラティス初心者","柔軟性","よくある質問","マシンピラティス"]),
 ("reel","美脚","内ももに効かせる“クラム”やってみよ🦵",
  "横向きで膝を開くだけ…なのにプルプル!\nお尻と内ももが目覚めると、脚のラインが変わります✨",
  ["美脚","内もも","ヒップアップ","ピラティス","下半身痩せ"]),
 ("feed","更年期","ゆらぎ世代こそピラティスを、と思う理由",
  "40代から体は変わる。だからこそ“整える運動”を。\n激しさより、呼吸と背骨。ゆらぎ世代の味方です🌷",
  ["更年期","ゆらぎ世代","40代女性","ピラティス","健康習慣"]),
 ("carousel","まとめ","保存版|今週の#おうちピラティス まとめ🏠",
  "産後・睡眠・反り腰…今週の投稿をまとめました。\nスワイプで気になるものから試してね👉保存推奨📌",
  ["おうちピラティス","まとめ","保存版","セルフケア","ピラティス習慣"]),
]

# ===== HTML テンプレート ======================================================
CSS = """
:root{--ink:#3a3a3a;--mut:#9a8f88;--ac:#c98b9e;--ac2:#a86b80;--bg:#fbf7f4;--card:#fff;--line:#eee2da}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:-apple-system,"Hiragino Kaku Gothic ProN","Hiragino Sans","Meiryo",sans-serif;line-height:1.85;font-size:16px}
a{color:var(--ac2);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:740px;margin:0 auto;padding:0 18px 80px}
header.site{background:linear-gradient(135deg,#e8c9d2,#cdb4c6);color:#fff;padding:20px 0;margin-bottom:0}
header.site .wrap{display:flex;align-items:center;justify-content:space-between}
header.site a{color:#fff}.logo{font-weight:700;letter-spacing:.06em;font-size:1.1rem}
nav.top a{margin-left:16px;font-size:.9rem}
.banner{background:#fff6e8;border:1px solid #f0d9a8;color:#8a6d2f;font-size:.82rem;
padding:8px 14px;border-radius:8px;margin:16px auto;max-width:740px}
.crumb{font-size:.82rem;color:var(--mut);margin:18px 0 6px}
h1{font-size:1.55rem;line-height:1.5;margin:.2em 0 .4em}
h2{font-size:1.2rem;border-left:4px solid var(--ac);padding-left:12px;margin:2em 0 .6em}
.meta{color:var(--mut);font-size:.85rem;margin-bottom:8px}
.kw{display:inline-block;background:#f3e7ec;color:var(--ac2);border-radius:20px;padding:2px 12px;font-size:.78rem;margin-right:6px}
.lead{font-size:1.05rem;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin:14px 0}
.takeaway{background:#f6eef1;border:none}.takeaway li{margin:.3em 0}
.author{display:flex;gap:14px;align-items:flex-start;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-top:28px}
.avatar{width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,#e8c9d2,#cdb4c6);
flex:0 0 56px;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.disc{background:#fdf0f0;border:1px solid #f3cccc;color:#9c4a4a;font-size:.85rem;border-radius:10px;padding:12px 16px;margin-top:18px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}
.post{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.tag{font-size:.72rem;border-radius:5px;padding:1px 8px;color:#fff;margin-right:6px}
.t-reel{background:#e0567a}.t-feed{background:#c98b9e}.t-carousel{background:#a86b80}
.theme{font-size:.78rem;color:var(--mut)}
.cap{white-space:pre-wrap;font-size:.92rem;margin:8px 0}
.hash{color:var(--ac2);font-size:.82rem}
.next{display:flex;gap:12px;flex-wrap:wrap;margin-top:24px}
.next a{flex:1 1 220px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:.9rem}
.foot{color:var(--mut);font-size:.8rem;border-top:1px solid var(--line);margin-top:50px;padding-top:18px}
.toc a{display:block;padding:10px 0;border-bottom:1px solid var(--line)}
"""

def page(title, body, active=""):
    return f"""<!DOCTYPE html><html lang="ja"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{html.escape(title)}</title>
<style>{CSS}</style></head><body>
<header class="site"><div class="wrap">
<a href="index.html" class="logo">Studio Miki｜体験記</a>
<nav class="top"><a href="index.html">記事一覧</a><a href="instagram.html">Instagram例</a></nav>
</div></header>
<div class="banner">⚠️ これは<b>コンテンツ教育用のサンプル</b>です。インストラクター名・エピソード・写真はすべて架空。実在の事実に差し替えてご利用ください。</div>
<div class="wrap">{body}
<div class="foot">Studio Miki（架空）｜SEOコンテンツ サンプル ／ 生成: 2026-06-10<br>
本サンプルは noindex 設定。健康に関する記述は一般的情報であり、診断・治療を目的としたものではありません。</div>
</div></body></html>"""

def author_box():
    return f"""<div class="author"><div class="avatar">美樹</div><div>
<b>{PERSONA['name']}</b><br><span class="meta">{PERSONA['role']}／{PERSONA['creds']}</span>
<p style="margin:.5em 0 0;font-size:.9rem">{PERSONA['bio']}</p></div></div>"""

# ---- 記事ページ ----
def render_article(a, prev, nxt):
    secs = ""
    for s in a["sections"]:
        ps = "".join(f"<p>{p}</p>" for p in s["ps"])
        secs += f"<h2>{s['h']}</h2>{ps}"
    take = "".join(f"<li>{t}</li>" for t in a["takeaway"])
    disc = '<div class="disc">※本記事は筆者の個人的な体験に基づく一般的な情報です。効果には個人差があり、痛みや不調が続く場合・妊娠中・産後・持病のある方は、必ず医師など専門家にご相談ください。</div>' if a["medical"] else ""
    nxt_html = ""
    if prev: nxt_html += f'<a href="blog-{prev["id"]}.html">← {prev["title"][:24]}…</a>'
    if nxt:  nxt_html += f'<a href="blog-{nxt["id"]}.html">{nxt["title"][:24]}… →</a>'
    body = f"""
<div class="crumb"><a href="index.html">記事一覧</a> ＞ 体験記</div>
<span class="kw">狙いKW: {a['kw']}</span>
<h1>{a['title']}</h1>
<div class="meta">{PERSONA['name']}・{a['date']}・{a['read']}</div>
<div class="lead">{a['lead']}</div>
{secs}
<div class="card takeaway"><b>この記事のまとめ</b><ul>{take}</ul></div>
{disc}
{author_box()}
<div class="next">{nxt_html}</div>
"""
    return page(a["title"]+"｜Studio Miki", body)

# ---- ハブ(記事一覧) ----
def render_index():
    items = ""
    for a in ARTICLES:
        items += f"""<a href="blog-{a['id']}.html">
<b>{a['title']}</b><br><span class="meta">狙いKW: {a['kw']}・{a['date']}</span></a>"""
    body = f"""
<h1>ピラティス体験記ブログ（サンプル5記事）</h1>
<p class="lead">{PERSONA['name']}が、自身の体験をベースに綴る体験記。"穴"テーマ（産後・睡眠・自律神経）と王道（反り腰・初心者）を狙ったSEOサンプルです。</p>
<div class="toc">{items}</div>
{author_box()}
<div class="next"><a href="instagram.html">📷 Instagram投稿例300本 + 秘訣10ルールを見る →</a></div>
"""
    return page("ピラティス体験記ブログ｜Studio Miki", body)

# ---- Instagramページ ----
def render_ig():
    cards = ""
    for i,(typ,theme,title,cap,tags) in enumerate(IG,1):
        hashs = " ".join("#"+t for t in tags)
        cards += f"""<div class="post">
<div><span class="tag t-{typ}">{typ.upper()}</span><span class="theme">#{i:02d}・{theme}</span></div>
<b>{title}</b>
<div class="cap">{cap}</div>
<div class="hash">{hashs}</div></div>"""
    body = f"""
<div class="crumb"><a href="index.html">記事一覧</a> ＞ Instagram投稿例</div>
<h1>Instagram投稿例 30本（サンプル）</h1>
<p class="lead">フィード/リール/カルーセルの構成・キャプション・ハッシュタグのたたき台です。
1投稿1メッセージ、最初の1行をフック、最後にCTAと保存導線を入れる構成にしています。</p>
<div class="grid">{cards}</div>
{author_box()}
<div class="next"><a href="index.html">← ブログ体験記5記事に戻る</a></div>
"""
    return page("Instagram投稿例30｜Studio Miki", body)

# ---- 出力 ----
def main():
    with open(f"{OUT}/index.html","w",encoding="utf-8") as f: f.write(render_index())
    for i,a in enumerate(ARTICLES):
        prev = ARTICLES[i-1] if i>0 else None
        nxt = ARTICLES[i+1] if i<len(ARTICLES)-1 else None
        with open(f"{OUT}/blog-{a['id']}.html","w",encoding="utf-8") as f:
            f.write(render_article(a, prev, nxt))
    # instagram.html は generate_instagram_examples.py が生成する(300本+秘訣10ルール)
    print(f"wrote {len(ARTICLES)} articles + index -> {OUT}")
    print("instagram.html は python generate_instagram_examples.py で生成してください")
    print("pages:", os.listdir(OUT))

if __name__=="__main__":
    main()
