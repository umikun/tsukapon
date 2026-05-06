---
created: 2026-05-06
tags:
  - 調査
  - Obsidian
  - プラグイン
  - ファイルエクスプローラ
  - vault運用
  - ワークフロー
source: https://x.com/eryidebiji/status/2051647798223991023
action: 運用参考
---

# 二一的笔记氏が「Obsidianユーザー全員すぐ入れろ」と推す Notebook Navigator プラグインを解剖する

> [!summary] TL;DR
> - Chinese Obsidian クリエイター 二一的笔记（@eryidebiji、5.4K フォロワー）が **Notebook Navigator + 双窗格モード** を「30分使って欠点ゼロ、Obsidian の使い方が変わる」と熱烈推奨
> - 開発元は **Johan Sanneblad（Apple / Google / Microsoft 等で innovation 経験を持つ PhD）**。標準ファイルエクスプローラを **2ペイン UI（フォルダ木 + ファイルリスト + プレビュー）**に置換。10万ノート対応・モバイル最適化・キーボード優先設計
> - Tsukapon vault（71 フォルダ階層・iCloud sync・SNS運用 / _ kiwami / _ memory 等の縦割り）と相性は良いが、**File Tree Alternative や Quick Switcher++ 等の既存プラグインとは競合**。muscle memory コストとのトレードオフが本当の判断軸

---

## 📌 元テキスト（抜粋）

> 所有使用 Obsidian 的人
> 请立刻安装 Notebook Navigator 插件
>
> 并在「插件设置 - 桌面外观」中
> 开启「双窗格模式」
>
> 真的无敌了
> 试用了半小时找不到任何槽点
> 也许会完全改变你的 Obsidian 使用习惯
> 可以替代一大批零散小插件
> 并且非常的克制且有品味
> 这个真的很重要
>
> 相信我
> 你会在 5 分钟内感受到这个插件的美好
> 我真的很少有这样的评价

