---
created: 2026-05-01
tags:
  - 調査
  - Claude Code
  - MCP
  - Design System
  - Impeccable
  - Anthropic
  - AI Slop
source: "[[Clippings/Post by @Oluwaphilemon1 on X.md]]"
embed: 要検討
---

# Claude Code の "AI slop UI" を殺す — デザインMCP / スキル / コネクタ 2026年版マップ

> **🔗 関連コンテンツ**
> - 📰 元クリップ: [[Clippings/Post by @Oluwaphilemon1 on X.md]]
> - 🛠 開発系メモ: [[_ memory/short-term.md]]
> - 📋 全スキル一覧: [[Claudian-スキル一覧.md]]

> **TL;DR**
> 「Claude Code で生成した UI が全部 Inter + 紫グラデ + 角丸カードに見える問題」(通称 *AI slop*) に対し、2026年Q1〜Q2 で4つの解が並んだ：① Anthropic 公式 **Claude Design**（4/17、コードベースとデザインファイルから design system を自動構築）、② サードパーティ **Impeccable** スキル（Paul Bakaus、25個のアンチパターン検出ルール）、③ **Figma MCP + Code Connect**（既存 Figma コンポーネントを実コードへマッピング）、④ Anthropic 公式 **9種クリエイティブコネクタ**（Blender / Adobe / Autodesk Fusion 他、4/28）。元ツイートの「デザインMCP」はこのうち①または③が最有力候補で、現状 "MCP" と "Skill" が混在しているため言葉のゆらぎは要注意。

## 📌 元テキスト（抜粋）

> 速報：Claude CodeはUIデザインがひどい…。ついに誰かがそれを修正しました。
> 彼らはClaude専用のデザインツールを提供するMCPを構築しました。
> 既存のデザインチームを読み取り、実際に一致するコンポーネントを生成し、それらを直接コードベースにドロップします。
> もうすべてのプロジェクトでInter + 紫のグラデーション + カードグリッドは終わりです。
>
> （引用元の Anthropic 公式アカウント @claudeai 2026-04-28 投稿）
> Claude は、クリエイティブプロフェッショナルがすでに使用しているツールに接続します。
> 新しい Blender コネクタにより、Claude から直接シーンをデバッグしたり、新しいツールを構築したり、すべてのオブジェクトにわたって変更を一括適用したりできます。

出典: [[Clippings/Post by @Oluwaphilemon1 on X.md]] / 元URL: <https://x.com/Oluwaphilemon1/status/2049911163409125673>

> ⚠️ 翻訳ゆらぎ: 原文の "design team" は文脈的に **"design system"** の誤訳/誤打の可能性が高い。"既存のデザインチームを読み取る" のではなく、"既存のデザインシステム（トークン・コンポーネント）を読み取る" が技術的に妥当。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **AI slop** | AI生成の判子的UI（Inter + 紫グラデ + カードグリッド + 角丸）の総称 | "AI slop UI", "distributive convergence" |
| **distributive convergence** | LLMが学習データの統計的中心に収束する性質。AIが似たUIを出す根本原因 | Anthropic 公式が使う用語 |
| **MCP (Model Context Protocol)** | Claude等LLMに外部ツール接続を提供するオープンプロトコル | "MCP server", "MCP connector" |
| **Claude Design** | Anthropic Labs の対話型デザインツール。codebase + デザインファイルから自動で design system を構築 | claude.ai/design |
| **Impeccable** | Paul Bakaus による Claude Code/Cursor/Codex 横断のデザインスキル（MCP**ではない**） | `npx skills add pbakaus/impeccable` |
| **frontend-design skill** | Anthropic 公式の元祖デザインスキル。277,000 installs | "Claude Code skills" |
| **Code Connect** | Figma コンポーネントを実コードのコンポーネントに 1:1 マッピングする仕組み | Figma MCP |
| **DESIGN.md** | Google Stitch 仕様準拠のデザイン言語ファイル。Impeccable が生成 | "DESIGN.md format" |
| **Creative Connectors** | Anthropic が 4/28 にリリースした9種コネクタ群 | Adobe / Blender / SketchUp / Splice / Resolume / Affinity / Autodesk Fusion / Ableton |
| **Blender MCP** | Blender の Python API を介して Claude が3Dシーンを操作 | Anthropic は Blender Development Fund のパトロンに |

