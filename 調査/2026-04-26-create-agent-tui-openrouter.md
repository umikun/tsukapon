---
created: 2026-04-26
tags: [調査, create-agent-tui, OpenRouter, AIエージェント, TUI, agent-harness]
source: "[[Clippings/Post by @L_go_mrk on X 2.md]]"
---

# create-agent-tui ──「自分専用AIエージェント」をTypeScriptで一発スキャフォールドするOpenRouterのスキル

> **TL;DR**
> - `create-agent-tui` は **OpenRouter公式が配布するSkill**。CLIバイナリではなく、Claude CodeやCursor等のAIコーディングアシスタントに「TUI付きエージェント雛形を作って」と頼むためのSKILL.md一式。
> - 中身は **TypeScript + `@openrouter/agent` SDK + Ink(React TUI)** のスキャフォールダ。`create-react-app` のターミナル版と公式が比喩する。
> - 強みは「ツール（ファイル操作／シェル／Web検索など）・スラッシュコマンド・見た目を後付けで足し引きできる雛形」を1コマンド相当で出せる点。**OpenRouterの300以上のモデルを切替可能**で、業務用途に育てやすい。
> - 一方で、Claude Code・Codex CLI・Cursor・OpenCode・Hermes Agent等の**完成度の高い既製品**が既にあるため、「自前TUIを育てる手間」を払う価値があるかは要見極め。

---

## 📌 元テキスト（抜粋）

> これ発想がくっっっっっそやばすぎる。
> create-agent-tui：
> 自分が使いやすい思い通りの「ターミナルのUI」を作って、そこでAIを動かすことができる。ファイル操作・シェル実行・Web検索などのツールを後付けで増減できるので、業務に合わせて育てられる。
> まさに"自分のためだけの"真のAIエージェントを作ることが可能。。。

出典: [[Clippings/Post by @L_go_mrk on X 2.md]]

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| TUI (Terminal User Interface) | ターミナル上で動くキーボード操作のリッチUI | `Ink` `Textual` `bubbletea` |
| Agent Harness | LLM呼び出し・ツール実行・停止条件をループする"外殻" | `agent loop` `tool calling loop` |
| `@openrouter/agent` | OpenRouter公式のエージェントSDK（callModel／tool定義／停止条件） | `OpenRouter SDK Agentic Usage` |
| OpenRouter Skills | AIコーディング助手向けの再利用可能スキル配布形式（SKILL.md） | `npx skills add OpenRouterTeam/skills` |
| Ink | ReactでターミナルUIを書ける Vercel 系ライブラリ | `Ink React CLI` |
| `create-react-app` メタファ | "雛形をワンコマンドで吐く"のターミナル版 | `scaffolder` `bootstrap` |
| スラッシュコマンド | `/model` `/new` `/compact` 等の対話内コマンド | `slash command Claude Code` |
| OpenRouter | 300+ モデルを単一APIで叩けるルーター/プロキシ | `OpenRouter models` |

---

## 🧭 背景 / なぜ今これが話題なのか

2024〜2025年にかけて、**「ターミナルで動くAIコーディングエージェント」**が一気に主役級プロダクトに昇格した。代表例は **Claude Code**（Anthropic）、**Codex CLI**（OpenAI）、**Aider**、**OpenCode**、**Cursor のCLIモード** あたり。共通項は「IDEに引きこもらず、ターミナル＋ファイルシステム＋シェルを直接触らせる」設計で、**"AI as a CLI native"** の世界観が定着した。

ところが、いざ自社業務に当て込もうとすると、**既製品はどれも"そのままだと痒い所に手が届かない"**。

- ツール（社内API・DB・社内Slack）を増やしたい
- 表示スタイル（emoji / minimal / 非表示）や入力欄、起動バナーを変えたい
- スラッシュコマンドを業務独自フローに合わせたい
- モデルをタスク別に切り替えたい（重い設計はOpus、雑用はHaiku、長文はGemini等）

これらを満たそうとすると **「自分でAgent Harnessを作る」** 流れになる。が、ループ・トークン管理・セッション保存・streamingなど、足回りを書くだけで体力を持っていかれる。

