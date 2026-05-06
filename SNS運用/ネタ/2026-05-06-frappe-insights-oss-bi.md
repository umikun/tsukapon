---
created: 2026-05-06
tags: [調査, BI, OSS, Frappe, データ分析, ノーコード]
source: https://x.com/L_go_mrk/status/2050853366717206660
action: 投稿ネタ
---

# Frappe Insights──"SQL不要BI"の正体と、Metabase/Superset 二強時代に挑むインド発OSS

> **TL;DR**
> - AI駆動塾（[@L_go_mrk](https://x.com/L_go_mrk)・1.7万フォロワー）が紹介した **frappe/insights** は、**ERPNext提供元のFrappe社**が開発する100% OSS の BIツール。Vue UI + Ibis（SQL DataFrame）+ eCharts のスタックで、ステップ式クエリビルダー＋ドラッグ&ドロップダッシュボードを実現
> - 投稿は **3,803view / 保存47（保存率1.236%）** で本日調査の中で**最高保存率**。「これ無料でいいんですか…！？」型のOSS発掘フックが効いている
> - ただし OSS BI 市場の主要6社（Metabase / Apache Superset / Redash / Lightdash / Evidence / Grafana）に **Frappe Insights は入っていない**。**ERPNext生態系のユーザー以外には知名度が低く、本格採用は限定的**

---

## 🗒 メモ

> ⚠️ このセクションは **冒頭に配置**（2026-05-06 ルール）。「使い方」を最初に書いてアクションが起きやすい設計

### このネタの使い道（仮説）

**SNS活用候補**:

- 🟢 **保存率1.236%は本日調査4本中最高** → このパターンの構造を深掘りする価値あり
  - 保存率ランキング（本日調査）:
    1. **AI駆動塾 Frappe Insights**: 1.236%（imp 3,803 / 保存47）⭐ 最高
    2. チャエン Claude金融エージェント: 0.795%（imp 21,494 / 保存171）
    3. Mario Nawfal LLMスタック: 0.69%（imp 144,536 / 保存1,001）
    4. Rikuo WebMCP: 0.38%（imp 240,817 / 保存922）
  - **「これ無料でいいんですか…！？」型のフック**＋**画像1枚**＋**短い箇条書き機能説明**＋**GitHubリンク**で**最強の保存欲求パターン**
- 🟢 **W19保存型単発②（5/9予定）への応用**: AI駆動塾型の「OSS発掘フック+1機能特化説明+GitHubリンク」が**A4 1枚テンプレに最適**。マトリクス型より、**シンプルなOSS紹介型**のほうが保存率高い可能性
- 🟡 **連投シリーズ⑦（leaf）の派生**: 既存の「○○が△△を置き換える」型に並ぶ第3パターンとして「**○○系OSSの実態**」型を派生候補に追加可能（既存ストックには「○○のベストスタックって本当に最適？」型が入っているが、これとは別軸）

### 戦略的な接続点

- **AI駆動塾アカウントの分析**: フォロワー1.7万・「OSS紹介ボット」系の発信で**継続的に保存獲得**するモデル。模倣可能な発信戦術として価値あり
- **W19戦略「imp量より関係濃度」軸との関係**: imp 3,803 で保存47は**「imp少なくても刺さる人には刺さる」**典型例。批評型ポジ転換の方向性を裏付け
- **連投⑤@Tokimoさん共感返信パターン**: AI駆動塾投稿に**「自分も Obsidian × Claude Code でこの種のBIツール検討中」**型の共感型リプを入れる枠あり

### 派生する仮説／問い

- 「**○○ボット型アカウント**」（OSS紹介・記事まとめ・LLMニュース等）の保存率は **個人クリエイター系より高い**？
- AI駆動塾型の「**フック1行＋機能箇条書き4-5個＋画像1枚**」フォーマットを **W19保存型単発②**に流用可能か
- Frappe Insights 自体を**Tsukapon vault の Daily Log analytics と連携**できるか（DuckDB対応なので技術的に可能性あり）

### 投稿フォーマットの当たり

- **批評型リプを入れる場合**: 「Frappe Insights は ERPNext生態系の文脈外だと採用ハードル高そう。Metabase / Superset との使い分けに興味あります」型の **比較軸提示型**
- **保存型単発②の改良**: 「これ無料でいいんですか…！？」型のフックで **AIニュース×OSS発掘** ハイブリッドにする
- **note記事化**: 「AI業界の人が**個人開発でこっそり使いたいOSS BI 5選**」型のリスト記事候補

### 自分の運用への応用

- **Tsukapon vault Daily Log のデータを Frappe Insights で可視化**できる可能性（DuckDB経由）
  - ただし Frappe Framework のセットアップ自体が重い（フルスタック）→ 個人運用には**過剰な気がする**
  - 軽量な代替として **Metabase Docker版** or **DuckDB + Apache Superset** が現実的
- **OSS BI ツール発掘** をテーマにした連投題材は**W20候補ストック**に追加価値あり

---

## 📌 元テキスト（抜粋）

> これ無料でいいんですか...！？
> frappe/insights: SQLが書けなくてもBIダッシュボードが作れるOSSのビジネスインテリジェンス基盤です。MySQL/PostgreSQL/DuckDB/BigQuery対応。ステップ式のクエリビルダーで「四半期ごとの地域別売上」みたいな分析を、ドラッグ&ドロップで組み立てられます。

出典: [AI駆動塾（@L_go_mrk）の投稿](https://x.com/L_go_mrk/status/2050853366717206660) / 2026-05-03 08:22 UTC / 画像1枚（559×347px）添付 / 1.7万フォロワー・認証済個人

### 投稿のエンゲージメント数（取得日 2026-05-06）

| 指標 | 値 | 評価 |
|---|---:|---|
| ビュー（imp）| 3,803 | 中規模 |
| いいね | 48 | ER 1.26% |
| リツイート | 2 | RT率 0.053% |
| **ブックマーク** | **47** | **保存率 1.236%（同業比 12倍）** ⭐ |
| 引用RT | 2 | 議論性は弱い |
| 返信 | 0 | 会話性ゼロ |

→ **保存率1.236%は本日調査4本の中で最高**。RT・返信が少ない一方で、保存だけが突出する **「個人で試したい」型の典型** バズ。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Frappe Insights** | Frappe社（ERPNext提供元）開発のOSS BIツール。100%オープンソース、ステップ式クエリビルダー＋ダッシュボード | `frappe/insights GitHub` |
| **Frappe Framework** | Pythonフルスタック web フレームワーク。ERPNext と同じ技術基盤 | `Frappe Framework Python` |
| **ERPNext** | Frappe社が開発する OSS ERPシステム。世界10万社以上で利用 | `ERPNext open source` |
| **BI（Business Intelligence）** | 企業データの可視化・分析ツール。Tableau/Power BI/Looker が3強 | `BI tool comparison 2026` |
| **Metabase** | OSS BI市場最大シェア。**60,000+ 組織採用**。Docker 1コンテナで起動 | `Metabase open source BI` |
| **Apache Superset** | エンタープライズ向けOSS BI最強。Airbnb / Lyft / Twitter等で採用 | `Apache Superset enterprise` |
| **DuckDB** | インメモリ型OLAP DB。2026年に急速に普及（Pandas置き換え候補）| `DuckDB analytics` |
| **Ibis** | Python の DataFrame API で SQL を抽象化するライブラリ。Frappe Insights のクエリ層 | `Ibis Python SQL` |
| **eCharts** | Apache 開発の OSS チャート可視化ライブラリ。Frappe Insights の描画層 | `eCharts visualization` |
| **クエリビルダー** | SQL を書かずにマウス操作でクエリを組み立てる UI | `query builder no-code` |
| **ステップ式** | クエリ作成を「テーブル選択→フィルタ→集計→可視化」の段階で進めるUI | `step-by-step query` |
| **OSS BI市場6強** | Metabase / Apache Superset / Redash / Lightdash / Evidence / Grafana | `open source BI tools 2026` |

---

## 🧭 背景 / なぜ今これが話題なのか

### Frappe社の立ち位置

**Frappe Technologies**（インド・ムンバイ拠点）は、**ERPNext** を中心とした OSS ERPエコシステムを2008年から提供。世界**10万社以上**で利用される ERPの代表的OSS。Frappe Insights は **ERPNext のデータを可視化する内製ツール**として開発が始まり、後に**汎用BIツール**として独立。

### 2025〜2026: OSS BI市場の活況

OSS BIツール市場は2025〜2026年に活況。背景：

- **Tableau / Power BI / Lookerの値上げ** で OSS への移行需要拡大
- **DuckDB の台頭**（インメモリOLAP）で「自前環境でBI」のハードルが激減
- **GenAI ブーム**でデータ分析の民主化が加速（自然言語クエリ等）

OSS BIの**主要6強**: Metabase（60,000+組織）、Apache Superset（Airbnb等）、Redash、Lightdash、Evidence、Grafana。**Frappe Insights はこの主要6強には入っていない**。

### AI駆動塾[@L_go_mrk](https://x.com/L_go_mrk)の発信文脈

[@L_go_mrk](https://x.com/L_go_mrk) は **AI・OSS発掘系アカウント**（1.7万フォロワー）。**「これ無料でいいんですか…！？」型のフック**で OSS紹介を継続発信。今回も同パターン。**保存率1.236%は同業比12倍**で、**「個人で試したい」型の保存欲求**を最大化する型として完成度が高い。

### 2026-05-03 投稿のタイミング

GW中（5月連休・3日目）の投稿。GW中はTL自体が薄いが、**「あとで試そう」型のOSS紹介**は逆に保存されやすい時期。投稿は **大バズには至らずも保存率突出**という典型的な発掘系コンテンツの数字構造。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| **SQLが書けなくても BIダッシュボードが作れる** | 公式ドキュメントで「ステップ式クエリビルダー」を確認。SQL不要は事実だが、**複雑なクエリは結局 SQL を書いた方が早い** | [Frappe Insights GitHub](https://github.com/frappe/insights) | ✅ 一致（基本ケース）|
| **OSS のビジネスインテリジェンス基盤** | 100% OSS（GitHub公開・Apache 2.0等のOSSライセンス）| [GitHub](https://github.com/frappe/insights) | ✅ 一致 |
| **MySQL/PostgreSQL/DuckDB/BigQuery対応** | 公式README で4種DB対応を確認 | [Frappe Insights公式](https://frappe.io/insights) | ✅ 一致 |
| **ステップ式クエリビルダー** | テーブル選択→ジョイン→フィルタ→計算→可視化の段階別UI を確認 | [Frappe Insights Docs](https://docs.frappe.io/insights/introduction) | ✅ 一致 |
| **ドラッグ&ドロップでダッシュボード組み立て** | 公式機能として確認（charts on dashboard, drag-drop arrangement）| [Frappe Insights公式](https://frappe.io/insights) | ✅ 一致 |
| 「これ無料でいいんですか…！？」のフック | OSS で完全無料は事実。ただし**自前ホスティングのインフラコスト**は発生（GPU不要だが Frappe Framework の Python環境が必要）| [Frappe Cloud](https://cloud.frappe.io/marketplace/apps/insights) | ⚠️ 一致（ただし"運用コスト"の前提が抜けている）|

---

## 🌐 最新動向（2026-05時点）

- **Frappe Insights は2026-02時点で active development** 継続中。最新リリースは2025年〜2026年初頭にかけて積み上げ — [Frappe Insights Releases](https://github.com/frappe/insights/releases), 2026-02
- **OSS BI市場は Metabase が最大シェア**。60,000+組織採用、Docker 1コンテナで起動可能。Self-hosted Community Editionは無料、Cloud版は$85/月〜（5ユーザー）— [Domo OSS BI 2026](https://www.domo.com/learn/article/open-source-bi-tools), 2026
- **Apache Superset** は Airbnb / Lyft / Twitter / 多数の大企業で本番運用。**RBAC・Row-level security・OAuth/SAML** でエンタープライズ要件カバー — [Basedash 2026](https://www.basedash.com/blog/best-open-source-bi-tools-compared-2026), 2026
- **Metabase置き換え候補**: Lightdash、Evidence、Supaboard等の **新興BIツール**が台頭。AI連携（自然言語クエリ）が新標準化 — [Supaboard 2026](https://supaboard.ai/blog/top-5-metabase-alternatives-for-seamless-embedded-analytics-in-2025), 2026
- **DuckDB の急速な普及**で「ローカルBI」が現実的に。Frappe Insights も DuckDB対応で恩恵を受ける位置 — [Basedash 2026](https://www.basedash.com/blog/best-open-source-bi-tools-compared-2026), 2026

---

## 🧩 関連概念・隣接分野

- **Metabase**: OSS BI最大シェア。**Frappe Insights の最大の競合**。Docker 1コンテナで即起動、SQL不要UIが洗練。**個人・小規模チームならまず Metabase を検討すべき**
- **Apache Superset**: エンタープライズ最強。**大規模・複雑な要件**ではこちらが正解。Frappe Insights は規模感が違う
- **DuckDB**: インメモリOLAP DB。Frappe Insights の DuckDB対応はこの流れに乗る形。**個人で大量データ分析**したい時の主要技術
- **ERPNext**: Frappe社のフラッグシップERP。Frappe Insights の本来のメイン用途は **ERPNext のデータ可視化**。ERPNext使っていない人にはハードル高め
- **Looker / Power BI / Tableau**: 商用BI3強。OSS BI が伸びる背景にこれらの値上げあり

---

## 🪞 反対意見 / 別角度からの視点

### 肯定側の主張（AI駆動塾含む）

- **完全無料 OSS** で BIダッシュボード構築可能
- **SQL不要のクエリビルダー** で非エンジニアもアクセス可能
- **DuckDB対応** で個人ローカル運用も可能
- **Frappe Framework** のエコシステムで ERPNext との連携が強力

### 否定 / 慎重派の主張

- **OSS BI市場の主要6強に入っていない**: Metabase / Superset の知名度・コミュニティ規模に大きく劣る。**ドキュメント・トラブルシュート情報が薄い**可能性
- **Frappe Framework のセットアップが重い**: Python フルスタックのため、Docker 1個で済む Metabase より**インストール・運用負荷が高い**
- **ERPNext生態系外では採用ハードル高い**: 本来は ERPNext の付属ツール。**汎用BI として使う価値はあるが、Metabase の方が成熟している**
- **「SQL不要」の罠**: 簡単なクエリは確かに不要だが、**複雑な分析は結局SQL or Pythonが必要**。「完全に SQL から解放される」は誇張気味
- **エンタープライズ機能不足**: RBAC / Row-level security / OAuth等は Apache Superset の方が充実
- **AI駆動塾の発信パターン**: 「これ無料でいいんですか…！？」は**保存欲求トリガー**として強力だが、**OSS紹介ボット型の量産発信**で個別ツールの選定軸までは深く扱わない傾向

### 中立的に見るときの補助線

> **OSS BI を選ぶなら、まず Metabase。Frappe Insights は ERPNext使ってる場合の優先候補**

| シーン | 推奨ツール |
|---|---|
| 個人・小規模チーム・初学者 | 🟢 Metabase（Docker 1個で起動） |
| エンタープライズ・大規模 | 🟢 Apache Superset |
| ERPNext運用中で BI連携したい | 🟢 Frappe Insights |
| インフラ最小・ローカル中心 | 🟡 DuckDB + 軽量UI（Lightdash 等）|
| AI連携・自然言語クエリ重視 | 🟡 Supaboard / Evidence |

→ **「AI駆動塾の発掘＝Frappe Insights が最適解」とは限らない**。用途別に検討するのが現実解。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Frappe Insights の **個人ローカル運用ハンズオン**（Docker起動・DuckDB接続・Tsukapon Daily Log を可視化）
- [ ] Metabase との **同一データセット可視化比較**（同じCSVを両方で扱って体験差を見る）
- [ ] **AI駆動塾アカウントの発信戦略分析**（OSS紹介投稿の頻度・保存率・フォロワー成長への寄与）
- [ ] 「**これ無料でいいんですか…！？**」型フックの **再現可能性**（同パターンを自分でやって保存率1%超えるか）
- [ ] DuckDB + Frappe Insights で **Tsukapon Daily Log の可視化**ができるか（vault運用への応用）
- [ ] **Frappe Cloud（マネージドサービス）の料金**：自前運用が重い場合の代替

---

## 📚 参考資料

- [GitHub - frappe/insights](https://github.com/frappe/insights) — 一次情報・機能・技術スタック, 取得日 2026-05-06
- [Frappe Insights公式](https://frappe.io/insights) — プロダクトページ・スクリーンショット, 取得日 2026-05-06
- [Frappe Insights Documentation - Introduction](https://docs.frappe.io/insights/introduction) — 機能詳細, 取得日 2026-05-06
- [Frappe Insights Releases](https://github.com/frappe/insights/releases) — リリース履歴・更新頻度, 取得日 2026-05-06
- [Frappe Cloud Marketplace](https://cloud.frappe.io/marketplace/apps/insights) — マネージド版料金, 取得日 2026-05-06
- [12 Open Source BI Tools and Free BI Picks for 2026 - Domo](https://www.domo.com/learn/article/open-source-bi-tools) — OSS BI市場マップ, 取得日 2026-05-06
- [Best open source BI tools compared 2026 - Basedash](https://www.basedash.com/blog/best-open-source-bi-tools-compared-2026) — 主要6強比較, 取得日 2026-05-06
- [Top 5 Metabase Alternatives - Supaboard](https://supaboard.ai/blog/top-5-metabase-alternatives-for-seamless-embedded-analytics-in-2025) — 新興BI比較, 取得日 2026-05-06
- [Metabase vs Apache Superset - Startupik](https://startupik.com/metabase-vs-apache-superset-open-source-bi-tools-compared/) — 二強比較, 取得日 2026-05-06

---

*作成日: 2026-05-06 / 調査者: Claudian + WebSearch + WebFetch / 環境: Tsukapon vault内モード / 新テンプレ（メモ冒頭）準拠*
