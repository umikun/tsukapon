---
created: 2026-05-06
tags:
  - 調査
  - Obsidian
  - PARA
  - Dataview
  - Bases
  - デイリーノート
source: https://x.com/obsidianstudio9/status/2051833087852687741
action: 取り込み検討
---

# Obsidian Vault整理「5ステップで一発で整う」を裏取りしてみる

> **🔗 関連コンテンツ**
> - 🐦 同投稿者の別ツイート（AIエージェント vault化）: [[Clippings/Post by @obsidianstudio9 on X.md]]
> - 🐦 同投稿者の別ツイート（Obsidian創業者AI路線）: [[Clippings/Post by @obsidianstudio9 on X 1.md]]
> - 🧠 Obsidian × Claude Code 全体マップ: [[Claudian-obsidian-skills活用マップ.md]]
> - 📝 関連ネタ: [[SNS運用/ネタ/2026-04-26-obsidian-claude-code-second-brain.md]]

> **TL;DR**
> 「PARA + テンプレ + デイリーノート + Dataview + 週1レビュー」という5本柱の組み合わせ自体は2026年5月時点でも王道で、**枠組みとしては正しい**。ただし**Dataviewは公式に「もう更新しない」状態でBases / Datacoreへの移行期**であること、**週1レビュー5分は実態より短すぎ**（PKM界隈の標準は20-30分）の2点はツイート時点で要アップデート。Templater + デイリーノート起点の運用は引き続きベストプラクティス。

## 📌 元テキスト（抜粋）

> Obsidian Vaultが散らかってる人、この順番でやれば一発で整う。
> PARA法でフォルダを4つだけ作る。
> テンプレートを設定して入力コストをゼロにする。
> デイリーノートを起点に全ての情報をつなぐ。
> Dataviewプラグインで自動集計する。
> 週1で5分レビューする習慣だけ作れば、Vaultは勝手に育つ👇