---

## 🧭 背景 / なぜ今これが話題なのか

### Claude Code は UI が下手、はもう"半ば公式"の認識

2025年後半から Claude Code (CLI 版) でフロントエンド生成する人が増えるにつれ、生成される UI が **「全プロダクト同じ顔」** になる現象が顕著になった。コミュニティ用語では *AI slop* と呼ばれ、典型的なシグネチャは:

- Inter フォント (もしくは Roboto / system-ui)
- 白背景 × 紫グラデーション
- 角丸カードのグリッド配置
- 控えめなアニメーション

Anthropic 自身がこれを **"distributive convergence"**（分布的収束）と呼んでいる。LLMは学習データの「中央値」を出力する習性があり、"modern dashboard" と命じられた瞬間に何千枚という近似デザインの統計平均を吐き出す。

### 2026年Q1〜Q2 で集中対応

| 日付 | 出来事 | プロバイダ |
|---|---|---|
| **2026-04-17** | Anthropic Labs が **Claude Design** を Research Preview で公開（claude.ai/design） | Anthropic 公式 |
| **2026-04-28** | **9種クリエイティブコネクタ**（Adobe / Blender / Autodesk / Ableton / SketchUp / Splice / Resolume / Affinity / Adobe Express）を一斉発表 | Anthropic 公式（パートナー連名） |
| **2026-04-30** | **Impeccable v3.0.6** リリース（Live mode / 拡張フォント検出） | Paul Bakaus（Renaissance Geek） |
| 同期間 | **frontend-design skill**（Anthropic 公式オリジナル）が累計 **277,000 installs** 突破 | Anthropic |
| 通年 | **Figma MCP + Code Connect** が実プロダクトの design system → コード自動生成のデファクトに | Figma |

