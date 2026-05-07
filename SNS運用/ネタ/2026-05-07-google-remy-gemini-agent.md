---
created: 2026-05-07
tags:
  - 調査
  - Google
  - Gemini
  - AIエージェント
  - Remy
  - OpenClaw
source: https://x.com/kawai_design/status/2051980301690380516
action: 投稿ネタ
---

# Google "Remy" — Gmail/Drive/Calendar に住み着く Gemini 個人エージェントの正体

> **TL;DR**
> Business Insider が2026-05に報じたGoogleの社内テスト中エージェント「Remy」は、Gemini を「答えるAI」から「動くAI」に変える24時間秘書プロジェクト。9to5Googleが Google app 17.20 の文字列から実装の輪郭を裏取り済みで、OpenAI傘下の OpenClaw（旧 Clawdbot/Moltbot）への明確な対抗。最大の論点は「賢さ」ではなく「**どこまで権限を渡すか**」で、ユーザー側の準備は AI ツール追加ではなく**仕事の棚卸し**から。

## 📌 元テキスト（抜粋）

> Googleの本命は、検索ではなく秘書です。
>
> Business Insiderによると、Googleは Gemini向け個人エージェント「Remy」を社内テスト中。仕事、学校、日常のために24時間動く個人エージェントとして説明されています。
>
> 重要なのは、OpenClaw型の体験が Gmail、Calendar、Drive、Docsの導線に入る可能性です。
>
> つまり、AI選びは「どのモデルが賢いか」から「どこまで権限を渡すか」に変わります。

