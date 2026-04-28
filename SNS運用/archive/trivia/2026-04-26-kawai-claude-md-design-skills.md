---
created: 2026-04-26
tags: [調査, CLAUDE.md, DESIGN.md, デザインシステム, Claude-Code, AIデザイン, KAWAI]
source: "https://x.com/kawai_design/status/2043994567729373358"
---

# KAWAI流「CLAUDE.md = 全スキル共通の脳」── デザインスキル群を"同じ記憶"で動かす運用論

> **TL;DR**
> - SHIFT AIのCDO・KAWAI(@kawai_design) が提唱しているのは、**CLAUDE.md にブランド定義（世界観・カラー・タイポ・運用ルール）を集約して、サムネ生成／note記事執筆／その他デザインスキルが"同じ記憶"を参照する**運用思想。
> - キモは **「スキル＝個別ジョブ、CLAUDE.md＝共有メモリ、DESIGN.md＝見た目の憲法」** という3層構造。バラバラに動かすと採点・FBがブレるので、**根を共通化してから枝（スキル）を増やす**順番が正しい。
> - 立ち上げ手順は段階的で、まずは **note記事執筆スキル → サムネ採点・改善FBスキル** を先に動かし、徐々に他デザインスキルへ拡張。"いきなり全部スキル化"は失敗する。
> - 注目: 弊vaultの [[CLAUDE.md]] と [[note記事用サムネイルのデザインシステム仕様書]] は、まさにこの構造の弱い実装になっている。**CLAUDE.md → DESIGN.md → 各スキル の参照線を強める伸びしろ**がある。

---

## 📌 元テキスト（抜粋）

> これ発想がくっっっっっそやばすぎる。
> create-agent-tui：
> 自分が使いやすい思い通りの「ターミナルのUI」を作って、そこでAIを動かすことができる。ファイル操作・シェル実行・Web検索などのツールを後付けで増減できるので、業務に合わせて育てられる。

引数で指定された対象URL: <https://x.com/kawai_design/status/2043994567729373358>

該当の **@kawai_design 投稿の内容**（X本文取得は402ブロックされたため、検索結果のサマリで補完）:

> 「デザインスキルを統合運用するには、**CLAUDE.md という共有のブランド定義**を全スキルが参照することが重要。サムネに対して採点と意味のあるFBが返せるのも、すべてのスキルが"同じ記憶"を持っているから。**まずはnote記事執筆スキルから始めて段階的に複数のデザインスキルを構築する**アプローチを採っている」

