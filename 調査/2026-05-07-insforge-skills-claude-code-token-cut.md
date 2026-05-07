---
created: 2026-05-07
tags:
  - 調査
  - ClaudeCode
  - InsForge
  - Skills
  - context-engineering
  - MCP
  - トークン最適化
source: https://x.com/ClaudeCode_love/status/2051935773231087929
action: 投稿ネタ
---

# Claude Code のトークン消費を1/3にした「InsForge Skills + CLI」の正体 — 2.8倍削減の裏側と再現条件

> **🔗 関連コンテンツ**
> - 🤖 同テーマ（Claude Code拡張）: [[調査/2026-05-04-claude-code-superpowers-plugin.md]]
> - 🤖 Claude × MCP の文脈設計論: [[調査/2026-05-01-claude-design-mcp-anti-ai-slop.md]]
> - 🧠 LLMスタック比較: [[SNS運用/ネタ/2026-05-06-best-llm-stack-2026.md]]
> - 🛠 同日のネタ（兄弟ファイル）: [[SNS運用/ネタ/2026-05-07-frappe-insights-oss-bi.md]]
> - 🧰 OSS無料代替シリーズ: [[SNS運用/ネタ/2026-05-06-dont-pay-ai-tool-alternatives.md]]
> - 📎 元クリップ: [[Clippings/Post by @ClaudeCode_love on X 2.md]]

> **TL;DR**
> Avi Chawla（Daily Dose of Data Science）が2026-04に公開した実験で、**Claude Code のバックエンドを Supabase → InsForge に差し替えただけで 10.4M → 3.7M トークン（2.8倍削減）／エラー10→0／コスト$9.21→$2.81** を達成。カラクリは **Skills（Progressive Disclosure型の事前知識）＋ CLI（複数MCP呼び出しを1コマンドに集約）＋ MCP（状態取得は1回で完結）** の3層アーキテクチャ。InsForgeは Apache 2.0・GitHub 8.5kスター・PostgreSQL ベースの "AIネイティブBaaS"。**ただし実験はDocuRAG 1ケースのみ・条件設定にInsForge有利のバイアスあり**。「Claude Code高い」じゃなく「文脈設計が雑」を可視化した好例ではあるが、数字の3倍削減を鵜呑みにせず **「Skills × Progressive Disclosure × CLI集約」のパターンとして抽象化して持ち帰る** のが正解。

---

## 🗒 メモ

> ⚠️ このセクションは **冒頭に配置**（2026-05-06 ルール変更）。**「この調査をどう使うか」のアクション仮説**を最初に書くことで、次のアクションが見えやすくなる。

### 投稿ネタとしての切り口

- **フックは「2.8倍削減」の数字＋"だが鵜呑み禁止"の二段構え**。ただ煽るだけのアカウントとの差別化
- **構成案（Xスレッド5投稿 / news-thread v2型）**:
  1. **要約**: 「Claude Code のトークン1/3にした方法、本当に効いたの？」（10.4M→3.7M、$9.21→$2.81）
  2. **見解**: 効いたのは "InsForge" ではなく **「Skills × Progressive Disclosure × CLI集約」のパターン** だった
  3. **不安**: ただし実験は1ケース（DocuRAG）・著者にバイアスあり・Supabase条件が不利寄り
  4. **アクション**: 自分の `.claude/commands/` に応用するなら〜（メタデータ最小化・状態取得を1回にまとめる・CLI化）
  5. **誘導**: 詳細は note記事 or [[Claudian-スキル一覧.md]] 参照
- **Threadsスレッド版**: 同構成で投稿
- **note記事化**: 1500字程度。「数字に踊らされず、Skills設計の原則を持ち帰る」がテーマ

### このネタの使い道

