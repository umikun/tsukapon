---
created: 2026-05-07
tags:
  - 調査
  - ClaudeCode
  - Codex
  - MCP
  - OpenAI
  - エージェント連携
source: 直接貼付（ChatGPT/Claudeとの会話履歴）
action: 運用参考
---

# Claude Code から Codex（OpenAI CLI）を MCP 経由で呼ぶ手順 — `codex mcp serve` は誤記、正解は `codex mcp-server`

> **🔗 関連コンテンツ**
> - 🤖 同テーマ（Claude Codeのコンテキスト最適化）: [[調査/2026-05-07-insforge-skills-claude-code-token-cut.md]]
> - 🤖 Claude Codeプラグイン拡張: [[調査/2026-05-04-claude-code-superpowers-plugin.md]]
> - 🛠 Codex×外部サービス活用例: [[SNS運用/ネタ/2026-05-06-codex-gpt55-ios-20min-workflow.md]]
> - 🛠 Codex×他ツール統合: [[SNS運用/ネタ/2026-05-06-codex-heygen-hyperframes-elevenlabs-stack.md]]
> - 🧰 Claudianのスキル運用全体: [[Claudian-スキル一覧.md]]

> **TL;DR**
> Claude Code から Codex を MCP で呼ぶ手順は概ね正しいが、**コマンド表記に1文字レベルの間違いあり**。元テキストの `codex mcp serve` は誤りで、**公式は `codex mcp-server`（ハイフン区切り、`mcp` と `server` の間にスペースなし）**。`codex mcp` は別物で、Codex側に **他の** MCPサーバーを追加・管理するためのコマンド群。さらに2026-03-30から **OpenAI公式の「Codex Plugin for Claude Code」** が公開されており、自前でMCP登録するより**プラグイン経由の方が今は主流**。「セカンドオピニオン用途」なら公式プラグイン、「カスタム制御したい」ならMCP直接接続、と使い分けるのが2026年5月時点のベストプラクティス。

---

## 🗒 メモ

> ⚠️ このセクションは **冒頭に配置**（2026-05-06 ルール変更）。**「この調査をどう使うか」のアクション仮説**を最初に書くことで、次のアクションが見えやすくなる。

### このネタの使い道

- **第1用途（運用参考）**: 自分の Claude Code 環境に Codex を組み込むための **正しい手順書** として使う。元の会話の「`codex mcp serve`」を鵜呑みにすると `Error: unrecognized subcommand` で詰まる。**正解は `codex mcp-server`**
- **第2用途（投稿ネタ・派生）**: 「ハマりポイント」 + 「公式プラグインの方が楽」 まで踏み込めば AI/Claude Code 界隈ウケする note 記事になる
- **戦略接続**: Claudian（Claude Code）運用の幅を広げる土台。Codex連携が動けば、後段で「Anthropic 4.7 vs GPT-5 同タスク比較」のレビュー記事も書ける

### 実行手順（自分用 cheat-sheet・コマンドだけ抜粋）

```bash
# 1. Codex CLI インストール
npm install -g @openai/codex

# 2. Codex ログイン（ChatGPTアカウント or APIキー）
codex login
# または: codex login --api-key

# 3. Claude Code に Codex を MCP として登録（⚠️ 正しいコマンドはこれ）
claude mcp add codex -- codex mcp-server

# 4. 確認
claude
# Claude Codeセッション内で:
/mcp
# → codex が `connected` ならOK
```

### 派生ネタ候補

- 「`codex mcp serve` でハマった話と公式プラグイン乗り換え」体験ログ note記事
- 「Claude Code × Codex の双方向通信（agent-bridge）でAIをペアプロさせてみた」
- 「Codex Plugin vs MCP直接接続、結局どっち？」比較記事
- 「Codex CLI v0.x → 1.x のコマンド体系の変化まとめ」（CLI仕様変更が頻繁）

### 自分用の検証タスク

