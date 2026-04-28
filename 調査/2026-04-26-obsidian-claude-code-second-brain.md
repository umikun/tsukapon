---
created: 2026-04-26
tags: [調査, Obsidian, ClaudeCode, セカンドブレイン, PKM]
source: Clippings/Post by @_guillecasaus on X.md
---

# Obsidian × Claude Code で「第二の脳」 — 2026年Q2にバズってる本当の中身

> **TL;DR**
> @_guillecasaus の「土曜の1時間でNetflixより価値があるコース」ツイートは、リンクを貼らない**保存誘発型のティザー**フォーマット。指している"完全なコース"は単一ではなく、**2026年Q1〜Q2に爆発した「Obsidian + Claude Code = Second Brain」ジャンル全体**を指している（Substack/Medium/YouTubeで数十本、GitHubでも★200〜★700級のスターターが複数）。
> 中核アーキテクチャはどこも同じで、**Vault = メモリ層 / `CLAUDE.md` + `memory.md` = 起動時に自動読込される人格・ルール / `.claude/commands/` = 呼び出せるskill / MCPで外部接続**。**Notion等のクラウドDBで詰まる「AIが直接ファイルを読めない」問題をObsidianの "ただのMarkdownフォルダ"** が突破するのがキモ。
> このVault（[[CLAUDE.md]] + `_ memory/` + `.claude/commands/`）はまさにその先行実装なので、新たに見るべきは**他の人がどう自動化レイヤーを盛ってるか**（自動執筆 / scheduled agents / 知識グラフ化）。次の一手は llm-wikid 系のKarpathy-styleか、scheduled agentsで朝会要約を自動生成する方向。

## 📌 元テキスト（抜粋）

> 土曜日にNetflixを見る代わりに、これに1時間使ってみて。
> Obsidian + Claude Codeを使って「第二の脳」を作る方法を教えてくれる完全なコース。
> アイデアを捉え、整理し、あなたと一緒に考えるシステム。
> 🔖 保存しておいて、後で感謝するよ。

