---
created: 2026-04-29
tags: [調査, postiz, sns自動化, oss, n8n]
source: https://x.com/so_ainsight/status/2048959897405215137?s=12
---

# Postiz：GitHub 29.7k☆「全自動SNS運用OSS」の実態と、セルフホスト"永年0円"の落とし穴

> **TL;DR**
> - Postiz（gitroomhq/postiz-app）はGitHub Star **29.7k**（2026-04-29時点）の自己ホスト型SNS運用OSS。X/Instagram/TikTok/LinkedIn等14〜18プラットフォームへのスケジュール投稿、AI文章+画像生成、Canva風デザイナー、n8n/Make/Zapier API連携を1本に詰め込んだ「Buffer + Hootsuite + Canva のOSS版」
> - ライセンスは元ツイート紹介の論調と違い **AGPL-3.0**（Apache 2.0ではない）。**自分で使うだけなら永年0円・機能制限なしは事実**だが、改変版を社内SaaSとして他人に提供すると**ソース開示義務**が発生する点だけ要注意
> - 「全自動」は半分嘘。Docker操作・OAuthアプリ申請（プラットフォームごとの開発者ポータル承認）・Instagramの不安定さ・分析の貧弱さなど、**実運用に持ち込む前に潰すべき穴が4つ**ある。最新版は v2.21.7（2026-04-27リリース）でアップデートは活発

## 📌 元テキスト（抜粋）

> ガチで時代、変わる。GitHubスター29,500超のオープンソースが、SNS運用を全自動化するツールを公開しました。名前はPostiz。
> ・X/Instagram/TikTok/LinkedInなど30以上のSNSへ一括スケジュール投稿
> ・AIが投稿文と画像を生成、Canva風エディタで仕上げまで完結
> ・n8n/Make/Zapier連携の公式APIで「投稿の自動化フロー」が組める
> セルフホストすれば永年0円、機能制限なし。👇

