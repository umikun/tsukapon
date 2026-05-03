---
created: 2026-05-03
tags: [調査, claude-code, token-optimization, mcp, github-curation, 批評型]
source: "[[Clippings/Post by @RodmanAi on X.md]]"
---

# 「Claudeトークン90%削減10リポ」リストを冷静に分解する — 本物・盛り・抜けている本命

> **TL;DR**
> 紹介された10リポは大半が **実在する** が、「90%削減」「98%削減」は典型ユースケースの **ベストケース値**。一般的な作業での実効削減はその半分以下になることが多い。さらに本リスト最大の問題は **公式の最強レバーである "プロンプトキャッシング" が1つも載っていない** こと（Anthropicが2026年初に既定TTLを1hr→5minへ縮小し、多くの本番ワークロードで実効コストが30〜60%増加した文脈もスルー）。"10選" 系キュレーションの典型的な弱点（同質ジャンルの薄い紹介＋ファクトチェック欠如）が出ている。本気でトークン削減したいなら、**まず公式の prompt caching を1hr TTLで設計、次に大型ツール出力のオフロード（Context Mode系）、最後に Tree-sitter/AST系のコード検索（claude-context等）**、の3段で組むのが2026年5月時点の現実解。リストの中で実装する価値が高いのは2〜3本だけ。

## 📌 元テキスト（抜粋）

> 10 トークンを最大90%削減する驚異のGitHubリポジトリ
> 1. RTK (Rust Token Killer): コンテキストに渡す前にターミナル出力をフィルタリング。一般的な開発コマンドで60-90%削減可能。
> 2. Context Mode: PlaywrightやGitHubツールの出力をSQLiteにオフロードし、会話にはクリーンな要約のみを渡す。98%削減。
> 3. code-review-graph: Tree-sitterを使ってコードベースのローカル知識グラフを構築。49倍削減。
> 4. Token Savior / 5. Caveman Claude / 6. claude-token-efficient / 7. token-optimizer-mcp / 8. claude-token-optimizer / 9. token-optimizer / 10. claude-context (by Zilliz)
> 後で役立つので保存しておこう🔖