元ツイート (@Oluwaphilemon1) はこの流れの中で「MCP」というラベルを使っているが、技術的には **MCP / Skill / 独立SaaS** が混在しており、後述の「主張のファクトチェック」でゆらぎを確認する。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Claude Code は UI デザインがひどい」 | 公式の Cookbook / Anthropic ブログでも distributive convergence として明記。Inter / 紫グラデ / 角丸カードへの収束は事実認定済み | [Prompting for frontend aesthetics](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics) / [Impeccable](https://impeccable.style/) | ✅ 一致 |
| 「Claude 専用デザインツールの **MCP** を構築した」 | "MCP" を名乗るのは **Figma MCP** や **Blender MCP**。Impeccable は **Skill** であり MCP ではない。Claude Design は独立 SaaS。元ツイートの "MCP" はラベル誤用の可能性が高い | [Claude Design](https://www.anthropic.com/news/claude-design-anthropic-labs) / [Impeccable GitHub](https://github.com/pbakaus/impeccable) / [Figma MCP guide](https://github.com/figma/mcp-server-guide) | ⚠️ ほぼ一致（言葉のゆらぎあり） |
| 「既存のデザインシステムを読み取り、一致するコンポーネントを生成」 | Claude Design は "reads your codebase and design files" して design system を抽出。Figma MCP + Code Connect は既存 Figma → 実コードの 1:1 マッピングを行う。Impeccable も "scans tokens, components, rendered output" | [Anthropic Labs 発表](https://www.anthropic.com/news/claude-design-anthropic-labs) / [Figma 公式 Help](https://help.figma.com/hc/en-us/articles/39888612464151) | ✅ 一致 |
| 「コードベースに直接ドロップ」 | Claude Design は Claude Code 連携でハンドオフ。Impeccable は Cursor / Claude Code / Gemini CLI / Codex に組み込み | [Impeccable 機能](https://impeccable.style/) | ✅ 一致 |
| 「Inter + 紫グラデ + カードグリッドは終わり」 | あくまで "回避手段が揃った" 段階。デフォルト挙動を変えるにはスキル/MCP/コネクタの導入が前提 | [Frontend-design skill 解説](https://abduzeedo.com/impeccable-open-source-ai-design-skill-better-ui) | ⚠️ 誇張気味 |
| 「Blender コネクタで scene デバッグ・一括変更」 | 公式リリースで確認済み（4/28）。Blender developer が MCP コネクタを構築、Anthropic は Blender Development Fund パトロンに | [Anthropic creative connectors](https://www.anthropic.com/news/claude-for-creative-work) / [9to5Mac](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/) | ✅ 一致 |

---

## 🌐 最新動向（2026-05-01時点）

- **Anthropic Labs が Claude Design を Research Preview 公開**: claude.ai/design で対話型に UI を試作 → Claude Code へハンドオフ。Pro / Max / Team / Enterprise 加入者に段階展開 — [Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs), 2026-04
- **9種クリエイティブコネクタが一斉ローンチ**: Adobe（Creative Cloud 50+ アプリ）/ Blender / Autodesk Fusion / Ableton / Splice / SketchUp / Resolume / Affinity / Adobe Express。Blender は MCP ベースで他LLMからも利用可 — [9to5Mac](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/), 2026-04-28
- **Impeccable v3.0.6 リリース**: Live mode（HMR連携でブラウザ内反復）、フォント検出拡張。インストールは `npx skills add pbakaus/impeccable` の1行 — [Impeccable](https://impeccable.style/), 2026-04-30
- **frontend-design skill が累計277K installs**: Anthropic 公式の元祖デザインスキル。Impeccable はこれを土台に拡張 — [Emelia](https://emelia.io/hub/impeccable-ai-design-skill), 2026-04
- **VoltAgent / awesome-claude-design**: 68種の DESIGN.md フォーマット雛形をオープンソース集約、ワンショット UI 生成のテンプレ集として広がる — [GitHub](https://github.com/VoltAgent/awesome-claude-design), 2026-04
- **"Claude for CAD" のラベル登場**: Blender + Autodesk Fusion 連携で 3Dモデリング領域への進出が業界誌に取り上げられた — [DEVELOP3D](https://develop3d.com/ai/claude-for-cad-blender-autodesk-fusion/), 2026-04

---

## 🧩 関連概念・隣接分野

- **MCP (Model Context Protocol)**: Anthropic が公開しているLLM向けツール接続プロトコル。Blender / Figma / Slack 等のツールが「MCPサーバー」を立て、Claude が標準クライアントとして接続。今回の "デザイン MCP" 話題のベース技術
- **Claude Skills**: Markdown ベースのプロンプト規約集。MCP より軽量で、Claude Code / Cursor / Codex / Gemini CLI を横断する。Impeccable / frontend-design はここに属する
- **Code Connect (Figma)**: Figma コンポーネントを実コードのコンポーネント識別子（React/Vue/SwiftUI 等）に 1:1 マッピング。MCP 経由で Claude が「カスタム Button」を勝手に再発明せず、既存コードベースの `<Button>` を呼ぶようになる
- **DESIGN.md / design tokens**: AIに「この案件の見た目ルール」を教える構造化ファイル。色・タイポ・余白・モーションを記号化して、Claude がプロンプト時に必ず参照する
- **OKLCH カラー指定**: Impeccable が推す現代的色空間。CSS Color Module Level 4。HSL/RGB より知覚均一でグラデが破綻しにくい

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「スキル/MCPを噛ませれば AI slop は卒業できる」「デザインシステム読み取り → 一致コンポーネント生成は実プロダクトで効く」「Anthropic 自体が distributive convergence を認め、解決ツールを公式提供している」
- **否定 / 慎重派の主張**:
  - **解決は "回避手段の追加" であって "デフォルトの改善" ではない**。スキル/MCPを導入しないと挙動は変わらない（普通のユーザーには遠い）
  - **Claude Design は research preview**。プロダクション運用は時期尚早の声も
  - **Impeccable は Skill であり MCP ではない**。元ツイートを鵜呑みにすると技術選定で迷子になる
  - "67種の DESIGN.md テンプレ"が広がるほど **テンプレ間で再び収束** する皮肉（"Impeccable 風" が新しい AI slop になりかねない）
  - Code Connect 等は **既存デザインシステムが整備されている前提**。0→1 のプロジェクトには効かない
- **中立的に見るときの補助線**:
  - 自プロジェクトの段階で選び分け: 0→1 の試作 = `frontend-design` skill / 既存プロダクト改修 = Figma MCP + Code Connect / 厳しい品質要求 = Impeccable + 自前 DESIGN.md / Pro+ 加入者の対話試作 = Claude Design
  - "MCP / Skill / SaaS" の3区分を意識して情報を読む。SNS では雑に "MCP" と呼ばれがち

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] @Oluwaphilemon1 が指していた具体的プロダクトは Claude Design / Impeccable / Figma MCP のどれか（元ツイートのリプライまで読み込めば特定可能）
- [ ] Claude Design の "research preview" がいつ GA になるか、料金体系の最終形
- [ ] Impeccable の "Live mode + HMR" を Next.js / SvelteKit / Astro でどこまで使えるか実機検証
- [ ] Claude Code に Figma MCP を組んだ際の Code Connect マッピング精度（既存コードベースのコンポーネント命名規則との衝突）
- [ ] AI slop 対策のテンプレ群（DESIGN.md 雛形 68種）自体の "テンプレ収束" 問題への対処
- [ ] 日本国内（note・Zenn・Qiita）で Claude Design を実プロジェクト投入した事例レポート

---

## 📚 参考資料

- [Claude for Creative Work (Anthropic 公式 4/28 リリース)](https://www.anthropic.com/news/claude-for-creative-work) — 9コネクタ詳細, 取得日 2026-05-01
- [Introducing Claude Design by Anthropic Labs](https://www.anthropic.com/news/claude-design-anthropic-labs) — Claude Design 4/17 ローンチ, 取得日 2026-05-01
- [Impeccable 公式 (impeccable.style)](https://impeccable.style/) — Skill 仕様 / v3.0.6 / インストール手順, 取得日 2026-05-01
- [Impeccable GitHub (pbakaus/impeccable)](https://github.com/pbakaus/impeccable) — ソース / アンチパターンルール, 取得日 2026-05-01
- [Claude Code and Figma: Set up the MCP server (Figma 公式)](https://help.figma.com/hc/en-us/articles/39888612464151-Claude-Code-and-Figma-Set-up-the-MCP-server) — Figma MCP セットアップ, 取得日 2026-05-01
- [Anthropic Cookbook: Prompting for frontend aesthetics](https://platform.claude.com/cookbook/coding-prompting-for-frontend-aesthetics) — distributive convergence の定義, 取得日 2026-05-01
- [9to5Mac: Anthropic releases 9 Claude connectors](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/) — クリエイティブコネクタ報道, 取得日 2026-05-01
- [DEVELOP3D: Claude for CAD arrives with Blender / Autodesk Fusion](https://develop3d.com/ai/claude-for-cad-blender-autodesk-fusion/) — CAD領域進出, 取得日 2026-05-01
- [VoltAgent: awesome-claude-design (GitHub)](https://github.com/VoltAgent/awesome-claude-design) — 68種 DESIGN.md テンプレ集, 取得日 2026-05-01
- [Emelia: Impeccable 完全ガイド](https://emelia.io/hub/impeccable-ai-design-skill) — frontend-design 277K installs 出典, 取得日 2026-05-01
- 元クリップ: [[Clippings/Post by @Oluwaphilemon1 on X.md]] — Xポスト原文（2026-04-29）

---

## 🗒 メモ

- **note記事化候補（強）**: 「Claude Code の UI が全部同じ顔になる問題と、それを殺す4つの解（Claude Design / Impeccable / Figma MCP / Creative Connectors）」というテーマは AI 実務層に刺さる。"distributive convergence" の用語解説 + 4手段の使い分けマトリクスでまとめれば 1本の柱になる
- **X連投シリーズ候補**: 「神プロンプト系」と並走させる形で、"Claude Code の UI が AI slop な理由" 4ツイート連投。Anthropic 自身が認めている "distributive convergence" は強いフック
- **Tsukapon 自身への適用**: vault の `_ kiwami/my-clone/` 人格データを DESIGN.md 化して Claudian に渡せば、生成されるドキュメント・記事のトーンも収束を避けやすい（応用案）
- **元ツイートの "MCP" 表記**: SNS 上では MCP / Skill / Connector / SaaS が雑に "MCP" と呼ばれている。記事化する際は **3区分の整理** を最初に置くと差別化できる
- **継続ウォッチ**: Claude Design が research preview から GA に移るタイミング、Impeccable v4 の方向性、Figma MCP に競合（Penpot / Sketch）が乗ってくるか
