# Claudian — obsidian-skills 活用マップ

> **🔗 関連コンテンツ**
> - 📋 全スキル一覧: [[Claudian-スキル一覧.md]]
> - 📜 vault運用ルール: [[CLAUDE.md]]
> - 🛠 導入アクション（2026-04-28）: [[action-20260428]]
> - 📰 導入記事（出典）: [[Clippings/ObsidianでClaudeCodeを使い始めたら、次に入れるべき「obsidian-skills」｜sutero（ステロ）.md]]
> - 💾 配置先: `.claude/skills/`（vault内・当vault専用）

作成日: 2026-04-28
目的: Tsukapon vault 内で **obsidian-skills（5スキル）** をどう活用するかの**実装ガイド兼アイデア帳**。
スキル本体: `.claude/skills/{obsidian-markdown, obsidian-bases, defuddle, json-canvas, obsidian-cli}/`

---

## 🎯 5スキルの位置づけ早見表

| スキル | 役割 | 発火タイミング | Tsukaponでの使用頻度 |
|---|---|---|---|
| **obsidian-markdown** | Obsidian記法の生成・検証 | 全スキルの裏方 | 🔥🔥🔥 常時稼働 |
| **obsidian-bases** | `.base`でMD群をDB化 | 一覧・集計が欲しい時 | 🔥🔥🔥 導入余地大 |
| **defuddle** | URL→クリーンMarkdown変換 | 外部URL読み込み時 | 🔥🔥 自動発動 |
| **json-canvas** | `.canvas`で関係性を視覚化 | 戦略図・俯瞰図作成時 | 🔥🔥 月1〜週1 |
| **obsidian-cli** | Bashからvault操作 | 自動化スクリプト時 | 🔥 自動化拡張用 |

---

## 1️⃣ obsidian-markdown — 全領域で「裏方」として常時稼働

### 主な発火タイミング
- `/re-daily` がnote記事を生成・リライトする時（callout・wikilink・frontmatterの正しさ保証）
- `/thread`・`/news-thread` がX投稿スレッドを書き出す時
- `/deep-dive` が `調査/` にノートを作る時の関連リンク埋め込み
- CLAUDE.md「🔗 自動リンク設置」ルール実行時

### Tsukapon特有の活用ポイント
| 用途 | 具体例 |
|---|---|
| **frontmatter標準化** | `SNS運用/post/day*.md` の `date / theme / status / tags` を全ファイル統一 → Bases で集計可能に |
| **callout の使い分け** | 戦略メモは `> [!note]`、KPI警告は `> [!warning]`、勝ちパターンは `> [!success]` |
| **block ID活用** | [[SNS運用/analytics/フォロワー改善.md]] の重要原則に `^principle-1` 等を振り、各週の戦略メモから `[[フォロワー改善#^principle-1]]` で引用 |
| **embed `![[]]`** | 週次レポートに過去ベスト投稿のスクショや本文を埋め込み |

→ **明示的に呼ぶ場面**: 「このノートのObsidian記法を obsidian-markdown スキルでチェックして」

---

## 2️⃣ obsidian-bases — 「散らかったMD群を一覧化する切り札」

vault内に `.base` は導入時点でゼロ。**最も投資対効果が高い**領域。

### 候補①: SNS投稿の運用ダッシュボード `SNS運用/post/posts.base` ✅ **2026-04-28 作成済**

- 対象: `SNS運用/post/day*.md` + `SNS運用/post/thread/*.md` + `SNS運用/post/article/*.md`
- ビュー:
  - **全投稿（更新順）**: 種別・更新日・サイズで横断
  - **🐦 デイリーX投稿**: `day*.md` 専用
  - **🧵 note紹介スレッド**: `thread/` 専用
  - **📰 X Articles**: `article/` 専用
  - **🖼 ギャラリー（最新30件）**: cards view
- 効用: 「今週何本投稿した？」「保留中の下書き棚卸し」が**1画面で完結**

### 候補②: note記事の収益化ステータス `SNS運用/note/notes.base`（未作成）

- 対象: `SNS運用/note/*.md` + `SNS運用/note/_有料記事/*.md`
- frontmatter例: `published / paywalled / price / pv / likes / publish_date`
- ビュー: 公開日順テーブル / 有料記事だけのcards / 月別 group by
- 効用: **ストック型コンテンツ資産の可視化**（[[SNS運用/noteの今後と収益化戦略.md]] の実装ツール）

### 候補③: 週次レポート横断ビュー `SNS運用/analytics/weeks.base`（未作成）

- 対象: `WNN分析レポート.md` / `WNN戦略メモ.md`
- frontmatter例: `week / focus_hours / posts / followers_delta / top_post`
- ビュー: 週次推移テーブル → **トレンド把握**

### 候補④: 調査ノートの分類 `調査/research.base`（未作成）

- frontmatter: `topic / source_type / depth(浅/中/深) / outcome(運用反映済 / 保留)`
- 「outcome=保留」フィルタで**眠ってる調査の救出**

### 候補⑤: アーカイブの検索性UP `SNS運用/archive/archive.base`（未作成）

- 対象: `SNS運用/archive/{post,threads,note}/*.md` ＋ `archive.md`
- 過去のヒット投稿を**テーマ・反応数で再発掘**

→ **明示的に呼ぶ場面**: 「obsidian-bases スキルで○○.base を作って」

---

## 3️⃣ defuddle — 既に毎日「裏で」効いてる

### 自動発動するケース
- `/deep-dive` で外部URLを調査する時 → 広告除去で**トークン削減**
- `/re-daily` がnote記事の参考URLを読み込む時
- `/news-thread` がAIニュースをスレッド化する時
- `Clippings/` に追加されたWeb記事の**初期取り込み**（手動）

