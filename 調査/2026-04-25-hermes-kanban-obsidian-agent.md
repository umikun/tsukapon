---
created: 2026-04-25
tags: [調査, Obsidian, Hermes, Kanban, AIエージェント, LocalFirst, NousResearch]
source: "[[Clippings/Post by @ShaneRobinett on X.md]]"
---

# Hermes Kanban v1.5.0：Obsidian × Nous Research のローカルAIエージェント基盤を読み解く

> **TL;DR**
> Hermes Kanban は **Nous Research の自己改善型エージェント「Hermes Agent」を Obsidian の Kanbanボードで操縦するためのブリッジプラグイン**。本体の Hermes Agent は2026年2月にローンチされ既にGitHub星40,000超の大本命OSSで、Karpathy提唱の「RAGを使わずAIが育てるmarkdownナレッジベース」もスキルとして取り込んでいる。今回の v1.5.0（2026-04-24）はその"Obsidianフロントエンド"側を整える地味だが重要な更新で、**完全ローカル × ファイル実体markdown × Kanban駆動で自律エージェントが回る**世界観の現在地を映している。ただし本体スター182 / 依存先obsidian-kanban / Hermes Agentそのものの導入が前提なので、**気軽に試すというより「Hermesエコシステム住人」専用**なのが実態。

## 📌 元テキスト（抜粋）

> Hermes Kanban v1.5.0 がリリースされました！ Obsidian内でHermesエージェントを実行しているすべての人にとっての大きなアップグレードです。
> ・スマートカードアーカイブ：完了したカードをDone → Kanban/archive.md に自動移動
> ・ボードテンプレート：Sprint、Bug Triage、Release、またはPersonalボードをワンクリック
> ・GitHub設定：フルコンフィグパネル — 同期機能は近日公開
> ・BRATサポート：超簡単な自動更新
> これによりHermesは真の自律型プロジェクト共同パイロットに進化：目標をKanbanボードに分解、日次スタンドアップを実行、ブロックを追跡 — すべてObsidianのボールト内で完全にローカル。

