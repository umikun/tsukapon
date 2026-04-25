# Claude Codeに入れるべき拡張機能

> **🔗 関連コンテンツ（反映済みアーカイブ）**
> - 📋 Claudianスキル一覧（反映先）: [[Claudian-スキル一覧.md]]
> - 📘 vault全体ルール: [[CLAUDE.md]]

Claude Code触り始めた人、頼むから **Playwright・Superpowers・Context7** の3つだけは先に入れて。
AIのアウトプットが別物になる。ハルシネーション8割減。

全6つ、**0円**。入れ方は下記。

## 6つの効果

| # | 拡張機能 | 効果 |
|---|---|---|
| ① | **Playwright** | ブラウザ自動操作。動作確認を自分でやる必要が消滅。 |
| ② | **Code Review** | コードレビュー自動化。 |
| ③ | **GitHub** | 「プルリク作って」で自動作成。 |
| ④ | **Frontend Design** | AIが作るUIの「ダサい問題」解決。プロっぽくなる。 |
| ⑤ | **Superpowers** | Claudeの能力を底上げ。ジュニア→シニアに化ける感覚。 |
| ⑥ | **Context7** | 最新情報反映＋ハルシネーション抑制。 |

> 僕はContext7入れてからClaudeが的外れな回答する頻度が体感8割減ったwww

## 入れ方

ターミナルで以下を実行するだけ。

```bash
claude plugins install <プラグイン名>
```

- 1つあたり **30秒**、6つで **3分**。
- Anthropicの公式ストアに全部ある。
- ChatGPTにもGeminiにもない **Claude Code限定の武器**。

**保存して今日入れて🔥**

---

## 調査メモ（2026-04-15）

### ❌ 事実と異なる情報

| 誤情報 | 実態 |
|---|---|
| `claude plugins install` コマンド | **存在しない**。Claude Codeにプラグインストアはない |
| 「Anthropicの公式ストアに全部ある」 | 公式ストアは**存在しない** |
| 「Claude Code限定の武器」 | MCPサーバー自体は他ツールでも利用可能 |

正しいMCPサーバーの追加方法は `claude mcp add <サーバー名>` コマンド。

### 各ツールの実用性評価

| 拡張 | 評価 | コメント |
|---|---|---|
| ① Playwright MCP | ⭐⭐⭐ 有用 | ブラウザ自動テストに便利。ただし **claude-in-chrome** を導入済みなら用途が被る |
| ② Code Review | ⚠️ 不要 | Claude Code に **標準搭載済み**（`/review` スキル） |
| ③ GitHub | ⚠️ 不要 | `gh` CLIでPR作成等が既に可能。標準機能で十分 |
| ④ Frontend Design | ❓ 不明 | 具体的に何を指すか不明確。公式のものではない可能性が高い |
| ⑤ Superpowers | ❓ 要注意 | 「能力を底上げ」は曖昧。非公式ツールはプロンプト注入リスクあり |
| ⑥ Context7 MCP | ⭐⭐⭐ 有用 | ライブラリの **最新ドキュメント** を取得できるMCPサーバー。ハルシネーション対策に効果的 |

### 🎯 結論：導入すべきは Context7 のみ

```bash
# Context7の正しいインストール方法
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

- Playwright → claude-in-chrome で代替済み
- Code Review / GitHub → Claude Code 標準機能で対応済み
- Frontend Design / Superpowers → 信頼性不明
- **Context7 だけが「今ない機能」を補完してくれる**（最新ドキュメント参照）

### ⚠️ このポスト自体の信頼性

- 「ハルシネーション8割減」「ジュニア→シニアに化ける」は主観的で検証不能
- 存在しないコマンドを紹介 → 投稿者自身の理解が浅い可能性
- SNSの煽り系テック情報は公式ドキュメントで裏取りが必要
