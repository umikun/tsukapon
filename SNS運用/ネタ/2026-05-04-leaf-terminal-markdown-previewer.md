---
created: 2026-05-04
tags: [調査, ターミナル, markdown, CLI, rust, AI-workflow]
source: "[[Clippings/Post by @NainsiDwiv50980 on X 1]]"
---

# leaf — ターミナル内で「GUI級のマークダウンプレビュー」を実現するRust製TUI

> **🔗 関連コンテンツ**
> - 📌 元クリッピング: [[Clippings/Post by @NainsiDwiv50980 on X 1]]
> - 🧠 同日の関連調査: [[調査/2026-05-04-claude-code-superpowers-plugin]] / [[調査/2026-05-04-gemini-notebooklm-workflow]]
> - 🛠 vault運用との接点: [[CLAUDE.md]]（Obsidian + Claude Code 第二の脳運用）
> - 📰 W18振り返りで触れた連投シリーズ④（Obsidian × Claude Code）: [[SNS運用/analytics/W18分析レポート.md]]

> **TL;DR**
> - leafは **Rust製のターミナルMarkdownプレビューア**（GitHub `RivoLink/leaf` ・★532 ・MIT・最新v1.18.2が2026-05-03リリース）
> - 売りは **「ライブプレビュー＋ファジーピッカー＋LaTeX/Mermaid対応＋Vimキーバインド」をターミナル単独で完結** させる点。`aichat "..." > notes.md && leaf --watch notes.md` のようなAI×CLIワークフローに刺さる
> - 競合は **glow / frogmouth / mdcat / termimad** など。leafはこの中で**「ライブリロード×LaTeX×Vimキーバインド」を全部取った後発勢**で、Show HN（Hacker News）では46pt獲得しつつも「依存数の多さ」「LLM生成っぽい絵文字リスト」への批判もあり

## 📌 元テキスト（抜粋）

> あなたのターミナルが、マークダウンアプリを置き換えようとしています。ほとんどの開発者は今でもこうしています：→ ターミナルでマークダウンを書く → プレビューするためにブラウザ/エディタに切り替える → 戻って修正、繰り返し。そのコンテキストスイッチング？ フローを殺します。さあ、leafをご紹介します。ターミナル内でGUIのようなマークダウン体験を提供する、100%オープンソースのツールです……

出典: [[Clippings/Post by @NainsiDwiv50980 on X 1]]（X投稿・2026-05-04 / @NainsiDwiv50980）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **TUI** | Text User Interface。ターミナル上でマウス＋キーボードを使うGUI風UI | `Textual` `tui-rs` `ratatui` |
| **watchモード** | ファイル保存を検知して自動再描画する常駐モード | `inotify` `fswatch` `notify crate` |
| **ファジーファイルピッカー** | 部分一致検索で候補を絞るファイル選択UI | `fzf` `skim` `nucleo` |
| **LaTeX** | 数式記述言語。`$E=mc^2$` 形式でマークダウンに埋め込まれる | `KaTeX` `MathJax` |
| **Mermaid** | テキストで書く図/フローチャート記法 | `mermaid-cli` `flowchart` |
| **stdinパイプ** | 標準入力から流し込む UNIX流の連結方法（`cmd1 \| cmd2`）| `pipe` `xargs` |
| **aichat** | ターミナル上でChatGPT/Claude等のLLMにクエリするCLIツール | `aichat` `llm` `Simon Willison llm` |
| **frontmatter** | `---` で挟むYAMLメタデータブロック | `Obsidian frontmatter` `Hugo front matter` |
| **AUR** | Arch Linux User Repository。コミュニティ作のパッケージ群 | `yay` `paru` |
| **Cargo** | Rust公式パッケージ・ビルドツール | `cargo install` `crates.io` |
| **Show HN** | Hacker News の自作プロダクト紹介投稿カテゴリ | `news.ycombinator.com/show` |

---

## 🧭 背景 / なぜ今これが話題なのか