出典: [[Clippings/Post by @ShaneRobinett on X.md]] / [リリースページ](https://github.com/GumbyEnder/hermes-kanban/releases/tag/v1.5.0)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Hermes Agent | Nous Researchが2026年2月公開したOSS自己改善型AIエージェント | Hermes Agent Nous Research |
| Hermes Kanban | Hermes Agent ↔ ObsidianのKanbanボードを繋ぐブリッジプラグイン | hermes-kanban GumbyEnder |
| Nous Research | Hermes系LLMで知られるOSS寄りのAI研究グループ | Nous Research Teknium |
| obsidian-kanban | mgmeyersが開発するKanbanボードプラグイン（Hermes Kanbanの依存先） | obsidian-kanban mgmeyers |
| BRAT | Beta Reviewer's Auto-update Tool。コミュニティ未掲載プラグインを自動更新で使う | BRAT TfTHacker |
| LocalFirst | クラウドに頼らずローカル実行・ローカル保存を主軸にする思想 | local-first software |
| LLM Knowledge Base | KarpathyがX上で提唱した「RAGの代わりにAIがmarkdownを育てる」アーキ | Karpathy LLM Knowledge Base |
| MultiLevel Memory | Hermesの長期/中期/短期記憶階層 | Hermes multi-level memory |
| 永続的ターミナルアクセス | Hermes Agentが自前のシェルを持ち続ける機能 | Hermes persistent terminal |
| デイリースタンドアップ | エージェントが毎朝タスク状況をレビューする儀式 | AI standup automation |

---

## 🧭 背景 / なぜ今これが話題なのか

**2025年: Obsidian + AIエージェント熱の予兆**
Andrej KarpathyがX上で「**LLM Knowledge Base** ＝ RAGに頼らず、AI自身がmarkdownのナレッジライブラリを育てる」アーキテクチャを共有し話題に（[VentureBeat](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)）。これがObsidianコミュニティに刺さり、「vault = AIの長期記憶」という発想が定着し始めた。

**2026年2月: Nous Research が "Hermes Agent" を公開**
「LLMの忘却問題」を多階層メモリ＋永続的ターミナルアクセスで解決する自律型エージェントとしてローンチ（[Dev|Journal 2026-02-26](https://www.earezki.com/ai-news/2026-02-26-nous-research-releases-hermes-agent-to-fix-ai-forgetfulness-with-multi-level-memory-and-dedicated-remote-terminal-access-support/)）。任意のLLM（Nous Portal / OpenRouter 200+ / NVIDIA NIM / Ollama / OpenAI）を背後に置けて、$5 VPSからGPUクラスタまで動かせる柔軟性が売り。Karpathyの LLM Knowledge Base もビルトインスキルとして取り込み、**ObsidianはHermesの主要フロントエンドの1つ**として位置づけられた。

**2026年3-4月: エコシステム拡大**
- AMDが Ryzen AI Max+ / Radeon GPU で Hermes Agent をローカル実行する公式ブログを公開（[AMD公式](https://www.amd.com/en/blogs/2026/run-hermes-agent-locally-on-amd-ryzen-ai-max-processors-and-radeon-gpus.html)）
- Ollama + Hermes Agent のローカル構成記事が連発（[Medium / Mehul Gupta 2026-04](https://medium.com/data-science-in-your-pocket/hermes-agent-with-ollama-setup-b0a442f53241)）
- GitHub星 **40,000超** を獲得、ヘルメスは "OpenClawの代替を超える" と報じられる（[36kr](https://eu.36kr.com/en/p/3764418640003840)）

**2026年4月24日: Hermes Kanban v1.5.0 リリース**
GumbyEnder氏のObsidianプラグイン × Hermesスキル（[GumbyEnder/hermes-kanban](https://github.com/GumbyEnder/hermes-kanban)）。本体スター182・MITライセンス・TypeScript+JavaScript製。**REST APIをローカルポート27124で公開し、Hermes Agent側からKanbanカードをCRUDする**設計。今回の更新はアーカイブ自動化、テンプレート、GitHub設定UI、BRAT対応など、**プラグインとしての"完成度"をまとめて押し上げる**地味だが本質的な内容。

**ハンドル名タグの意味**
@NousResearch（本体）/ @Teknium（Nous中核人物）/ @kepano（Steph Ango = Obsidian CEO）/ @mgmeyers（obsidian-kanban作者）/ @obsdmd（Obsidian公式）— **Hermes側 + Obsidian側の主要人物全員に向けたアナウンス**で、エコシステム認知を狙ったポストとわかる。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Hermes Kanban v1.5.0 がリリースされた | リリース日 2026-04-24、リリースページ実在 | [GitHub Release](https://github.com/GumbyEnder/hermes-kanban/releases/tag/v1.5.0) | ✅ 一致 |
| 完了カードを `Done → Kanban/archive.md` に自動移動 | リリースノート記載通り。タイムスタンプ保持・設定可能 | [GumbyEnder/hermes-kanban README](https://github.com/GumbyEnder/hermes-kanban) | ✅ 一致 |
| ボードテンプレート（Sprint / Bug Triage / Release / Personal） | v1.5.0で追加。ワンクリック生成は実装済み | [GitHub README](https://github.com/GumbyEnder/hermes-kanban) | ✅ 一致 |
| GitHub設定パネル（同期機能は近日公開） | フルコンフィグUIはあるが**同期機能自体はまだ未実装＝予告ベース** | [GitHub README](https://github.com/GumbyEnder/hermes-kanban) | ⚠️ ほぼ一致（同期は未実装） |
| BRATサポートで自動更新 | BRATはTfTHacker製のコミュニティ標準ツール、未掲載プラグインの自動更新に対応 | [TfTHacker/obsidian42-brat](https://github.com/TfTHacker/obsidian42-brat) | ✅ 一致 |
| 「Obsidianのボールト内で完全にローカル」 | プラグイン自体はローカル動作。ただし背後のHermes Agentが**外部API（OpenRouter等）を使う構成も可**。"完全ローカル"はOllama等を選んだ場合のみ | [Hermes Agent docs](https://hermes-agent.nousresearch.com/docs/) / [AMD blog](https://www.amd.com/en/blogs/2026/run-hermes-agent-locally-on-amd-ryzen-ai-max-processors-and-radeon-gpus.html) | ⚠️ ほぼ一致（構成依存） |
| 「自律型プロジェクト共同パイロット」「目標をKanbanに分解 / 日次スタンドアップ / ブロック追跡」 | READMEに「ボード自動生成」「日次スタンドアップ」「週次レビュー」「リアルタイムカード操作」明記 | [GumbyEnder/hermes-kanban README](https://github.com/GumbyEnder/hermes-kanban) | ✅ 一致 |
| Hermesは "真の自律型" に進化 | Hermes Agent本体の機能（多階層メモリ・永続ターミナル・自己改善スキル）を踏まえれば妥当な表現。ただし**プラグイン1つで実現するわけではなく、Hermes Agent本体導入が前提** | [Dev\|Journal 2026-02](https://www.earezki.com/ai-news/2026-02-26-nous-research-releases-hermes-agent-to-fix-ai-forgetfulness-with-multi-level-memory-and-dedicated-remote-terminal-access-support/) | ⚠️ ほぼ一致（前提条件あり） |

---

## 🌐 最新動向（2026-04時点）

- **Hermes Agent 本体が GitHub 40,000+ stars で OpenClaw代替超えと報じられる** — Nous Researchの自己改善型エージェントが2026年OSSのスター大本命に — [36kr](https://eu.36kr.com/en/p/3764418640003840), 2026
- **Hermes Kanban v1.5.0 リリース、`archive.md` 自動化・テンプレート・BRAT対応** — Obsidian側の運用フローが整備された — [GitHub Release](https://github.com/GumbyEnder/hermes-kanban/releases/tag/v1.5.0), 2026-04-24
- **AMD公式が Ryzen AI Max+ / Radeon GPU での Hermes Agent ローカル実行ガイドを公開** — ハードベンダー巻き込みで"完全ローカルAIエージェント"の現実味が増した — [AMD blog](https://www.amd.com/en/blogs/2026/run-hermes-agent-locally-on-amd-ryzen-ai-max-processors-and-radeon-gpus.html), 2026
- **Hermes Agent + Ollama でのローカル設定記事がMediumで連発** — 個人開発者でも動かせるレシピが揃ってきた — [Mehul Gupta / Medium](https://medium.com/data-science-in-your-pocket/hermes-agent-with-ollama-setup-b0a442f53241), 2026-04
- **Karpathy の "LLM Knowledge Base" がHermes組み込みスキルに採用** — RAGなしでmarkdownナレッジを育てる発想が標準実装に — [VentureBeat](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an), 2026
- **Obsidian側でも AI × Kanban 連携が群雄割拠**：Kanban Plus (AI支援) / Obsidian-PM (ガント+依存関係) / Bases Kanban など — [Obsidian Stats: Kanban tag](https://www.obsidianstats.com/tags/kanban), 2026
- **"vault内に 07-agents/ フォルダを切ってAgentごとに SOUL.md + kanban + reports/" 構成事例** — Obsidianを15エージェント以上のオーケストレーション基盤に使う事例も — [DEV: I Ditched My AI Agent Dashboard for Obsidian](https://dev.to/thedaviddias/i-ditched-my-ai-agent-dashboard-for-obsidian-37la), 2026

---

## 🧩 関連概念・隣接分野

- **LLM Knowledge Base (Karpathy)**: 「AIがmarkdownを書き足し続ける長期メモリ」発想。HermesとObsidianを繋ぐ思想的バックボーン
- **Local-First Software**: クラウド依存を減らし、ファイル実体・オフライン動作・データ主権を重視する潮流。ObsidianとHermes Agent両方の哲学
- **MCP (Model Context Protocol)**: 外部ツール・API・ローカルファイルを統一的にAIに繋ぐ仕様。Hermes Agentもこの方向と相性が良い
- **エージェントワークフロー**: 単発の応答ではなく、目標分解→タスク化→実行→振り返りのループを自動化する設計。Kanbanはその"見える化"の最も自然なUI
- **Obsidian周辺のAIエージェント拡張**: Obsidian-PM、Kanban Plus、obsidian-llm-plugin（Claude/Codex/Gemini連携）、Auralite など、2026年にエコシステムが分厚くなっている

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（元ポスト寄り）**:
  - markdownファイル実体ベース → vaultが"AIの長期記憶"そのものになる
  - Kanbanという既存UIに乗せたので、人間とAIの作業状況が同じ画面で見られる
  - Local-First / プライバシー重視 / 完全ローカル運用が選択可能
  - Hermes Agent本体のスター40,000規模に乗っかる勝ち馬
- **否定 / 慎重派の主張**:
  - **Hermes Kanban本体スターは182**、コミュニティ規模はまだ小さい。バス係数1人（GumbyEnder氏）
  - 「完全にローカル」は構成依存。**外部LLM API（OpenRouter等）を使うとローカルじゃない**
  - obsidian-kanban への依存があり、その互換性に振り回されるリスク
  - Hermes Agentの導入自体がVPS/コンテナ/Ollamaなど一定のセットアップを要求 → 一般ユーザー向きではない
  - 2026年4月時点でGitHub設定パネルはあるが**同期は"近日公開"**、機能的には発展途上
  - Obsidianには既に `mgmeyers/obsidian-kanban` + AI系プラグインの組み合わせや、Obsidian-PM等の選択肢がある。**Hermes固有でなくて困るユースケース**は限定的
- **中立的に見るときの補助線**:
  - 「自律エージェント時代のObsidian運用テンプレ」を見る材料としては筋が良いが、**プラグイン単体ではなくHermes Agent + Ollama + Obsidian + Hermes Kanban の4点セット導入が前提**と理解する
  - vault = AIの記憶・Kanban = 進捗UIという**思想を学ぶには最良の事例**。実装そのものを採用するかは別問題
  - 自分のワークフロー（Claudian + 単一vault）と組み合わせるなら、**Hermes Agent本体は入れず、思想と運用パターン（archive.md自動化、Sprint/Triageテンプレ、日次スタンドアップ）だけ移植**するのが現実的

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Hermes Kanban の REST API（ポート27124）の認可モデル — 他プラグインから叩けるか
- [ ] Claude Code / Claudian と Hermes Agent を**併用**するワークフローは成立するか
- [ ] Obsidian-PM・Kanban Plus・Bases Kanban との機能比較表
- [ ] Hermes Agent + Ollama を Mac (Apple Silicon) で動かす最小構成のコスト
- [ ] Karpathy LLM Knowledge Base スキルが**実際にどんなmarkdown構造**を作るのか具体例
- [ ] "v1.5.0 GitHub設定パネル" → 近日公開の同期機能は何を同期するのか（Issue/PR/Project Board？）

---

## 📚 参考資料

- [GitHub: GumbyEnder/hermes-kanban](https://github.com/GumbyEnder/hermes-kanban) — リポジトリ概要・機能・技術スタック・依存関係, 取得日 2026-04-25
- [GitHub Release: hermes-kanban v1.5.0](https://github.com/GumbyEnder/hermes-kanban/releases/tag/v1.5.0) — リリースノート一次情報, 取得日 2026-04-25
- [GitHub: NousResearch/hermes-agent](https://github.com/nousresearch/hermes-agent) — Hermes Agent本体, 取得日 2026-04-25
- [Hermes Agent公式ドキュメント](https://hermes-agent.nousresearch.com/docs/) — 機能・対応モデル・運用形態, 取得日 2026-04-25
- [Dev|Journal: Nous Research releases Hermes Agent (2026-02)](https://www.earezki.com/ai-news/2026-02-26-nous-research-releases-hermes-agent-to-fix-ai-forgetfulness-with-multi-level-memory-and-dedicated-remote-terminal-access-support/) — ローンチ時の解説, 取得日 2026-04-25
- [36kr: Hermes Agent 40,000-Star OpenClaw代替超え](https://eu.36kr.com/en/p/3764418640003840) — 2026年4月時点のトラクション, 取得日 2026-04-25
- [AMD blog: Run Hermes Agent Locally on AMD Ryzen AI Max+](https://www.amd.com/en/blogs/2026/run-hermes-agent-locally-on-amd-ryzen-ai-max-processors-and-radeon-gpus.html) — ハードベンダーの公式対応, 取得日 2026-04-25
- [Medium: Hermes Agent with Ollama Setup (Mehul Gupta)](https://medium.com/data-science-in-your-pocket/hermes-agent-with-ollama-setup-b0a442f53241) — ローカル構築レシピ, 取得日 2026-04-25
- [VentureBeat: Karpathy LLM Knowledge Base bypasses RAG](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an) — 思想的バックボーン, 取得日 2026-04-25
- [GitHub: TfTHacker/obsidian42-brat](https://github.com/TfTHacker/obsidian42-brat) — BRATの一次情報, 取得日 2026-04-25
- [GitHub: obsidian-community/obsidian-kanban](https://github.com/obsidian-community/obsidian-kanban) — 依存先プラグイン, 取得日 2026-04-25
- [DEV: I Ditched My AI Agent Dashboard for Obsidian](https://dev.to/thedaviddias/i-ditched-my-ai-agent-dashboard-for-obsidian-37la) — vault内Agent管理の実例, 取得日 2026-04-25

---

## 🗒 メモ

- **これは自分のClaudianワークフローと近い設計思想**：vault = 長期記憶 / markdownファイル実体 / ローカルファースト。**Hermes Agent本体を導入するかは別として、設計の参考になる要素が多い**
- 移植する価値がある実装パターン（Claudian側に取り込めるネタ）：
  - `archive.md` 自動化（完了タスクをタイムスタンプ付きで別ファイルに移動）
  - Sprint / Bug Triage / Release / Personal のボードテンプレート → vault内に `templates/kanban-*.md` として用意
  - 日次スタンドアップ儀式（毎朝AIがタスク状況を要約） → 既存の `_ kiwami/tools/daily-log/` と組み合わせる発想
  - 週次レビュー儀式 → [[SNS運用/analytics/]] の週次レポートと連動できそう
- note記事化候補:「Obsidian × ローカルAIエージェントの2026年ベストプラクティス：Hermes Kanban v1.5.0 を題材に」
- X短尺バラ売り:
  - ①Karpathyの LLM Knowledge Base ＝ RAG卒業の発想
  - ②Hermes Agent 40,000 stars / AMD公式対応 のスケール感
  - ③vault内に `archive.md` 自動化を取り込むだけでもタスク管理が一段クリーンになる
- 関連: [[CLAUDE.md]] / [[Claudian-スキル一覧.md]] / [[2026-04-23-claude-obsidian-llm-wiki]]（Karpathy由来の発想を扱った既存ノート）/ [[2026-04-24-claude-code-plugin-marketplace]]
- 自分のスタンスは **"Hermesエコシステムには乗らない、思想だけ取り込む"** が現実的。Claudian (Claude Code + Obsidian) で十分回っているので、わざわざ別エージェントランタイムを増やす理由は今のところ薄い