出典: [二一的笔记 @eryidebiji](https://x.com/eryidebiji/status/2051647798223991023) — 2026-05-05 21:58 JST、1,036 likes / 125 RT / 34 reply、メディアなし

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Notebook Navigator** | Obsidian の標準ファイルエクスプローラを 2ペイン UI に置換するコミュニティプラグイン | "obsidian notebook navigator" |
| **双窗格モード（Dual-pane mode）** | プラグイン設定 → Desktop Appearance で有効化。フォルダ木と ファイルリストを左右に並べる Bear/Apple Notes 風 UI | "dual-pane" obsidian plugin |
| **Johan Sanneblad** | プラグイン開発者。PhD、Apple/Google/Microsoft/EA/Lego/Volvo 等で innovation 開発経験 | Johan Sanneblad innovation |
| **virtualized rendering + IndexedDB cache** | 大規模 vault（10万ノート超）でも軽快に動かすための実装技法。可視範囲だけ DOM 描画＋永続キャッシュ | obsidian plugin performance large vault |
| **Featured Image plugin 連携** | サムネイル自動生成のための連携プラグイン。Notebook Navigator のプレビュー UI と組み合わせる | "Featured Image" obsidian |
| **二一的笔记 / eryinote** | Chinese 圏の Obsidian / Notion チュートリアルクリエイター。YouTube + Telegram コミュ + 有料 Notion コース | 二一的笔记 obsidian |

---

## 🧭 背景 / なぜ今これが話題なのか

**1. Obsidian 標準ファイルエクスプローラへの慢性的な不満**
標準のサイドバーは **フォルダ階層をクリックで開閉する 1 ペイン**。フォルダを開くたびにスクロール位置が動き、深い階層では迷子になる。Bear / Notion / Craft / Apple Notes 等の **2ペイン UI（左:フォルダ → 右:ファイルリスト）** に慣れたユーザーには物足りない、というのが背景にある長年の不満。

**2. Notebook Navigator は "対案" として 2025 年に登場、急速に評価を集めている**
2025 年中頃に Obsidian Forum で公式公開（[Obsidian Forum 紹介](https://forum.obsidian.md/t/notebook-navigator-is-now-available-meet-your-new-obsidian-interface/105704)）、その後コミュニティプラグイン公式登録（[GitHub PR #6886](https://github.com/obsidianmd/obsidian-releases/pull/6886)）。**Bear や Apple Notes のような 2ペイン UI を Obsidian に持ち込む** という明確な設計思想で、Joplin・Heptabase 等の隣接ツールユーザーからの流入も呼んでいる。

**3. 開発者が "本物" のソフトウェア設計者**
Johan Sanneblad 氏は **PhD in Software Development**、Apple / Google / Microsoft / EA / Lego / Volvo Cars / Yamaha 等で innovation 開発に従事した経歴（[公式サイト](https://notebooknavigator.com/)）。趣味プラグインではなく、UX 設計の実務知見が乗ったプロダクト。**Obsidian ストアでもメンテナンス頻度・品質指標で上位**（[Obsidian Stats](https://www.obsidianstats.com/plugins/notebook-navigator)）。

**4. パフォーマンスへの本気度**
**virtualized rendering + IndexedDB caching** で 10 万ノート規模の vault でも軽快に動作するよう設計（[GitHub README](https://github.com/johansan/notebook-navigator)）。**v2.6.3 で CodeQL セキュリティスキャン + OpenSSF Scorecard を導入**、ESLint も Obsidian 公式準拠で warning 1 つで失敗するよう CI 構成。**プラグインとしては異例の品質保証**。

**5. 二一的笔记氏の推薦は "ベンチマーク済みの目" によるもの**
著者は中国語圏の Obsidian / Notion チュートリアルクリエイター（YouTube `@eryinote`、Telegram コミュニティ運営、有料 Notion コース提供）。プラグインを比較・批評する**目利き的ポジション**で、「自分はこういう絶賛をめったに出さない」という自己認識がある人物の推薦は重みがある。

**6. タイミング: GW 連休 = vault 運用見直し需要**
2026 GW（4/29〜5/6）終盤の **5/5 21:58 JST** 投稿。連休中に「vault を整理しよう」と腰を据える Obsidian ユーザーは多く、タイミング設計としても正解。1,036 likes / 125 RT は中華圏 Obsidian クラスタのフォロワー 5.4K に対して**高エンゲージ率**。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Obsidian ユーザー全員に勧める価値がある | 標準ファイルエクスプローラは長年の不満点。2ペイン UI への置換は確かに大きな改善。ただし全員必須かは workflow による | [GitHub README](https://github.com/johansan/notebook-navigator) | ⚠️ ほぼ一致（"全員" は誇張、"多くのユーザーに有益" が正確） |
| 双窗格モードの設定場所 | プラグイン設定 → Desktop Appearance に "Dual-pane" 設定が存在 | [Wiki](https://github.com/johansan/notebook-navigator/wiki) | ✅ 一致 |
| 一大批零散小插件を置き換えられる | File Tree Alternative / Better Notes Explorer / Quick Switcher++ / Various File Preview 系の機能を統合。確かに複数置換は可能 | [Elizabeth Tai blog](https://elizabethtai.com/2025/11/25/how-to-use-notebook-navigator-obsidian-community-plug-in/) | ✅ 一致（具体的に置換できるプラグインの例は別ノート要） |
| 克制且有品味（控えめでセンスがある） | 1〜5 行の本文プレビュー、サムネイル自動生成、フォルダ/タグ単位の表示カスタマイズ等、装飾的でなく機能的な設計 | [公式サイト](https://notebooknavigator.com/) | 🔍 未確認（主観評価だが、UI スクショからは整合的） |
| 5 分で良さがわかる | チュートリアル系記事も「5〜10 分のセットアップで効果実感」と同様の時間感を述べている | [Elizabeth Tai blog](https://elizabethtai.com/2025/11/25/how-to-use-notebook-navigator-obsidian-community-plug-in/) | ✅ 一致 |
| 開発者が信頼に足る | Johan Sanneblad 氏は PhD + Apple/Google 等の innovation 経験あり | [公式 About](https://notebooknavigator.com/), [Obsidian Stats](https://www.obsidianstats.com/plugins/notebook-navigator) | ✅ 一致 |

---

## 🌐 最新動向（2026-05-06 時点）

- **2026-05-05 21:58 JST**: 二一的笔记氏が中国語圏 Obsidian コミュニティに対して双窗格モード推奨。1,036 likes で拡散中 — [元ツイート](https://x.com/eryidebiji/status/2051647798223991023), 2026-05
- **2026-Q1〜Q2**: Notebook Navigator が継続アップデート中。**v2.6.3 で CodeQL + OpenSSF Scorecard 導入**、セキュリティ意識の高さを示す — [GitHub Releases](https://github.com/johansan/notebook-navigator/releases), 2026-Q1
- **2026-Q1**: Property value filters（プロパティ値部分一致フィルタ）と Word count tooltip 追加 — [Obsidian Stats](https://www.obsidianstats.com/plugins/notebook-navigator), 2026-Q1
- **2025-11-25**: Elizabeth Tai による初心者向け解説記事公開、英語圏でも認知拡大 — [elizabethtai.com](https://elizabethtai.com/2025/11/25/how-to-use-notebook-navigator-obsidian-community-plug-in/), 2025-11
- **2025-中頃**: Obsidian Forum で公開、コミュニティプラグイン公式登録 — [Obsidian Forum](https://forum.obsidian.md/t/notebook-navigator-is-now-available-meet-your-new-obsidian-interface/105704), 2025
- **継続論争**: Obsidian 公式に「**標準のファイルエクスプローラを Notebook Navigator 等のプラグインに置き換えられる設定**」が欲しい、というフォーラム議論が続いている — [Obsidian Forum スレッド](https://forum.obsidian.md/t/set-default-file-explorer-internal-or-plugin-like-notebook-navigator/108593/27), 継続中

---

## 🧩 関連概念・隣接分野

- **File Tree Alternative**: 同じく標準エクスプローラ置換系の老舗プラグイン。Notebook Navigator との比較が頻繁に発生する
- **Bear / Apple Notes / Heptabase の 2ペイン UI**: Notebook Navigator のデザイン思想の出処。**ノートアプリの "標準" UI** として 2ペイン式は確立済み
- **Featured Image プラグイン**: 連携してサムネイル自動生成。Notebook Navigator のビジュアル機能を最大化する組み合わせ
- **Quick Switcher++ / Omnisearch**: ファイル探索の別アプローチ（検索優先）。Notebook Navigator は閲覧優先。**workflow 哲学が異なる**
- **Dataview / Bases**: 「ファイルエクスプローラを使わずクエリビューで探す」流儀。Notebook Navigator とは**思想が逆**で、両立は可能だが住み分けが必要
- **Mobile Obsidian の使用感**: モバイルでの 2 ペイン表示は画面狭く、Notebook Navigator も**モバイル時はシングルペイン自動切替**仕様

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - **UI の品質が高く、設計者が本物**: Johan 氏の経歴 + virtualized rendering + CodeQL 等の品質保証は他の趣味プラグインを大きく上回る
  - **複数プラグインの統合**: File Tree Alternative + プレビュー系 + ピン留め系 を 1 つで置換できる。**プラグインの数が減る**のはパフォーマンスとメンテナンス両面で利得
  - **"Bear / Apple Notes 化"** したい層にとって完成度が高い

- **否定 / 慎重派の主張**:
  - **Dataview / Bases 派には不要**: 「クエリで探す」流儀のヘビーユーザーは 2 ペイン UI を使わない。Notebook Navigator はそういう層には肥大化したリソース消費
  - **muscle memory コスト**: Obsidian 歴が長い人ほど標準エクスプローラの操作が体に染み付いている。**置き換えのコストは過小評価できない**（数日〜数週間）
  - **モバイルでの恩恵は限定的**: 画面狭く、モバイル時は自動シングルペインなので「**双窗格の良さ**」は享受しづらい。デスクトップ専用の改善と割り切るべき
  - **"全員に勧める" は言い過ぎ**: 二一的笔记氏の主張は熱量先行。**少なくとも Tsukapon のような複雑な縦割り vault では、入れる前に File Tree Alternative や File Explorer Plus 等との比較が要る**
  - **iCloud sync 環境での挙動**: Tsukapon は iCloud + MEGA の二重バックアップ環境。**IndexedDB キャッシュ**が iCloud sync 衝突を起こさないかは未検証

- **中立的に見るときの補助線**:
  - 「**今のファイルエクスプローラに 5 分以上ストレスを感じているなら入れる、ストレスがないなら現状維持**」が判断基準としてシンプル
  - 入れる場合は **GW のような腰を据えられる時期に試して、合わなければ即外せる** ように事前に削除手順を確認しておく

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] **iCloud sync + IndexedDB キャッシュの挙動**: Tsukapon vault は iCloud Documents 配下。Notebook Navigator のキャッシュが iCloud で衝突しないか実機検証
- [ ] **Tsukapon vault との相性ベンチマーク**: 71 階層の縦割り構造（SNS運用 / _ kiwami / _ memory / 調査 / Clippings / pending / archive 等）で 2 ペイン UI が逆に不便にならないか
- [ ] **既存プラグインとの競合マップ**: Tsukapon の `.obsidian/plugins/` 配下にあるプラグインのうち、Notebook Navigator で置き換え可能なもの・衝突するものをリストアップ
- [ ] **モバイル版 Obsidian での実用度**: workspace-mobile.json が頻繁に変わる Tsukapon の運用で、モバイル時の Notebook Navigator の挙動は本当に使えるか
- [ ] **Bases / Dataview とどう住み分けるか**: vault 内の `.base` ファイル（obsidian-bases スキル領域）を使う流儀と Notebook Navigator の閲覧 UI の併用パターン
- [ ] **二一的笔记氏が "替え可能な小プラグイン" を具体的に挙げているか**: リプライ欄や YouTube に具体名リストがあるなら拾う

---

## 📚 参考資料

- [二一的笔记 元ツイート（@eryidebiji 2026-05-05）](https://x.com/eryidebiji/status/2051647798223991023) — 投稿の一次情報, 取得日 2026-05-06
- [Notebook Navigator 公式サイト](https://notebooknavigator.com/) — 機能・開発者プロフィールの一次ソース, 取得日 2026-05-06
- [GitHub: johansan/notebook-navigator](https://github.com/johansan/notebook-navigator) — README・最新リリース情報, 取得日 2026-05-06
- [Obsidian Forum: Notebook Navigator is now available](https://forum.obsidian.md/t/notebook-navigator-is-now-available-meet-your-new-obsidian-interface/105704) — 公式コミュニティでの初出, 取得日 2026-05-06
- [Obsidian Stats: Notebook Navigator](https://www.obsidianstats.com/plugins/notebook-navigator) — DL 数・更新頻度・品質指標, 取得日 2026-05-06
- [Elizabeth Tai: How to use Notebook Navigator](https://elizabethtai.com/2025/11/25/how-to-use-notebook-navigator-obsidian-community-plug-in/) — 初心者向け実践解説, 取得日 2026-05-06
- [GitHub PR #6886: Add plugin Notebook Navigator](https://github.com/obsidianmd/obsidian-releases/pull/6886) — コミュニティプラグイン公式登録の経緯, 取得日 2026-05-06
- [Obsidian Forum: Set default File Explorer 議論](https://forum.obsidian.md/t/set-default-file-explorer-internal-or-plugin-like-notebook-navigator/108593/27) — 標準置換 API の議論, 取得日 2026-05-06
- [二一的笔记 YouTube チャンネル](https://www.youtube.com/@eryinote) — 著者の活動範囲確認, 取得日 2026-05-06

---

## 🗒 メモ

- **試す価値は十分ある**: Tsukapon vault は **71 フォルダ階層 × 縦割り構造**で、標準エクスプローラのスクロール疲労が確実に発生している。**2 ペイン UI で `SNS運用/post/day*.md` の一覧表示**が改善するなら日次運用の体感が上がる
- **試す前にチェックリスト**:
  - [ ] `.obsidian/plugins/` 配下の File Tree Alternative や類似系プラグインを把握 → 競合確認
  - [ ] iCloud sync 衝突チェック（IndexedDB の保存先がローカルキャッシュ or vault 内かを確認）
  - [ ] workspace-mobile.json と workspace.json への影響範囲を git status で監視
  - [ ] **GW 中に検証 → 合わなければ即削除** の方針で
- **二一的笔记氏のフォーマット研究**: 「全員に勧める」「30分で欠点ゼロ」「私は普段こういう評価を出さない」の **強気3点セット**は、Chinese 圏の "推荐文化" の典型。日本語 X で同じ語気で書くと押し付けがましく見えるが、**「自分は普段こういう評価を出さない人」のメタ宣言**だけは my-clone 文体に流用できる（信頼担保の言い回しとして）
- **記事化候補**: 「**Obsidian ファイルエクスプローラ系プラグイン4種比較（Notebook Navigator / File Tree Alternative / File Explorer Plus / Quick Explorer）**」型のレビュー記事は SEO 観点でも需要あり。実機検証して書けば 1 本立つ
- **Tsukapon の Obsidian スキル領域整理**: 既に `obsidian-markdown` / `obsidian-bases` / `obsidian-cli` / `json-canvas` 等のスキルがあるので、もし Notebook Navigator を採用するなら **`obsidian-skills` 領域に「ファイル探索 UI」枠を追加**することも視野
- **業務利用クライアントへの提案**: Obsidian を業務 KMS として使うクライアントが今後出てきた場合、Notebook Navigator は **「Obsidian を導入したけど階層が深くなって迷子」** 系の相談に対する標準提案になり得る。クライアント提案ストックに追加する価値あり