- **第1用途（投稿ネタ）**: AI／Claude Code界隈は強い関心領域。「ファクトチェック付きで紹介する」スタイルでフォロワー価値を出す
- **第2用途（運用参考）**: Claudian自身が `.claude/commands/` でスキル運用しているため、**Progressive Disclosure型の設計思想**は直接応用可能。`/deep-dive` `/news-thread` 等が肥大化したら参考にする
- **戦略接続**: W18戦略メモの「OSS紹介枠」 + 「Claude Code活用シリーズ」枠の両方に接続可能

### 派生ネタ候補

- 「Anthropic公式 Skills 機能 vs InsForge Skills の違い」 — Anthropic公式の Agent Skills 仕様と比較する深掘り記事
- 「自分の `.claude/commands/` を Progressive Disclosure 化する10分リファクタ」 — 体験ログ系
- 「BaaS の AIネイティブ化（InsForge / Convex / PowerSync）2026年マップ」 — 比較記事

### 自分用の検証タスク

- [ ] `/deep-dive` のメタデータが何トークンか測ってみる
- [ ] InsForge を実際にDockerで立てて `claude --resume` でトークン消費を比較
- [ ] Claudianの既存スキルで「最初にフルロードしてる重い知識」を洗い出して Progressive Disclosure 化できるか検討

---

## 📌 元テキスト（抜粋）

> 【速報】Claude Codeのトークン消費を1/3にした方法が公開されて話題😳
>
> ・Before: 10.4Mトークン・エラー10個・$9.21
> ・After: 3.7Mトークン・エラー0個・$2.81
> ・使ったのは「Insforge Skills + CLI」
> ・ローカルで動くOSSのコンテキストエンジニアリング層
>
> つまり ❌ Claude Codeにそのまま丸投げ → ⭕ バックエンドで文脈を整理してから渡す
>
> →「Claude Codeが高い」んじゃない。「使い方が非効率だった」だけ。

