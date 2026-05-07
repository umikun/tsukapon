---
created: 2026-05-07
tags:
  - 調査
  - OSS
  - BI
  - frappe-insights
  - データ可視化
source: https://x.com/L_go_mrk/status/2050853366717206660?s=20
action: 投稿ネタ
---

# frappe/insights — SQLレスでBIダッシュボードが組める"小粒"OSS、その実力と落とし穴

> **TL;DR**
> frappe/insights は ERPNext で有名な Frappe チームが開発する OSS の BI ツール。MySQL/PostgreSQL/DuckDB/BigQuery にステップ式GUIで繋げるのが売りで、V3 から内部エンジンを Ibis に切り替えて拡張性が増した。ただし 2026-05時点で GitHub スター929（Superset 7.2万、Metabase 4.7万）と規模はまだ小さく、ライセンスが **AGPL-3.0** なので「自社プロダクトに組み込んで顧客提供」の用途では要注意。社内ダッシュボード用途なら有力な選択肢。

## 📌 元テキスト（抜粋）

> これ無料でいいんですか...！？
>
> frappe/insights:
>
> SQLが書けなくてもBIダッシュボードが作れるOSSのビジネスインテリジェンス基盤です。MySQL/PostgreSQL/DuckDB/BigQuery対応。
>
> ステップ式のクエリビルダーで「四半期ごとの地域別売上」みたいな分析を、ドラッグ&ドロップで組み立てられます。
>
> https://github.com/frappe/insights