出典: [[Clippings/Post by @_guillecasaus on X.md]]（投稿: 2026-04-25, [元ツイート](https://x.com/_guillecasaus/status/2048047011807543548)）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Second Brain (PKM) | Tiago Forte 提唱の個人知識管理コンセプト | Building a Second Brain, PARA |
| Obsidian Vault | プレーンMarkdownで自分の知識を貯めるフォルダ | obsidian, local-first |
| CLAUDE.md | Claude Code が起動時に必ず読むルール/人格定義ファイル | claude code memory |
| memory.md | 永続メモリ。session間で参照される長期記憶 | claude code persistent memory |
| MCP | Model Context Protocol。AI⇔外部ツールの標準連携 | mcp servers |
| `.claude/commands/` | slashコマンドとして呼べるskill群 | claude code skills |
| Karpathy method | Andrej Karpathy が紹介したLLM-augmented PKMスタイル | llm wiki, llm-wikid |
| PARA | Projects/Areas/Resources/Archive 整理フレーム | Tiago Forte PARA |
| Scheduled agents | cron/launchdで定期発火するagent | claude code scheduled |
| Knowledge graph | ノート間リンクを構造化して可視化 | obsidian graph view, graphify |

---

## 🧭 背景 / なぜ今これが話題なのか

「Second Brain（第二の脳）」自体は **Tiago Forte が2014年頃から広めた PKM 方法論**で、Obsidian は2020年公開のローカルMarkdownエディタとして PKM 界隈の定番に成長した。ここに **Claude Code（Anthropic, 2024年後半リリース）** が加わって、2025年中盤の Skills / MCP / Sub-agents 解放で「**Vaultを直接読み書きできるエージェント**」が現実化した結果、2026年Q1〜Q2に "Obsidian + Claude Code = Second Brain" 系コンテンツが一気に爆発した。

火付け役の1つは **Andrej Karpathy が2026年Q1にXで紹介した "LLMで補強したPKM" スタイル**。これを受けて `shannhk/llm-wikid`（★211, "Karpathy-style LLM knowledge base for Obsidian"）など派生リポが続出。YouTube/Substack/Medium で同テーマのチュートリアルが並走し、@_guillecasaus のツイートはその波に乗ったキュレーション系投稿。

GitHubのStarter Kit群も2026-04時点で複数の活発な選択肢がある：

- `alchaincyf/obsidian-ai-orange-book` ★729（中国語圏の橙皮书シリーズ）
- `huytieu/COG-second-brain` ★367（17 skills + 6 worker agents + people CRM、`gstack`/`gbrain`派生）
- `eugeniughelbur/obsidian-second-brain` ★282（autonomous writes + scheduled agents + `_CLAUDE.md` cross-surface context）
- `smixs/agent-second-brain` ★242（音声→Telegram→knowledge base 系）
- `shannhk/llm-wikid` ★211（Karpathy-style）
- `Abilityai/cornelius` ★86 / `iurykrieger/claude-bedrock` ★39 / `jessepinkman9900/claude-second-brain` ★38

要するに「@_guillecasaus が言う"完全なコース"」は**特定の1本というより、上のジャンル全体を指すバズワード化したフレーズ**と読むのが正確。実際にツイートはリンクを含まない**保存誘発型ティザー**で、指す対象を曖昧にして拡散効率を上げるテンプレ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Obsidian + Claude Codeで「第二の脳」が作れる | 公式・コミュニティ双方で実装パターン確立済（Vault = memory層, CLAUDE.md + memory.md = ルール） | [whytryai: Build Your Second Brain](https://www.whytryai.com/p/claude-code-obsidian), [MindStudio guide](https://www.mindstudio.ai/blog/build-ai-second-brain-claude-code-obsidian) | ✅ 一致 |
| 1時間で完全なコースが完了する | 1時間で**完成**は無理。setup自体は30分前後だが、運用に乗せて自分のworkflowに馴染ませるには数週間かかるのが普通 | [NxCode: Complete Guide 2026](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026) | ⚠️ ほぼ一致（誇張） |
| 「アイデアを捉え→整理→一緒に考える」 | スタンダードな PARA + Claude Codeでの自動分類/要約のパターン。実装可能 | [TowardsAI: From Notes to Knowledge](https://pub.towardsai.net/from-notes-to-knowledge-the-claude-and-obsidian-second-brain-setup-37af4f47486f) | ✅ 一致 |
| Netflixより価値がある | 完全に主観。判断不能 | — | 🔍 未確認（修辞） |
| "完全なコース"が存在する | 添付リンクなし。**特定の1本のコースを指す根拠は見つからない**。ジャンル全体（YouTube動画群+Substack記事群）を指している可能性が高い | [YouTube多数](https://www.youtube.com/watch?v=Y2rpFa43jTo) | ❌ 要注意（リンク欠落） |
| ObsidianはAIが直接ファイル読める | プレーンMarkdownでローカル、Claude Code はファイルシステム経由で直接 read/write 可能。Notion等のクラウドDBと違ってAPIラッパー不要 | [whytryai](https://www.whytryai.com/p/claude-code-obsidian), [TowardsAI](https://pub.towardsai.net/from-notes-to-knowledge-the-claude-and-obsidian-second-brain-setup-37af4f47486f) | ✅ 一致（最大の差別化ポイント） |

> 集計: ✅3 / ⚠️1 / ❌1 / 🔍1。骨格は事実だが「**1時間で完成 / 完全なコース**」は典型的な保存誘発レトリック。

---

## 🌐 最新動向（2026-04-26時点）

- **Karpathy-style PKM** が2026年Q1に流行。`shannhk/llm-wikid`（★211）が「Karpathy-style LLM knowledge base for Obsidian」として代表枠 — [GitHub shannhk/llm-wikid](https://github.com/shannhk/llm-wikid), 2026-04
- **alchaincyf/obsidian-ai-orange-book** が中国語圏で★729。シリーズ化された "橙皮书"（オレンジブック）方式のステップバイステップガイド — [GitHub alchaincyf/obsidian-ai-orange-book](https://github.com/alchaincyf/obsidian-ai-orange-book), 2026-04
- **eugeniughelbur/obsidian-second-brain（★282, 最終push 2026-04-25）** が autonomous writes / scheduled agents / `_CLAUDE.md` cross-surface context を統合。"living second brain" の現時点最有力スターター — [GitHub](https://github.com/eugeniughelbur/obsidian-second-brain), 2026-04
- **COG-second-brain（★367）** は **17 skills + 6 worker agents + people CRM** を盛り、Garry Tan の `gstack`/`gbrain` 系の "盛り盛り構成" を継承。Cursor/Kiro/Gemini CLI/Codexまで互換 — [GitHub huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain), 2026-04
- **音声→Vaultパイプライン**: `smixs/agent-second-brain`（★242）が Telegram音声→knowledge base + Todoist + 日報まで自動化。Ebbinghaus忘却曲線でのメモリdecayを実装 — [GitHub smixs/agent-second-brain](https://github.com/smixs/agent-second-brain), 2026-04
- **YouTubeコース化**: "Obsidian + Claude Code: The Second Brain Setup That Actually Works"（3週間前）、"How To Build The ULTIMATE AI Second Brain"（2週間前）、"Karpathy method pt 2"（2日前）と毎週新作 — [YouTube Y2rpFa43jTo](https://www.youtube.com/watch?v=Y2rpFa43jTo), 2026-04
- **Notionからの移行論**: TowardsAI / NxCode / MindStudio が揃って "ObsidianはAIが直接ファイル読めるからNotionより向く" を強調。**"local-first" + "plain markdown" の優位性が AIエージェント時代に再評価**されてる — [TowardsAI](https://pub.towardsai.net/from-notes-to-knowledge-the-claude-and-obsidian-second-brain-setup-37af4f47486f), 2026-04

---

## 🧩 関連概念・隣接分野

- **このVault自体（Tsukapon）**: [[CLAUDE.md]] + [[_ memory/short-term.md]] + [[_ memory/mid-term.md]] + [[_ memory/long-term.md]] + `.claude/commands/` の構成は、上記スターター群とほぼ同じアーキテクチャを**先取りで手動実装**してる状態
- **Claude Code Setup プラグイン**: 公式の `claude-code-setup`（[[調査/2026-04-26-claude-code-setup-plugin.md]]）も "vaultをスキャンして提案" できる
- **awesome-claude-code 系**: skill/MCP/subagentの母集団は [[調査/2026-04-26-claude-code-100-best-repos.md]] を参照
- **Plugin Marketplace 全体**: [[調査/2026-04-24-claude-code-plugin-marketplace.md]] と接続
- **PARA / Building a Second Brain**: Tiago Forte の方法論。フォルダ構成（Projects / Areas / Resources / Archive）は今もこのジャンルのデフォルト
- **OpenChronicle 系のローカルAIメモリ**: Macで時系列に行動を貯めるアプローチ（[[調査/2026-04-24-openchronicle-mac-ai-memory.md]]）。Vault型と並走できる

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側（@_guillecasaus / コース系発信者）**: 「クラウドDBに縛られない自分専有のSecond Brainが、AIエージェント時代には最強の生産性インフラになる」
- **否定 / 慎重派**:
  - **"1時間で完成" 神話**: 実際は **CLAUDE.md / memory.md / .claude/commands/ をどう書くかが本体**で、自分の語彙・workflow・関心テーマを反映するのに数週間〜数ヶ月かかる。1時間でできるのはディレクトリ作成だけ
  - **メモリ肥大化リスク**: scheduled agents や autonomous writes を盛りすぎると、**Vault が自動生成テキストの墓場**になる。読まれないノートが増えるとそもそもの "second brain" 機能が劣化
  - **過信リスク**: AIに「整理してもらう」依存度が高まると、**自分で考えるサイクルが減る**。"考える代わりにAIに考えさせる" のは Tiago Forte が提唱した本来のSecond Brainとは方向が逆
  - **保存誘発型ツイートの構造**: リンクなしで「保存して」と言うのは **シェア指標を稼ぐためのテンプレ**。実際のコンテンツ密度は薄いことが多い
- **中立的に見る補助線**: **「自分が現状でPKMで詰まってる工程」を1つだけ特定して、そこだけCに任せる**のが正解。例: "週次レビューだけ自動化" / "Clippingsの整理だけ任せる" / "セッション冒頭のメモリ読み込みだけ強化"。一気に全部AI化しようとしない

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] @_guillecasaus が実際に指している"完全なコース"は何か（リプライツリーや過去ツイートで特定可能か）
- [ ] eugeniughelbur/obsidian-second-brain の `_CLAUDE.md` cross-surface context は具体的に何を解いているのか（Claude.ai web版とCLIでの context共有？）
- [ ] このVaultの `_ memory/` 3層構造を huytieu/COG-second-brain や Karpathy-style の構造と **アーキテクチャ比較**してみる価値あり
- [ ] **Scheduled agents** を launchd で組む場合、すでにある [[Macで定期的に同期.md]] と統合する設計はどうなるか
- [ ] 音声→Vault パイプライン（smixs/agent-second-brain 系）を**iPhoneショートカット + Whisper + Claude Code**で自前実装する場合の最小構成

---

## 📚 参考資料

- [whytryai: Build Your Second Brain With Claude Code & Obsidian](https://www.whytryai.com/p/claude-code-obsidian) — アーキテクチャ全体像, 取得日 2026-04-26
- [TowardsAI: From Notes to Knowledge](https://pub.towardsai.net/from-notes-to-knowledge-the-claude-and-obsidian-second-brain-setup-37af4f47486f) — Claude/Obsidianセットアップ詳細, 取得日 2026-04-26
- [MindStudio: Build AI Second Brain](https://www.mindstudio.ai/blog/build-ai-second-brain-claude-code-obsidian) — 3レイヤー解説, 取得日 2026-04-26
- [NxCode: Complete Guide 2026](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026) — 2026年版チュートリアル, 取得日 2026-04-26
- [Substack noahvnct: How to Build Your AI Second Brain](https://noahvnct.substack.com/p/how-to-build-your-ai-second-brain) — 個人実装記, 取得日 2026-04-26
- [Every podcast: Claude Code as a Thinking Partner](https://every.to/podcast/how-to-use-claude-code-as-a-thinking-partner) — 概念的整理, 取得日 2026-04-26
- [GitHub eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) — ★282 living second brain, 取得日 2026-04-26
- [GitHub huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) — ★367 17skills + 6agents, 取得日 2026-04-26
- [GitHub alchaincyf/obsidian-ai-orange-book](https://github.com/alchaincyf/obsidian-ai-orange-book) — ★729 中国語圏ガイド, 取得日 2026-04-26
- [GitHub shannhk/llm-wikid](https://github.com/shannhk/llm-wikid) — ★211 Karpathy-style, 取得日 2026-04-26
- [YouTube: The Second Brain Setup That Actually Works](https://www.youtube.com/watch?v=Y2rpFa43jTo) — 動画チュートリアル, 取得日 2026-04-26
- [元ツイート @_guillecasaus](https://x.com/_guillecasaus/status/2048047011807543548) — 出典, 取得日 2026-04-26

---

## 🗒 メモ

このVault自体が **完璧な実例** なので、note記事化のネタが豊富：

- **「@_guillecasaus が言う"1時間"は嘘。1ヶ月かけてSecond Brainを育ててみた」型**
  - 自分の `_ memory/short-term.md` / `mid-term.md` / `long-term.md` の運用ログを公開する**実走系note**
  - "自動化の墓場にしないために決めた4つのルール"（過信しない / scheduled agentsを最初から盛らない / 月1で見直す / 自分の語彙を反映する）
- **「Obsidian × Claude Code 系GitHubスターター10本を比較してみた」型**
  - 上記の eugeniughelbur / COG / orange-book / llm-wikid / smixs / cornelius / claude-bedrock / claude-second-brain を **アーキテクチャ表で比較**する記事
  - "結局どれを採用するか" の判断軸を提示するとSEOに強い
- **「Karpathy-method を日本語で実装してみる」型**
  - llm-wikid の構造を**日本語Vaultでフォーク**したらどうなるかの実験記
  - X/Threadsで反応取りやすい。Karpathy x 日本語で検索ボリューム未開拓
- **CLAUDE.md改訂候補**: "Second Brain運用ルール" として「scheduled agents は手動承認なしには発火させない」「自動生成ノートは `_auto/` 配下に隔離する」を明文化しておくと、未来の自分が安心して拡張できる

@_guillecasaus 系の "リンクなしで保存誘発" フォーマットは [[SNS運用/analytics/フォロワー改善.md]] 文脈でも参考になる（**「保存」してもらうことが目的なら本文に詳細を盛らない方が伸びる**という逆説）。