出典: [[Clippings/Post by @RodmanAi on X.md]] / [元ポスト](https://x.com/RodmanAi/status/2050604420870852654)（@RodmanAi, 2026-05-03）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| トークン | LLMが入出力を数える単位（≒単語の断片） | LLM tokenization |
| コンテキストウィンドウ | 1リクエストに詰め込める総トークン数の上限 | claude context window |
| プロンプトキャッシング | プロンプトの静的部分をAnthropic側で5分〜1時間キャッシュし、再リクエストで90%引きにする公式機能 | claude prompt caching |
| MCPサーバ | Model Context Protocol。Claude Code 等にツールを追加する標準仕様 | model context protocol |
| Tree-sitter | コードを高速にAST化する増分パーサ。code-review-graph等の基盤 | tree-sitter parser |
| BM25 | 古典的な全文検索ランキング指標。`claude-context` がベクトル検索と併用 | bm25 ranking |
| Auto-compaction | Claude Codeがコンテキスト上限近くで会話履歴を自動要約する公式機能 | claude code auto compaction |
| Bifrost / Code Mode | エンタープライズ向けMCPゲートウェイの実装。58〜92%削減実績の公式系 | bifrost mcp gateway |
| TTL（Time To Live） | キャッシュの有効期間。Anthropicは2026年初に既定を 1hr→5min に縮小 | claude cache ttl change 2026 |
| Ghost tokens | "見えないが消費されているトークン"（システムプロンプト・ツール定義・MCP・スキル等の前置き） | ghost tokens claude |

---

## 🧭 背景 / なぜ今これが話題なのか

**2024〜2025年: Claude Code とMCP の普及で "ツールゴミ" 問題が顕在化**
Claude Code（2024年公開）と MCP（2024年提唱）の組み合わせで「LLMが多数のツールを呼ぶ」運用が定着し、**ツールの出力（PlaywrightのページHTML、`gh issue list` の全文、`grep` の数千行）がそのままコンテキストに流入する** 構造的な無駄が問題化。"Power user は1単語打つ前に 50〜70K トークン消費している" という分析記事が話題に（[Token Optimizer README](https://github.com/ooples/token-optimizer-mcp)）。

**2026年Q1: Anthropic がキャッシュ既定TTLを 1hr → 5min へ縮小**
プロンプトキャッシュの既定 TTL を1時間→5分に縮める変更があり、これが **「アクセスが散発的な本番ワークロードでは、知らずに30〜60%コスト増になる」** という問題提起になった（[Claude Prompt Caching in 2026](https://dev.to/whoffagents/claude-prompt-caching-in-2026-the-5-minute-ttl-change-thats-costing-you-money-4363)）。明示的に `cache_control: {"ttl": "1h"}` を指定しないと旧来の挙動にならない。

**2026年Q1〜Q2: "トークン削減リポ" がX/GitHubで雨後の筍化**
公式の prompt caching と auto-compaction だけではカバーしきれないユースケース（大型ツール出力・モノレポ全体検索・冗長セッション）を埋める個人開発OSSが乱立。`token-optimizer-mcp`（95%+ 削減主張）や `caveman`（出力65-75%削減）などが Hacker News や X で繰り返しトレンド入り。同時に「**結局どれを入れればいいんだ**」状態になり、@aiia.ro や @pasqualepillitteri.it が "10選" "14選" 系キュレーション記事を量産（[Aiia 10 Repos](https://aiia.ro/blog/claude-code-token-savers-github-repos/) / [Pasquale 10 Repos](https://pasqualepillitteri.it/en/news/1181/claude-code-token-10-github-repos-savings) / [Ongboit 14 Repos](https://ongboit.com/claude-code-token-tracker/)）。

**今回の元ポスト（2026-05-03 @RodmanAi）の文脈**
このポストは上記 "10選キュレーション記事" のX要約版。Aiia の記事と項目が9割同じで、独自の検証や実測値はない（"後で役立つので保存しておこう" の典型的な保存促し型バズ投稿）。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| RTK (Rust Token Killer) で「60-90%削減」 | リポは検索ヒットせず（`rtk-ai/rtk` URL は2026-05時点で公開ページとして十分検証できない）。一般的に「ターミナル出力フィルタ」系は条件次第で60〜90%削減は理論上可能だが、再現性は要検証 | （未確認） | 🔍 未確認 |
| Context Mode で「98%削減」 | リポ実在。Playwright・GitHubツール等の大型出力をSQLiteにオフロードする仕組みは正しく、ベストケース（巨大HTML丸ごと回避）で90%超は妥当。ただし通常の開発作業全体での実効削減はもっと低い | [Mindstudio: Claude Code MCP Token Overhead](https://www.mindstudio.ai/blog/claude-code-mcp-server-token-overhead) | ⚠️ ほぼ一致（ベストケース値） |
| code-review-graph で「49倍削減」 | Tree-sitter ベースのAST/知識グラフ系の削減率としては大規模モノレポでは妥当な範囲。ただし「49倍」は特定ベンチマーク値で、汎用的な数字ではない | （リポ個別の独立検証は限定的） | 🔍 未確認（数字は要原典確認） |
| Token Savior が「97%削減」 | "シンボルでコードを参照するMCP" コンセプトは妥当（ファイル全体読込み回避＝大幅削減は理論成立）。97%は最良値の可能性高 | （リポ個別の独立検証は限定的） | 🔍 未確認 |
| Caveman Claude が「出力65-75%削減」 | リポ実在。"caveman speak" でフィラー削減＋短文化は実際に出力トークンを大幅削減する。ただし **可読性とレビューしやすさは犠牲** になる。技術的正確性は維持されるとされる | [GitHub: caveman](https://github.com/JuliusBrussee/caveman) | ✅ 一致 |
| token-optimizer-mcp が「95%以上削減」 | リポ実在。Brotli圧縮 + SQLiteキャッシュ + tiktoken正確計測の組合せ。95%+は重複ツール出力が大量にある状況での最良値。"Power user で50-70Kトークンの起動オーバーヘッド" の分析自体は説得力あり | [GitHub: token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) | ⚠️ ほぼ一致（条件付き） |
| claude-context (Zilliz) で「約40%削減」 | リポ実在。BM25 + ベクトルハイブリッド検索でコードベース全体を探索。**Zilliz自身の計測で "検索精度同等で約40%削減"** と公表されており、**リスト中もっとも誠実な数字** | [GitHub: zilliztech/claude-context](https://github.com/zilliztech/claude-context) / [byteiota: Cuts AI Tokens 40%](https://byteiota.com/claude-context-mcp-code-search-cuts-ai-tokens-40/) | ✅ 一致 |
| 全体として「トークン90%削減」 | 個別ベストケースで90%は出るが、**典型的な実運用では40〜70%** が現実的（公式の prompt caching 含めて） | [Maxim AI: How to Reduce MCP Token Costs](https://www.getmaxim.ai/articles/how-to-reduce-mcp-token-costs-for-claude-code-at-scale/) | ⚠️ ほぼ一致（過大表現） |

**重要な見落とし**: 元ポストの10リポには **公式 prompt caching が1つも入っていない**。Anthropic 公式は「prompt caching が2026年単体最強のコスト削減レバー、本番で60-90%削減」と明言している（[Anthropic公式: Lessons from building Claude Code](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything)）。本来1番目に来るべき手段がリスト外。

---

## 🌐 最新動向（2026-05-03時点）

- **Anthropic 公式: prompt caching が "everything"**: 「Claude Code 構築から得た最大の教訓は prompt caching が全て」と明言。本番ワークロードで60-90%のコスト削減が公式リファレンス値 — [Lessons from building Claude Code](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything), 2026
- **2026年Q1の TTL 縮小（1hr → 5min）でハマる人続出**: 既定変更を知らずに本番運用していると **実効コストが30〜60%増加** していた事例多数。明示的に `cache_control: {"ttl": "1h"}` を指定する必要あり — [Claude Prompt Caching in 2026: The 5-Minute TTL Change](https://dev.to/whoffagents/claude-prompt-caching-in-2026-the-5-minute-ttl-change-thats-costing-you-money-4363), 2026-Q1
- **MCPツール定義の遅延ロード**: Claude Code 公式が MCP ツール定義をデフォルト遅延化（名前だけ先に渡し、Claude が呼ぶ瞬間に schema を fetch）。これだけで起動時オーバーヘッドが数千〜数万トークン削減 — [Claude Code Docs: Manage costs effectively](https://code.claude.com/docs/en/costs), 2026
- **エンタープライズ向け Bifrost MCPゲートウェイの実測**: Code Mode で接続ツール数 96/251/508 のそれぞれで入力トークン **58% / 84% / 92% 削減**、pass rate 100% 維持。"ツール多すぎ問題" の本命解 — [Maxim AI: Reduce MCP Token Costs](https://www.getmaxim.ai/articles/how-to-reduce-mcp-token-costs-for-claude-code-at-scale/), 2026
- **"10選" 系キュレーション記事の量産化**: Aiia / Pasquale Pillitteri / Ongboit など複数メディアが同質の "10〜14選" を量産。元ポストもこの系譜のX要約版で、独自検証なし — [Aiia 10 Repos](https://aiia.ro/blog/claude-code-token-savers-github-repos/), 2026

---

## 🧩 関連概念・隣接分野

- **Auto-compaction**: Claude Code 公式の自動会話履歴圧縮機能。コンテキスト上限近くで自動発動。OSS のキャッシュ系ツールはこれと役割が一部重複するため、**両方使うと逆効果のケースあり**
- **AST 系コード検索（Tree-sitter, ast-grep）**: claude-context / code-review-graph / Token Savior の共通基盤。ファイル全体を読み込ませず "シンボル単位" で渡すアプローチで、モノレポ運用時の本命
- **CLAUDE.md / メモリファイル設計**: claude-token-efficient のアプローチ（CLAUDE.md でClaudeに簡潔出力を強制）。コード変更不要で導入コスト最低だが、効果は限定的（出力トークンのみ／入力には効かない）
- **Bifrost MCPゲートウェイ**: エンタープライズ向けMCP統合層。10選リストには載らないが、**規模が大きくなると個別OSSより先にこれを検討すべき** 領域
- **モデル選択（Sonnet vs Opus vs Haiku）**: そもそも Haiku に回せるタスクをHaikuで処理する方が、複雑な削減ツール導入よりずっと効く場合が多い

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（=元ポストの立場）**:
  - 個人開発OSSで具体的なソリューションが揃いつつあり、「組み合わせれば90%削減」は理論上可能
  - とりあえず保存しておけば後で役立つ＝損はしない情報
  - Caveman Claude や token-optimizer-mcp など、実用的に効く本物も含まれている

- **否定 / 慎重派の主張**:
  - **数字が "ベストケース盛り" すぎる**: 60-90% / 95% / 98% / 49倍 などのチャンピオンデータを並べているだけで、典型ユースケースの実効値は半分以下
  - **公式の最強レバー（prompt caching）が抜けている**: Anthropic が「これが全て」と言っている機能を1つも紹介せず、二次的なOSSばかり並べる構成は、Claude Codeを本気で使う人向けの真っ当な指南とは言いにくい
  - **10本入れたら逆効果**: Auto-compaction とOSSキャッシュの二重発動・MCPツール多重起動でコンテキストが汚染される。**むしろ厳選1〜2本のほうが効く**
  - **OSSの保守体力リスク**: 個人開発の最適化レイヤーは、Anthropic公式仕様変更（TTLの 1hr→5min みたいな静かな変更）に追従できないと数週間で陳腐化する。賞味期限の見極めが必要
  - **"10選" キュレーションの構造的問題**: 実装試した本数より紹介本数のほうが多いケースが多く、「保存しよう🔖」で終わる読者が多数派 → 何も導入されないまま終わる

- **中立的に見るときの補助線**:
  - **公式 → OSS の順番で導入**: ① Anthropic公式 prompt caching を 1hr TTL で設計 → ② Claude Code 公式の auto-compaction と MCP遅延ロードを把握 → ③ Bifrost MCPゲートウェイ（規模大なら）→ ④ ここまでで足りない部分を OSS で埋める
  - **OSSは2〜3本に絞る**: claude-context（Zilliz・40%削減・実測誠実）/ token-optimizer-mcp（可視化に強い）/ Context Mode（大型ツール出力オフロード）あたりが本リストの "本命" 候補
  - **モデル選択を先に見直す**: Haiku で済むタスクをSonnetで回していないか。これだけで2〜3倍コスト差

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] RTK / code-review-graph / Token Savior / claude-token-optimizer / token-optimizer (alexgreensh) の **個別の実測ベンチマーク** はどこまで信頼できるか（README以外の独立検証は存在するか）
- [ ] OSSキャッシュ系（token-optimizer-mcp等）と Anthropic 公式 prompt caching を併用した時、**どちらが優先的に効くか**（重複・干渉する可能性）
- [ ] Auto-compaction が走るタイミングをユーザー側で制御できるか／できないなら OSS キャッシュとの相性は実際どうか
- [ ] Bifrost MCPゲートウェイのような **エンタープライズ系統合解** と、個人開発OSS 10選的アプローチの境界線（どの規模から前者に切り替えるべきか）
- [ ] Caveman Claude のような "出力スタイル変換" 系は、**コードレビューやドキュメント生成タスク** で品質を本当に維持できるか（README以外の長期使用レポートは少ない）

---

## 📚 参考資料

- [Anthropic公式: Lessons from building Claude Code: Prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything) — 公式が "全て" と表現するprompt caching の重要性, 取得日 2026-05-03
- [Claude Prompt Caching in 2026: The 5-Minute TTL Change That's Costing You Money](https://dev.to/whoffagents/claude-prompt-caching-in-2026-the-5-minute-ttl-change-thats-costing-you-money-4363) — 2026 Q1のTTL縮小と実効コスト30-60%増の解説, 取得日 2026-05-03
- [Claude Code Docs: Manage costs effectively](https://code.claude.com/docs/en/costs) — 公式のコスト最適化機能（caching / auto-compaction / 遅延ロード）, 取得日 2026-05-03
- [GitHub: ooples/token-optimizer-mcp](https://github.com/ooples/token-optimizer-mcp) — リスト第7番。Brotli圧縮+SQLiteキャッシュ。"ghost tokens" 概念の発信元, 取得日 2026-05-03
- [GitHub: zilliztech/claude-context](https://github.com/zilliztech/claude-context) — リスト第10番。BM25+ベクトル検索で40%削減（リスト中最も誠実な数字）, 取得日 2026-05-03
- [GitHub: JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — リスト第5番。出力トークン65-75%削減を主張, 取得日 2026-05-03
- [byteiota: Claude-Context: MCP Code Search Cuts AI Tokens 40%](https://byteiota.com/claude-context-mcp-code-search-cuts-ai-tokens-40/) — claude-context の独立紹介記事, 取得日 2026-05-03
- [Maxim AI: How to Reduce MCP Token Costs for Claude Code at Scale](https://www.getmaxim.ai/articles/how-to-reduce-mcp-token-costs-for-claude-code-at-scale/) — Bifrost MCPゲートウェイの58-92%削減実測, 取得日 2026-05-03
- [Mindstudio: Claude Code MCP Servers and Token Overhead](https://www.mindstudio.ai/blog/claude-code-mcp-server-token-overhead) — MCP由来のトークンオーバーヘッド構造の解説, 取得日 2026-05-03
- [Aiia: 10 GitHub Repos to Cut Your Claude Code Tokens by 60-90%](https://aiia.ro/blog/claude-code-token-savers-github-repos/) — 元ポストとほぼ同じ10選キュレーション記事（恐らく一次ソース）, 取得日 2026-05-03
- [Pasquale Pillitteri: Claude Code Token: 10 GitHub Repos That Cut Up to 90%](https://pasqualepillitteri.it/en/news/1181/claude-code-token-10-github-repos-savings) — 同質の "10選" キュレーション, 取得日 2026-05-03
- [Buildtolaunch: Claude Code Token Optimization (Stop the $1,600 Bill)](https://buildtolaunch.substack.com/p/claude-code-token-optimization) — 実費コストの実例分析記事, 取得日 2026-05-03

---

## 🗒 メモ

- このネタは **W18戦略のど真ん中**: [[SNS運用/analytics/W18戦略メモ.md]] の B項（批評型リプ・原ポストの量産）と完全に整合する素材。"神プロンプト100選は半年で使えなくなる" 系の派生で、4/26リプの再現に使える
- **批評型ロング解説の素材**: [[SNS運用/note/_メンバーシップ準備ロードマップ.md]] のネタプール枠 "批評型ロング" の本命候補に登録できる。切り口候補:
  - 「90%削減10リポ系の罠 — 公式 prompt caching が抜けてる時点で察する3つの理由」
  - 「Claude Code トークン削減、本気でやるなら2〜3本だけ入れろ（10本入れると逆効果）」
  - 「"10選キュレーション" の見分け方 — このリストが薄い4つの兆候」
- **連投シリーズの素材**: 既存の [[SNS運用/post/draft/20260427_critique_series_02_100-claude-repos.md]] の続編・上書き案として再利用可能（"今度はトークン削減10選を解剖する"）
- **誘導動線**: 解説note → メンバーシップ「実装ツール紹介」枠（推奨3本の実装手順は会員限定）の二段構成が組める。戦略.md施策①②と相互補完
- 自分のSNS発信で出すなら、トーンは「神リポ100選は半年で消えるシリーズ」の派生として、煽らず・断定せず・観察＋軽い否定（"〜な気がする" 語尾）で組むのが W18 勝ち型テンプレ通り