出典: [@kawai_design 該当投稿](https://x.com/kawai_design/status/2043994567729373358) ／ 隣接エディタ選択: [[Clippings/Post by @L_go_mrk on X 2.md]]（こちらは別話題のcreate-agent-tui。混在しているため本ノートはX URL側を主題に扱う）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| CLAUDE.md | プロジェクトルートに置きClaude Codeが毎セッション読み込むルールブック | `Claude Code memory file` `project rules` |
| DESIGN.md | デザインシステム（色・フォント・余白・コンポーネント等）をMarkdown化した"見た目の憲法" | `KAWAI DESIGN.md` `Google Stitch design tokens` |
| Claude Skill | `.claude/commands/*.md` で定義する再利用可能ジョブ。`/foo` で呼び出す | `Claude skills directory` |
| ブランド定義 | 世界観／トーン＆マナー／カラーパレット／タイポ／運用Do&Don't を1ヶ所に集約した記述 | `brand guideline markdown` |
| 採点・意味のあるFB | サムネ等の出力を**ルール基準でスコア化**し、改善案を返すこと（センス依存からの脱却） | `AI design feedback rubric` |
| KAWAI(@kawai_design) | SHIFT AI CDO、デザイン×AI領域の主要発信者。"DESIGN.mdの提唱者"の1人 | `KAWAI BOOKS` `MiriCanvas ambassador` |
| 共有メモリ | 複数スキル/エージェント間で同じコンテキストを参照する設計 | `shared context` `agent memory` |
| 段階的スキル化 | 1スキルずつ作って共通基盤に紐付ける増やし方 | `incremental skill expansion` |

---

## 🧭 背景 / なぜ今これが話題なのか

2024〜2025年: Claude Code が `CLAUDE.md` を**プロジェクトのルールブック**として標準サポート。READMEがプロジェクト説明の定番だった世界に対し、**"AIが読む前提の規約ファイル"** が定着。

2025年末〜2026年Q1: KAWAI 氏らが **DESIGN.md** を提唱。Figmaで管理していたデザインシステムを **「色／フォント／余白／コンポーネント／Do&Don't／レスポンシブ／AIプロンプトガイド」** の9セクションでMarkdown化し、Claude Code・Google Stitch・Lovart 等の生成系AIに **「これに沿って作って」** と渡せるようにした流れが拡大。**「センスは不要になった」** というキャッチで noteで反響を呼んだのが2026年4月（[KAWAI記事](https://note.com/kawaidesign/n/nbf90149e30db)）。

2026年Q2(=今): スキル粒度（`.claude/commands/*.md`）でデザイン作業をジョブ分割する運用が広がる中、**「サムネ生成スキル」「note記事執筆スキル」「LP生成スキル」がそれぞれ独自のブランド観で動いてしまう** 問題が顕在化。**KAWAIの今回の投稿**は、その解決策として **「CLAUDE.md にブランド定義を集約 → 各スキルがそれを参照 → 採点・FBの基準が統一される」** という統合運用論を打ち出したもの。

つまり構造としては:

```
CLAUDE.md（共有メモリ：全スキルが冒頭で読む憲法）
   ├─ DESIGN.md（見た目の憲法：色／タイポ／余白／コンポ）
   ├─ ブランド定義（世界観／トーン／NGワード）
   └─ 各スキル（.claude/commands/*.md）
        ├─ /thumbnail-score      ← CLAUDE.md＋DESIGN.md を毎回参照
        ├─ /note-write           ← 同上
        └─ /lp-generate          ← 同上
```

この構造によって、**サムネに対する「ここが10点中6点」みたいな採点と、「色のコントラストがDESIGN.md準拠で●●を3に変えると上がる」みたいな具体FB**が出せるようになる。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「CLAUDE.md を全スキル共通のブランド定義として使う」 | KAWAI 氏は note・X・Threads で、**CLAUDE.md に「UI／資料生成時はDESIGN.mdの値だけ使うこと」と書く運用**を推奨。Claude Help Center も Claude Design でデザインシステムを設定する公式手順を提供 | [DESIGN.md×CLAUDE.md解説（Cloud and Code）](https://cloud-and-code.com/posts/claude_design_md/), [Set up your design system in Claude Design](https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design) | ✅ 一致 |
| 「サムネに対して採点と意味のあるFBが返せるのは、全スキルが同じ記憶を持っているから」 | KAWAI 氏は **OCR + WCAGガイドライン** で4要素を採点する「デザイン定量化Webアプリ」を Claude Code で構築済み。採点ロジックがDESIGN.mdの値に紐付いている | [@kawai_design 関連発信まとめ（検索結果）] | ✅ 一致 |
| 「note記事執筆スキルから始めて段階的に複数のデザインスキルを構築」 | KAWAI が運営する **KAWAI BOOKS（note）は600+記事のAI×デザイン記事庫**。実際にnote執筆を起点にデザインスキル群を増やしている運用が確認できる | [KAWAI BOOKS（note）](https://note.com/kawaidesign) | ✅ 一致 |
| 「DESIGN.md は color / typography / spacing / components / Do&Don't 等 9セクション構成」 | KAWAI 自身が Threads で「**基盤(世界観/カラー/タイポ)・スタイル(コンポ/レイアウト/奥行き)・運用(Do&Don't/レスポンシブ/AIプロンプト)** の3カテゴリ × 9セクション」を公開 | [@kawai_design_ig (Threads)](https://www.threads.com/@kawai_design_ig/post/DW9GHhkktlk/) | ✅ 一致 |
| 「投稿日は2026年4月下旬」（status ID `2043994567729373358` 周辺） | 同アカウントの近接ID（`2044007470159540336`）が同日帯のフォローアップ投稿として確認でき、**2026年4月下旬の発信**で整合 | [@kawai_design follow-up post](https://x.com/kawai_design/status/2044007470159540336) | ⚠️ ほぼ一致（X本文の直接取得は402ブロック、近接IDから推定） |

---

## 🌐 最新動向（2026-04-26時点）

- **DESIGN.md が"AIデザインの常識"として浸透**: KAWAI記事「センスは不要になった」が2026-04-08に公開、Cloud and Code 等の技術ブログでも実装解説が拡散 — [Cloud and Code: DESIGN.mdを入れるだけで…](https://cloud-and-code.com/posts/claude_design_md/), 2026-04
- **クラスメソッドが自社デザインガイドをDESIGN.md化して公開**: 大手SIerがコーポレートデザインシステムをそのままMarkdownに落として運用検証 — [DevelopersIO: クラメソのデザインガイドをDESIGN.mdで実装](https://dev.classmethod.jp/articles/design-md-ai-agent-design-system/), 2026-04
- **Claude Design の公式機能化**: Anthropic 公式が "Claude Design" としてデザインシステム設定機能をHelp Centerに整備、対話でデザインシステム→UI→スライドまで生成可能に — [Get started with Claude Design](https://support.claude.com/en/articles/14604416-get-started-with-claude-design), 2026-04
- **Claude Code向けUI/UXスキル18選など"スキル束"記事の量産**: スキルマーケット的なまとめ記事が一気に増加。デザイン領域のスキル化競争 — [The 18 Best Claude Code Skills for UI/UX Design](https://pasqualepillitteri.it/en/news/576/claude-code-skills-design-uiux-guide), 2026
- **Qiita 2026年4月更新「Claude Codeフロントデザインskills10選」**: 日本コミュニティでも実務スキル束が定番コンテンツ化 — [Qiita: Claude Codeの役に立つフロントデザインのskills10選](https://qiita.com/kamome_susume/items/41300417840aa107472e), 2026-04

---

## 🧩 関連概念・隣接分野

- **Claude Skills（`.claude/commands/`）**: 1スキル=1ジョブで定義。KAWAI流の運用は「全スキルが冒頭で CLAUDE.md と DESIGN.md を読み込む」前提で書かれる。
- **DESIGN.md**: KAWAI が普及の中心。**色・タイポ・余白・コンポ・運用Do&Don't** をMarkdownで明文化。Figma/SketchをAIフレンドリーに置換する動き。
- **Google Stitch（Gemini ベースの UI 生成ツール）**: DESIGN.md 風のテキスト仕様を入れて UIを吐かせるユースケースが多い。
- **多階層メモリ（短期/中期/長期）**: 弊vault [[_ memory/short-term.md]] [[_ memory/mid-term.md]] [[_ memory/long-term.md]] と同思想。**「全スキルが同じ記憶を読む」設計はHermesエージェント発想と地続き**。
- **採点rubricベースのAIフィードバック**: 「主観のセンス」から「客観のスコア」への移行。WCAG／OCR／コントラスト比など機械可読な指標が採点軸。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「CLAUDE.md にブランド定義を集約すれば、スキルが増えても採点・FBの軸がブレない。サムネとnoteタイトルとLPコピーが"同じ世界観"で揃う。これがないと、スキル数が増えるほど一貫性が失われる」
- **否定 / 慎重派の主張**:
  - **CLAUDE.md 肥大化のリスク**: ブランド定義・運用ルール・絶対ルール・例外…全部詰め込むと数千行になり、毎セッションのコンテキスト消費が膨張する。**DESIGN.md・BRAND.md・OPS.md 等に分割し、CLAUDE.md は"参照マップ"に留める**ほうが健全という意見。
  - **デザインスキル統合の前にユーザー検証が先**: 「ブランド定義をいくら整えても、刺さるサムネ／刺さるタイトルかどうかは結局A/B検証次第」。**統合運用論はクリエイター側の自己満足になりがち**との指摘。
  - **Claude Code 依存の前提**: CLAUDE.md ＋ Claude Skills は Anthropic ロックイン構造。Cursor / Codex / Aider 等を併用するチームでは、**スキル定義の重複・分裂**が起きる。
  - **段階的スキル化＝先延ばしの言い訳になりうる**: 「note執筆スキルから」と言いつつ、結局2スキル目が出ないまま終わるケースも多い。**ロードマップを明示して期限を切る**運用が必要。
- **中立的に見るときの補助線**: 「**スキル数が3つを超えたタイミング**で、CLAUDE.md → DESIGN.md → 各スキルの参照線を見直す」のが実務的なバランス。1〜2スキルなら統合運用は過剰設計、5スキル以上なら必須。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] KAWAI が運用している **デザインスキルの具体的なファイル構成**（`.claude/commands/` の中身）。実物のSKILL.mdサンプルが公開されているか
- [ ] **DESIGN.md と Claude Skills（"design-system" skill）の使い分け基準**。どこまでDESIGN.md単独で済み、どこからスキル化が必要か
- [ ] **採点rubricの具体例**: 4要素・WCAG準拠・OCR検査をどう組み合わせて10点満点に落としているか
- [ ] 弊vault [[CLAUDE.md]] と [[note記事用サムネイルのデザインシステム仕様書]] の **接続線をどう強化するか**（現状は仕様書がCLAUDE.mdから明示参照されていない）
- [ ] **Claudianスキル群（[[Claudian-スキル一覧.md]]）への適用**: re-daily / thread / quote-rewrite / md-format 等が「同じ記憶」を読む設計になっているか棚卸しする価値あり
- [ ] **失敗パターンの収集**: CLAUDE.md統合運用で破綻したケース（肥大化・スキル衝突・コンテキスト溢れ）の事例

---

## 📚 参考資料

- [@kawai_design 該当投稿（X URL）](https://x.com/kawai_design/status/2043994567729373358) — 元ツイート（本文直接取得は402のため、検索エンジンのスニペット＋著者の他発信から内容再構成）, 取得日 2026-04-26
- [@kawai_design follow-up post](https://x.com/kawai_design/status/2044007470159540336) — 同日帯の連投。投稿時期推定の補助, 取得日 2026-04-26
- [KAWAI: 【センスは不要になった】DESIGN.mdがAIデザインの常識を変える理由](https://note.com/kawaidesign/n/nbf90149e30db) — DESIGN.md の思想と書き方, 取得日 2026-04-26
- [KAWAI: 画像生成AI（3種）の比較まとめ](https://note.com/kawaidesign/n/nbf2089efa698) — KAWAI の最近の発信トーン把握, 取得日 2026-04-26
- [@kawai_design_ig (Threads): DESIGN.mdの構造を公開します](https://www.threads.com/@kawai_design_ig/post/DW9GHhkktlk/) — 9セクション構成（基盤/スタイル/運用）の一次情報, 取得日 2026-04-26
- [Cloud and Code: DESIGN.mdを入れるだけで、Claude Codeのデザインが劇的に変わる](https://cloud-and-code.com/posts/claude_design_md/) — CLAUDE.md と DESIGN.md の橋渡しの実装解説, 取得日 2026-04-26
- [DevelopersIO: クラメソのデザインガイドをDESIGN.mdで実装してみた](https://dev.classmethod.jp/articles/design-md-ai-agent-design-system/) — 大手企業の実装事例, 取得日 2026-04-26
- [Set up your design system in Claude Design (Anthropic Help Center)](https://support.claude.com/en/articles/14604397-set-up-your-design-system-in-claude-design) — Anthropic公式のデザインシステム設定手順, 取得日 2026-04-26
- [The 18 Best Claude Code Skills for UI/UX Design](https://pasqualepillitteri.it/en/news/576/claude-code-skills-design-uiux-guide) — スキル束記事の代表例, 取得日 2026-04-26

---

## 🗒 メモ

- このノートは引数のX URLを主題に扱った。エディタ選択側（[[Clippings/Post by @L_go_mrk on X 2.md]] の create-agent-tui）は別話題のため、別ノート [[2026-04-26-create-agent-tui-openrouter]] にすでに分離済み。混在入力時は **引数のURL > エディタ選択** で優先順位を決めた。
- **弊vault適用案**: 現状の [[CLAUDE.md]] は運用ルール中心で、ブランド定義（世界観／カラー／タイポ）が薄い。[[note記事用サムネイルのデザインシステム仕様書]] が事実上のDESIGN.mdになっているが、**CLAUDE.md側から「サムネ生成・note執筆時は仕様書のトーンを参照すること」と明示参照を入れる**だけで、KAWAI流統合運用に1段近づく。[[Claudian-スキル候補.md]] にエントリ化する価値あり。
- **note記事化の切り口**: 「**Claudian全スキルを"同じ記憶"で動かす ── KAWAI流CLAUDE.md統合運用を3ヶ月試した結果**」のような実体験ベース記事が反響取りやすい。"スキル数3つの壁"を切り口にすると刺さりそう。
- **X単発化**: 「CLAUDE.md は"プロジェクトのルールブック"だけじゃない。**スキル間の共有メモリ**でもある。サムネ採点／note執筆／LP生成が同じ世界観で揃うのは、ここが効いてる」
- **観察**: 元の `<editor_selection>` と引数URLが別話題だったため、ユーザーが**別の話題に乗り換えた**と判断した。次回以降、引数URLとエディタ選択が衝突するときは冒頭で「どちらを主題にしますか？」と確認するスキル改修も候補。