- [ ] `claude mcp add codex -- codex mcp-server` を実行して `/mcp` で `connected` になるか確認
- [ ] Codex Plugin for Claude Code（`openai/codex-plugin-cc`）も入れて、MCP直接接続との挙動差を比較
- [ ] 双方向通信用 `raysonmeng/agent-bridge` を試す（ChatGPT奥義候補の検証）
- [ ] 会話の最後に書かれた `~/.codex/config.toml` への `claude` 登録（逆方向）も試す

---

## 📌 元テキスト（抜粋）

> 画像、見ました！これはClaude CodeからCodex（OpenAIのCLI）をMCP経由で呼び出してる画面ですね。やり方わかりますよ。
>
> 仕組みとしては、**Codex CLIをMCPサーバーとしてClaude Codeに登録**することで、Claude Codeのセッション中に「codex」というツールとして呼び出せるようになる、という連携です。
>
> ```bash
> claude mcp add codex -- codex mcp serve
> ```
>
> Codex MCPは **`codex mcp serve`** が正式コマンド（古い情報だと `codex mcp` だけのもありますが、新しめのバージョンは `serve` サブコマンドが推奨）

出典: 直接貼付（Dev6さん向けの回答テキスト、ChatGPT/Claudeとの会話）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code | Anthropic公式のターミナル型コーディングエージェント | `claude code anthropic` |
| Codex CLI | OpenAI公式のターミナル型コーディングエージェント。`@openai/codex` パッケージ | `openai codex cli` |
| MCP (Model Context Protocol) | エージェント↔ツール接続の標準プロトコル。Anthropic主導で2024年公開 | `model context protocol` |
| `codex mcp-server` | Codexを **MCPサーバーとして** stdio で起動する公式コマンド（実験的） | `codex mcp-server stdio` |
| `codex mcp` | Codexから **他の** MCPサーバーを管理するコマンド群（add/list/get/login/logout/remove） | `codex mcp add` |
| Codex Plugin for Claude Code | OpenAI公式のClaude Code向けプラグイン。MCP登録不要 | `openai codex-plugin-cc` |
| AgentBridge | Claude Code ↔ Codex の双方向通信を実現するOSS（コミュニティ製） | `raysonmeng agent-bridge` |
| `~/.codex/config.toml` | Codex CLI の設定ファイル。MCPサーバー登録もここに書ける | `codex config toml` |
| `~/.claude.json` | Claude Code の設定ファイル。MCPサーバー登録もここに書ける | `claude.json mcp` |

---

## 🧭 背景 / なぜ今これが話題なのか

### Claude Code と Codex CLI の "ターミナル系エージェント" 二強時代

2025年は Claude Code（Anthropic）が独走、2026年に入って **Codex CLI（OpenAI）** が「Rust製・MCPクライアント＋サーバー両対応・GitHub Action連携」で急速にキャッチアップ。「2026年で最も Claude Code のインフラ準備が整った競合」と評される地位に到達。

この状況で、**「両方を並走させて使い分ける」「相互レビューさせる」** というワークフローが注目され、その入口として MCP 経由の連携が話題に。

### MCP の "クライアント／サーバー両対応" の意味

Codex CLI には **2つのモード** がある:

1. **MCPクライアント**: 他のMCPサーバー（Brave Search、GitHub等）を呼ぶ → コマンドは `codex mcp add` 等
2. **MCPサーバー**: Codex自身を他のエージェント（Claude Code等）から呼べるツールとして公開する → コマンドは `codex mcp-server`

混同しやすいが、**コマンドが違う**。元テキストの `codex mcp serve` は どちらでもなく、誤記。

### 2026-03-30 の "Codex Plugin for Claude Code" 公開