出典: [[Clippings/Post by @ClaudeCode_love on X 2.md]]（[@ClaudeCode_love on X](https://x.com/ClaudeCode_love/status/2051935773231087929), 2026-05-04）／一次情報は [@_avichawla on X](https://x.com/_avichawla/status/2046685172666712571)（2026-04）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code | Anthropic公式のターミナル型コーディングエージェント | `claude code anthropic` |
| InsForge | PostgreSQLベースのAIネイティブBaaS。Supabaseの「エージェント特化版」的位置付け | `InsForge backend agent` |
| Skills（Agent Skills） | エージェントが必要に応じて読み込める「再利用可能な知識・指示パッケージ」 | `anthropic agent skills` |
| Progressive Disclosure | メタデータだけ先に見せ、必要時にフル内容を開示する設計パターン | `progressive disclosure llm context` |
| Context Engineering | コンテキストウィンドウに「次の一手に最適な情報だけを詰める」工学 | `context engineering` |
| MCP (Model Context Protocol) | Anthropicが提唱したエージェント↔ツール接続規格 | `model context protocol` |
| BaaS | Backend-as-a-Service。認証・DB・ストレージ等をAPIで提供するクラウド層 | `backend as a service` |
| pgvector | PostgreSQLのベクトル検索拡張。RAGで定番 | `pgvector RAG` |
| DocuRAG | 実験で構築されたPDF Q&Aアプリ。OAuth+PDF+pgvector+QA | `RAG PDF chatbot` |
| Avi Chawla | Daily Dose of Data Science 運営者。本実験の著者 | `Avi Chawla DDS` |

---

## 🧭 背景 / なぜ今これが話題なのか

### 「Claude Code 高すぎ問題」の蓄積

2025年後半〜2026年春にかけて、Claude Code のヘビーユーザー（特にSonnet 4.5・Opus 4.5世代）から **「1セッション$5〜$10平気で飛ぶ」** という悲鳴が増加。GitHub Discussions では「89%トークン削減できた」というスレッドや、note・Substack で「$1,600 Bill 回避ガイド」のような記事が乱立した。

主犯と目されたのが **MCP の "all-or-nothing" コンテキストロード**。MCPサーバーを繋ぐとそのサーバーのスキーマ全体がコンテキストに乗るため、20個繋ぐだけで起動時に数万トークン消費する事例が報告されていた。

### Anthropic公式 Skills 機能の登場（2026年初）

Anthropicが公式に **Agent Skills** を `claude.com/docs/agents-and-tools/agent-skills` で提供開始。「メタデータだけ先に見せ、エージェントが関連と判断したら本体をロードする」**Progressive Disclosure** が標準パターン化。Claude Code の `~/.claude/commands/` も同じ思想。

### InsForge の "Skills + CLI + MCP" 三層化

InsForge（GitHub 8.5kスター、Apache 2.0、PostgreSQL+Deno+Next.js）は2026年初に **2.0** をリリース。単なるBaaSではなく **"AIエージェント用の意味論レイヤー"** として位置付け、以下の3層を提供:

1. **Skills**（静的知識）: `insforge` `insforge-cli` `insforge-debug` `insforge-integrations` の4つに分割。Progressive Disclosure
2. **CLI**（直接実行）: `--json` 出力＋セマンティック終了コード。複数MCP呼び出しを1コマンドに集約
3. **MCP**（ライブ状態）: `get_backend_metadata` で完全なバックエンド状態を1呼び出し（約500トークン）

### 2026-04のAvi Chawla実験で爆発

[Avi Chawla（Daily Dose of Data Science）](https://blog.dailydoseofds.com/p/how-we-cut-our-claude-code-token) が **同じDocuRAG（OAuth+PDF+pgvector+QA）アプリを Supabase版 と InsForge版で並行ビルド**し、Claude Code のトークン消費を実測比較。その結果が「10.4M→3.7M、エラー10→0、$9.21→$2.81」で、**X・LinkedIn・Hacker Newsで爆散**。

日本では Akshay Pachaar の動画も併せて拡散され、5月初旬に @ClaudeCode_love が日本語で速報展開 → 一般層に拡大。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| トークン消費を1/3にした | 10.4M → 3.7M ＝ 約2.8倍削減（厳密には1/2.8）。「1/3」は概ね妥当な丸め | [Avi Chawla の元実験記事](https://blog.dailydoseofds.com/p/how-we-cut-our-claude-code-token) | ✅ 一致 |
| エラー10個→0個 | 著者の計測通り。ただしSupabase版は12ユーザーメッセージ・InsForge版は1ユーザーメッセージで、エラー比較の前提が異なる | 同上 | ⚠️ ほぼ一致（条件不揃い） |
| コスト $9.21 → $2.81 | 著者の計測通り | 同上 | ✅ 一致 |
| Insforge Skills + CLIが原因 | Skills（事前知識）＋ CLI（呼び出し集約）＋ MCP（1回で状態取得）の3層全部の合算効果。Skillsだけではない | 同上＋[InsForge GitHub](https://github.com/InsForge/InsForge) | ⚠️ ほぼ一致（"+ CLI"は正しいが"Skills単独"の印象だと誤解） |
| ローカルで動くOSS | Apache 2.0・self-host対応（Docker Compose）・cloud-hosted版もあり | [InsForge GitHub](https://github.com/InsForge/InsForge) | ✅ 一致 |
| Claude Codeが高いんじゃなく使い方が非効率 | 著者の主張。**ただし「Supabase MCPの設計が悪い」だけで Claude Code 自体の効率の話ではない** 可能性も | 同上 | 🔍 解釈次第（フレーミング論点） |
| 「Insforge Skills」と呼べる単独機能 | 公式名称は「Skills」（複数）。`insforge` `insforge-cli` `insforge-debug` `insforge-integrations` の4スキル群 | [InsForge GitHub](https://github.com/InsForge/InsForge) | ⚠️ ほぼ一致（呼称の単純化） |

---

## 🌐 最新動向（2026-05時点）

- **InsForge v2.1.1 リリース（2026-05-06）**: 36リリース達成、活発に開発中 — [GitHub Releases](https://github.com/InsForge/InsForge/releases), 2026-05
- **GitHub 8.5kスター（2026-05時点）**: 2026年初の v2.0 ローンチ後に約5kから急増 — [InsForge GitHub](https://github.com/InsForge/InsForge), 2026-05
- **Avi Chawla の実験記事が AI界隈で大バズ**: blog.dailydoseofds.com、X、LinkedIn、Hacker Newsで連鎖拡散 — [How We Cut Our Claude Code Token Usage 2.8x!](https://blog.dailydoseofds.com/p/how-we-cut-our-claude-code-token), 2026-04
- **Anthropic 公式 Agent Skills の整備**: Skills は Claude Code 経由でも Anthropic API でも使える正式機能に — [Agent Skills - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), 2026
- **NeoLabHQ の "context-engineering-kit" など派生OSS群**: Claude Code Skills を OpenCode / Cursor / Antigravity / Gemini CLI でも使える形にしたキット — [GitHub: NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit), 2026
- **「Skills でトークン80%削減」系の記事も登場**: dev.to で日本人開発者によるノウハウ記事 — [Reduce Token Consumption by 80%! Claude Code Skills Utilization Techniques](https://dev.to/kato11/reduce-token-consumption-by-80-claude-code-skills-utilization-techniques-1g7), 2026
- **CLI Proxy 系の代替手法も並走**: kilocode の議論では「10Mトークン89%削減」の事例も — [I saved 10M tokens (89%) on my Claude Code sessions with a CLI proxy](https://github.com/Kilo-Org/kilocode/discussions/5848), 2026

---

## 🧩 関連概念・隣接分野

- **Anthropic Agent Skills**: 公式の Skills 仕様。`SKILL.md` でメタデータ＋本体を分離。Claudian の `.claude/commands/` も同じ思想 → [[Claudian-スキル一覧.md]]
- **MCP (Model Context Protocol)**: Anthropic 提唱のエージェント↔ツール接続規格。「Skillsは静的知識／MCPはライブ状態」と役割分担するのが2026年のベストプラクティス
- **Supabase**: もっとも近い競合BaaS。GitHub 70k超・コミュニティ巨大。ただし MCP の応答が「全スキーマを返す」傾向で文脈肥大化しがち
- **Convex / PowerSync / Neon**: BaaS の "AIネイティブ化" 競合。それぞれ独自のエージェント連携を模索中
- **Context Engineering（文脈工学）**: Lance Martin（LangChain）等が提唱した概念。「コンテキストウィンドウは予算」と捉え、何を入れるか・何を抜くかを設計する工学
- **Progressive Disclosure**: UXデザイン由来の概念。Claude Code Skills、ChatGPT カスタムGPT、Cursor Rules でも採用される定番パターン

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - Skills × CLI × MCP の三層化は確かにエージェント向け設計として理にかなっている
  - 数字（2.8倍削減）は再現条件さえ揃えれば嘘ではない
  - InsForgeはApache 2.0・self-host可能でロックインリスクが低い
  - 「Claude Code高い問題」に **コンテキスト設計** という解を示した功績は大きい

- **否定 / 慎重派の主張**:
  - **実験はDocuRAG 1ケースのみ**。一般化可能性は未検証（リアルタイム協調・複雑統合では結果が違う可能性）
  - **条件設定にInsForge有利のバイアス**: Avi Chawla記事自身が、Supabase版でOAuth設定をMCP外で手動実施させているなど不公正な条件あり
  - **「Skills + CLI」が削ったのか、"InsForge + Skills + CLI" のパッケージが削ったのか分離されていない**: 同じ Skills 設計を Supabase 用に書けば結果は近づくかも
  - **InsForgeへのロックインリスク**: BaaSとして使うと結局はベンダー依存。Apache 2.0でも実装移植は重い
  - **数字を煽りに使う系のSNS投稿**が多く、本質（Skills設計原則）が伝わらず「ツール買えば解決」の誤解を生む
  - **著者バイアス**: Avi ChawlaはInsForge推しの記事を複数本書いており、純粋な比較ではなくマーケコンテンツ寄り

- **中立的に見るときの補助線**:
  - **「2.8倍削減」は条件次第。半分眉唾で受け取り、"Skills × Progressive Disclosure × CLI集約" のパターンだけ抽象化して持ち帰る**
  - 自分の `.claude/commands/` でも同じ原則は応用可能（フルロード→メタデータ＋本体分離、複数tool呼び出し→bash 1発に集約）
  - InsForge自体は良いプロダクトだが、これを使うかどうかは「PostgreSQL + Anthropic Skills を自分で組むか、まとめて買うか」のトレードオフ判断

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] 同実験を **Supabase + 自作Skillsで再現** したら数字はどう変わるか（純粋に Skills 設計の効果を切り出せるか）
- [ ] Anthropic 公式 Agent Skills と InsForge Skills の仕様差異（メタデータフォーマット、ロードタイミング、優先順位）
- [ ] Claude Code 4.5 / 5.0 世代でのトークン削減効果（ContextRot 改善との相互作用）
- [ ] InsForge を実運用でホスティングする場合のコスト（Fly.io上のCompute、edge functionsなど）
- [ ] 日本のSaaSでInsForge採用事例はあるか（Apache 2.0なので情報外に出にくい）
- [ ] Cursor / OpenCode / Antigravity でも同じ Skills × Progressive Disclosure パターンが効くか
- [ ] 「2.8倍削減」を訴求する他アカウントの数字検証（kilocodeの89%削減等とのクロスチェック）

---

## 📚 参考資料

- [@ClaudeCode_love on X](https://x.com/ClaudeCode_love/status/2051935773231087929) — 元クリッピング元の日本語ツイート, 取得日 2026-05-07
- [@_avichawla on X](https://x.com/_avichawla/status/2046685172666712571) — 一次情報のAvi Chawla X投稿, 取得日 2026-05-07
- [How We Cut Our Claude Code Token Usage 2.8x!](https://blog.dailydoseofds.com/p/how-we-cut-our-claude-code-token) — Avi Chawla の元実験記事（DocuRAG構築）, 取得日 2026-05-07
- [Claude Code Optimization Breakthrough: 3x Fewer Tokens (Blockchain News)](https://blockchain.news/ainews/claude-code-optimization-breakthrough-3x-fewer-tokens-and-zero-errors-using-insforge-skills-cost-analysis) — 第三者媒体の解説, 取得日 2026-05-07
- [GitHub: InsForge/InsForge](https://github.com/InsForge/InsForge) — リポジトリ・スター数・ライセンス・技術スタック確認, 取得日 2026-05-07
- [InsForge公式サイト](https://insforge.dev/) — プロダクトポジショニング, 取得日 2026-05-07
- [Agent Skills - Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) — Anthropic公式 Skills 仕様, 取得日 2026-05-07
- [Two Skills to Fix the Context Gap in Claude Code](https://blog.dailydoseofds.com/p/two-skills-to-fix-the-context-gap) — Avi Chawlaの追加記事（Skills設計論）, 取得日 2026-05-07
- [Claude Code Token Optimization: Stop the $1,600 Bill (2026 Guide)](https://buildtolaunch.substack.com/p/claude-code-token-optimization) — Claude Codeコスト最適化の総合ガイド, 取得日 2026-05-07
- [GitHub: NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) — 同思想の派生OSSキット, 取得日 2026-05-07
- [I saved 10M tokens (89%) on Claude Code with a CLI proxy (kilocode)](https://github.com/Kilo-Org/kilocode/discussions/5848) — 別アプローチでの大幅削減事例（クロスチェック用）, 取得日 2026-05-07
- [Reduce Token Consumption by 80%! Claude Code Skills Utilization Techniques (dev.to)](https://dev.to/kato11/reduce-token-consumption-by-80-claude-code-skills-utilization-techniques-1g7) — 日本人開発者の Skills活用ノウハウ, 取得日 2026-05-07