出典: [[Clippings/Post by @kawai_design on X 1]]（[@kawai_design on X](https://x.com/kawai_design/status/2051980301690380516), 2026-05-06）／引用note: [GoogleのRemy計画と人間の準備（KAWAI）](https://note.com/kawaidesign/n/na6169a376fdf)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Remy | Googleが社内テスト中のGemini製個人エージェントのコードネーム | `Google Remy Gemini agent` |
| Gemini Agent | Geminiに組み込まれる行動可能な機能。Remyは社内向けの強化版 | `Gemini Agent planner` |
| Connected Apps | 外部サービスとの権限連携。Gmail/Drive/Spotify/WhatsApp等 | `Gemini connected apps` |
| Dogfooding | 自社製品を社員に先行使用させて改善する開発手法 | `software dogfooding` |
| OpenClaw | OpenAI傘下のオープンソース個人エージェント（旧 Clawdbot/Moltbot） | `OpenClaw Steinberger` |
| Peter Steinberger | OpenClaw作者。2026-02にOpenAIの個人エージェント部門責任者に就任 | `Steinberger OpenAI` |
| Least-privilege | エージェントに渡す権限を最小限にする設計原則 | `least privilege AI agents` |
| Gemini Privacy Hub | Geminiの活動履歴・データ利用設定を一元管理する画面 | `Gemini Privacy Hub` |

---

## 🧭 背景 / なぜ今これが話題なのか

### 「個人エージェント」レースの2026年マップ

2026年に入ってから、AIベンダー各社は**「単発の質問応答」から「自動でタスクをこなす個人エージェント」**へ完全に軸足を移した。トップ4社の動き：

- **OpenAI** — Steinberger買収（2026-02）でOpenClaw路線。Codex（コーディング）と次の"スーパーアプリ"を統合
- **Google** — Geminiに「Gemini Agent」として組み込む路線。社内コードネーム Remy で5月から本格dogfooding
- **Anthropic** — Claude Computer Use系の延長で開発者向けに先行。"Moltbot"商標で Steinberger に苦情を入れた経緯あり
- **Meta** — 後発だが Llama 系で参戦中

### Remyの一次ソース（Business Insider）が報じた具体内容

社員向けに公開されている Gemini アプリ内の説明文には：

> "Remy is your 24/7 personal agent for work, school, and daily life, powered by Gemini. It elevates the Gemini app into a true assistant that can take actions on your behalf."

連携対象（Connected Apps）は **Gmail / Calendar / Docs / Drive / Keep / Tasks** といった Google Workspace に加え、**GitHub / Spotify / YouTube Music / Google Photos / WhatsApp / Google Home / Android utilities** まで広い。

### 9to5Google の裏取り（Google app 17.20）

ベータ版アプリ内の文字列から、UI構造も判明：
- ナビ内に専用セクションを設置
- タスクを **完了 / 進行中 / ユーザー入力待ち / スケジュール済み** の4ステートで管理
- パーソナルコンテキストとして **チャット履歴・アップロードファイル・位置情報・Cookie** を利用

### なぜ Google が「本命」と言われるのか

OpenClaw / Anthropic 系エージェントは「自分でセットアップしてつなぐ」ハードルがある。一方 Gemini Agent / Remy は **既に10億単位のユーザーが使う Gmail・Drive 動線にそのまま乗る**ため、普及スピードが桁違いに速い可能性がある。元ポストの「検索ではなく秘書が本命」という主張は、ここを衝いている。

### KAWAI が note で出した実用論点

引用元のnoteは、報道のまとめではなく**読者向けアクション**まで踏み込んでいる：

- 2025年まで: 「どのモデルが賢いか」で選ぶ時代
- 2026年以降: 「どこまで権限を渡すか」で選ぶ時代
- 第一歩は AI追加ではなく **仕事の棚卸し**：
  - **任せて良い**: 予定確認・資料探索・メール分類など読み取り中心
  - **任せてはいけない**: 送信・削除・支払い・外部共有など書き込み中心

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Business Insider 報道 | 報道は実在。9to5Google・IT Pro等で2次引用が多数 | [9to5Google: Gemini Agent planner](https://9to5google.com/2026/05/06/gemini-agent-planner-upgrade/) | ✅ 一致 |
| Google が Gemini 向けエージェント「Remy」を社内テスト | dogfooding 段階で社員向け Gemini アプリで稼働中 | [SQ Magazine: Google Testing Gemini AI Agent Remy](https://sqmagazine.co.uk/google-testing-gemini-ai-agent-remy/) | ✅ 一致 |
| 仕事・学校・日常のために24時間動く | 公式説明文 "24/7 personal agent for work, school, and daily life" と一致 | [IT Pro: Google Remy](https://www.itpro.com/technology/artificial-intelligence/google-is-building-its-own-openclaw-alternative-remy-elevates-the-gemini-app-into-a-true-assistant) | ✅ 一致 |
| OpenClaw型の体験がGmail/Calendar/Drive/Docsの導線に入る | Connected Apps に Gmail/Calendar/Docs/Drive が含まれることを9to5Googleが確認 | [9to5Google](https://9to5google.com/2026/05/06/gemini-agent-planner-upgrade/) | ✅ 一致 |
| AI選びは「賢さ」から「権限委譲」へシフト | これは著者解釈。報道側でも user-control 設計の重要性は強調されている | [AI News: Remy User Control](https://www.artificialintelligence-news.com/news/google-remy-ai-agent-gemini-user-control/) | ⚠️ ほぼ一致（解釈は主観） |
| OpenClaw（OpenAI製） | OpenClaw自体はOSSで、Steinberger作。OpenAIは2026-02にSteinbergerを採用しバックに付いた | [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) | ⚠️ ほぼ一致（"OpenAI製"は不正確、"OpenAI傘下のOSS"が正確） |

---

## 🌐 最新動向（2026-05時点）

- **Remy は現在 dogfooding（社員向けテスト）段階**。一般公開時期は未発表 — [9to5Google](https://9to5google.com/2026/05/06/gemini-agent-planner-upgrade/), 2026-05
- **Google app 17.20 ベータに Remy 関連文字列が混入**。タスク管理UIの実装も確認 — [9to5Google](https://9to5google.com/2026/05/06/gemini-agent-planner-upgrade/), 2026-05
- **OpenAI が Steinberger を採用**（2026-02）。OpenClawはOpenAI支援のOSS Foundation化。Codex／"super app"と統合方針 — [CNBC: OpenClaw rise](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html), 2026-02
- **Anthropic が "Moltbot" 名称に商標苦情**（2026-01）。これがOpenClawへの改名きっかけ — [OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw), 2026-01
- **Gemini Privacy Hub による権限管理が前面化**：Apps Activity の確認・削除、自動削除、データ利用許諾を1画面で管理 — [AI News](https://www.artificialintelligence-news.com/news/google-remy-ai-agent-gemini-user-control/), 2026-05
- **Google と Meta が個人エージェント開発で Anthropic / OpenAI に追走中** — [The Decoder](https://the-decoder.com/google-and-meta-race-to-build-personal-ai-agents-as-anthropic-and-openai-pull-further-ahead/), 2026

---

## 🧩 関連概念・隣接分野

- **Computer Use / Browser Use エージェント**: Anthropic / OpenAI が先行する「PC操作する型」のエージェント。Remyは「Connected App API経由」中心で、画面操作型とは設計思想が違う
- **Least-privilege（最小権限の原則）**: セキュリティの基本原則。Google Research も「目的に合わせて agent の権限を最小化せよ」と公言。仕事の棚卸しはこれを実装する個人版
- **Workspace Add-ons / MCP**: 自社サービスに AI エージェントから繋ぐためのプロトコル。今後 Remy が外部サービスを増やすときの拡張点
- **AI透明性・監査ログ**: エージェントが「いつ・どのファイルに・何をしたか」を後から追えること。Gemini Privacy Hub はこの方向性
- **OpenClaw / Hermes / Nemoclaw**: 2026年のOSSエージェント御三家。エンジニア向けセルフホスト派の代表

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - Gmail/Drive/Calendar の **既存導線に入る**ため、ユーザーが「AIを使う」意識なしに普及する
  - 個人コンテキスト（メール履歴・ファイル・予定）を持っているのは Google 最大の差別化
  - Privacy Hub による中央管理で、OpenClawのバラバラ設定より統制しやすい
  - 著者の「権限委譲視点で選ぶ」は実用的な判断軸

- **否定 / 慎重派の主張**:
  - **記事の重要前提が未確定**: Business Insider 報道は「**いつ・本当に公開するか・どこまで自律行動するか**」を明示していない（AI Newsが警告）。発表前のビジョン段階の話を「本命」と断じるのは早計
  - **「OpenClaw型」表現は不正確**: OpenClawはOSSで、OpenAIは"傘下"であって"作者"ではない。SNSの簡略化で OpenAI=OpenClaw と読まれかねない
  - **Google の過去パターン**: Bard/Duet/Gemini 含めリブランド・統合の繰り返し。Remyも社内コードネームで終わって別名でリリースされる可能性
  - **権限委譲＝便利＝危険**: 「送信・削除・支払い」を AI に許す瞬間に、社内不正・誤操作・プロンプトインジェクションのリスクが質的に変わる。著者の「棚卸し」推奨はこの裏返し
  - **プライバシーの非対称性**: Gmail全文をAIに渡すと、メール送信者（第三者）の同意なしに本文を学習・参照させることになる。法務・コンプラ観点では慎重な議論が要る

- **中立的に見るときの補助線**:
  - 「**何を任せて何を任せないかの基準を、Remy 公開を待たずに自分で言語化しておく**」のが当面の正解
  - エージェントを評価する尺度は ①権限スコープの細かさ ②監査ログの可視性 ③人間の確認ステップの組み込みやすさ — の3つで見ると差が見える

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Remy はどこまで自律的に動くのか（送信・購入を確認なしで実行できるのか）
- [ ] Workspace 法人プラン（Business/Enterprise）での挙動と管理者権限の関係
- [ ] OpenClaw / Remy / Anthropic（Claude Computer Use）の **権限粒度**比較を別ノートで
- [ ] 日本企業のセキュリティポリシー観点で、"AIエージェントに何を許すか"の社内規程テンプレートが存在するか
- [ ] Apple Intelligence / Siri agent 路線が来年（2026年後半〜2027年）どこまで巻き返すか
- [ ] 「仕事の棚卸し」を効率化するワークシートの存在（記事化候補）

---

## 📚 参考資料

- [9to5Google: Google preps 'Gemini Agent' as your '24/7 digital partner'](https://9to5google.com/2026/05/06/gemini-agent-planner-upgrade/) — アプリ文字列・UI構造の裏取り, 取得日 2026-05-07
- [IT Pro: Google is building its own OpenClaw alternative](https://www.itpro.com/technology/artificial-intelligence/google-is-building-its-own-openclaw-alternative-remy-elevates-the-gemini-app-into-a-true-assistant) — 公式説明文の引用, 取得日 2026-05-07
- [AI News: Google tests Remy AI agent for Gemini](https://www.artificialintelligence-news.com/news/google-remy-ai-agent-gemini-user-control/) — User Control・Privacy Hub の解説, 取得日 2026-05-07
- [SQ Magazine: Google Reportedly Testing New Gemini AI Agent Called Remy](https://sqmagazine.co.uk/google-testing-gemini-ai-agent-remy/) — Connected Apps一覧, 取得日 2026-05-07
- [The Decoder: Google and Meta race to build personal AI agents](https://the-decoder.com/google-and-meta-race-to-build-personal-ai-agents-as-anthropic-and-openai-pull-further-ahead/) — 競争構図の整理, 取得日 2026-05-07
- [OpenClaw - Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) — Steinberger買収・改名経緯, 取得日 2026-05-07
- [CNBC: From Clawdbot to Moltbot to OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html) — OpenClawの誕生・改名史, 取得日 2026-05-07
- [Benzinga: Google Tests New AI Agent To Take On OpenClaw](https://www.benzinga.com/markets/tech/26/05/52313193/google-tests-new-ai-agent-to-take-on-openclaw-with-advanced-task-automation-report) — マーケット視点の解説, 取得日 2026-05-07
- [note: GoogleのRemy計画と人間の準備（KAWAI）](https://note.com/kawaidesign/n/na6169a376fdf) — 元ポストの引用note, 取得日 2026-05-07

---

## 🗒 メモ

- **記事ネタ濃度高い**。「Remy = 検索ではなく秘書」のフックは noteの再投で十分使える
- 自分の文脈での切り口候補:
  1. **AI選び基準のシフト**を中心に、「賢さ→権限委譲」を3レイヤー（個人／チーム／会社）で書き分ける
  2. **「任せていいタスク／NGタスク」棚卸しシート**を実例付きで作って読者特典化（KAWAIが既に書いているので差別化にPDFテンプレ付録を）
  3. **OpenClaw vs Remy vs Claude vs Apple** の権限粒度比較表（差別化の本命）
- X展開する場合は、「OpenClaw型」の表現が誤解を生むので **「OpenAI傘下のOpenClaw的UX」** など正確な言い回しに直す
- **要警戒**: Business Insider報道はビジョン段階の話。「Remyが○月にリリース」のような断定はまだ書かない