OpenAIが [Codex Plugin for Claude Code](https://community.openai.com/t/introducing-codex-plugin-for-claude-code/1378186)（GitHubは `openai/codex-plugin-cc`）を公式リリース。**「すでにClaude Codeを使っている人が、Codexを同じワークフローに組み込む簡単な方法」** と位置付けられている。

特徴:
- ローカルのCodex CLI＋Codex App Server経由で動く
- 既存のCodex認証・設定・MCPセットアップをそのまま流用
- 用途: ① 標準Codexレビュー、② 懐疑的対抗レビュー、③ 別エージェントからの二次レビュー

これにより「自前でMCP登録」のハードルが下がり、**多くの場合はプラグインで十分**になった。

### 2026-04-16 の Codex 90+ プラグイン同梱アップデート

OpenAIがCodexアップデートで **90以上のプラグイン**（Atlassian Rovo、CircleCI、CodeRabbit、GitLab Issues、Microsoft Suite、Render等）を公開。**プラグインは「Skills + アプリ統合 + MCPサーバー」をまとめたパッケージング単位** に進化。

### 2026年4〜5月の "AgentBridge" 登場

[`raysonmeng/agent-bridge`](https://github.com/openai/codex/discussions/15374) が **Claude Code Channels (MCP) と Codex App Server の間で双方向通信** を実現。**「実行中のセッションに mid-execution で割り込みできる」** ピュアローカルMCPサーバーで、ChatGPT/Claudeの "ペアプロ" ワークフローを可能にする。元テキストの「ChatGPT奥義、例のアレ」はこれの可能性が高い。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| `npm install -g @openai/codex` でインストール | 公式パッケージ名は `@openai/codex` で正しい。Node.js 18.18以降が必要 | [CLI – Codex / OpenAI Developers](https://developers.openai.com/codex/cli) | ✅ 一致 |
| `codex login` でChatGPTアカウントログイン可 | ChatGPT Plus/Pro/Team で利用可。`codex login --api-key` でAPIキーログインも可 | 同上 | ✅ 一致 |
| **`codex mcp serve` が正式コマンド** | ❌ **誤り**。公式コマンドは **`codex mcp-server`**（ハイフン区切り、サブコマンドではなく単一コマンド）。`codex mcp serve` は存在しない | [Command line options – Codex CLI / OpenAI Developers](https://developers.openai.com/codex/cli/reference) | ❌ 要注意（最重要） |
| `codex mcp` だけだと古い情報 | ❌ **誤り**。`codex mcp` は今も**現役の公式コマンド群**。ただし用途が違って、Codex側に**他の**MCPサーバーを追加管理するためのコマンド（`codex mcp add/list/get/login/logout/remove`） | 同上 | ❌ 要注意 |
| `claude mcp add codex -- codex mcp serve` で登録 | コマンド構文（`claude mcp add <name> -- <cmd>`）は正しいが、後半の `codex mcp serve` を `codex mcp-server` に修正すれば動く | [Connect Claude Code to tools via MCP / Claude Code Docs](https://code.claude.com/docs/en/mcp) | ⚠️ ほぼ一致（コマンド修正で動作） |
| Claude Code内 `/mcp` で接続確認 | `/mcp` コマンドは公式に存在し、登録済みMCPサーバー一覧と接続状態を表示 | 同上 | ✅ 一致 |
| Codex側使用量はChatGPTプランまたはAPI課金 | 公式仕様通り | [CLI – Codex / OpenAI Developers](https://developers.openai.com/codex/cli) | ✅ 一致 |
| 逆方向（CodexからClaude Code）も可、`~/.codex/config.toml` に登録 | 公式に `~/.codex/config.toml` 経由で他のMCPサーバー登録可。`claude` を登録する場合の実装は要確認だが、原理上は可能 | [Model Context Protocol – Codex / OpenAI Developers](https://developers.openai.com/codex/mcp) | ⚠️ ほぼ一致（Claude側がMCPサーバー化対応してれば） |
| 「ChatGPT奥義、例のアレ」の正体 | 推測だが、2026年4〜5月に話題の `agent-bridge`（Claude↔Codex双方向通信）か、Codex Plugin for Claude Code の懐疑的対抗レビュー機能の可能性が高い | [openai/codex Discussion #15374](https://github.com/openai/codex/discussions/15374) | 🔍 推測（特定情報なし） |

---

## 🌐 最新動向（2026-05時点）

- **Codex Plugin for Claude Code 公開（2026-03-30）**: OpenAI公式。MCP登録より楽 — [OpenAI Developer Community](https://community.openai.com/t/introducing-codex-plugin-for-claude-code/1378186), 2026-03
- **Codex 90+ プラグイン同梱アップデート（2026-04-16）**: Atlassian Rovo / CircleCI / CodeRabbit / GitLab Issues / Microsoft Suite / Render など — [Zuplo Blog](https://zuplo.com/blog/openai-codex-mcp-plugins-api-teams), 2026-04
- **AgentBridge による Claude Code ↔ Codex 双方向通信実現**: ローカルMCPサーバー、mid-execution割り込み対応 — [openai/codex Discussion #15374](https://github.com/openai/codex/discussions/15374), 2026-04
- **`codex mcp-server` が公式CLIに正式追加**: 実験的扱いだが安定動作 — [Command line options – Codex CLI](https://developers.openai.com/codex/cli/reference), 2026
- **`tuannvm/codex-mcp-server` 等のサードパーティラッパーは依然有効**: 公式に飽き足らない人向け — [GitHub: tuannvm/codex-mcp-server](https://github.com/tuannvm/codex-mcp-server), 2026
- **Claude Code MCP公式ドキュメントが充実**: `claude mcp add` のCLIフラグ・JSON設定の両対応を整理 — [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp), 2026-05
- **NVM/PATH問題の周知**: MCPサーバーは親プロセスの環境変数を継承しないため、`env.PATH` 明示が必須という運用知見が定着 — [Cor.inc Blog](https://cor-jp.com/en/blog/codex-mcp-troubleshooting/), 2026

---

## 🧩 関連概念・隣接分野

- **Anthropic Agent Skills**: Claude Code の `.claude/commands/` 経由で動くスキル群。MCPと役割分担: 「Skillsは静的知識／MCPはライブツール」 → [[Claudian-スキル一覧.md]]
- **Codex Plugin for Claude Code（公式）**: `openai/codex-plugin-cc`。MCP登録より簡単な公式ルート
- **AgentBridge（コミュニティOSS）**: 双方向セッション統合。`raysonmeng/agent-bridge`
- **InsForge Skills**: 同じ「コンテキスト工学」系の最適化アプローチ → [[調査/2026-05-07-insforge-skills-claude-code-token-cut.md]]
- **Codex CLI plugins 90+**: 「プラグイン = Skills + App統合 + MCPサーバー」のパッケージング進化形
- **`@modelcontextprotocol/sdk`**: MCPサーバー自作用のTypeScript SDK。本格カスタムするなら必須

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - MCP経由で複数AIを使い分けられるのは強力（モデル比較、セカンドオピニオン、専門領域の使い分け）
  - ローカル動作で外部ホップなし、低レイテンシ
  - OSS的・標準準拠で長期運用に向く
  - 双方向（AgentBridge）まで使えば本格的なAIペアプロが可能

- **否定 / 慎重派の主張**:
  - **コマンド名のtypo一つで詰む** — `codex mcp serve` vs `codex mcp-server` のような微妙な違いに弱く、CLI仕様変更も頻繁
  - **公式 Codex Plugin for Claude Code が出た今、自前MCP登録はオーバーキル**になりつつある（多くの人はプラグインで十分）
  - **コスト二重化リスク**: ChatGPT Plus + Anthropic API を両方払うことになる。本当に両方必要か精査
  - **MCPサーバー起動時のPATH問題**（NVM環境で `command not found` 多発）は2026年でもよくハマる
  - **デバッグの難しさ**: 「Claude Codeが呼んだCodexがエラー出した」場合のスタックトレースが分かりづらい
  - **応答時間の積み上がり**: Claude → Codex往復で1リクエスト10秒超えも珍しくない

- **中立的に見るときの補助線**:
  - **「セカンドオピニオン」「Codex特化タスク」用途なら公式 Codex Plugin で十分**。MCP登録は不要
  - **カスタム制御したい・双方向通信したい・他のMCPサーバーと併用したい**場合だけ MCP直接接続
  - 入門時は **公式プラグインから始めて、不足を感じたらMCP接続に降りる** 順序が安全

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] `codex mcp-server` の `--port` オプションや stdio 以外のトランスポート対応状況
- [ ] Codex Plugin for Claude Code と MCP直接接続を併用した時の挙動（重複呼び出しになるか）
- [ ] AgentBridge の実運用安定性とセキュリティ（mid-execution割り込みの誤動作リスク）
- [ ] `~/.codex/config.toml` に Claude Code を登録する逆方向の正確な記法
- [ ] Codex 0.x → 1.x のコマンド体系変更履歴と移行ガイド
- [ ] 「ChatGPT奥義、例のアレ」の正体（AgentBridge？Plugin？別の何か？） — 元会話のコンテキスト追跡
- [ ] Codex Plugin と Claude Code の利用ログ（トークン消費）の合算可視化方法

---

## 📚 参考資料

- [Command line options – Codex CLI / OpenAI Developers](https://developers.openai.com/codex/cli/reference) — `codex mcp` と `codex mcp-server` の正確な仕様（最重要ファクトチェック源）, 取得日 2026-05-07
- [CLI – Codex / OpenAI Developers](https://developers.openai.com/codex/cli) — Codex CLI 公式概要・インストール手順, 取得日 2026-05-07
- [Model Context Protocol – Codex / OpenAI Developers](https://developers.openai.com/codex/mcp) — Codex のMCPクライアント機能解説, 取得日 2026-05-07
- [Connect Claude Code to tools via MCP / Claude Code Docs](https://code.claude.com/docs/en/mcp) — Claude Code 側の MCP 接続公式手順, 取得日 2026-05-07
- [Introducing Codex Plugin for Claude Code](https://community.openai.com/t/introducing-codex-plugin-for-claude-code/1378186) — 2026-03-30 公開の公式プラグイン解説, 取得日 2026-05-07
- [OpenAI Codex Ships 90+ Plugins with MCP Servers Inside (Zuplo)](https://zuplo.com/blog/openai-codex-mcp-plugins-api-teams) — 2026-04-16 アップデートの解説, 取得日 2026-05-07
- [Claude Code Channels (MCP) bidirectional Codex (openai/codex Discussion #15374)](https://github.com/openai/codex/discussions/15374) — AgentBridge による双方向通信の議論, 取得日 2026-05-07
- [GitHub: tuannvm/codex-mcp-server](https://github.com/tuannvm/codex-mcp-server) — サードパーティMCPラッパー, 取得日 2026-05-07
- [GitHub: agency-ai-solutions/openai-codex-mcp](https://github.com/agency-ai-solutions/openai-codex-mcp) — もう1つの代替MCPラッパー, 取得日 2026-05-07
- [How to Set Up Codex MCP for Claude Desktop / Cor.inc Blog](https://cor-jp.com/en/blog/codex-mcp-troubleshooting/) — NVM/PATH問題の典型例, 取得日 2026-05-07
- [Claude + Codex CLI: Agentic Coding (Sangho Oh / Medium)](https://medium.com/@sangho.oh/claude-codex-cli-agentic-coding-a98c83ba043e) — 実運用例の体験記事, 取得日 2026-05-07
- [GitHub: openai/codex-plugin-cc](https://github.com/openai/codex-plugin-cc) — OpenAI公式プラグインリポジトリ, 取得日 2026-05-07
