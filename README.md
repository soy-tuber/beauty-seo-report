# beauty-seo-report

ピラティス・美容系8サイトの **SEO分析**（お題＝記事テーマ／狙いキーワードの横断比較）。

📊 **レポート（GitHub Pages）**: https://soy-tuber.github.io/beauty-seo-report/

## 対象サイト
pilates-k.jp / clubpilates.co.jp / rintosull.jp / npilates.jp / ginza-blv.jp / parler.co.jp / bikatsu.jp / shiga-seitai.jp

## 何をしているか
1. 各サイトの `sitemap.xml` を再帰展開（ginza-blv のみ HTML クロール）
2. **SEO記事の核だけ抽出**（店舗お知らせ・お客様の声・テスト記事を除外 → 約765本）
3. 各記事の `title` / `meta description` / `keywords` / `h1` / `h2` を取得
4. クリーン化タイトル＋H2から **狙いキーワードを集計**（屋号サフィックスは除外）

## ファイル
| ファイル | 内容 |
|---|---|
| `crawl_sitemaps.py` | サイトマップ構造の調査 |
| `build_db.py` | 記事収集 → `seo.db` / `articles.csv` |
| `analyze.py` | 集計 → `report.md` / `keywords.csv` |
| `generate_html.py` | `docs/index.html`（公開レポート）生成 |
| `seo.db` | SQLite（articles テーブル） |
| `docs/` | GitHub Pages 配信ディレクトリ |

## 再生成
```bash
python build_db.py      # 記事を取り直す（数分）
python analyze.py       # 集計し直す
python generate_html.py # HTMLを作り直す
```

データは公開サイトマップ・公開ページの公開メタ情報に基づく。レポートは `noindex` 設定。