**OpenRouter** は元々「1本のAPIキーで300+モデルを切り替えられるルーター」として支持されてきたが、2025〜2026年にかけて **`@openrouter/sdk` → `@openrouter/agent` という"エージェント用SDK"** を分離し、さらに **AIコーディングアシスタント向けのSkill配布**（`npx skills add OpenRouterTeam/skills`）まで整えた。**`create-agent-tui` はその"配布されるスキル"の1枚** で、**「Claude Codeに頼むと、Ink+TypeScript+OpenRouter Agent SDKの動くTUIプロジェクトが`npm start`で立ち上がる状態まで生成される」** というのが正体。

つまり技術的には、**①OpenRouter Agent SDK（中身）、②Ink/React（TUI描画）、③SKILL.md（生成手順を記述したスキル）** の3点セット。**「create-react-app for terminal agents」** という公式比喩が一番近い。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「ターミナルのUIを自分で作って、そこでAIを動かせる」 | Ink（Reactベース）でTUIをカスタマイズ可能。スタイル（grouped/emoji/minimal/hidden）、入力欄（block/bordered/plain）、ローダー（gradient/spinner/minimal）等を選択 | [Build Your Own Agent TUI – OpenRouter Docs](https://openrouter.ai/docs/guides/coding-agents/create-agent-harness-tui) | ✅ 一致 |
| 「ファイル操作・シェル実行・Web検索などのツールを後付けで増減できる」 | ツール定義は`tools.ts`に追加する設計。デフォルトは`get_current_time`/`calculate`等の最小例で、ファイル操作・シェル・Web検索は**自分で書き足す or 雛形プリセットで選ぶ**形。"後付けで増減できる"は正しいが"最初から豊富に揃っている"わけではない | [create-agent SKILL.md](https://openrouter.ai/skills/create-agent/SKILL.md) | ⚠️ ほぼ一致（誇張気味） |
| 「業務に合わせて育てられる」 | スラッシュコマンド（`/model` `/new` `/help` `/compact` `/session` `/export`）、セッション管理、設定の差し替えが想定済み。CLI REPL／HTTP APIサーバー（Hono/Express + SSE）／両対応の3パターンで生成できる | [OpenRouter Docs – create-agent-harness-tui](https://openrouter.ai/docs/guides/coding-agents/create-agent-harness-tui) | ✅ 一致 |
| 「真のAIエージェント」 | 内部で`@openrouter/agent`の callModel ループを回し、複数ターン・ツール実行・停止条件を扱う"フルAgent Harness"。定義としては正しい。ただし"真の"という形容は主観 | [OpenRouter Agentic Usage Docs](https://openrouter.ai/docs/sdks/agentic-usage) | ⚠️ ほぼ一致（"真の"は感想） |
| 「OpenRouterの300+モデルを切り替え可能」 | `--model anthropic/claude-sonnet-4`等で任意モデル指定可、OpenRouterのモデルカタログをそのまま使える | [OpenRouter Models](https://openrouter.ai/models) | ✅ 一致 |

---

## 🌐 最新動向（2026-04-26時点）

- **OpenRouter Skills エコシステムの整備**: `npx skills add OpenRouterTeam/skills` 経由でClaude Code / Cursor / Copilotに導入可能なスキル群を配布。`create-agent`／`create-agent-tui`／`openrouter-typescript-sdk`／`openrouter-agent-migration` などが揃う — [OpenRouter Skills](https://openrouter.ai/skills/create-agent/SKILL.md), 2026-04
- **`@openrouter/agent` パッケージの分離**: 旧 `@openrouter/sdk` から callModel・tool定義・停止条件を切り出し、エージェント特化のSDKが別パッケージ化された — [OpenRouter Agentic Usage](https://openrouter.ai/docs/sdks/agentic-usage), 2026-Q1
- **競合TUIエージェントの百花繚乱**: `Ralph TUI`（Claude Code/OpenCode/Factory Droidをタスクリストで自律ループ）、`agent-deck`（Claude/Gemini/OpenCode/Codexのセッション管理）、`tui-use`（既存TUIアプリにエージェントを"打鍵させる"）、`tamux`（永続セッション+合意形成エージェント）など、**TUIエージェントOSSが2026年Q1〜Q2で集中投下** — [GitHub検索結果群], 2026-04
- **"Build Your Own"潮流**: Mager社の "Claude Agent SDK: Build Your Own AI Terminal in 10 Minutes"(2026-03)、OpenHarness v0.1.7のReact TUIアップデート、Hermes Agentのslash-command autocomplete実装など、**自前TUIを10分で立てるDIYブーム** — [Mager Blog](https://www.mager.co/blog/2026-03-14-claude-agent-sdk-tui), 2026-03
- **Codex Skills（OpenAI）の同時並走**: OpenAIも"Agent Skills"を Codexで提供開始しており、**スキル配布フォーマット競争**が始まっている — [Agent Skills – Codex | OpenAI Developers](https://developers.openai.com/codex/skills), 2026-04

---

## 🧩 関連概念・隣接分野

- **OpenRouter Agent SDK (`@openrouter/agent`)**: create-agent-tui が生成するコードの中身。callModelループ・Zodスキーマでのツール定義・stop conditionsを扱う"内殻"側。TUIを使わないheadless運用も可能（`src/headless.ts`）。
- **Ink（React for CLI）**: TUI描画レイヤー。ReactコンポーネントでターミナルUIを組める。OpenRouterはこれを採用。Pythonで同じことをやりたいなら **Textual**（DavidKoleczek/agent-tui等が採用）が近い。
- **SKILL.md / Agent Skills フォーマット**: AIコーディングアシスタントに渡す"再利用可能な手順書"の業界標準化が進行中。Anthropic（Claude Skills）・OpenAI（Codex Skills）・OpenRouter（OpenRouter Skills）が並走。
- **MCP (Model Context Protocol)**: ツールを"プロトコル化"してエージェントに刺す Anthropic 系の規格。create-agent-tui は MCP ではなく直接Zodツール定義だが、思想的には隣接。MCPサーバを呼ぶツールを追加することもできる。
- **既製TUIエージェント群**: [[Clippings/]] 内にある Claude Code・OpenCode・Codex CLI 関連のクリップ（あれば）と並べて見ると差分が分かる。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「業務独自のツール・スラッシュコマンド・見た目をフル制御できる雛形が一発で出るのは破壊的に楽。OpenRouterのモデル切替も最強。学習コストは"npm start" レベル」
- **否定 / 慎重派の主張**:
  - **既製品の完成度が桁違い**: Claude Code・Codex CLI・Cursor は数十人規模のチームが磨き上げており、自前TUIで追いつくのは現実的でない。"育てられる"=メンテナンスを永続的に背負うこと。
  - **OpenRouterロックイン**: SDK・スキル・モデルカタログがすべてOpenRouterに寄っているので、ベンダー集中リスクがある（料金・API変更・サービス継続性）。
  - **TUIへの過大評価**: 業務用途では結局IDE統合（Cursor/VSCode拡張）の方がDX高いという声も根強い。TUIは"開発者のおもちゃ"に留まる懸念。
  - **"create-agent-tui"の名前衝突**: GitHub上には [DavidKoleczek/agent-tui](https://github.com/DavidKoleczek/agent-tui)（Python/Textualベース）、[pproenca/agent-tui](https://github.com/pproenca/agent-tui)（既存TUIアプリをエージェントに操作させる別物）など、**名前が似た無関係プロジェクト**が複数存在。元ツイートを真に受けて検索すると別物に着地しがち。
  - **バージョンが v0.0.0**: SKILL.md上は開発初期段階の表記。プロダクション利用には人柱要素あり。
- **中立的に見るときの補助線**: 「既製品で間に合うか／間に合わないか」を業務要件で先に切り分ける。**社内API・社内DB・独自スラッシュコマンドが3つ以上必要**ならcreate-agent-tuiの自前路線、そうでなければClaude Code＋skill側のカスタマイズで足りる場合が多い。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] create-agent-tui のデフォルト生成物に、**ファイル操作／シェル実行／Web検索ツール**は実際に同梱されているか（SKILL.mdの例示は時刻・計算のみ）。プリセットメニューに含まれるのか、毎回 Claude Code に書かせるのか
- [ ] **MCPサーバとの連携**: Anthropic系MCPサーバを `tools.ts` 内から呼ぶ標準パターンは確立されているか
- [ ] **ライセンスと商用利用条件**（OpenRouter Skills 全体）、自社製品にバンドルできるか
- [ ] **コスト試算**: OpenRouter経由でClaude Sonnet 4を1日中エージェントループに回した場合の月額目安、Claude Code直接利用との価格差
- [ ] **vault運用への持ち込み**: Obsidianファイル操作専用ツールを足した"vaultネイティブAgent TUI"を自分用に作れるか（`Edit/Read/Glob/Grep` + Dataview連携）
- [ ] 競合 [Hermes Agent](https://github.com/nousresearch/hermes-agent) や Mariozechner の minimal coding agent との実装比較

---

## 📚 参考資料

- [Build Your Own Agent TUI – OpenRouter Documentation](https://openrouter.ai/docs/guides/coding-agents/create-agent-harness-tui) — create-agent-tui の公式ガイド（機能・スタイル・スラッシュコマンド・必要環境を抽出）, 取得日 2026-04-26
- [create-agent SKILL.md – OpenRouter](https://openrouter.ai/skills/create-agent/SKILL.md) — 同梱ツール定義・依存ライブラリ・スキルメタデータを確認, 取得日 2026-04-26
- [Agentic Usage – OpenRouter SDK Docs](https://openrouter.ai/docs/sdks/agentic-usage) — `@openrouter/agent` SDK の callModel ループ仕様, 取得日 2026-04-26
- [OpenRouter Models](https://openrouter.ai/models) — 対応モデルカタログ（300+）, 取得日 2026-04-26
- [OpenRouter Quickstart](https://openrouter.ai/docs/quickstart) — APIキー取得とSDK導入手順, 取得日 2026-04-26
- [DavidKoleczek/agent-tui (GitHub)](https://github.com/DavidKoleczek/agent-tui) — 名前が似ているがPython/Textualベースの**別プロジェクト**であることを確認, 取得日 2026-04-26
- [pproenca/agent-tui (GitHub)](https://github.com/pproenca/agent-tui) — TUIアプリ操作用の別プロジェクトであることを確認, 取得日 2026-04-26
- [Claude Agent SDK: Build Your Own AI Terminal in 10 Minutes – Mager](https://www.mager.co/blog/2026-03-14-claude-agent-sdk-tui) — 自前TUIエージェントDIYの隣接事例, 取得日 2026-04-26
- [Agent Skills – Codex (OpenAI Developers)](https://developers.openai.com/codex/skills) — スキル配布フォーマット競争の文脈, 取得日 2026-04-26

---

## 🗒 メモ

- 元ツイートの "ファイル操作・シェル実行・Web検索などのツールを後付けで増減できる" は **構造的には事実**だが、**「最初から全部入っている」わけではない**点は補足したい。スキル本体に同梱されているのは最小ツール例で、Claude Code に「ファイル操作とシェル実行ツールを足して」と追加で頼むか、自分で `tools.ts` に書く構成。SNSで紹介する時はここを正確に言わないと、触ってみて「思ってたのと違う」となる人が出そう。
- **vaultネイティブAgent TUI** を作る発想は普通に強い。Obsidian の Edit/Read/Glob/Grep 相当をツールに登録した上で、`/daily` `/note` `/thread` 等のスラッシュコマンドを業務フローに合わせて足せば、Claudian の進化形になる。**[[Claudian-スキル候補.md]]** に "vault-native agent TUI 試作" として候補登録する価値あり。
- noteネタ化するなら「**Claude Code/Codex CLIで間に合わない人だけ読む、自前TUIエージェント時代の歩き方**」みたいな切り口。"create-react-app for agents" のメタファをそのまま冒頭に持ってくると刺さりやすい。
- X投稿化するなら、**名前衝突3兄弟の話**（OpenRouter版／DavidKoleczek版／pproenca版）が短くて面白い。「create-agent-tui で検索すると3つ出てくる、本物はOpenRouterのSkill」という単発ポストでもいい。
