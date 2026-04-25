---
created: 2026-04-25
tags: [調査, 認証, OSS, OpenAuth, Auth0, Clerk, セルフホスト]
source: "[[Clippings/Post by @L_go_mrk on X 1.md]]"
---

# OpenAuth は本当に Auth0 / Clerk の代替になるのか？個人開発者向け検証メモ

> **TL;DR**
> OpenAuth は SST チーム製のOSSで「**Hono ベースの OAuth 2.0 発行者（issuer）**」として動く。Lambda / Cloudflare Workers / Node / Bun に置けるのでセルフホストの自由度は高い。ただし**意図的にユーザー管理機能を持たない**ため、Auth0 や Clerk のような「ダッシュボード・MFA UI・組織管理・監査ログ込みのフルIAM」とは比較レイヤーが違う。「代替」という言い方は半分正しく半分ミスリード。フル代替を狙うなら **Stack Auth / Logto / SuperTokens / Better Auth** の方が筋が良い。

## 📌 元テキスト（抜粋）

> 個人開発者の方は見て欲しい。 Auth0やClerkの代替になるかもしれないOSS認証サーバーが公開されていました...！！！ 自分のインフラに置けるのでユーザー情報も外部に預けずに済みます。 https://github.com/anomalyco/openauth

出典: [[Clippings/Post by @L_go_mrk on X 1.md]] / [元ポスト](https://x.com/L_go_mrk/status/2047641200937541963)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| OpenAuth | SSTチーム製のOSS OAuth 2.0 issuer。Honoベース、サーバーレス前提 | OpenAuth SST Hono |
| SST | TypeScript製のフルスタック・サーバーレスインフラ管理ツール | SST AWS Cloudflare |
| Hono | エッジ/サーバーレスで動く軽量Webフレームワーク | Hono framework |
| OAuth 2.0 / OIDC | 認可・認証の業界標準プロトコル | OAuth OIDC IdP |
| Issuer / IdP | アクセストークンを発行する側のサーバー | OAuth issuer IdP |
| Auth0 | OktaグループのフルマネージドIDaaS | Auth0 enterprise IAM |
| Clerk | モダンなUI付き認証SaaS（Next.jsエコシステムで人気） | Clerk Next.js |
| Stack Auth | OSSのAuth0/Clerk代替。UIごと提供 | stack-auth |
| Better Auth | TypeScript製OSS認証フレームワーク（フルスタック向け） | Better Auth TypeScript |
| Logto | OSSコア+クラウドのIAM。SaaS/AI向けポジション | Logto IAM |
| SuperTokens | OSS認証。Firebase Auth/Cognito代替を謳う | SuperTokens core |

---

## 🧭 背景 / なぜ今これが話題なのか

**2024年12月: OpenAuth Beta発表**
SST（Serverless Stack）チームが「OpenAuth Beta」をブログで公開（[SST Blog](https://sst.dev/blog/openauth-beta/)）。「Hono の上に乗った issuer 関数を、Lambda や Workers にそのまま置ける OAuth プロバイダ」というポジショニング。SSTの inbuilt component として `Auth` から差し替える形で提供された。

**2025年3月: v0.4.3 リリース、リポジトリは `anomalyco/openauth` に**
最新の安定版は @openauthjs/openauth@0.4.3（2025-03-04）。リポジトリは `sst/openauth` から `anomalyco/openauth` に移管された経緯があり（SSTメンテナがanomaly社で立ち上げた組織と思われる）、**機能的には同一**。スター数は6.9k、MITライセンス（[GitHub anomalyco/openauth](https://github.com/anomalyco/openauth)）。

**2026年4月時点: ベータのままだが個人開発者界隈で再注目**
公式ドキュメント [openauth.js.org](https://openauth.js.org/) も整備されており、「自前インフラで認証サーバーを動かす」選択肢として日本語SNSでも周期的にバズる。元ポストもその波の1つ。

**周辺の競合状況**
2026年現在、OSSセルフホスト認証は群雄割拠：
- **Stack Auth**: Auth0/Clerk代替を真正面から名乗る。UIまでセットで提供（[stack-auth.com](https://stack-auth.com/)）
- **Logto**: SaaS/AIアプリ向けのポジション、OSSコア+クラウドのハイブリッド（[Logto blog 2026](https://blog.logto.io/top-7-auth-providers-2026)）
- **SuperTokens**: Firebase Auth / AWS Cognito 代替を謳うOSS（[supertokens-core](https://github.com/supertokens/supertokens-core)）
- **Better Auth**: TypeScriptネイティブのフレームワーク型OSS、2025年以降急伸
- **Keycloak**: 旧来のJava製IAMの王者、エンタープライズで根強い

OpenAuth はこの中でも「**極小のissuerとして使う**」尖った位置づけで、UIや組織管理を持たない分シンプル。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Auth0やClerkの代替になるかもしれないOSS認証サーバー」 | OAuth 2.0 issuer としては代替になり得るが、Auth0/Clerk のフル機能（UI・MFA・組織・ロール管理・監査ログ）は意図的に未提供。レイヤーが違う | [GitHub README](https://github.com/anomalyco/openauth) / [SST Blog](https://sst.dev/blog/openauth-beta/) | ⚠️ ほぼ一致（フル代替ではない） |
| 「公開されていました…！！！」（最近公開のニュアンス） | 2024年12月にBeta公開、2025年3月にv0.4.3。元ポスト時点ですでに**1年4ヶ月以上前**から存在する。新発見ではない | [SST Blog 2024-12](https://sst.dev/blog/openauth-beta/) | ❌ 要注意（新しくない） |
| 「自分のインフラに置ける」 | ◯ Lambda / Workers / Node / Bun / コンテナで動く。状態は最小限のKV（DynamoDB / Cloudflare KV等）に逃がせる | [openauth.js.org](https://openauth.js.org/) | ✅ 一致 |
| 「ユーザー情報も外部に預けずに済む」 | ◯ 自前インフラ運用なのでデータ主権は守れる。**ただしユーザーレコード自体は自分で設計・実装する必要**がある（ユーザー管理機能はOpenAuth側に存在しない） | [README "intentionally does not solve user management"](https://github.com/anomalyco/openauth) | ⚠️ ほぼ一致（責任は自分） |
| 個人開発者向け | ベータのままなのと、UI・MFA・組織管理を自分で書く前提なので、**「最速で綺麗にログイン画面を出したい」個人開発には逆に不向き**。むしろ Clerk / Stack Auth の方が早い | [Logto 2026比較](https://blog.logto.io/top-7-auth-providers-2026) / [zenn 認証基盤比較](https://zenn.dev/mergelog/articles/3088d40ef1b07b) | ❌ 要注意 |

---

## 🌐 最新動向（2026-04時点）

- **OpenAuth は依然ベータ、最新は @openauthjs/openauth@0.4.3（2025-03-04リリース）** — 1年以上メジャーバージョン昇格していない点は要注意 — [GitHub anomalyco/openauth](https://github.com/anomalyco/openauth), 2025-03
- **Stack Auth が "OSSの Auth0 / Clerk 代替" として急伸** — UIコンポーネントごとセルフホスト可能、より直接的な代替候補 — [stack-auth.com](https://stack-auth.com/), 2026
- **Logto が "SaaS / AIアプリ向け" ポジションで認知拡大** — エージェント時代のM2M認証ニーズに合わせて成長 — [Logto blog 2026](https://blog.logto.io/top-7-auth-providers-2026), 2026
- **SST 公式ドキュメントには OpenAuth × Next.js / AWS のクイックスタートが整備** — 個人で AWS Lambda に乗せるなら最短ルート — [SST docs: OpenAuth with SST and Next.js](https://sst.dev/docs/start/aws/auth/), 2026
- **Better Auth が TypeScript ネイティブの新興としてGitHubトレンド入り** — フルスタック寄りで Drizzle / Prisma との統合が強い — [Logto 2026比較](https://blog.logto.io/top-7-auth-providers-2026), 2026

---

## 🧩 関連概念・隣接分野

- **OAuth 2.0 / OIDC**: OpenAuth はOAuth 2.0準拠のissuer。"認証"ではなく"認可"の標準プロトコル。OIDCはその上にIDトークンを乗せた拡張
- **Hono**: OpenAuth の土台。Cloudflare Workers / Bun / Node どこでも動くJSフレームワーク。SSTがHonoに賭けている事実上の証
- **IDaaS vs OSS vs Managed**: 認証基盤は概ね「IDaaS（Auth0/Clerk）」「OSSセルフホスト（Keycloak/SuperTokens/Logto/Stack Auth/OpenAuth）」「Managed（Cognito/Firebase Auth）」の3分類で語られる（[Future Tech Night](https://future-architect.github.io/articles/20210812b/)）
- **データ主権 (Data Sovereignty)**: 元ポストの「外部に預けずに済む」の核心。GDPR・改正個情法・国内顧客向けLP系で需要が高まる文脈
- **エージェント時代のM2M認証**: 2026年は AIエージェント同士のOAuth・MCP関連認証が話題。Auth Provider側もエージェント対応が差別化軸に（[Logto 2026](https://blog.logto.io/top-7-auth-providers-2026)）

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（元ポスト寄り）**:
  - OAuth issuerをセルフホストできるのは個人開発でも価値がある
  - Lambda/Workersに置けるので運用コストはほぼゼロに近い
  - SSTエコシステムにいるならゼロ設定に近い
- **否定 / 慎重派の主張**:
  - **ベータ1年4ヶ月停滞**。本番運用は要慎重判断
  - 「Auth0/Clerkの代替」と呼ぶには**ユーザー管理・MFA・組織機能・監査ログが完全に欠落**している（仕様としてそう設計されている）
  - 個人開発で"最速"を狙うなら Clerk無料枠 or Stack Auth の方が早い
  - OpenAuth は「OAuth issuerだけ要る、ユーザーデータは自分のDBで管理したい玄人向け」の道具
- **中立的に見るときの補助線**:
  - "代替" の意味を分解：①プロトコル代替 = ◯　②開発体験代替 = △　③フル機能代替 = ❌
  - 個人開発の最初の認証は Clerk → 軌道に乗ってデータ主権が必要になったら Stack Auth / Logto に移行 → さらに尖ったカスタムが必要なら OpenAuth、というレイヤー分けが現実的

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] OpenAuth が 1.0 (GA) に到達する見込みはあるか、SST側のロードマップ
- [ ] `sst/openauth` → `anomalyco/openauth` への移管経緯（anomaly co の正体・組織図）
- [ ] OpenAuth + 自前ユーザーDBの設計テンプレート（Drizzle/Prismaとの組み合わせ実例）
- [ ] Stack Auth / Better Auth / Logto / OpenAuth の**個人開発実装時間ベンチマーク**
- [ ] 2026年の AIエージェント向けM2M認証ユースケースで、各OSS認証基盤がどれだけMCP/OAuth拡張に追従しているか

---

## 📚 参考資料

- [GitHub: anomalyco/openauth](https://github.com/anomalyco/openauth) — 最新リリース・README・対応プロバイダの一次情報, 取得日 2026-04-25
- [OpenAuth 公式ドキュメント](https://openauth.js.org/) — 機能・対応プロトコル・デプロイ先, 取得日 2026-04-25
- [SST Blog: OpenAuth Beta (2024-12)](https://sst.dev/blog/openauth-beta/) — 公開時点の設計思想と背景, 取得日 2026-04-25
- [SST docs: OpenAuth with SST and Next.js](https://sst.dev/docs/start/aws/auth/) — Next.js × Lambda クイックスタート, 取得日 2026-04-25
- [Stack Auth 公式](https://stack-auth.com/) — Auth0/Clerk代替の代表選手, 取得日 2026-04-25
- [GitHub: stack-auth/stack-auth](https://github.com/stack-auth/stack-auth) — UI込みOSS認証, 取得日 2026-04-25
- [GitHub: supertokens/supertokens-core](https://github.com/supertokens/supertokens-core) — Firebase Auth / Cognito代替, 取得日 2026-04-25
- [Logto blog: Top 7 best auth and agent-friendly providers in 2026](https://blog.logto.io/top-7-auth-providers-2026) — 2026年時点の市場マップ, 取得日 2026-04-25
- [Zenn: 認証基盤 Clerk / Logto / Supabase / Auth0 / AWS Cognito を比較してみた](https://zenn.dev/mergelog/articles/3088d40ef1b07b) — 日本語の比較記事, 取得日 2026-04-25
- [Future Tech Night: IDaaS / OSS / Managed 比較](https://future-architect.github.io/articles/20210812b/) — 認証基盤の分類フレーム, 取得日 2026-04-25

---

## 🗒 メモ

- 元ポストは「公開されていました…！！！」ニュアンスだが、実は2024年末からあるベータ。**新発見ネタとして拡散するのは情報の鮮度的に弱い**
- このトピック、Web制作者目線の note 記事化向き：「**個人開発の認証 OSS 4選を本気比較：OpenAuth / Stack Auth / Better Auth / Logto**」みたいな比較表は今ちょうど需要ある
- X短尺で「OSS認証＝即代替」と言い切らず、**「ユーザー管理は自前で書く前提」「ベータ停滞」**の2点を留保するのが誠実
- 自分の案件用には、**OpenAuth は Cloudflare Workers + Hono + Drizzle のスタックと相性が良い**ので、軽量SaaSを作るときの第一候補に置いておく価値はある
- 関連: [[SNS運用/post/フォロワー改善.md]]（個人開発系の信頼を上げるテーマ）/ [[Claudian-スキル一覧.md]]（将来的に「OSS技術スタック比較」スキルを `/compare-stack` として作っても面白い）