出典: [[Clippings/Post by @L_go_mrk on X 7]]（[@L_go_mrk on X](https://x.com/L_go_mrk/status/2050853366717206660?s=20), 2026-05-03）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Frappe Framework | Python製のフルスタックWebフレームワーク。ERPNextのベース | `frappe framework`, `ERPNext` |
| Insights V3 | 2024〜2026にかけてリリースされた大型刷新版 | `frappe insights v3 ibis` |
| Ibis | Pythonからデータフレーム的にSQLを組み立てるライブラリ。複数DBバックエンドに同じ書き方で繋げる | `ibis-project python` |
| DuckDB | ローカル/組込み型のOLAPエンジン。Parquet/CSVを直接クエリできる | `duckdb analytics` |
| AGPL-3.0 | GPLのネット越し提供版。SaaSとして配信した場合もソース開示義務 | `AGPL SaaS compliance` |
| Query Lineage Graph | クエリ・テーブル・チャートの依存関係を可視化する機能（v3新機能） | `data lineage BI` |
| Datastore | クエリ結果をキャッシュ＋再加工できる倉庫レイヤー | `frappe insights datastore` |
| eCharts | Apache製の可視化ライブラリ。InsightsのチャートUIに採用 | `apache echarts` |

---

## 🧭 背景 / なぜ今これが話題なのか

### Frappeチームと「ERPNext経済圏」

Frappe Technologies はインドのスタートアップで、OSS ERP の **ERPNext** を10年以上開発しているチーム。Frappe Framework（Python+Vue.js）の上に ERP・HR・CRM・Helpdesk・Builder などを横展開しており、Insights はその「BI 担当」として位置付けられている。

ERPNextユーザーが「自社の取引・在庫・経費データを社内ダッシュボードで見たい」というニーズに応えるのが本来の出自で、外部DBへの接続も同じ思想で増えてきた。

### V3 への刷新（2024〜2025）

2024年の Frappeverse カンファレンスで V3 が予告され、2025年に GA。一番大きな変更は **クエリエンジンを Ibis に乗せ替えた** こと。

- 旧版: Insights 独自のクエリビルダー → SQL生成
- V3: GUI操作 → Ibis (Python DataFrame風 API) → 各DBの方言SQLに変換

これにより新しいデータソース追加が「Ibis のバックエンドを書くだけ」で済むようになり、DuckDB対応もこの流れで実現した。

### 2026年4月の主要アップデート

- **Datastore上でのSQL記述**: GUI で組んだクエリを Datastore に落として、その上から SQL で書き直せる。重いクエリの最適化用
- **Query Lineage Graph**: チャート → クエリ → 元テーブル の依存を可視化。循環依存検出にも使える
- v3.9.5（2026-04-29）が最新リリース

### なぜ今 X で拡散されたのか

- ERPNext勢以外にはほぼ無名だったが、**「DuckDB対応」と「ノーコードBI」** の組み合わせが2026年のデータエンジニアリング界隈の関心と一致した
- Metabase の OSS 版が機能制限の方向に行きがちなことへの不満で代替探しが活発
- Frappe Cloud Marketplace 経由のSaaS提供も整備され、「自分でホストしたくない人」のオンボーディングが楽になった

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 無料で使える | AGPL-3.0 でセルフホスト無料。ただし AGPL の制約あり（後述） | [GitHub: insights/license.txt](https://github.com/frappe/insights/blob/develop/license.txt) | ⚠️ ほぼ一致（無料だが条件付き） |
| SQLが書けなくてもBIダッシュボード | ステップ式クエリビルダーUIあり。ただし高度な分析は最終的にSQL/Ibis知識が必要なシーンも | [Frappe Insights README](https://github.com/frappe/insights) | ✅ 一致 |
| MySQL/PostgreSQL/DuckDB/BigQuery 対応 | 公式サポート確認。V3 で Ibis 経由に統合 | [Insights V3 - Adding more data source types](https://discuss.frappe.io/t/insights-v3-adding-more-data-source-types/143595) | ✅ 一致 |
| ドラッグ&ドロップで分析を組み立て | チャート配置はDnDダッシュボード対応。クエリ構築はステップ式（純DnDというよりフォーム積み上げ） | [Frappe Insights Documentation](https://docs.frappe.io/insights/introduction) | ⚠️ ほぼ一致（ニュアンス調整） |
| 「四半期ごとの地域別売上」のような分析が可能 | グルーピング・期間・ピボット機能があり標準で対応 | [Frappe Insights Tools Guide](https://discuss.frappe.io/t/frappe-insights-tools-guide/140202/5) | ✅ 一致 |

---

## 🌐 最新動向（2026-05時点）

- **v3.9.5 リリース（2026-04-29）**: 最新安定版。Datastore SQL とQuery Lineage Graph が目玉 — [GitHub Releases](https://github.com/frappe/insights/releases), 2026-04
- **GitHub スター929 / フォーク452 / オープンIssue 189**: 規模感としてはまだ小〜中規模。Superset 72k・Metabase 47k と比べると桁違いに小さい — [GitHub: frappe/insights](https://github.com/frappe/insights), 2026-05
- **Frappe Cloud Marketplace でSaaS提供**: セルフホストせずに使いたい場合の選択肢が整備された — [Frappe Cloud Marketplace](https://cloud.frappe.io/marketplace/apps/insights), 2026
- **Ibis移行が完了し新バックエンド追加が容易に**: コミュニティでSnowflake・ClickHouseなど追加要望が議論中 — [Insights V3フォーラム](https://discuss.frappe.io/t/insights-v3-adding-more-data-source-types/143595), 2026
- **OpenAlternative の評価では「Metabaseの代替候補」枠**: 競合最有力としてMetabaseが挙げられている — [Best Open Source Frappe Insights Alternatives](https://openalternative.co/alternatives/frappe-insights), 2025-2026

---

## 🧩 関連概念・隣接分野

- **Metabase**: もっとも近いポジションのOSS BI。スター47k、ユーザー多。Insights の比較対象として常に名前が挙がる。Insights は「Frappeエコシステム連携」、Metabase は「単体完結」が違い
- **Apache Superset**: 大規模・本格派のOSS BI。スター72k。SQL Lab+リッチな可視化が強み。導入難度は Insights より高い
- **Redash**: SQL書ける前提のクエリ共有ツール。Insights は逆の方向（SQLレス）
- **DuckDB + dbt + ローカルBI**: 「巨大データウェアハウスを持たずに分析する」最近のトレンド。Insights のDuckDB対応はこの文脈で価値が高い
- **Embedded Analytics**: SaaSプロダクトに分析画面を埋め込む用途。Insights は AGPL のため**この用途には向かない**（後述）

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - Frappe Framework に乗っているので ERPNext 含む既存業務データへの接続が圧倒的に楽
  - V3 で Ibis 採用により今後のDB追加が早い
  - Vue製UIは現代的で、Metabaseより新しい印象
  - スター929 = 「枯れていない」が、活発に開発されているのはむしろポジティブ

- **否定 / 慎重派の主張**:
  - **AGPL-3.0 のリスク**: 自社プロダクトに組み込んで顧客に提供（SaaS含む）すると、Insightsの改変ソースだけでなく**周辺の自社コードまで開示義務が及ぶ可能性**がある（解釈の幅あり、要法務確認）。Embedded Analytics 用途では Metabase Pro や Apache 系のほうが安全
  - **コミュニティ規模**: Issue 189件オープン、コントリビューター数も Metabase/Superset と桁違い。バグを踏んだら自力解決が必要な場面が増える
  - **Frappe Framework依存**: Insights だけ単体で動かすのではなく、Frappeフレームワーク一式（bench, MariaDB, Redis, Node, Python ...）が必要。Docker起動でも依存重め
  - **「ドラッグ&ドロップ」は半分マーケコピー**: クエリ構築は実際には「ステップ式（追加→集計→フィルタ→保存）」のフォーム操作。完全なBIキャンバスではない
  - **本格的な統計・MLは別ツール推奨**: 軸はあくまで集計と可視化。Predictive Analytics 系は同梱されない

- **中立的に見るときの補助線**:
  - 「**社内ダッシュボード用途・ERPNextと併用・データソース数本まで**」なら強い候補
  - 「**自社SaaSに組み込む** or **数百ダッシュボードを横展開する大企業導入**」なら Metabase / Superset / 商用 Looker の方が安全
  - AGPLは「使う」分には無料、「他人に提供する」と義務発生、と覚えると判断しやすい

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] V3 の Ibis 移行で旧版（V2）からの移行コストは実際どれくらいか（クエリ互換性）
- [ ] Frappe Cloud のマネージド版料金と、自前ホストの運用コストの損益分岐
- [ ] Snowflake / ClickHouse 対応の進捗（コミュニティで議論中）
- [ ] Embedded Analytics 用に AGPL を回避する商用ライセンスは提供されているか
- [ ] 日本語UI/タイムゾーン/会計年度（4月始まり）の対応度
- [ ] 同じ「OSS+ノーコードBI」枠の **Lightdash** や **Evidence** との比較

---

## 📚 参考資料

- [GitHub: frappe/insights](https://github.com/frappe/insights) — リポジトリ本体・スター数・最新リリース・技術スタック確認, 取得日 2026-05-07
- [Frappe Insights ドキュメント](https://docs.frappe.io/insights/introduction) — 公式ドキュメント・機能概要, 取得日 2026-05-07
- [Insights V3 - Adding more data source types](https://discuss.frappe.io/t/insights-v3-adding-more-data-source-types/143595) — V3 と Ibis 移行の経緯, 取得日 2026-05-07
- [Product Updates for April 2026 | Frappe Blog](https://frappe.io/blog/product-updates/product-updates-for-april-2026) — 2026-04 の機能アップデート（Datastore SQL、Query Lineage Graph）, 取得日 2026-05-07
- [Insights License (AGPL-3.0)](https://github.com/frappe/insights/blob/develop/license.txt) — ライセンス本文確認, 取得日 2026-05-07
- [Best Open Source Frappe Insights Alternatives](https://openalternative.co/alternatives/frappe-insights) — Metabaseが第一代替候補とされている, 取得日 2026-05-07
- [Apache Superset vs Metabase 比較](https://openalternative.co/compare/apache-superset/vs/metabase) — 競合OSS BIのスター数比較, 取得日 2026-05-07
- [Concerns About AGPL Licenses (LinkedIn記事)](https://www.linkedin.com/pulse/concerns-mit-gpl-agpl-licenses-frappes-licensing-shift-alaa-alsalehi-zptgf) — Frappe系のAGPL運用上の論点, 取得日 2026-05-07

---

## 🗒 メモ

- このネタ、X記事転載に向いている。**「無料で使える！」だけで済ませず AGPL の落とし穴まで触れる**と差別化できる
- 構成案: ①「これ無料でいいんですか…？」のフックを引用 → ②機能紹介（4つのDB対応＋Ibis） → ③**しかしAGPLの罠**でひっくり返す → ④「社内ダッシュボード用途ならアリ」で着地
- ERPNext を実運用していない読者層（=自分のフォロワー）には、ERPNext との接続部分はそこまで強調せず、**「DuckDBにつなげるノーコードBI」** として紹介するのが刺さりそう
- Lightdash / Evidence / Briefer など"次世代BI"勢との比較は別ノートで深掘り余地あり
