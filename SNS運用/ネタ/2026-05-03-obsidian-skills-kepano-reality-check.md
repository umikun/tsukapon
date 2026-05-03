---
created: 2026-05-03
tags: [調査, obsidian, kepano, agent-skills, claude-code, 批評型, vault運用]
source: "[[Clippings/Post by @obsidianstudio9 on X 1.md]]"
---

# 「Obsidian創業者がVault全体をAIエージェントに変えた」の真相 — 実話と盛りを切り分ける

> **TL;DR**
> kepano（Obsidian CEO・Steph Ango）が 2026年初頭に `obsidian-skills` を公開したのは **事実**。Claude Code / Codex CLI / OpenCode 等の Agent Skills 仕様準拠AIに「Obsidian Markdown / Bases / JSON Canvas / CLI / 外部URL取得」の使い方を教える **5つのSKILL.mdファイル**で、GitHubで12,900+スター獲得。**ただし元ポストは "実話" と "盛り" を混ぜている**: ① obsidian-skills 自体は「**agent に Obsidianの読み書き方法を教えるドキュメント集**」であって "agent system" ではない（実行体は Claude Code / Codex 側）。② 「日次ノート自動生成」「既存ノートの自動リンク付け」「プロジェクト管理の自動化」「Canvasへの自動配置」「CLAUDE.md でAIルール定義」は **obsidian-skills の機能ではない**（CLAUDE.md は Claude Code の標準仕様、自動リンク等はユーザーが自前で書くか別プラグイン）。③ 「Obsidian公式が全力で舵を切っている」は誇張で、kepano は "Obsidian は pure local notes app のままで、agent を扱う公式skillだけ提供" のスタンス。冷静な評価は「**Markdown/Bases/Canvas を扱う agent の操作品質を底上げする良い基礎レイヤー、ただし"OS化" は使う側の設計次第**」。Tsukapon vault は既に5本導入済み（[[_ memory/short-term.md]] 参照）で、実体験から言うと CLAUDE.md トークン削減効果は限定的（+1,170byte 増加した実例あり）、本領は **"スキル責務の明示化"** にあった。

## 📌 元テキスト（抜粋）

> 【速報】「Obsidianの創業者が機能を出したんじゃない。Vault全体をAIエージェントに変えた」と話題に😳
> プラグインでもない。単なるインテグレーションでもない。フルエージェントシステム。
> Claude Code・Codex・OpenCodeがVault内で直接動作する。読み込み・書き込み・推論をVaultの中だけで完結させる。
> ・日次ノートの自動生成 / ・既存ノートの自動リンク付け / ・プロジェクト管理の自動化 / ・Canvasへの自動配置 / ・CLAUDE.mdでAIのルールを定義
> Obsidian公式がこの方向に全力で舶（→舵）を切っている。これは「メモアプリ」の進化ではなく「パーソナルAI OS」の誕生🔥