ターミナル内Markdownプレビューは2010年代から定番の「あったら便利」カテゴリで、有力な先人が複数いる：

- **2017年〜**: `axiros/terminal_markdown_viewer`（Python製）が初期の代表格
- **2020年〜**: **glow**（Charmbracelet・Go）がHNとGitHubで人気を獲得。「ターミナルでも美しい静的レンダリング」を確立
- **2023年〜**: **frogmouth**（Textualize・Python）が「ブラウザ風ナビゲーション＋ブックマーク＋履歴」で台頭
- **2024〜2025年**: AI CLI（`aichat` `llm` `gpt-cli` `Claude Code`）が普及し、**「LLM出力 → markdownファイル → 即プレビュー」**のニーズが急増
- **2026-04下旬**: leafがHN [Show HN](https://news.ycombinator.com/item?id=47888423) に投下（46pt / 25コメント）→ 5/3にv1.18.2 → 5/4に @NainsiDwiv50980 のXポストで再度拡散

**今このタイミングで話題な3つの理由**:

1. **AI×CLIワークフローの一般化**: Claude Code等が「ターミナルからmarkdown生成」を当たり前にした。生成物を即座に綺麗に確認したい需要が爆増
2. **Rust製TUIの黄金期**: `ratatui`（旧tui-rs）の成熟でRustでのリッチTUI開発コストが激減。leaf含む後発勢が一気に投入できる土壌
3. **glowへの不満点を埋める**: glowは静的レンダリング止まりで**ライブリロード非対応**。leafはこの欠点を直球で潰しに来た

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 100%オープンソース | MITライセンスでGitHub公開・Rust 96.1% | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| ライブプレビューと自動リロード（watchモード） | ドキュメント記載・公式機能 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| ファジーファイルピッカー | 公式README記載 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| 美しいテーマ（ocean、forest、solarized） | テーマピッカー機能・複数テーマ確認 | [leaf公式](https://leaf.rivolink.mg/) | ✅ 一致 |
| フルマークダウン + テーブル + LaTeXサポート | LaTeX→Unicode変換、テーブル境界Unicode描画 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致（※LaTeXはUnicode変換であり完全な数式エンジンではない点に注意） |
| コードブロックのシンタックスハイライト | 40+言語対応・行番号付き | [leaf公式](https://leaf.rivolink.mg/) | ✅ 一致 |
| ビルトインTOCナビゲーション + 検索 | サイドバーTOC・1〜9で見出しジャンプ・検索 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| stdinで動作（パイプ入力） | CLI-friendly設計でstdin対応明記 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| サブスクリプションなし・トラッキングなし | MITライセンスでオフライン動作 | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| 「ターミナル内でそのまま」摩擦なし | TUIで完結（外部GUIアプリ不要） | [GitHub](https://github.com/RivoLink/leaf) | ✅ 一致 |
| 「他のマークダウンアプリを置き換える」 | 置き換える"可能性"はあるが、ObsidianやTyporaのような **編集体験** はない（あくまでプレビュー特化） | [HN議論](https://news.ycombinator.com/item?id=47888423) | ⚠️ ほぼ一致（誇張気味）|

---

## 🌐 最新動向（2026-05時点）

- leaf v1.18.2 がリリース。HN指摘の `cargo audit` セキュリティ脆弱性も最新版で修正済 — [Hacker News](https://news.ycombinator.com/item?id=47888423), 2026-04
- frogmouth がTextualize公式から「ブラウザ風ナビゲーション機能の決定版」と位置付け継続 — [BrightCoding](https://www.blog.brightcoding.dev/2026/02/14/frogmouth-the-revolutionary-terminal-markdown-browser), 2026-02
- `ratatui` v0.30前後の安定化により Rust製TUIプロジェクトが急増中。leafもこの恩恵 — [crates.io](https://crates.io/crates/md-tui), 2026
- 2026年版「Best Markdown Viewer」記事ではfrogmouth/glow/leafの3強が常連 — [MacMD Viewer](https://macmdviewer.com/blog/best-markdown-viewer), 2026
- AUR `leaf-markdown-viewer-bin` パッケージも登場し ArchLinux勢が即座に試せる体制に — [AUR](https://aur.archlinux.org/packages/leaf-markdown-viewer-bin), 2026

---

## 🧩 関連概念・隣接分野

- **glow（Charmbracelet・Go）**: leafの最大の競合。静的レンダリングの美しさが定評だが、ライブリロード非対応。leafの差別化ポイントの直接の比較対象
- **frogmouth（Textualize・Python）**: ブラウザ風ナビ・履歴・ブックマーク。leafが「軽量・即時プレビュー」なら frogmouth は「常駐ブラウザ」。用途が微妙にズレる
- **mdcat**: 「fancy cat for Markdown」。Kitty/iTerm2前提で爆速だが**テーブル非対応**。プレビュー深度はleaf > mdcat
- **Charmbracelet エコシステム**: glow / gum / lazygit など Go製TUIの一大勢力。**Rust製leafはここへの対抗馬**
- **AI CLI（aichat / llm / Claude Code）**: leafの存在意義を下支えする。LLM出力 → markdown → leaf --watch のフローが想定ユースケースの中心
- **Obsidian**: GUI版の「第二の脳」代表格。leafはObsidianの**完全代替ではなく補完**（ターミナル中心ワークフローの隙間を埋める）

---

## 🪞 反対意見 / 別角度からの視点

### 肯定側の主張（ポストの主張）
- ターミナル←→GUIの**コンテキストスイッチがフローを殺す**
- AI CLI出力を即プレビューする最短経路
- オフライン・サブスクなしで快適

### 否定 / 慎重派の主張（HN議論より）
- **「pandoc + lynx で十分では」**: 既存のシンプルツールの組み合わせで代替可能（依存数を増やす理由が薄い）
- **「LLM生成っぽいREADME」**: 機能リストの絵文字チェックボックス連発が"自分で書いた"感が薄い・コミュニティから疑念
- **「依存数多すぎ＝サプライチェーン攻撃リスク」**: Rustエコシステムの依存ツリーは深く、`cargo audit` でも実際に脆弱性が出た
- **「screenshot不足」**: GUI"のような"を謳うわりにREADMEに視覚的サンプルが少ない（これは v1.18.2 までに改善されたか要確認）

### 中立的に見るときの補助線

「leafは置き換える」 vs 「pandoc+lynxで十分」は**用途の前提が違う**:

| シーン | 適切なツール |
|---|---|
| 5秒だけサクっと見たい | mdcat / pandoc+lynx |
| AI CLI出力をライブで見たい | **leaf** |
| markdownを"ブラウザ的に"探索したい | frogmouth |
| 静的レンダリングの美しさ重視 | glow |
| GUIで本格編集 | Obsidian / Typora / VSCode |

→ leafは **「AI×CLI×ライブプレビュー」** の特定ニッチでは現状の最適解候補。ただし**「全部置き換える」は過大広告**で、Obsidianのような編集体験は提供しない。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] leafの **Wiki-link `[[]]` 解決** はどこまで対応してる？ ObsidianのvaultをCLIで開きたい時に有用
- [ ] **画像表示** はSixel/iTerm2のインラインプロトコル対応？ それともテキスト代替？
- [ ] **更新頻度** v1.18.2のメジャーバージョン進行ペース → サステナビリティはどうか
- [ ] Claude Code等の **Hooks経由でleafを自動起動** するワークフローは作れるか
- [ ] glowの **ホスト機能（glow.sh）** に相当する共有機能はleafにあるか
- [ ] 自分のObsidian vault運用（[[CLAUDE.md]]）に **CLIプレビューを組み込む価値** は？ Obsidianネイティブで足りるか

---

## 📚 参考資料

- [GitHub - RivoLink/leaf](https://github.com/RivoLink/leaf) — 一次情報・機能リスト・ライセンス・最新版v1.18.2確認, 取得日 2026-05-04
- [leaf公式サイト](https://leaf.rivolink.mg/) — 機能詳細・テーマ・プラットフォーム対応, 取得日 2026-05-04
- [Show HN: leaf – a terminal Markdown previewer with a GUI-like experience](https://news.ycombinator.com/item?id=47888423) — コミュニティ評価・批判・代替案議論（46pt/25comment）, 取得日 2026-05-04
- [Best Markdown Viewer in 2026](https://macmdviewer.com/blog/best-markdown-viewer) — 2026年時点の市場マップ, 取得日 2026-05-04
- [Frogmouth: The Revolutionary Terminal Markdown Browser - BrightCoding](https://www.blog.brightcoding.dev/2026/02/14/frogmouth-the-revolutionary-terminal-markdown-browser) — frogmouth との比較軸, 取得日 2026-05-04
- [GitHub - charmbracelet/glow](https://github.com/charmbracelet/glow) — 主要競合の確認, 取得日 2026-05-04
- [GitHub - Textualize/frogmouth](https://github.com/textualize/frogmouth) — ブラウザ風機能の比較, 取得日 2026-05-04
- [AUR (en) - leaf-markdown-viewer-bin](https://aur.archlinux.org/packages/leaf-markdown-viewer-bin) — ArchLinuxパッケージ存在確認, 取得日 2026-05-04

---

## 🗒 メモ

### このネタの使い道（仮説）

**SNS活用候補**:
- ✅ W19の批評型ポスト題材として強い: 「『あなたのターミナルがmarkdownアプリを置き換える』←本当に置き換えるのは"プレビュー特化のニッチ"だけ。Obsidianの代替にはならない」型のツッコミポスト
- ✅ 連投シリーズ⑤⑥のサブ題材としても使える: **「『○○が△△を置き換える』系の煽り解剖」** の例として最適
- ⚠️ note記事の単独テーマには弱い（既知ツールカテゴリで目新しさが中程度）→ 「AI CLI ワークフロー特集」の中で1パートとして扱うのが筋

**自分の運用への応用**:
- Claude Code から markdown 生成 → leaf でプレビューのフロー、**動作検証する価値はある**
- ただし普段は Obsidian で編集→プレビューが最速なので、leafは「**SSH先のサーバー上でAI出力を確認する時**」に役立つ位置づけになりそう
- 連投シリーズ⑤「Anthropic Skills 全部入れろ煽り解剖」の3点コンパクト型に**「ターミナルツールも"全部入れる"が罠」**として横スライドできる素材

### 仮説：批評型ポストの題材として

> "あなたのターミナルがmarkdownアプリを置き換える"系の海外バズ
> 中身を見たら「プレビュー特化の良ツール」だった😅
> 「置き換える」は煽りで、実際はObsidian/Typoraの **代替ではなく補完** です。
>
> 自分も毎日Obsidian + Claude Codeで第二の脳運用してて思うのは
> 🧠 編集体験はObsidianが圧勝
> 🧠 ターミナル完結は"AI出力の即プレビュー"でだけ刺さる
> 🧠 用途を切り分けないとツール疲れする
>
> "全部置き換える"は煽り。"使う場所を切り分ける"のが本体です。

→ ✅ **2026-05-04 格納完了**: W19連投シリーズ⑦の追加候補として [[SNS運用/analytics/W19戦略メモ.md]] の「🆕 連投シリーズ⑦ 追加候補」セクションに本文ドラフト・投下条件・派生展開アイデアを格納済み。

**投下判断のフロー**:
- 5/5(火) ⑤投下 → 数字測定
- 5/8(金) ⑥投下 → 数字測定
- 5/9(土) 19:00頃: ⑤+⑥合計imp 600+ なら⑦GO判定
- GO時: 5/9 夜 or 5/10朝に投下
- NO-GO時: W20送り＋3点コンパクト型の改良検討

---

*作成日: 2026-05-04 21:35 / 調査者: Claudian + WebSearch + WebFetch / 環境: Tsukapon vault内モード*
