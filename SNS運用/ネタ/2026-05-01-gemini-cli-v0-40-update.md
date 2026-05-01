---
created: 2026-05-01
tags: [調査, gemini-cli, claude-code, ai-agent, mcp, gemma]
source: "[[Clippings/Claude Codeに似てきた？【最新アップデート】Gemini CLI〜v0.40で何が変わったか〜.md]]"
---

# Gemini CLI v0.40でCLAUDE.md的な4階層メモリ・スキル抽出・ローカルGemma対応が入り、Claude Code/Codexと同じ土俵に乗った

> **TL;DR**
> Gemini CLI v0.40系（2026-04-24前後リリース）は「賢いCLI」から「文脈を持ち続ける開発エージェント」に方向転換した。具体的には①4階層`GEMINI.md`メモリ ②セッション履歴からスキルを自動抽出する Auto Memory（confuciusサブエージェント） ③`gemini gemma`によるローカルモデル統合 ④experimental task tracker ⑤MCPリソース読み取りツール、の5本柱。元記事は「Subagents/Hooks/Plugins ではClaude Codeが先行」と書いているが、実は**Gemini CLIも2026年4月にSubagentsを正式導入済み**で、差分はもう一段縮まっている。

## 📌 元テキスト（抜粋）

> Gemini CLIは、ただの「ターミナルで使えるGemini」ではなくなりました。2026年4月末のv0.40系アップデートで、記憶、タスク管理、ローカルGemma、MCPリソース、セキュリティ強化が入り、Claude CodeやCodexと比較すべき開発エージェントに近づいています。……v0.40.0のリリースノートには、従来のMemoryManagerAgentを置き換え、4階層のメモリをプロンプト駆動で編集する変更が入っています。……Gemini CLI v0.40.0では、`gemini gemma`によるローカルモデルセットアップが追加されました。

出典: [[Clippings/Claude Codeに似てきた？【最新アップデート】Gemini CLI〜v0.40で何が変わったか〜.md]]（@kawai_design / 2026-04-25公開）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Gemini CLI | Googleがオープンソース提供するターミナル向けAIエージェント。v0.40系で大規模機能追加 | `google-gemini/gemini-cli`, `geminicli.com/docs` |
| GEMINI.md | プロジェクト/ディレクトリ/個人/グローバルの4階層に置くMarkdown形式の記憶ファイル | `four-tier memory`, `prompt-driven memory` |
| Auto Memory | 過去セッションログから繰り返し作業を検出して`SKILL.md`を起こす実験機能 | `confucius subagent`, `skill-creator` |
| MCP (Model Context Protocol) | AIエージェントと外部ツール/リソースをつなぐ共通プロトコル。Anthropic発で各社採用 | `mcp resources`, `tools to list and read MCP resources` |
| Gemma | Googleのオープンモデル。CLIから`gemini gemma setup`で導入し、ルーティング判定をローカル化できる | `LiteRT-LM`, `Ollama gemma4` |
| Task Tracker | 単一セッション内で目的を内部タスク化し進捗を追う実験機能 | `experimental.taskTracker`, `tracker CRUD` |
| CLAUDE.md / Skills / Subagents / Hooks / Plugins | Claude Codeの運用構成要素。常時文脈/再利用手順/別インスタンス/決定的処理/配布パッケージ | `code.claude.com/docs`, `Skills vs Commands` |
| Codex Cloud | OpenAI Codexのクラウド側。バックグラウンドでPR作成・レビュー・テスト追加まで委任できる | `Codex CLI`, `Codex IDE` |
| Subagent | 主エージェントが下請けに投げる独立コンテキストの専門エージェント。Claude Code・Gemini CLI双方が採用 | `built-in subagents`, `parallel agent workflows` |

---

## 🧭 背景 / なぜ今これが話題なのか

2024〜2025年は「ターミナル上のチャットUIで賢いLLMを呼び出す」CLIが乱立した時期で、Anthropic Claude Code、OpenAI Codex CLI、Google Gemini CLIが並走していた。差はモデル単体の賢さよりもむしろ**運用構造**——文脈の持たせ方、タスク分担、外部接続、ローカル/クラウド切替——に出始めていた。

Claude Codeは2025年〜2026年にかけて`CLAUDE.md`/Skills/Subagents/Hooks/Plugins という階層を整備し、「個人が使う賢いCLI」から「チームが配布できる開発ワークフロー基盤」へ進化した。Codexは並行してCodex Cloud/IDE/SDK/CI連携を厚くし、「実装を丸投げできる委任エージェント」のポジションを取った。