出典: [[Clippings/Post by @obsidianstudio9 on X 1.md]] / [元ポスト](https://x.com/obsidianstudio9/status/2050753469452317064)（@obsidianstudio9, 2026-05-03）

> ⚠️ **本文に "舶を切る" の誤字あり**（正しくは "舵を切る"）。AI生成ありがちなミス、紹介投稿としての品質に疑問符

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| obsidian-skills | kepano製の公式 Agent Skills 集（5本） | github kepano obsidian-skills |
| kepano (Steph Ango) | Obsidian CEO。2024年にlead/CEOへ | kepano steph ango obsidian ceo |
| Agent Skills 仕様 | Anthropic 提唱のAgent向けスキル定義仕様 | agent skills specification |
| Claude Code | Anthropic CLI/IDE統合エージェント | claude code anthropic |
| Codex CLI | OpenAI のCLIエージェント | codex cli openai |
| OpenCode | OSS のCLIエージェント | opencode cli |
| obsidian-markdown | Wikilinks/callouts/frontmatter/embeds の使い方を教えるskill | obsidian flavored markdown |
| obsidian-bases | Bases (DB的ビュー) の操作を教えるskill | obsidian bases v1.9 |
| json-canvas | JSON Canvas形式の操作を教えるskill | json canvas obsidian |
| obsidian-cli | Obsidian CLI の操作を教えるskill | obsidian cli |
| defuddle | 外部URLからクリーンMarkdown抽出 | defuddle cli |
| CLAUDE.md | Claude Code がプロジェクトルートに置くルールファイル | claude.md claude code |
| SKILL.md | Agent Skills 仕様の定義ファイル形式 | skill.md agent skills |

---

## 🧭 背景 / なぜ今これが話題なのか

**2024年: kepano が Obsidian リードへ昇格**
Erica Xu と Shida Li の Obsidian 創業者2人体制から、CEO/Lead として **Steph Ango (kepano)** が 2024年に表立った代表に。Are.na 元CEO、ローカルファースト設計の論者として元々有名。

**2025年8月: Obsidian v1.9.10 で Bases が正式リリース**
Notion 的な DB ビューを Obsidian 内で実現する Bases が公式機能として提供開始。ローカルMarkdownのまま構造化データ層を持てるようになり、AI連携基盤として大きな転換点に（[Obsidian Roadmap](https://obsidian.md/roadmap/)）。

**2026年初頭: kepano が `obsidian-skills` を公開**
kepano 個人GitHub に Agent Skills 仕様準拠の **5つのSKILL.mdファイル** を公開。**主要生産性ツール創業者が初めて公式に Agent Skills を出した** 事例として注目（[Obsidian's CEO Just Taught AI How to Use His Own App](https://medium.com/@hamzakhaledlklk/obsidians-ceo-just-taught-ai-how-to-use-his-own-app-here-s-the-0-way-to-do-it-too-97acbe8cfefe)）。

**2026年Q1〜Q2: コミュニティで派生・解説・"OS化" 言説が拡散**
12,900+ スター獲得、Medium / Substack 各所で "Obsidian + Claude Code は AI second brain の最適解" 系記事が量産。**"パーソナルAI OS"** という呼び方は @obsidianstudio9 のような紹介系インフルエンサー由来で、kepano 本人や Obsidian 公式は使っていない。

**今回の元ポスト（2026-05-03 @obsidianstudio9）の文脈**
@obsidianstudio9 はObsidian周辺コンテンツに特化したインフルエンサー的アカウント。"【速報】" "🔥" "誕生" の煽りトーン + 本文の "舶を切る" 誤字。事実ベースは正しいが、**obsidian-skills が提供しないもの（自動リンク/自動Canvas配置/プロジェクト自動化）を機能リストに混ぜている**点で誤認を誘発。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Obsidianの創業者が機能を出した」 | kepano (Steph Ango) は **CEO/lead**。創業者は Erica Xu と Shida Li。"創業者" 表現は厳密には不正確 | [kepano GitHub](https://github.com/kepano) / [Obsidian roadmap](https://obsidian.md/roadmap/) | ⚠️ ほぼ一致（"創業者" は誤り、CEOが正解） |
| 「Vault全体をAIエージェントに変えた」 | obsidian-skills は **agent に Obsidianの操作方法を教えるSKILL.mdファイル集**。実行体は外部の Claude Code / Codex / OpenCode 側で、Vault自体がagentになるわけではない | [GitHub: kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | ❌ 要注意（誇張） |
| 「プラグインでもない、単なるインテグレーションでもない、フルエージェントシステム」 | 実体は **MIT ライセンスの SKILL.md 5本**（ドキュメント集）。"フルエージェントシステム" は強い言いすぎ | [DeepWiki: kepano/obsidian-skills](https://deepwiki.com/kepano/obsidian-skills) | ❌ 要注意（過大表現） |
| 「Claude Code・Codex・OpenCodeがVault内で直接動作する」 | 各CLIエージェントが vault パスを作業ディレクトリにして動作するのは事実。ただし "vault内で完結" ではなく、エージェント本体は OS のプロセスとして動く | [obsidian-skills README](https://github.com/kepano/obsidian-skills) | ⚠️ ほぼ一致（言葉の問題） |
| 「日次ノートの自動生成」 | obsidian-skills には**含まれていない**。Daily Notes は Obsidian標準機能 + 個別スキル/プラグイン（自分で書くか Templater 等）で実現 | [obsidian-skills README](https://github.com/kepano/obsidian-skills) | ❌ 要注意（obsidian-skillsの機能ではない） |
| 「既存ノートの自動リンク付け」 | obsidian-skills には**含まれていない**。Smart Connections や Note Linker 等の **別プラグイン** の機能 | [Note Linker](https://www.obsidianstats.com/plugins/obisidian-note-linker) | ❌ 要注意（別物） |
| 「プロジェクト管理の自動化」 | obsidian-skills には**含まれていない**。これはユーザーが Bases + 自作スキルで組むもの | [obsidian-skills README](https://github.com/kepano/obsidian-skills) | ❌ 要注意（別物） |
| 「Canvasへの自動配置」 | obsidian-skills の `json-canvas` は **JSON Canvas 形式の読み書き方法を教える** だけで、自動配置ロジックは含まない。"自動配置" を実現するには別途実装が必要 | [obsidian-skills README](https://github.com/kepano/obsidian-skills) | ❌ 要注意（"自動配置" は機能ではない） |
| 「CLAUDE.mdでAIのルールを定義」 | CLAUDE.md は **Claude Code の標準仕様**で、obsidian-skills とは別物。誰でも書ける（Tsukapon vault の [[CLAUDE.md]] 参照） | [Claude Code Docs](https://code.claude.com/docs/en/) | ❌ 要注意（obsidian-skills と無関係） |
| 「Obsidian公式が全力で舵を切っている」 | kepano は obsidian-skills を **個人GitHub** で公開。Obsidian本体は依然 pure local notes app のままで、AI機能を本体に組み込む方針は明示されていない | [Obsidian Roadmap](https://obsidian.md/roadmap/) | ⚠️ ほぼ一致（"全力で" は強すぎ） |
| 「パーソナルAI OS の誕生」 | これは紹介系インフルエンサーの煽り表現。kepano 本人や Obsidian 公式は使っていない。OS化は **使う側の設計次第** | （複合判断） | ⚠️ ほぼ一致（誇張表現） |

---

## 🌐 最新動向（2026-05-03時点）

- **obsidian-skills は12,900+スター獲得、Agent Skills 仕様の代表例に**: 主要生産性ツール創業者/CEOが Agent Skills を公式提供した最初の事例として継続的に注目 — [Claude Skills Hub: Steph Ango's Official Agent Integration](https://claudeskills.info/blog/obsidian-claude-skills-guide/), 2026
- **派生プロジェクトが急増**: `breferrari/obsidian-mind`（vault に持続記憶を持たせる）、`Ar9av/obsidian-wiki`（Karpathy LLM Wiki パターン実装）、`Boboegg/obsidian-skills`（kepano のフォーク）など派生・拡張プロジェクトが相次ぎ登場 — [obsidian-mind GitHub](https://github.com/breferrari/obsidian-mind), 2026
- **Obsidian Skills Review 2026**: 独立評価記事多数。"AI agent が Obsidian vault をプロのように扱える基盤" として高評価、ただし **"agentic 機能そのものは外部CLI次第"** との指摘 — [Vibecoding: Obsidian Skills Review](https://vibecoding.app/blog/obsidian-skills-review), 2026
- **Codex CLI / OpenCode / Gemini CLI 等の対応拡大**: Anthropic だけでなく OpenAI の Codex CLI、Gemini CLI、OpenCode（OSS）でも obsidian-skills が動作する点が "オープン仕様の勝利" として強調されている — [obsidian-skills README](https://github.com/kepano/obsidian-skills), 2026
- **CEO 個人 GitHub での公開＝Obsidian本体への AI機能組み込みは見送り**: kepano は本体は local-first・privacy-first を維持し、AI連携は "外部エージェント + 公式skill提供" のハイブリッド戦略を選択 — [Obsidian Roadmap](https://obsidian.md/roadmap/), 2026

---

## 🧩 関連概念・隣接分野

- **Agent Skills 仕様 (Anthropic)**: SKILL.md 形式で agent に特定領域の操作方法を教える標準仕様。obsidian-skills はこの仕様の参照実装の1つ
- **Karpathy LLM Wiki パターン**: AgriciDaniel/claude-obsidian など別系統の "vault を AI に維持させる" アプローチ。obsidian-skills は **基礎レイヤー**、Karpathy 系は **上位アプリ層**
- **Obsidian Bases (v1.9.10+)**: 構造化データ層。obsidian-bases skill が読み書き方法を教える
- **JSON Canvas 仕様**: Obsidian 由来のオープン規格。json-canvas skill が操作を教える
- **CLAUDE.md / AGENTS.md**: Claude Code / Codex の各標準ルールファイル。obsidian-skills と組み合わせて使うのが王道

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（=元ポストの立場）**:
  - kepano（CEO）が Agent Skills を公式提供した意義は確かに大きい
  - Markdown / Bases / Canvas / CLI / Web取得の5領域カバーは vault 操作の基礎を網羅
  - 12,900+スターの実績、派生プロジェクトの急増がコミュニティ評価を裏付け
  - Codex / OpenCode / Gemini CLI 含む横断対応で、ベンダーロックインがない

- **否定 / 慎重派の主張**:
  - **"フルエージェントシステム" は誇張**: 実体は SKILL.md 5本のドキュメント集。実行体は外部CLIで、obsidian-skills 単体では何も "実行" しない
  - **元ポストが列挙する5つの機能（日次ノート自動生成・自動リンク・プロジェクト自動化・Canvas自動配置・CLAUDE.md）はすべて obsidian-skills の機能ではない**: 別プラグイン、別仕様、ユーザー自作の組合せ。読者が「obsidian-skills 入れればこれ全部できる」と誤解するレベルのミスリード
  - **"創業者" の誤記**: 厳密には kepano は CEO/lead で、創業者は Erica Xu と Shida Li
  - **"Obsidian公式が全力で舵を切る" は実態と乖離**: kepano は CEO 個人 GitHub での公開。本体は local-first・privacy-first を維持で、AI機能本体組み込みは見送り
  - **CLAUDE.md スリム化効果は実プロジェクトで確認されない**: Tsukapon vault の実例では234行/11,764byte → 253行/12,934byte（**+19行/+1,170byte**）と逆に増加。sutero記事の "半分以下削減" は Obsidian記法説明が大量にあるCLAUDE.md向けで、行動ルール100%構成のCLAUDE.mdには不適用。obsidian-skills の本領は "**スキル責務の明示化**" にある
  - **"舶を切る" 誤字**: AI生成系投稿でよく出る typo。紹介投稿としての品質と手間の薄さを示唆

- **中立的に見るときの補助線**:
  - **obsidian-skills は "agent の Obsidian リテラシーを底上げする基礎レイヤー" として優秀**。これは事実
  - **"OS化" を実現するのは使う側の設計**: kepano が出したのは部品であり、組み立てはユーザー責任
  - **本気で vault × agent を運用するなら**: obsidian-skills（基礎） + CLAUDE.md（ルール） + 自作スキル群 + 多階層メモリ（短期/中期/長期）+ 自己改善ループ。Tsukapon vault がまさにこの構成
  - **過剰な期待値で導入すると失望する**: "全部自動でやってくれる" 系の幻想を持つと、SKILL.md 開いて「あれ？ドキュメントだけ？」となる

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] kepano 本人が Obsidian 本体への AI 機能組み込みについて公開発信したコメント（2026年）の有無
- [ ] obsidian-skills の派生プロジェクト（breferrari/obsidian-mind, Ar9av/obsidian-wiki, Boboegg/obsidian-skills など）の **実機能比較表**
- [ ] Codex CLI / Gemini CLI / OpenCode で obsidian-skills を使った時の **挙動差**（Claude Code 以外の実例レポートが少ない）
- [ ] CLAUDE.md スリム化の "成功事例" と "失敗事例" の分布（sutero型 vs Tsukapon型 のどちらが多数派か）
- [ ] Obsidian 公式が今後 AI 機能を本体組み込みする可能性はあるか（roadmap 観察）

---

## 📚 参考資料

- [GitHub: kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — 公式リポジトリ。SKILL.md 5本の本体, 取得日 2026-05-03
- [obsidian-skills README](https://github.com/kepano/obsidian-skills/blob/main/README.md) — 提供スキル・インストール方法・対応CLIの一次情報, 取得日 2026-05-03
- [DeepWiki: kepano/obsidian-skills](https://deepwiki.com/kepano/obsidian-skills) — 内部構造の解説, 取得日 2026-05-03
- [Claude Skills Hub: Steph Ango's Official Agent Integration](https://claudeskills.info/blog/obsidian-claude-skills-guide/) — kepanoが公式提供した意義の解説, 取得日 2026-05-03
- [Obsidian's CEO Just Taught AI How to Use His Own App (Medium)](https://medium.com/@hamzakhaledlklk/obsidians-ceo-just-taught-ai-how-to-use-his-own-app-here-s-the-0-way-to-do-it-too-97acbe8cfefe) — 第三者解説, 取得日 2026-05-03
- [Obsidian Skills Review 2026 (Vibecoding)](https://vibecoding.app/blog/obsidian-skills-review) — 独立評価, 取得日 2026-05-03
- [Obsidian's Official Skills Are Here! (Kurtis Redux)](https://kurtis-redux.medium.com/obsidians-official-skills-are-here-it-s-time-to-let-ai-plug-into-your-local-vault-6c149aae84f6) — 個人開発者の導入レポート, 取得日 2026-05-03
- [How to Connect Obsidian to Claude Code + Build a Memory System (2026)](https://pixelnthings.com/connect-obsidian-to-claude-code/) — 実装ガイド, 取得日 2026-05-03
- [Turning Obsidian into an AI-Native Knowledge System (Mart Kempenaar)](https://medium.com/@martk/turning-obsidian-into-an-ai-native-knowledge-system-with-claude-code-27cb224404cf) — Claude Code との組合せレポート, 取得日 2026-05-03
- [GitHub: breferrari/obsidian-mind](https://github.com/breferrari/obsidian-mind) — vault に持続記憶を持たせる派生, 取得日 2026-05-03
- [Obsidian Roadmap 公式](https://obsidian.md/roadmap/) — 本体ロードマップで AI機能組み込み予定がない確認元, 取得日 2026-05-03
- [Note Linker (Obsidian Stats)](https://www.obsidianstats.com/plugins/obisidian-note-linker) — "自動リンク" 機能は別プラグイン由来である根拠, 取得日 2026-05-03

---

## 🗒 メモ

- **Tsukapon vault は当事者ポジション**: 2026-04-28 に obsidian-skills 5本導入済み（[[_ memory/short-term.md]] 参照）。**実体験ベースで批評型ロング解説が書ける唯一無二の素材**。"煽り紹介者と違って自分はもう1週間使ってる" 角度が信頼性として強い
- **CLAUDE.md スリム化の実例データは強い**: 234行/11,764byte → 253行/12,934byte（**+19行/+1,170byte**）の逆増実例は、sutero記事の "半分以下" 主張への有効な反論データ。**"何が削減され、何が削減されないか" の切り分け** ができる
- **W18戦略 B項+E項のど真ん中ネタ**: [[SNS運用/analytics/W18戦略メモ.md]] の批評型原ポスト＋"煽りに対するツッコミ" フレーム素材。「"フルエージェントシステム" の正体は SKILL.md 5本ですが」のテンプレが綺麗に決まる
- **批評型ロング解説の本命候補**: [[SNS運用/note/_メンバーシップ準備ロードマップ.md]] のネタプール枠 "批評型ロング" に登録。切り口候補:
  - 「obsidian-skills 1週間使った正直レビュー — 紹介投稿が嘘ついてる5箇所」
  - 「"Vault全体がAIエージェント" の正体 — kepano が出したのは "部品" であって "システム" ではない」
  - 「CLAUDE.md スリム化が効くvault・効かないvaultの違い（実測+1,170byte事例から）」
- **連投シリーズへの転用**: 既存の [[SNS運用/post/draft/20260427_critique_series_04_obsidian-second-brain.md]] と完全に同系統のテーマ（"完全なコース" の実態解剖）。続編・上位互換として再利用可能
- **当日の他調査ノートとの連動**: 本日 [[2026-05-03-claude-obsidian-knowledge-engine.md]] でも "Obsidian + Claude Code 系の煽りインフルエンサー乱立" を指摘済み。**4本連続で "煽り解剖" シリーズ** が組めるレベルでネタが揃ってきた
- **ルーチンB対象**: @obsidianstudio9 は "【速報】" "😳" "🔥" "誕生" を多用する典型的バズ狙いインフルエンサー + 本文に誤字あり = 信頼度低めの観察対象として登録価値あり
- **誘導動線**: 解説note（無料・実体験ベース批評）→ メンバーシップ「実装ツール紹介」枠（"Tsukapon vault 流 obsidian-skills 活用設計" 実務手順）の二段構成が自然