出典: [[Clippings/Post by @so_ainsight on X]] / [@so_ainsightの元投稿](https://x.com/so_ainsight/status/2048959897405215137?s=12)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Postiz | GitHubで開発が進むOSSのSNS統合管理ツール（gitroomhq製） | `postiz-app` `gitroomhq` |
| AGPL-3.0 | 改変してネットワーク提供したらソース公開義務が発生する強コピーレフトライセンス | `AGPL network use` `SaaS loophole` |
| n8n / Make / Zapier | ノーコード〜ローコードのワークフロー自動化サービス | `n8n-nodes-postiz` `make.com integration` |
| OAuth開発者ポータル | 各SNSの公式アプリ登録画面（Twitter Developer Portal等）。投稿APIを叩くには審査通過が必須 | `Twitter API v2 access` `Instagram Graph API` |
| Buffer / Hootsuite | 老舗SaaS型SNS管理ツール。Postizが「OSS代替」として並べられる比較対象 | `buffer alternative open source` |
| Mixpost | Postizの最大の競合OSS（Laravel製、買い切り型ライセンス） | `mixpost vs postiz` |
| 自己ホスト（self-hosted） | 自社サーバ/VPS/RaspberryPiで動かす運用形態 | `docker compose postiz` |
| 公式API | Postizが提供する投稿スケジューリング用RESTエンドポイント | `postiz public api` |

---

## 🧭 背景 / なぜ今これが話題なのか

**2010年代の「SNS管理SaaS黄金期」の終わり**から話を始める必要がある。

Buffer（2010年創業）と Hootsuite（2008年創業）が「複数SNSを1画面でスケジュール投稿」のジャンルを作り、10年代後半は両社で寡占。だが2023〜2025年に状況が変わる。

- **2023年**: Twitter API v2の有料化（Free→Basic $100/月）。SaaS各社が一斉に値上げ or 機能制限
- **2024年**: Hootsuite が Free Plan 廃止、最低 **$199/user/月** に。中小企業が離脱
- **2024年〜2025年**: AI生成（GPT-4o、Claude 3.5、Stable Diffusion XL等）がコモディティ化。「AI文章+画像生成」が課金理由として弱くなる
- **2025年**: OSSのSNSスケジューラ（Mixpost、Postiz、Postal）に注目集まる。特にPostizは「Canvaライク編集」「Public API」「30+プラットフォーム」で頭ひとつ抜ける
- **2026-04-27**: Postiz **v2.21.7** リリース。GitHub Star **29.7k** まで急伸（2025年秋時点で約20k → 半年で1.5倍）。`gitroomhq/postiz-agent` という Claude / OpenClaw 連携CLIまで派生

「**SaaSの値上げ + AI機能のコモディティ化 + AGPLでも"自分用なら気にせず使える"周知**」の3つが重なって、2026年Q2は OSS SNSスケジューラの実運用元年になりかけている。今回の元ツイートの "29,500超" という数字は、まさにこの上昇カーブのリアルタイム観測値だ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| GitHubスター29,500超 | 2026-04-29時点で **29.7k** | [GitHub gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | ✅ 一致（むしろ控えめ） |
| 30以上のSNSへ一括スケジュール投稿 | 公式GitHub Readmeで確認できるのは **14〜18プラットフォーム**（Instagram/YouTube/Dribbble/LinkedIn/Reddit/TikTok/Facebook/Pinterest/Threads/X/Slack/Discord/Mastodon/Bluesky等）。"30+"はマーケコピーで2倍盛り | [Postiz公式](https://postiz.com/) / [GitHub Readme](https://github.com/gitroomhq/postiz-app) | ⚠️ ほぼ一致（数字は誇張） |
| AIが投稿文と画像を生成、Canva風エディタで仕上げ | "AI Content Generation" と "Integrated Design Editor" は公式機能リストに明記 | [Postiz公式](https://postiz.com/) | ✅ 一致 |
| n8n/Make/Zapier連携の公式APIで自動化フローが組める | NPM `@postiz/node` SDK、`n8n-nodes-postiz` カスタムノード、Make.com連携が公式提供 | [GitHub gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | ✅ 一致 |
| セルフホストすれば永年0円、機能制限なし | コード自体はAGPL-3.0で自己利用なら無料・全機能解放。ただし**改変版をネット経由で他人に提供する場合はソース公開義務**。完全な"無制限"ではない | [GitHub License](https://github.com/gitroomhq/postiz-app) / [FOSSA AGPL解説](https://fossa.com/blog/open-source-software-licenses-101-agpl-license/) | ⚠️ ほぼ一致（自分用は事実、再配布/提供は条件付き） |
| ライセンスはApache 2.0という一部のレビュー記事の記載 | GitHub上の実LICENSEは AGPL-3.0 | [GitHub gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | ❌ 要注意（外部レビューの誤り） |

---

## 🌐 最新動向（2026-04-29時点）

- **v2.21.7 リリース（2026-04-27）** — Star 29.7k に到達、開発はかなり活発（過去30日で複数のマイナーリリース） — [GitHub gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app), 2026-04
- **Postiz Agent CLI 公開** — Claude / OpenClaw（≒Claude Code互換のローカルエージェント）から自然言語でPostizを操作してSNS投稿をスケジュールできるサブプロジェクト。エージェント時代のSNS運用UIの実験 — [GitHub gitroomhq/postiz-agent](https://github.com/gitroomhq/postiz-agent), 2026-04
- **Railway "Deploy Postiz" テンプレートが Updated May '26** — ワンクリックデプロイ環境が整備され、Docker未経験者の参入障壁が一段下がった — [Railway Deploy Postiz](https://railway.com/deploy/postiz), 2026-05
- **G2レビュー 4.8/5 に到達**（早期フィードバック中心、レビュー件数はまだ少ない） — [Postiz on G2](https://www.g2.com/products/postiz/reviews), 2026-04
- **クラウド版（postiz.com）の有料プラン $29/月〜** — 自前運用したくない層向けに公式SaaSも展開。完全OSS純粋路線ではなく、Open Coreに近いビジネスモデル — [Postiz公式](https://postiz.com/), 2026-04

---

## 🧩 関連概念・隣接分野

- **Mixpost**: Postizの最大の競合。Laravel製で買い切りライセンス（Pro $199 once）。Postizが「OSS無料 + クラウドサブスク」のOpen Core型なのに対し、Mixpostは「ソース閲覧可だが買い切り」型 — [Postiz vs Mixpost 比較](https://postiz.com/compare/postiz/mixpost)
- **n8n**: ノーコード自動化のOSSハブ。`n8n-nodes-postiz` を入れれば、RSS取得→GPT要約→Postiz投稿のフルパイプが組める。Postizを"投稿の出口"として置く設計が王道
- **Twitter API v2 / Instagram Graph API**: Postizを動かすための真の課金ポイントはここ。Twitter Basic $100/月、Instagram Graph APIは Meta for Developers の審査通過が必要。**「Postiz自体は無料」でも"投稿APIへのアクセス権"は別軸で必要**
- **OAuth 2.0 / PKCE**: Postizは公式OAuthフローを使い、APIキー/トークンを自社サーバに保存しないプライバシー設計。これがセキュリティ意識の高い企業が選ぶ理由
- **AGPL-3.0**: GoogleがAGPLコードの社内利用を原則禁止していることで有名な強コピーレフト。Postizの選択は「商用フォーク禁止」ではなく「フォークしてSaaS化するなら全部公開しろ」のメッセージ — [Google Open Source AGPL Policy](https://opensource.google/documentation/reference/using/agpl-policy)

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - SNS運用ツールは「機能の差」より「データ主権 + コスト」の戦いに移行している。Postizは両方を同時に解決
  - 自社のn8n/Makeワークフローと統合できれば、人手のSNS運用を90%削減できる
  - AGPLは「真にオープンなOSS」のシグナル。Buffer/Hootsuiteのベンダーロックを脱出する正攻法

- **否定 / 慎重派の主張**:
  - **「全自動化」は誇張**。OAuth申請、各プラットフォーム審査、Docker更新、DB（PostgreSQL）保守、Temporal（ジョブスケジューラ）監視……自社で運用部隊が組めない会社が手を出すと半年でソフト止まる
  - **Instagram連携は不安定**との報告複数（G2レビュー）。Meta API側の頻繁な仕様変更が原因で、SaaS版でも同様の問題は出ているがOSSは復旧が遅れがち
  - **分析機能が貧弱**。クロスプラットフォームのダッシュボード、社内インボックス、承認ワークフロー、ロールベース権限、ホワイトラベル出力 — 大手SaaSに比べていずれも「ない or 簡素」
  - **AGPLの社内SaaS化は要注意**。社内向けでも「ネット経由で提供」したら社員にソース閲覧権を与える義務が発生し得る（解釈は割れる）。法務部が嫌う
  - **"無料"の総コストはゼロではない**。VPS（月$10〜）+ Twitter API Basic（$100）+ Instagram審査工数 + 運用工数 = 月数万円の隠れコスト。年間で見ると Buffer Free〜$15プランより高くつくケースあり

- **中立的に見るときの補助線**:
  - **「自分1人〜小チーム + Mastodon/Bluesky/Threads主体」なら Postiz の費用対効果は最強**。X/Instagram の課金APIを避ければ実質無料
  - **「クライアント案件 + 承認ワークフロー必須 + 月100投稿超」なら Buffer/Hootsuite/Sprout Social の方が結局安い**（運用工数考慮で）
  - **n8n/Make との連携前提なら、Postizは"投稿の出口"として優秀**。AI生成→人間レビュー→Postizスケジュールのパイプを作れば、SaaSにない柔軟性が手に入る
  - 元ツイートの「全自動」「永年0円」は**"自分用ライトユース"なら正しい**。法人運用に持ち込む時は5重ぐらいの注釈が必要

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Postiz Agent CLI（Claude Code互換）でどこまで自然言語でSNS運用できるか実機検証
- [ ] n8n-nodes-postiz の具体的なノード仕様。RSS→GPT→Postiz の最短パイプを組んでベンチ
- [ ] AGPL-3.0が「自分1人で運用するクラウド版Postiz」に対して実務上どこまで縛りを生むか（弁護士見解）
- [ ] Twitter API Basic ($100/月) なしで Postiz をどこまで使い倒せるか。Mastodon + Bluesky + Threads + LinkedIn のみで運用可能か
- [ ] Mixpost との実機比較（同条件で1ヶ月運用した時の安定性・更新頻度・Instagram連携成功率）
- [ ] 自分の現運用（[[SNS運用/post]] / [[SNS運用/threads]] の手動コピペ）の「Postiz化」シミュレーション。1日30分削減できるか

---

## 📚 参考資料

- [GitHub - gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) — 一次情報（Star数、ライセンス、対応プラットフォーム、最新リリース）, 取得日 2026-04-29
- [Postiz公式サイト](https://postiz.com/) — 機能リスト・有料プラン・"agentic" 自称, 取得日 2026-04-29
- [Postiz Review 2026 - linkstartai](https://www.linkstartai.com/en/agents/postiz) — 2026年版の機能・価格レビュー, 取得日 2026-04-29
- [Postiz Review 2026 - socialrails](https://socialrails.com/blog/postiz-review) — 自己ホスト時の制約・分析機能の弱さレポート, 取得日 2026-04-29
- [Postiz Reviews on G2](https://www.g2.com/products/postiz/reviews) — Instagram連携不安定の実ユーザー報告, 取得日 2026-04-29
- [Top 12 Open Source Social Media Scheduler Tools - Postiz Blog](https://postiz.com/blog/open-source-social-media-scheduler) — Mixpost他競合との比較, 取得日 2026-04-29
- [Postiz vs Mixpost - Postiz Compare](https://postiz.com/compare/postiz/mixpost) — 公式比較ページ（バイアスあり前提で読む）, 取得日 2026-04-29
- [FOSSA - AGPL License 101](https://fossa.com/blog/open-source-software-licenses-101-agpl-license/) — AGPLのネットワーク条項解説, 取得日 2026-04-29
- [Google Open Source - AGPL Policy](https://opensource.google/documentation/reference/using/agpl-policy) — 大手企業がAGPLを忌避する理由, 取得日 2026-04-29
- [Railway - Deploy Postiz](https://railway.com/deploy/postiz) — ワンクリックデプロイ用テンプレ（Updated May '26）, 取得日 2026-04-29
- [GitHub - gitroomhq/postiz-agent](https://github.com/gitroomhq/postiz-agent) — Claude Code互換のCLIエージェント, 取得日 2026-04-29

---

## 🗒 メモ

- **note記事化候補**: 「"GitHub 29.7k OSSでSNS全自動化" を真に受けて月20万浮かせると思った話」みたいな**煽り解剖型**でいける。元ツイートの"30以上のSNS"は実機検証で14〜18に縮むので、批評型ポジションの定番ネタ
- **連投シリーズ④の素材**: [[SNS運用/post/draft/20260427_critique_series_04_obsidian-second-brain.md]] の次の素材として、Postiz煽りも候補に積める。"中身は普通の良ツール、煽り方が雑なだけ" のテンプレが効きやすい
- **自分のSNS運用への適用**: 現状 [[SNS運用/archive/post/day95]] / [[SNS運用/archive/threads/Threads-day95]] を手動でnoteから移していて、毎日15〜20分の転記コストが出ている。Postiz + n8n でこの工程だけ自動化できれば年間100時間級。次の四半期の運用改善議題に積む
- **Day Oneプロモとは別軸の有料記事ネタ**: 「BufferからPostizへの完全乗り換えガイド」「n8n×PostizでX/Threads/LinkedInを5分で同時投稿する設計図」あたりは検索流入が見込めるニッチ。[[SNS運用/note/_有料記事/]] の次弾候補
- **批判的に握っておく一番大事な1行**: **"無料"の本体コストは0円だが、Twitter API代と運用工数を含めると月3万〜10万円。Bufferの中位プランより高くつくこともある**。これを抜きで語ったら煽り側に回る