出典: [Post by @obsidianstudio9 on X (2026-05-06)](https://x.com/obsidianstudio9/status/2051833087852687741)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **PARA法** | Tiago Forteが提唱した「Projects / Areas / Resources / Archives」の4区分整理術 | `PARA method Tiago Forte` |
| **Projects（P）** | 期限・ゴールがある一時的タスク群 | `PARA project definition` |
| **Areas（A）** | 期限のない継続的責任領域（健康・仕事ロール等） | `PARA areas vs projects` |
| **Resources（R）** | 興味・参照用ストック | `PARA resources` |
| **Archives（X）** | 完了or不活性化したもの | `PARA archive workflow` |
| **デイリーノート** | 日付ファイルを1日1枚作って情報のハブにする運用 | `Obsidian daily notes hub` |
| **Templater** | 動的変数・JSが書けるテンプレートプラグイン | `Templater Obsidian SilentVoid13` |
| **Dataview** | Markdown/YAMLを擬似DBとして集計表示するクエリプラグイン | `Dataview blacksmithgu` |
| **Bases** | Obsidian 1.9.0(2025-05-21)で追加されたコア機能。`.base`ファイルでDB的ビュー | `Obsidian Bases plugin` |
| **Datacore** | Dataviewの後継として作者本人(blacksmithgu)が開発中の新クエリ基盤 | `Datacore Obsidian successor` |
| **週次レビュー** | 1週間分のデイリーノートを処理して恒久ノートに昇格させる作業 | `weekly review zettelkasten` |

---

## 🧭 背景 / なぜ今これが話題なのか

**PARA法の出自（2017年〜）。** Tiago Forteが運営する有料プログラム「Building a Second Brain（BASB）」の中心メソッドとして2017年頃から広まり、2022年に書籍 *The PARA Method* で総まとめされた。「Projects / Areas / Resources / Archives」の4区分は **「actionability（行動可能性）順」**で並べるのがミソで、トピック分類（Notion的タグ）と一線を画す思想。Obsidian界隈では2021〜2022年頃に [PARA Starter Kit](https://forum.obsidian.md/t/para-starter-kit/223) が公式フォーラムで人気となり、定番テンプレートとして定着した。

**Dataviewの全盛期と転機。** Dataviewは2021年1月リリース、累計300万DL超のObsidian最人気級プラグイン。「インラインクエリでメモをDBに変える」発想が刺さり、PARA × Dataviewの「自動化されたSecond Brain」がコミュニティのスタンダードになった。だが2025年5月21日、**Obsidian 1.9.0で「Bases」というコア機能（プラグイン同梱）が登場**し、流れが変わる。

**Bases時代の到来（2025-05〜）。** Basesは `.base` ファイルにYAML設定でテーブル/カードビューを書く方式で、**Dataviewのクエリより高速**（5万ノートでもほぼ即時表示）かつ **GUIでフィルタ・並び替えが組める**。同時期にDataview作者は更新停止を宣言、後継 **Datacore** を新規開発中というアナウンス。2026年に入ると主要なObsidianブログ（[medium.com / Len](https://medium.com/@lennart.dde/obsidian-dataview-is-dead-long-live-bases-9750e8a92877)、[Practical PKM](https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/) ほか）が一斉に「Dataviewは死んだ、Basesに移行せよ」記事を出す。

**「Vault整理」コンテンツの市場性。** 2024〜2026年にかけてObsidianのMAU増加 + AIエージェント連携（Claude Code, MCP）で **「PKM初心者の流入」** が増えた結果、「散らかったvaultを整える系」の入門ノウハウは引き続きX/note/Mediumで強い需要がある。今回のツイート（2026-05-06）はまさにその入門レイヤーを5ステップで畳んだ典型コンテンツ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| **「PARA法でフォルダを4つだけ作る」** | Projects / Areas / Resources / Archivesの4区分は本家定義どおり。「actionability順」で並べる思想含めて正確 | [The PARA Method (Tiago Forte)](https://www.buildingasecondbrain.com/para) | ✅ 一致 |
| **「テンプレートを設定して入力コストをゼロにする」** | Templaterは2026年も essential plugin。動的変数・日付・JS活用で「ゼロ」は誇張だが**入力コスト削減効果は実証済み** | [The Best Obsidian Plugins for 2026 - Sébastien Dubois](https://www.dsebastien.net/the-must-have-obsidian-plugins-for-2026/) | ⚠️ ほぼ一致（"ゼロ"はレトリック） |
| **「デイリーノートを起点に全ての情報をつなぐ」** | 「デイリーノートを central inbox / daily dashboard にする」運用は2026年標準ベストプラクティス | [Obsidian Daily Notes Workflow](https://aiproductivity.ai/guides/obsidian-daily-notes-workflow/) | ✅ 一致 |
| **「Dataviewプラグインで自動集計する」** | Dataviewは**no longer being actively developed**（2025〜）。後継Datacore開発中、コア機能Basesが推奨経路 | [Obsidian Dataview Is Dead. Long Live Bases.](https://medium.com/@lennart.dde/obsidian-dataview-is-dead-long-live-bases-9750e8a92877) / [Migrate to Bases](https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/) | ❌ 要注意（2026年は **Bases or Datacore** が正解） |
| **「週1で5分レビューする習慣」** | PKM界隈の標準は **15〜30分**。3-pass方式（10+15+5分）が主流で「5分」はその最終passのみ | [Setting Up a Weekly Review in Obsidian](https://goodsidekick.com/productivity/weekly-review-obsidian/) / [Daily Notes Workflow](https://aiproductivity.ai/guides/obsidian-daily-notes-workflow/) | ❌ 要注意（5分は短すぎ） |
| **Obsidian Bases リリース時期** | Obsidian 1.9.0 early access が **2025-05-21** にリリース、Basesはその目玉機能 | [Obsidian 1.9.0 Desktop changelog](https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0/) | ✅ 一致（参考事実） |

---

## 🌐 最新動向（2026-05-06時点）

- **Dataviewは"非アクティブ"宣言、Datacoreが次世代候補に** — Dataview作者blacksmithguが更新停止を表明し、後継のDatacoreを開発中。Bases登場で需要の半分は奪われた構図 — [Obsidian Dataview Is Dead. Long Live Bases.](https://medium.com/@lennart.dde/obsidian-dataview-is-dead-long-live-bases-9750e8a92877), 2026-04
- **Basesが事実上の標準クエリ機能に** — `.base`ファイル方式で5万ノートでも即時レンダリング、GUIフィルタ対応。1.9.x系で機能追加が継続中 — [Bases Plugin Overview (Practical PKM)](https://practicalpkm.com/bases-plugin-overview/), 2025-06〜2026
- **PARA × AIエージェント融合の流れ** — Claude CodeをObsidian vaultに繋ぎ、PARAの4フォルダにLLMが自動振り分けする運用例が登場（@obsidianstudio9自身が別ツイートで言及した「Vault全体をAIエージェント化」も同潮流） — [PARA × Claude Code productivity OS](https://aimaker.substack.com/p/para-method-tiago-forte-claude-code-obsidian-ai-productivity-os), 2026-04
- **Templaterは引き続き5つ星評価で必須プラグイン** — 2026-03時点でレビュー★5、initial setup後にデイリーノート爆速化が定番 — [Templater on Obsidian Stats](https://www.obsidianstats.com/plugins/templater-obsidian), 2026-03
- **週次レビューの3-pass化（10+15+5分）が主流** — 「Scan & Flag」「Permanent化」「翌週プラン」の3段階で計30分が現代PKMの標準 — [Setting Up a Weekly Review in Obsidian](https://goodsidekick.com/productivity/weekly-review-obsidian/), 2026
- **PARAは"空フォルダ事故"対策ルールが追加** — Tiago Forte本人が現場フィードバックを受け「中身が無いうちはフォルダ/タグを作るな」を運用ルールに追記 — [PARA Method Review (Medium / Carole)](https://medium.com/design-bootcamp/para-method-review-does-everyone-really-love-the-organizing-method-c7d1b1bb5ed7), 2025

---

## 🧩 関連概念・隣接分野

- **Building a Second Brain (BASB)**: PARA法の親元メソドロジ。CODE（Capture / Organize / Distill / Express）の4工程を回す思想で、PARAは「Organize」フェーズの実装。
- **Zettelkasten（ツェッテルカステン）**: 永続ノート同士をリンクで繋ぐドイツ発の手法。デイリーノートをfleeting notes起点としてZettelkastenに流す運用がObsidianの主流レイヤー2。
- **MOC（Map of Content）**: フォルダ階層ではなくindexノート＋wikilinkで知識を組織する手法。kepano（Obsidian CEO）はPARAより**MOC + flat folders**派で有名。
- **Datacore**: Dataviewの後継。リアクティブクエリ・パフォーマンス改善が目玉だが2026-05時点でβ未到達。Basesと棲み分けるかは未定。
- **Properties (Obsidian core)**: YAML frontmatterのGUI編集機能。Bases/Dataviewの両方とも「propertyに書かれた値」を読みに行くので、整理術の地盤として最重要。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: PARAは「actionability軸」で迷いを減らし、4フォルダだけというミニマルさが新規ユーザーに突破口を与える。デイリーノート + Dataview/Bases の組み合わせは2026年でも実証済みのフォーマット。
- **否定 / 慎重派の主張**:
  - **MOC派（kepano本人含む）**: フォルダ階層より「リンク + properties」のほうがObsidianの設計思想に合う。PARAの4フォルダ強制はWiki的ネットワークを切り刻む。([Kepano vault分解 / PARAZETTEL](https://parazettel.com/articles/what-i-learned-after-kepano-vault/))
  - **「PARAは過剰設計」派**: 仕事のロールが変わるたびにAreas/Projects境界を悩むのは生産性のロス。プロジェクト数が少ない人は単一インボックス方式で十分。([Confession! I Gave Up The PARA Method](https://www.fractalproductivity.club/p/confession-i-gave-up-the-para-method))
  - **「5分レビュー」派への反論**: 5分で終えられるのは「カレンダーの確認」レベル。永続ノートへの昇格を含めるなら最低15分は必要というのが [bagerbach.com](https://bagerbach.com/blog/weekly-review-obsidian/) や [Theo James](https://medium.com/@theo-james/weekly-reviews-in-your-second-brain-how-i-do-it-in-obsidian-65af0f6dd5f1) の共通見解。
- **中立的に見るときの補助線**:
  - 「最初の一歩」としてはPARA + デイリーノート + テンプレ + 何らかの集計（DataviewでもBasesでも）+ 週次レビューは**正解**。
  - ただし**現役で動かす**なら「Dataview→Bases」「5分→20-30分」の2点は2026-05時点の現実に合わせてアップデート推奨。
  - 「フォルダで整理しない」kepano流は中級者以上向け。初心者にはPARAが依然として近道。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Bases × PARAの実装ベストプラクティス（projects baseとareas baseを分けるか統合するか）
- [ ] Datacoreの正式リリース時期と、Basesとの棲み分けが今後どう決着するか
- [ ] Claude Code等のAIエージェントが「PARAへ自動振り分け」を実用レベルでこなせるか（精度のベンチマーク）
- [ ] 個人のPARAフォルダ運用が**3ヶ月後/1年後**にどう変質するかの縦断研究
- [ ] kepano流（flat + MOC）vs PARA派の収束/発散の方向感

---

## 📚 参考資料

- [The PARA Method (Tiago Forte)](https://www.buildingasecondbrain.com/para) — PARA本家定義の確認, 取得日 2026-05-06
- [PARA Starter Kit (Obsidian Forum)](https://forum.obsidian.md/t/para-starter-kit/223) — Obsidian界隈におけるPARA定着の発火点, 取得日 2026-05-06
- [Obsidian 1.9.0 changelog (公式)](https://obsidian.md/changelog/2025-05-21-desktop-v1.9.0/) — Bases登場日(2025-05-21)の一次ソース, 取得日 2026-05-06
- [Obsidian Dataview Is Dead. Long Live Bases. (Medium / Len)](https://medium.com/@lennart.dde/obsidian-dataview-is-dead-long-live-bases-9750e8a92877) — Dataview非アクティブ宣言の裏取り, 取得日 2026-05-06
- [Migrate to Obsidian Bases from Dataview (Practical PKM)](https://practicalpkm.com/moving-to-obsidian-bases-from-dataview/) — 移行手順とBasesの優位性, 取得日 2026-05-06
- [Bases Plugin Overview (Practical PKM)](https://practicalpkm.com/bases-plugin-overview/) — Basesの機能一覧, 取得日 2026-05-06
- [Obsidian Daily Notes Workflow (AI Productivity)](https://aiproductivity.ai/guides/obsidian-daily-notes-workflow/) — デイリーノート起点運用の標準形, 取得日 2026-05-06
- [Setting Up a Weekly Review in Obsidian (Good Sidekick)](https://goodsidekick.com/productivity/weekly-review-obsidian/) — 週次レビュー所要時間（30分標準）, 取得日 2026-05-06
- [How I conduct weekly reviews with Obsidian (Christian B. B. Houmann)](https://bagerbach.com/blog/weekly-review-obsidian/) — レビュー実践記, 取得日 2026-05-06
- [Templater Obsidian Stats](https://www.obsidianstats.com/plugins/templater-obsidian) — 2026-03時点で★5評価, 取得日 2026-05-06
- [PARA Method Review (Medium / Carole)](https://medium.com/design-bootcamp/para-method-review-does-everyone-really-love-the-organizing-method-c7d1b1bb5ed7) — 「空フォルダ問題」とPARA批判, 取得日 2026-05-06
- [Confession! I Gave Up The PARA Method (Fractal Productivity)](https://www.fractalproductivity.club/p/confession-i-gave-up-the-para-method) — PARA離脱事例, 取得日 2026-05-06
- [What I Learned After Kepano Vault (PARAZETTEL)](https://parazettel.com/articles/what-i-learned-after-kepano-vault/) — kepano流とPARAの対比, 取得日 2026-05-06
- [PARA Method × Claude Code (AI Maker Substack)](https://aimaker.substack.com/p/para-method-tiago-forte-claude-code-obsidian-ai-productivity-os) — PARAをAIで自動化する2026系の事例, 取得日 2026-05-06

---

## 🗒 メモ

- このツイートは**情報量はあるが2点(Dataview / 5分レビュー)で2026-05時点の最適解からズレている**。同じテーマでXに自分の投稿を出すなら「Bases時代の5ステップ」にアップデートすると差別化できる。
- 同投稿者(@obsidianstudio9)は[[Clippings/Post by @obsidianstudio9 on X.md|別の投稿でAIエージェント連携]]も発信しており、PARA × AIエージェントへの架け橋を狙う流れと一貫性がある。スレッド化して「**整理→自動化→AIエージェント**」の3層で書ききると `note → X` 流用が効きそう。
- 「**5分レビュー**」を信じてしまった初心者を想像すると、3〜4週でvaultが詰まるはず。日報/週報スキル（[[. claude/commands/daily-summary.md|/daily-summary]] や週次分析）と組ませると正しい所要時間（合計20〜30分）に近づけられる。
- 自分のvault運用に直接活かすなら: ①既存Dataviewクエリの **Bases移行棚卸し**、② `_ memory/short-term.md` 周りの週次レビューに「3-pass方式」を取り込む、の2本がToDo候補。
