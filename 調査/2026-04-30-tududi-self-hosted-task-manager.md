---
created: 2026-04-30
tags: [調査, tududi, self-hosted, task-management, GTD, open-source]
source: "[[Clippings/tududi - Organize Life and Work, Self-Hosted or Hosted.md]]"
---

# tududi — 「静かな」セルフホスト型タスク管理OSSの正体

> **TL;DR**
> tududi は GTD思想（Areas → Projects → Tasks）をベースにした MIT ライセンスのセルフホスト型タスク管理ツール。GitHub 2.7k stars、2026年3月に v1.0.0 リリース済みで、CalDAV・OIDC/SSO・Telegram連携など"小規模チームの自前運用"に必要な要素はひと通り揃った段階。Vikunja より軽量、Todoist の代替として個人〜家族用途で評価が高い一方、**通知・リマインダー機能が弱い**のが現時点の最大の弱点。

## 📌 元テキスト（抜粋）

> A calm, open system for life and work. Tasks, projects, notes, and smart views in one place. Self-host the open-source version, or use Tududi Hosted and skip the setup. 2,749 stars. Self-Hosted: €0/forever, MIT-licensed. Tududi Hosted: €5/month or €50/year (early adopter offer). GTD-style Areas → Projects → Tasks structure, Telegram integration, 24 languages, Docker-ready.