その間、Gemini CLIは「Google Search grounding × 1Mトークン × 無料枠」という素材は強いものの、運用的には1ショット利用の色が濃かった。ここに来て**v0.40系（2026年4月）で一気に運用層に踏み込んだ**のが、元記事が指摘している転換点。タイミング的にも、Googleは同月に**Subagents**を正式機能として追加しており（後述）、Claude Codeの設計思想を素直に取り込みつつ、Google独自資産（Search/Cloud/Gemma）で差別化する方向が固まった。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| v0.40.0は2026年4月末リリース | preview.3が2026-04-24公開。stableは続けて4月末〜5月頭 | [GitHub Releases v0.40.0](https://github.com/google-gemini/gemini-cli/releases/tag/v0.40.0), [Releasebot](https://releasebot.io/updates/google/gemini-cli) | ✅ 一致 |
| MemoryManagerAgentを置き換え、4階層をプロンプト駆動で編集 | PR #25716で「prompt-driven memory editing across four tiers」が明記。`autoMemory`フラグ分離はPR #25601 | [GitHub Releases v0.40.0](https://github.com/google-gemini/gemini-cli/releases/tag/v0.40.0) | ✅ 一致 |
| Auto Memoryで作業パターンをスキル化 | confuciusという専用サブエージェントがセッションログを読み`SKILL.md`を草稿。デフォルトOFF、設定は`~/.gemini/settings.json` | [Auto Memory公式](https://geminicli.com/docs/cli/auto-memory/), [Issue #24272](https://github.com/google-gemini/gemini-cli/issues/24272) | ✅ 一致 |
| `gemini gemma`でローカルモデルセットアップ追加 | PR #25498。LiteRT-LMランタイム経由でGemmaをロードし、ルーティング判定をローカル化。Ollama経由のgemma4:4b/12b/27bも代替可 | [Model routing docs](https://geminicli.com/docs/cli/model-routing/), [local-model-routing.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/core/local-model-routing.md) | ✅ 一致 |
| Task Trackerはexperimentalで進捗管理用 | `experimental.taskTracker`フラグで有効化、tracker CRUDツールを提供。PR #24556でドキュメント追加 | [Releasebot](https://releasebot.io/updates/google/gemini-cli) | ✅ 一致 |
| MCPリソースを読み書きする新ツール追加 | PR #25395で「tools to list and read MCP resources」追加 | [GitHub Releases v0.40.0](https://github.com/google-gemini/gemini-cli/releases/tag/v0.40.0) | ✅ 一致 |
| Subagents/Hooks/PluginsではClaude Codeが先行 | Hooks/Pluginsは事実上Claude Codeが先行。**ただしSubagentsは2026年4月にGemini CLIも正式実装**（built-in/カスタム/並列実行対応）。記事公開直前〜直後の追加なので「先行」表現は今や半分しか当たっていない | [InfoQ: Subagents in Gemini CLI](https://www.infoq.com/news/2026/04/subagents-gemini-cli/), [Google Developers Blog](https://developers.googleblog.com/subagents-have-arrived-in-gemini-cli/), [Subagents docs](https://geminicli.com/docs/core/subagents/) | ⚠️ ほぼ一致（要更新） |
| Gemini 3モデル、1Mトークン級コンテキスト | 公式README記載通り。Search grounding/MCP/シェル実行も同README | [geminicli.com docs](https://geminicli.com/docs/) | ✅ 一致 |
| Claude Codeは`CLAUDE.md`/Skills/MCP/Subagents/Hooks/Plugins/Agent teams で整理 | 公式docsで全て確認可。Skillsは`SKILL.md`を含むディレクトリ、CLAUDE.mdは「always-on context」、Skillsは「on-demand context」 | [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference), [alexop.dev customization guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/) | ✅ 一致 |

---

## 🌐 最新動向（2026-05-01時点）

- **Subagents正式実装**: Gemini CLIに built-in（汎用/CLI helper/codebase investigator）と自作の両方を持つSubagents機構が追加。明示的delegation・並列実行・チームでの保存共有に対応。Claude CodeのSubagentsとの機能差はだいぶ縮まった — [InfoQ, 2026-04](https://www.infoq.com/news/2026/04/subagents-gemini-cli/), [Google Developers Blog, 2026-04](https://developers.googleblog.com/subagents-have-arrived-in-gemini-cli/)
- **Auto Memory はデフォルトOFF**: `experimental.memoryManager`を使っていた既存ユーザーは、フラグ分離後に`/memory inbox`が消える退行報告あり（Issue #25623）。アップデート後は`autoMemory: true`を明示する必要がある — [Issue #25623](https://github.com/google-gemini/gemini-cli/issues/25623), 2026-04
- **Gemma 4対応プレビュー**: v0.41系プレビューで`gemma4:4b/12b/27b`をOllama経由でも回せる構成が整備中。ローカル+クラウドのハイブリッドルーティングが現実味 — [MindStudio guide, 2026-04](https://www.mindstudio.ai/blog/how-to-run-gemma-4-locally-ollama), [Medium - Gemma 4 Ollama, 2026-04](https://medium.com/@nitinsgavane/free-run-googles-gemma-4-locally-full-ollama-setup-guide-226ce94a6fdb)
- **Codex CLIにもGemma 4が乗った**: 「I ran Gemma 4 as a local model in Codex CLI」がHN上位入り。OpenAI/Google相互にローカルモデル+ローカルCLIの境界が曖昧になっている — [HN, 2026-04](https://news.ycombinator.com/item?id=47744255)
- **Pre-Configured Monitoring Dashboards**: Google CloudがGemini CLI向けに事前設定済みの可観測性ダッシュボードを提供開始。エージェント運用のSREライク化が進行 — [Google Cloud Blog, 2026-04](https://cloud.google.com/blog/topics/developers-practitioners/instant-insights-gemini-clis-new-pre-configured-monitoring-dashboards/)

---

## 🧩 関連概念・隣接分野

- **Anthropic Skills（`SKILL.md`）と Gemini Auto Memory**: 設計思想は近いが、Skillsは「人間が書いて配布する手順書」、Auto Memoryは「機械が会話履歴から候補を吸い上げる」。前者はトップダウン、後者はボトムアップで、組み合わせると面白い。詳細は [[Claudian-スキル一覧.md]] と [[Claudian-スキル候補.md]] に近い構図。
- **MCP (Model Context Protocol)**: 各社共通の外部ツール接続プロトコル。Gemini CLI v0.40で「リソース読み取り」も追加され、ツール実行だけでなくナレッジソース参照まで統一インタフェース化が進んでいる。
- **LiteRT-LM**: GoogleのGoogle/MediaPipe由来ローカルランタイム。Gemma配信のシム役。Ollamaとは別系統だが`gemini gemma setup`はこちらを優先する。
- **Codex Cloud / Background Tasks**: Geminiが「セッション内Task Tracker」を強化したのに対し、Codexは「クラウド側でPRをまるごと作る」方向。同じ"task management"でも粒度と置き場所が違う。
- **vault運用との接続点**: 4階層`GEMINI.md`は[[CLAUDE.md]]＋`_ memory/short-term.md / mid-term.md / long-term.md`の発想と非常に近い。本vaultの多階層メモリ思想（[[_ memory/short-term.md]]他）はGemini側でも汎用化しつつあると言える。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: Gemini CLIは無料枠・1M context・Google Search・Gemmaを束ねる立ち位置で、Claude Codeとは戦う場所が違う。元記事の「優劣ではなく使いどころ」スタンスは妥当。
- **否定 / 慎重派の主張**:
  - Auto Memoryは「confucius」が静かにバックグラウンドで動き、`SKILL.md`を勝手に下書きする。**生成物のレビューを人間が怠ると、誤った"癖"が固定化される**リスクが大きい（公式も「default to creating zero skills unless evidence is strong」と慎重）。
  - 4階層メモリは「人間が読めるMarkdown」とはいえ、4箇所に散ると整合性管理が逆に煩雑。Claude Codeの[[CLAUDE.md]]中央集権 + Skills分散の方が運用負荷は軽い、という見方もある。
  - Task Trackerもexperimental扱いで、`memoryManager`フラグ分離による既存ユーザーの退行（Issue #25623）が出ている。**プロダクション運用にはまだ早い**。
- **中立的に見るときの補助線**:
  - 「機能が増えた=Claude Codeに追いついた」ではなく、**運用のしやすさ・配布のしやすさ・チームでの再現性**で見る必要がある。Hooks（決定的処理）とPlugins（配布パッケージ）はGemini側まだ薄い。
  - Subagentsまでは追いついたので、次の差分は「**Hooks相当の決定的フックがあるか**」「**Pluginsレベルでパッケージ配布できるか**」「**ベンダーロックインの程度**（Google Cloud寄せ vs マルチプロバイダ）」に移る。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Gemini CLI に Claude Code Hooks 相当（決定的・非LLMの自動処理）はあるか？ `.gemini/hooks/`的な仕組みの有無
- [ ] Auto Memory が生成する`SKILL.md`の置き場所と、Claude Code のSkillsディレクトリ構造の互換性（相互移植できるか）
- [ ] 4階層`GEMINI.md`を本vaultの`CLAUDE.md` + `_ memory/`構成と並走させたとき、どう住み分けるか
- [ ] `gemini gemma`のローカルルーティング判定でどの程度クラウド呼び出しを削減できるか（コスト/レイテンシ実測）
- [ ] Subagents の並列実行が、Claude CodeのAgent teamsと比べてどこまで成熟しているか
- [ ] `experimental.taskTracker`が安定版に昇格する時期と、`/re-daily` のアクションプラン管理に流用できるか

---

## 📚 参考資料

- [Gemini CLI v0.40.0 Release (GitHub)](https://github.com/google-gemini/gemini-cli/releases/tag/v0.40.0) — v0.40.0変更点（メモリ4階層・skill-creator統合・MCPリソース・Gemma・Task Tracker）の一次ソース, 取得日 2026-05-01
- [Gemini CLI - Releasebot 2026-04](https://releasebot.io/updates/google/gemini-cli) — preview.3が2026-04-24と日付確認, 取得日 2026-05-01
- [Auto Memory公式ドキュメント](https://geminicli.com/docs/cli/auto-memory/) — confuciusサブエージェントとデフォルト設定, 取得日 2026-05-01
- [Issue #24272: background memory service for automatic skill extraction](https://github.com/google-gemini/gemini-cli/issues/24272) — Auto Memoryの設計議論, 取得日 2026-05-01
- [Issue #25623: memoryManager flag split regression](https://github.com/google-gemini/gemini-cli/issues/25623) — フラグ分離による既存ユーザー退行, 取得日 2026-05-01
- [Model routing公式](https://geminicli.com/docs/cli/model-routing/) — `gemini gemma setup`とLiteRT-LM, 取得日 2026-05-01
- [InfoQ: Subagents in Gemini CLI](https://www.infoq.com/news/2026/04/subagents-gemini-cli/) — 2026-04時点でSubagents正式実装の事実, 取得日 2026-05-01
- [Google Developers Blog: Subagents have arrived](https://developers.googleblog.com/subagents-have-arrived-in-gemini-cli/) — 公式アナウンス, 取得日 2026-05-01
- [Claude Code Plugins reference](https://code.claude.com/docs/en/plugins-reference) — Skills/Subagents/Hooks/Pluginsの一次定義, 取得日 2026-05-01
- [alexop.dev: Claude Code Customization Guide](https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/) — CLAUDE.md=always-on / Skills=on-demand の整理, 取得日 2026-05-01
- [Google Cloud Blog: Gemini CLI Monitoring Dashboards](https://cloud.google.com/blog/topics/developers-practitioners/instant-insights-gemini-clis-new-pre-configured-monitoring-dashboards/) — エージェント運用の可観測性整備, 取得日 2026-05-01
- [HN: Gemma 4 in Codex CLI](https://news.ycombinator.com/item?id=47744255) — ローカルモデル×ローカルCLIのクロス採用事例, 取得日 2026-05-01

---

## 🗒 メモ

本vaultはすでに[[CLAUDE.md]]＋`_ memory/`の多階層メモリと[[Claudian-スキル候補.md]]による自己改善ループを回している。Gemini CLIのGEMINI.md×4階層 + Auto Memoryは**ほぼ同じ発想に外部から到達した**形で、これは「`SKILL.md`を草稿させる→人間がレビューして昇格」の運用が業界共通解になりつつある証拠。

使い道としては：

1. X投稿ネタ: 「Gemini CLI v0.40がClaude Codeに似てきた件——記事とソースを5分で照合」系。元記事の弱点（Subagentsはもう追いついた）を補強したファクトチェック投稿が刺さりそう。
2. note記事化: 「**マルチエージェントCLI3兄弟（Claude Code/Codex/Gemini CLI）の現在地マップ 2026-05版**」。表で対比すると検索流入が見込める。
3. 自分の運用への取り込み: Gemini CLIを試験導入して、`GEMINI.md`に[[CLAUDE.md]]の絶対ルール群を翻訳投入してみる→挙動差を観察。Auto Memoryが`confucius`経由で起こす`SKILL.md`を、本vaultの[[Claudian-スキル候補.md]]に転載するパイプラインを試す価値あり。