### Tsukapon特有の活用ポイント
| シーン | コマンド例 |
|---|---|
| 競合のnote記事をリサーチ | `defuddle parse https://note.com/xxxxx --md -o /tmp/research.md` |
| AIニュース記事の本文だけ抽出 | `defuddle parse https://techcrunch.com/... --md` |
| Xの公式ブログ・OSS記事 | `defuddle parse <url> --md` → そのまま `調査/` へ |

### 注意
- **`.md` で終わるURL は WebFetch を使う**（既にMarkdownなので壊れる）
- GitHubのREADMEやmd直リンクは defuddle に通さない

→ **明示的に呼ぶ場面**: 通常は自動。失敗時のみ「defuddleでこのURLをparseして」と手動指定

---

## 4️⃣ json-canvas — 「俯瞰図ファイル」を増やす最初の一歩

vault内 `.canvas` は導入時点でゼロ。

### 即効性が高い候補トップ3

#### 🥇 `Claudian-スキル連携図.canvas`（未作成）
- 既存スキル11個（`/re-daily`, `/thread`, `/news-thread`, `/deep-dive`, `/weekly-analytics` 等）の**呼び出し関係**を図示
- 「`/re-daily` → `/thread` → `/quote-rewrite`」の連鎖が一目瞭然
- → [[Claudian-スキル一覧.md]] のテキスト表を**視覚化した別表現**

#### 🥈 `_ kiwami/my-clone/人格マップ.canvas`（未作成）
- 人格データの構成要素（口調 / 価値観 / 専門領域 / NGワード等）を放射状に
- 各ノードから関連 `.md` へfile-node でリンク
- → SNS投稿生成時の**人格ぶれチェック用**の参照図

#### 🥉 `SNS運用/analytics/週次レビューマップ.canvas`（未作成）
- 中央に「今週の数値」テキストノード
- そこから「勝ちパターン / 負けパターン / 仮説 / 翌週施策」を枝分かれ
- 毎週コピーして使い回す **テンプレ化可能**

### その他の候補
| ファイル | 用途 |
|---|---|
| `SNS運用/note/_設計/<記事名>.canvas` | note記事の論理構造（主張→論拠→例→CTA） |
| `_ kiwami/tools/daily-log/構成図.canvas` | Daily Log の依存関係（plist / py / json）を図示 |

→ **明示的に呼ぶ場面**: 「json-canvas スキルでスキル連携図を作って」

---

## 5️⃣ obsidian-cli — vault操作の自動化レイヤー

`obsidian` コマンドで**起動中のObsidianを直接操作**できる。Bashスクリプトに組み込みやすい。

### Tsukapon特有の活用ポイント

#### A. クイックノート作成の高速化
```bash
obsidian create name="2026-W18-メモ" content="## 気づき\n- " folder="SNS運用/analytics"
```
→ `/remember` の補助として **メモ階層への放り込み**を1コマンドで

#### B. vault横断検索
```bash
obsidian search query="フォロワー改善"
obsidian search query="tag:#x-strategy"
```
→ `/reflect` がパターン検出する時の**3回以上観察**カウントに使える

#### C. アクティブファイル操作
```bash
obsidian open file="Claudian-スキル一覧.md"
obsidian property file="day28.md" key="status" value="published"
```
→ **`status` プロパティの一括更新**（公開済みフラグ付け）

#### D. プラグイン開発／デバッグ（おまけ）
- `obsidian reload-plugin` / `obsidian run-js` / `obsidian screenshot`
- 今は使わないが、将来カスタムプラグイン作る時に便利

→ **明示的に呼ぶ場面**: 「obsidian-cli でvault内の `#weekly-analytics` タグ持つノート全部探して」

---

## 🎯 優先度マップ（Tsukaponで効果が出る順）

| 優先度 | スキル | 最初に作るもの | ステータス |
|---|---|---|---|
| 🔥🔥🔥 | **obsidian-bases** | `SNS運用/post/posts.base` | ✅ 2026-04-28 作成 |
| 🔥🔥🔥 | **obsidian-markdown** | （既に裏で稼働中） | 稼働中 |
| 🔥🔥 | **defuddle** | （既に裏で稼働中） | 稼働中 |
| 🔥🔥 | **json-canvas** | `Claudian-スキル連携図.canvas` | 未着手 |
| 🔥 | **obsidian-cli** | （Bash自動化に組み込み） | 未着手 |

---

## 📋 検討して見送った活用案（重複防止用ログ）

### Daily Log の Bases化（2026-04-28 見送り）
- `_ kiwami/tools/daily-log/{activity,clockify}/` の `.jsonl` / `.json` を直接Basesで扱うのは不可（Basesは `.md` frontmatter専用）
- ブリッジには日次サマリーMDの自動生成が必要 → 既存の専用ダッシュボード（Cowork artifact / 127.0.0.1:8765）が機能十分のため、現時点では着手しない
- 将来「週単位の推移を一覧で見たい」要望が出たら、`/weekly-analytics` 出力に frontmatter を足す候補③から再着手

---

## 🔗 関連スキル / ドキュメント

- [[Claudian-スキル一覧.md]] — vault内の全スキル一覧
- [[Claudian-スキル候補.md]] — 自己改善ループの候補置き場
- [[CLAUDE.md]] — vault運用ルールブック（外部スキル参照ルールを参照）
- [[action-20260428]] — 導入時のアクションプラン全文
- [[Clippings/ObsidianでClaudeCodeを使い始めたら、次に入れるべき「obsidian-skills」｜sutero（ステロ）.md]] — 出典記事
