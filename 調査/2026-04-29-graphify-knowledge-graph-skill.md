---
created: 2026-04-29
tags: [調査, graphify, claude-skills, knowledge-graph, obsidian, second-brain]
source: https://x.com/L_go_mrk/status/2048717291408294085
---

# Graphify：フォルダ丸ごと"ナレッジグラフ"化する新Skill──37.5k★・71.5倍トークン圧縮の中身

> **TL;DR**
> - Graphify（[safishamsi/graphify](https://github.com/safishamsi/graphify)）は **MIT・37.5k★** の Claude Code 用Skill。`/graphify` 一発でフォルダ内のコード／PDF／画像／動画／音声を読み込み、tree-sitter（コード）+ Leiden（クラスタリング）+ Claude（意味抽出）で**1枚のインタラクティブHTML+JSON+Markdownレポート**にする。v0.5.4（2026-04-28）と昨日もリリースが走っている超活発OSS
> - **キモは「コード生情報を外に出さない」設計**。AST構造はローカル解析、画像・動画はローカル文字起こし、Claudeに送るのは**意味記述だけ**。社内コードや個人vaultで安全に使える
> - 元ツイート著者の「ナレッジ管理に便利かも」は控えめすぎ。**71.5倍のトークン圧縮**（大規模コーパス）でClaude Codeの作業効率がレベル1段違ってくる。むしろObsidian vault（既存second-brain）に直接当てる方が個人運用での効果は大きい

## 📌 元テキスト（抜粋）

> ナレッジ管理に便利かも。メモ。
>
> Graphy：フォルダの中のコード・ドキュメント・PDF・画像・動画を丸ごと読み込んで、ナレッジグラフ化するSkills。
>
> https://github.com/safishamsi/graphify…

出典: [[Clippings/Post by @L_go_mrk on X 4]] / [@L_go_mrk の元投稿](https://x.com/L_go_mrk/status/2048717291408294085)

> 📝 元ツイートでは「Graphy」と表記されているが、正式名は **Graphify**（GitHubリポジトリ名と一致）。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Graphify | コード/ドキュメント/PDF/画像/動画をナレッジグラフ化するClaude Code用Skill | `safishamsi/graphify` |
| Skill（Claude Code） | `/コマンド名` 一発で起動する追加機能。`.claude/skills/` 配下にMarkdownで定義 | `claude code skills` |
| ナレッジグラフ | 概念（ノード）と関係（エッジ）で情報を構造化したデータ | `knowledge graph NetworkX` |
| tree-sitter | プログラミング言語のAST（構文木）を高速生成するOSSパーサ | `tree-sitter parsing` |
| Leiden community detection | グラフ上のノードを密接なクラスタに分割するアルゴリズム。Louvainの改良版 | `Leiden algorithm clustering` |
| god node | 極端に多くの依存を持つ「神ファイル」。リファクタリングの第1容疑者 | `god class antipattern` |
| MCP（Model Context Protocol） | Anthropic 提唱のAIエージェント-外部ツール連携プロトコル。GraphifyはMCPサーバとしても動く | `Anthropic MCP server` |
| `CLAUDE.md` 自動書き込み | Skillが Claude Code の常駐ルールに自分の利用案内を埋め込む仕組み | `CLAUDE.md auto-injection` |
| PreToolUse hook | Claude Codeのツール使用前に走るフック。grep/readの代わりにグラフ参照させる用途 | `claude code hooks pretooluse` |
| トークン圧縮 | 巨大ファイルをグラフ要約で渡してLLMの入力トークンを削減すること | `context compression LLM` |

---

## 🧭 背景 / なぜ今これが話題なのか

**「Claude Code が大規模リポを読むときに、コンテキスト窓を食いつぶす問題」を解決する Skill 群が2026年Q1〜Q2に一気に台頭**してきた、というのが文脈の核。

時系列で押さえる:

- **2024年10月**: Anthropic が Claude Code を一般公開。ファイル直読みはできるが、100ファイル以上のリポではコンテキスト消費が爆発する課題が顕在化
- **2025年Q4**: コミュニティが `/init` で CLAUDE.md を自動生成する文化を確立。だが「ファイル一覧」レベルで止まり、**依存関係や設計意図までは捕捉できない**
- **2026年1月**: tree-sitter ベースのコード理解Skill（GitNexus等）が登場。MCPサーバ化の流れが始まる
- **2026年3月**: Claude Skills の正式仕様化。`.claude/skills/` 配下のMarkdown1枚で機能配布できる「軽量プラグイン」エコシステムが爆発
- **2026年4月**: Graphify が頭ひとつ抜けて 37.5k★ に。ポイントは **multimodal（PDF/画像/動画）対応 + プライバシー設計（生コード非送信）**。同時期にObsidian連携の `claude-obsidian`、コードレビュー特化の `code-review-graph`（49倍トークン圧縮）も並走
- **2026-04-28**: Graphify v0.5.4 リリース。**SSRF/DNS rebinding 脆弱性修正**。本格運用フェーズに入った証

つまり Graphify が出てきた背景は、「Claude Code を**個人vault・社内コード・研究資料**に当てるとき、生ファイルを毎回読ませると遅いし高い」という運用上の摩擦を、**ナレッジグラフという中間層**で解消する、という流れ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Graphify はSkillである | ✅ Claude Code の Skill 形式で配布、`/graphify` コマンドで起動 | [GitHub safishamsi/graphify](https://github.com/safishamsi/graphify) | ✅ 一致 |
| フォルダのコード・ドキュメント・PDF・画像・動画を読み込む | ✅ サポート言語多数（Python/JS/TS/Go/Rust/Java/C/C++/Ruby/Swift等23+）、PDF/Markdown/DOCX/XLSX、PNG/JPG/WebP/GIF、MP4/MOV/MP3等、YouTube URLまで対応 | [GitHub safishamsi/graphify](https://github.com/safishamsi/graphify) | ✅ 一致（むしろ範囲広い） |
| ナレッジグラフ化する | ✅ NetworkX グラフ → Leiden クラスタリング → vis.js でインタラクティブHTML、JSON、Markdownレポート出力 | [GitHub safishamsi/graphify](https://github.com/safishamsi/graphify) | ✅ 一致 |
| 「Graphy」という名前 | ❌ 正式名は **Graphify**。元ツイートのタイポ | [GitHub safishamsi/graphify](https://github.com/safishamsi/graphify) | ❌ 要注意（タイポ） |
| 便利「かも」 | むしろ控えめすぎ。71.5倍トークン圧縮（大規模コーパス）と god node 検出は、Claude Codeの作業効率をレベル1〜2段引き上げる効果が公称ベンチで出ている | [Graphify公式](https://graphify.net/) | ⚠️ ほぼ一致（過小評価） |
| Claude Code 専用 | ❌ Claude Codeだけでなく、Codex・OpenCode・Cursor・Gemini CLI・Copilot CLI・Aider・Hermes・Kiroなど15+のAIアシスタントに対応 | [GitHub README](https://github.com/safishamsi/graphify) | ❌ 要注意（射程はもっと広い） |

---

## 🌐 最新動向（2026-04-29時点）

- **Graphify v0.5.4 リリース（2026-04-28）** — SSRF/DNS rebinding セキュリティ修正。本格運用フェーズへ — [GitHub Release](https://github.com/safishamsi/graphify), 2026-04
- **GitHub Star 37.5k 到達** — 2026年4月時点でClaude Code Skill エコシステム内で**最も人気**な部類。月次伸び率も鈍化なし — [GitHub safishamsi/graphify](https://github.com/safishamsi/graphify), 2026-04
- **トークン圧縮の実測値**: 大規模コーパス（52+ファイル）で **71.5倍**、コードレビュータスクで **6.8倍**、日常コーディングで **49倍** の入力トークン削減（公称） — [CLSkills Blog](https://clskillshub.com/blog/graphify-claude-code-integration), 2026-04
- **Obsidian / Karpathy LLM Wiki 連携の派生プロジェクト**: `claude-obsidian` や `Understand-Anything` がGraphifyのアプローチを応用してObsidian vaultをナレッジグラフ化 — [GitHub claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian), 2026-04
- **MCP-native な競合 GitNexus も並走**: ノードVer.のMCPサーバとしてClaude Code/Cursor向けに同様の機能を提供。GraphifyとはAPI差はあるが用途は被る — [MarkTechPost - GitNexus](https://www.marktechpost.com/2026/04/24/meet-gitnexus-an-open-source-mcp-native-knowledge-graph-engine-that-gives-claude-code-and-cursor-full-codebase-structural-awareness/), 2026-04

---

## 🧩 関連概念・隣接分野

- **Claude Skills エコシステム**: 2026年Q1に正式化された「Markdown 1枚で配布できる軽量プラグイン」仕組み。Graphifyはその代表例。すでに awesome-skills 系キュレーションリストが乱立 — [Awesome Claude Skills](https://awesome-skills.com/)
- **Karpathy LLM Wiki パターン**: Andrej Karpathyが提唱した「LLMを使って自分の知識を相互リンク付き wiki に育てる」運動。Graphify / claude-obsidian / Understand-Anything は実装系
- **Code Property Graph (CPG)**: 古典的な「コードを構造グラフ化する」研究分野。Graphifyのコード解析パスはCPGの簡略版
- **Leiden community detection vs Louvain**: グラフクラスタリングの2大アルゴリズム。Leidenは2019年提案でLouvainの「壊れたクラスタ」問題を修正した上位互換
- **既存vault（[[2026-04-26-obsidian-claude-code-second-brain]]）への適用**: 自分の調査ノート＋日次ノートをGraphifyに食わせると、テーマ間の隠れた接続が可視化される可能性
- **競合 GitNexus**: MCPサーバ実装に振り切ったnode版ナレッジグラフエンジン。Graphifyより設置がやや重いが、PreToolUse/PostToolUseフック連携が深い

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - tree-sitter + Leiden + Claude意味抽出の組み合わせは**理論的に正しい**設計。AST（決定論的）と意味（LLM）を分離している点が他Skillより堅牢
  - **生コード非送信プライバシー設計** — 社内利用やNDA案件でも導入しやすい数少ないSkill
  - 出力がHTML/JSON/Markdown 3 形式で**人間とLLMの両方が読める**。GRAPH_REPORT.md だけでも価値がある
  - MIT + 37.5k★ + 高頻度リリース = エコシステム上のロックインリスクが低い

- **否定 / 慎重派の主張**:
  - **初回実行コストが高い**: 大規模リポでClaudeに意味抽出させると数十〜数百ドルかかる可能性。「71.5倍圧縮」は2回目以降の話で、初回投資を加味した実質効果は要計測
  - **キャッシュ不整合リスク**: `manifest.json` は mtime ベースで、`--update` を部分ファイルリストで呼ぶとグラフが縮む（v0.5.1で修正されたとはいえ運用配慮が必要）
  - **過剰な抽象化の罠**: 小規模リポ（〜30ファイル）ではグラフ化のオーバーヘッドが価値を上回る。「ファイル直読みでいいだろ」という論
  - **画像・動画解析の精度**: PDFのレイアウトや図表、動画字幕の正確性はLLM依存で、Graphify固有の保証はない
  - **2026-04-28のSSRF修正**は、それまで脆弱性があったということ。社内利用前にCVE/SECURITY.md 確認推奨

- **中立的に見るときの補助線**:
  - **適用対象を選べば強い**: 50ファイル以上の大規模リポ／PDF/画像が混在する研究資料／Obsidian vault で月1回回す、みたいな使い方が費用対効果◎
  - **Claude Codeの公式機能との競合関係**: Anthropic自身が「コードベース理解」を強化していくと、Graphifyが取り込まれる or 不要になる可能性
  - **個人運用 vs 組織運用**: 個人vaultなら導入即試せる。組織導入はSSRF修正履歴・ライセンス・SOC2など別軸の検討が必要

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] 自分のObsidian vault（[[2026-04-26-obsidian-claude-code-second-brain]] で確認した second-brain運用）にGraphifyを当てた時の出力品質。`SNS運用/` 配下500+ファイルでgod node検出は意味のある示唆をくれるか
- [ ] 初回実行のClaude API料金実測。500ファイル中PDFが20本ある程度の規模で何ドルかかるか
- [ ] GitNexus との比較（同じvaultで両方走らせて出力比較）
- [ ] `claude-obsidian` Skill との併用パターン。役割分担できるか
- [ ] PreToolUse hookが既存のClaude Code運用（Daily Log・/re-daily等）に副作用を出さないか
- [ ] Graphifyの出力（graph.html）をWeb公開した場合のSEO/被リンク獲得の可能性。"AI/テック発信のbehind-the-scenes"として記事化できるか

---

## 📚 参考資料

- [GitHub - safishamsi/graphify](https://github.com/safishamsi/graphify) — 一次情報（README、機能、ライセンス、Star、リリース履歴）, 取得日 2026-04-29
- [Graphify公式サイト](https://graphify.net/) — マーケコピー、ベンチ数値、対応AIアシスタント一覧, 取得日 2026-04-29
- [Mustafa Genc - Graphify Build a Knowledge Graph](https://medium.com/@mustafa.gencc94/graphify-build-a-knowledge-graph-from-your-entire-codebase-without-sending-your-code-to-anyone-1b6924474b50) — 第三者レビュー記事, 取得日 2026-04-29
- [CLSkills - Graphify + Claude Code 49xトークン削減](https://clskillshub.com/blog/graphify-claude-code-integration) — トークン圧縮の実測値解説, 取得日 2026-04-29
- [Claude Cookbook - Knowledge graph construction with Claude](https://platform.claude.com/cookbook/capabilities-knowledge-graph-guide) — Anthropic公式のナレッジグラフガイド（Graphifyの理論的背景）, 取得日 2026-04-29
- [MarkTechPost - GitNexus 紹介](https://www.marktechpost.com/2026/04/24/meet-gitnexus-an-open-source-mcp-native-knowledge-graph-engine-that-gives-claude-code-and-cursor-full-codebase-structural-awareness/) — 競合プロダクト, 取得日 2026-04-29
- [GitHub - claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — Obsidian vault特化版, 取得日 2026-04-29
- [GitHub - Understand-Anything](https://github.com/Lum1104/Understand-Anything) — Karpathy LLM Wikiパターン実装, 取得日 2026-04-29

---

## 🗒 メモ

- **自分のvaultに当てる検証ネタ**: `SNS運用/` 配下と `_ kiwami/` 配下と `調査/` 配下を一括Graphify化したら、**「自分が無意識に何を中心に考えているか」のgod node**が見える可能性。批評型ポジションの裏付けデータとして強い
- **note記事化候補（攻める方向）**: 「自分のObsidian vault 800ファイルを Graphify に食わせたら、AI発信者としての"思考の偏り"が露呈した話」みたいな**自己解剖型の実験記事**。元ツイートの「便利かも」という温度感を**実装してみた**側に持ち上げる差別化
- **連投シリーズ素材としての位置**: Graphifyは煽り解剖型じゃなく**実装紹介型**になる。連投シリーズ⑤あたりで「批評型から実験型へ寄せる」一環として組める。[[SNS運用/post/draft/]] の次々弾候補
- **n8n連携の妄想**: [[2026-04-29-sns-automation-implementation-plan]] でn8nが動いている前提で、毎週日曜の夜にGraphifyをvaultに走らせて差分レポートをChatworkに通知、みたいな運用も組める。「自分の思考の変化を毎週可視化する」second-brain運用の発展形
- **既存second-brain記事との差別化**: [[2026-04-26-obsidian-claude-code-second-brain]] は「読む側」の話、Graphifyは「グラフ化する側」の話。両方押さえると「AI×個人ナレッジ管理」の縦串が通る
- **重要な"待った"**: 公称71.5倍圧縮の数字は「2回目以降」の話。**初回コストの実測なしに記事化すると煽り側に回る**。試すなら自費で1回回して、実数値を持って書く方が誠実