出典: [[Clippings/tududi - Organize Life and Work, Self-Hosted or Hosted.md]] / 公式サイト [cloud.tududi.com](https://cloud.tududi.com/)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| GTD (Getting Things Done) | David Allen 提唱の生産性メソッド。仕事を「収集→処理→整理→レビュー→実行」の5ステップで回す | "Getting Things Done" "5 steps GTD" |
| Areas → Projects → Tasks | GTD流の3階層構造。Areas=人生領域（仕事/健康/学習）、Projects=複数タスクで完結する目標、Tasks=実行単位 | "GTD areas of focus" |
| CalDAV | カレンダー・タスクをサーバ間で同期する標準プロトコル。Nextcloud/Baikal等が対応 | "CalDAV protocol" "RFC 4791" |
| OIDC / SSO | OpenID Connect（OAuth2の上に乗る認証層）。社内のGoogle Workspace/Okta/Azure ADでログインを統一 | "OIDC vs SAML" "Keycloak" |
| セルフホスト (Self-Hosted) | クラウドSaaSではなく自前サーバ（VPS, Raspberry Pi等）でアプリを動かす運用形態 | "awesome-selfhosted" |
| Pomodoro | 25分集中＋5分休憩を繰り返す時間管理術。tududiにはタイマー内蔵 | "Pomodoro technique" |
| Sequelize | Node.js向けORM。SQLite/PostgreSQL/MySQLを抽象化 | "Sequelize ORM Node.js" |

---

## 🧭 背景 / なぜ今これが話題なのか

**tududi は2023年頃に Chris Veleris (chrisvel) 氏が個人で立ち上げた OSS。** 公式リポジトリは `chrisvel/tududi` で、2026年4月時点で約2.7k stars。リポジトリ内コミットは911、リリース数は81と、**個人OSSとしてはかなり高頻度で更新されている**プロジェクトの部類に入る。

2024〜2025年にかけて Todoist の値上げと「PROプランへの機能囲い込み」に対する不満が SNS で広がり、**「タスク管理 SaaS 脱出」需要**が増えた。その流れで Vikunja・Super Productivity・tududi・Tasks.org などのセルフホスト系が一気に注目を集めるようになった、というのが2025〜2026年の流れ。XDA Developers の Dhruv Bhutani 氏が2025年8月に「Todoistを捨てて tududi に乗り換えた」という記事を出してから一段認知が広がった経緯がある。

2026年3月28日に **v1.0.0** が出たことで、ベータ感覚で触っていた人たちにも「本番投入候補」として評価される段階に入った。同時に有償ホスティング版「Tududi Hosted」（€5/月）を投入し、**OSS本体は無料で残しつつホスティング収益で運営を継続するデュアルモデル**に踏み出している（Vikunjaやsuper-productivityと同様の戦略）。

UI/UXのコンセプトは "calm, focused"（落ち着いた・集中できる）で、Things 3（macOS有料アプリ）や Apple Reminders に近いミニマル路線。Notion や ClickUp のような何でもアプリ路線とは明確に距離を置いている。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| GitHub 2,749 stars | 2026年4月時点で約2.7k stars。継続的に増加中 | [chrisvel/tududi (GitHub)](https://github.com/chrisvel/tududi) | ✅ 一致 |
| 24言語サポート | 公式が明記、日本語含む | [GitHub README](https://github.com/chrisvel/tududi) | ✅ 一致 |
| MITライセンス | リポジトリの LICENSE で確認 | [chrisvel/tududi](https://github.com/chrisvel/tududi) | ✅ 一致 |
| Docker一発で立ち上がる | `docker pull chrisvel/tududi:latest` → `docker run` で port 3002 起動。SQLite ファイルベース | [docs.tududi.com](https://docs.tududi.com/) | ✅ 一致 |
| Telegram連携でタスク作成 | 実装済み。daily digest（日次ダイジェスト）も配信可能 | [GitHub README](https://github.com/chrisvel/tududi) | ✅ 一致 |
| 「Best for technical users」(自己ホスト版) | 実際は Bhutani の記事でも "easy to install, even if you aren't deep into self-hosting" との評。Docker触れる人なら難易度は中程度 | [XDA Developers](https://www.xda-developers.com/i-ditched-todoist-for-this-open-source-productivity-app/) | ⚠️ ほぼ一致（やや謙遜気味） |
| €5/月 が "early adopter" 価格 | 公式が明示。将来値上げ余地を示唆 | [cloud.tududi.com](https://cloud.tududi.com/) | ✅ 一致 |
| 「ピン留めUI」「ガチに使える通知」あり | **通知/リマインダーは弱い**との実ユーザ評。期日超過の通知が来ない問題は2025年8月時点で指摘あり | [XDA Developers](https://www.xda-developers.com/i-ditched-todoist-for-this-open-source-productivity-app/) | ❌ 要注意（公式は触れていない弱点） |

---

## 🌐 最新動向（2026-04-30時点）

- **v1.0.0 リリース（2026-03-28）** — βを脱して安定版入り。本番運用を検討する人が増えるタイミング — [GitHub Releases](https://github.com/chrisvel/tududi/releases), 2026-03
- **OIDC/SSO 対応が拡充** — Google / Okta / Keycloak / Authentik / PocketID / Azure AD をサポート。社内導入が現実的になった — [GitHub README](https://github.com/chrisvel/tududi), 2026-02
- **CalDAV 双方向同期** — Nextcloud や Baikal と繋がるので、iOS純正リマインダー / macOSカレンダーから tududi のタスクを編集できる経路ができた — [GitHub README](https://github.com/chrisvel/tududi), 2026-02
- **Tududi Hosted（マネージド版）正式提供** — €5/月で自分専用インスタンス + 暗号化バックアップ + 自動アップデート。Docker触りたくないユーザを取り込む施策 — [cloud.tududi.com](https://cloud.tududi.com/), 2026-04
- **Super Productivity ブログの2026年比較記事で取り上げられる** — 「10 Best Open-Source Task Management Apps (2026)」に名前が入り、認知が拡大 — [super-productivity.com](https://super-productivity.com/blog/open-source-productivity-apps-comparison/), 2026

---

## 🧩 関連概念・隣接分野

- **GTD (Getting Things Done)**: tududiの3階層構造（Areas / Projects / Tasks）はそのままGTDのモデル。GTDを知らずに使うと「Areasって何？」で詰まりやすい
- **Vikunja**: 同じくセルフホスト型OSS。Kanbanボード・チーム機能が強く、tududiより"プロジェクト管理寄り"。tududiは"個人の生活OS"寄り
- **Super Productivity**: ポモドーロ＋タスク追跡が主役のローカルファースト OSS。tududiが「サーバ持ちたい人」、Super Productivityが「全部ローカルで済ませたい人」
- **Nextcloud Tasks**: 既にNextcloudを運用してるなら追加コストゼロでCalDAVベースのタスクが使える。tududiもCalDAV経由でNextcloudと繋がるため**併用できる**点に注目
- **awesome-selfhosted**: セルフホストOSS全般のカタログ。tududi含むタスク管理系の比較に使える [awesome-selfhosted.net](https://awesome-selfhosted.net/tags/task-management--to-do-lists.html)
- **CalDAV / iCalendar**: タスク管理OSSを選ぶときの「移行可能性」の鍵。CalDAV対応なら将来の引っ越しが楽

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「Todoistの月額に払い続ける意味がなかった。tududiはミニマルで集中できるし、自分のサーバなのでデータが完全に手元にある」（Bhutani / XDA）。MITライセンス・Docker一発・SSO対応で**小規模チームのセルフホストとしては一段階成熟した**
- **否定 / 慎重派の主張**:
  - 通知・リマインダーが弱い → 期日超過の push 通知や音声リマインダーがない。**「忘れないため」のツールとしては Todoist / TickTick の方が強い**
  - 個人OSSのリスク → コア開発者が事実上1人。BusFactor=1 問題（メンテナがいなくなったら詰む）
  - Tududi Hosted の €5/月 は、**Todoist Pro €4/月 より高い**ので「ホスティングしたい」だけなら経済合理性は薄い。Self-host する技術力があるユーザがメイン顧客
  - 大規模チームのワークフロー（依存関係グラフ、Gantt、リソース管理）は非対応 → そこは OpenProject / Plane / Vikunja の領域
- **中立的に見るときの補助線**:
  - 「個人〜家族で、データは自分の手元に置きたい、UIは静かな方が好き」→ tududiが刺さる
  - 「チームで複雑なプロジェクトを動かす」→ Vikunja か OpenProject
  - 「とにかく忘れたくない、通知が命」→ 現時点ではTodoist / TickTick の方が無難

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Tududi Hosted の SLA・バックアップ復旧時間（公式に記載なし）
- [ ] Telegram連携の認証方式と、Telegram障害時のフォールバック挙動
- [ ] iOSネイティブアプリの計画有無（現状PWAのみ？）
- [ ] CalDAV経由で Apple Reminders と双方向同期できた場合の実用度（ラベル/タグ/サブタスクの欠損率）
- [ ] BusFactor=1 リスクへの対処：コアコントリビュータ拡大計画、フォーク用意があるか
- [ ] 通知が弱い問題に対し、自前で `n8n` + Telegram bot で「期日超過アラート」を組めば実質的に補えるか（n8n運用ノウハウあり → [[project_n8n_filter_new_last_id_gotcha.md]]）
- [ ] Obsidian の Tasks プラグインや Dataview と「役割分担」させた場合の最適配分（Obsidian = 思考ノート、tududi = 実行タスク）

---

## 📚 参考資料

- [chrisvel/tududi - GitHub](https://github.com/chrisvel/tududi) — リリース履歴・スター数・機能一覧の一次ソース, 取得日 2026-04-30
- [Tududi 公式サイト (cloud.tududi.com)](https://cloud.tududi.com/) — 価格・Hosted版仕様・OSS版手順, 取得日 2026-04-30
- [Tududi 公式ドキュメント (docs.tududi.com)](https://docs.tududi.com/) — 技術スタック・Docker手順・認証方式, 取得日 2026-04-30
- [I ditched Todoist for this open-source productivity app — XDA Developers, 2025-08-10](https://www.xda-developers.com/i-ditched-todoist-for-this-open-source-productivity-app/) — 第三者レビュー（メリット/デメリット）, 取得日 2026-04-30
- [10 Best Open-Source Task Management Apps (2026) — Super Productivity Blog](https://super-productivity.com/blog/open-source-productivity-apps-comparison/) — 競合との位置づけ確認, 取得日 2026-04-30
- [Task Management & To-do Lists — awesome-selfhosted](https://awesome-selfhosted.net/tags/task-management--to-do-lists.html) — セルフホスト型タスク管理OSSの全体カタログ, 取得日 2026-04-30
- [Vikunja 公式](https://vikunja.io/) — 主要競合（チーム/Kanban寄り）の比較対象, 取得日 2026-04-30
- [How to Self-Host Tududi for Smarter Project Management — noted.lol](https://noted.lol/tududi/) — 第三者の運用ガイド, 取得日 2026-04-30

---

## 🗒 メモ

- vault運用との関係：Obsidianを「思考のキャンバス」として使い、tududiを「実行タスクキュー」として分けるとハマりそう。今のCLAUDE.mdの自動化（朝note公開・夕方リプ・週次分析）は時刻ベースなので、**期日超過通知が弱い tududi より launchd + n8n の方が信頼性が高い**。tududi導入するなら「個人の生活タスク（家事・買い物・読書リスト）」用途が現実的
- 記事化の角度：「Todoistから乗り換えるべきか？比較4本軸（通知強度 / データ主権 / 値段 / チーム規模）」みたいな構成で1本書ける。SNS運用ネタとしては「自己ホストOSS道楽」シリーズの素材
- 個人的判断：v1.0.0出たばかりで通知が弱いのは怖い。**半年〜1年待ってから検討する派**。今の運用を破壊してまで乗り換える理由は薄い
