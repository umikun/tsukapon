macOS Reminders の内容を見やすく一覧表示するスキルです。`/sync-reminders` の対になる読み取り専用スキル。

---

## 目的

`reminders` CLI の `show` / `show-all` をそのまま叩くと出力が読みにくい（インデックスと時刻だけのフラット表示）。これを **期限順・優先度・絵文字プレフィックス分類込みのMarkdownテーブル**で見やすく整形して出力する。CLAUDE.md「⏰ 絶対ルール」の権限マトリクスに従い、**読み取りのみ・副作用ゼロ**で動作する。

---

## 入力形式

### A. 引数なし（最頻パターン）

```
/show-reminders
```

→ `Tsukapon` リストの**未完了**リマインダーを期限順で表示

### B. 全リスト統合表示

```
/show-reminders --all
```

→ 全リスト（個人リスト含む）を取得し、以下の順で**セクション分けして表示**:

1. 🚨 期限3日以内（緊急・全リスト横断）
2. 📋 `Tsukapon` リストの未完了
3. 📅 個人リストの未完了（リスト別にネスト）

CLAUDE.md「⏰ 絶対ルール」読み取り権限に準拠した、朝のセッション起動時の標準フォーマット。

### C. 特定リスト指定

```
/show-reminders 全て
/show-reminders --list "全て"
```

→ 指定リストの未完了リマインダーを表示

### D. 完了済みも含める

```
/show-reminders --include-completed
/show-reminders --all --include-completed
```

→ 完了済みリマインダーも併せて表示（取り消し線付き）

### E. 今日期限のみ

```
/show-reminders --today
```

→ 今日が期限のリマインダーだけを抽出（`Tsukapon` + 個人リスト横断）

---

## 前提

- `reminders-cli` がインストール済み（`brew install keith/formulae/reminders-cli`）
- macOS リマインダーへのアクセス許可が `reminders` コマンドに付与済み

---

## 処理手順

### Step 1. 入力モードの判定

| 入力 | 動作 |
|---|---|
| 引数なし | 単一リスト表示（`Tsukapon`） |
| `--all` | 全リスト統合表示 |
| `--list <name>` または `<name>` | 指定リスト表示 |
| `--today` | 今日期限のみ |
| `--include-completed` | 完了済みフラグON |

### Step 2. リスト取得

```bash
# 単一リスト
reminders show "<list-name>" --format json

# 全リスト統合
reminders show-all --format json
```

`--include-completed` 指定がない場合は `isCompleted: false` でフィルタ。

### Step 3. ソート・グルーピング

#### 単一リスト表示時

期限の有無で2グループに分け、期限ありを期限昇順、期限なしを末尾にまとめる。

#### 全リスト統合表示時（`--all`）

1. **🚨 期限3日以内（緊急枠）**: 全リスト横断で、`dueDate` が今日〜3日後のものを抽出して最上部に表示
2. **📋 `Tsukapon`**: 残りの `Tsukapon` リスト（期限順）
3. **📂 個人リスト**: `Tsukapon` 以外のリストごとにサブセクション化

#### `--today` モード

今日（`date +%Y-%m-%d`）が期限のリマインダーを全リスト横断で抽出。

### Step 4. 表示整形

以下のMarkdownテーブル形式で出力:

```markdown
## 📋 Tsukapon（未完了 N件）

| # | タイトル | 期限 | 優先度 |
|---:|---|---|:-:|
| 0 | 09:00 🧵 ニューススレッドv2 初試行 | 今日 09:00 | — |
| 1 | 📋 ICA学費表カスタマイズ | 今日 15:00 | 🔴 high |
| 2 | 📋 アブニール 請求書ドラフト確認 | 5/7 (木) 18:00 | 🔴 high |
| 3 | 📚 obsidian-bases 全部読む | 5/10 (土) 23:59 | — |
| 4 | 🛒 バッテリー処分 | — | — |
```

#### 期限の表示ルール

| 状態 | 表示形式 | 例 |
|---|---|---|
| 過去 | 🔴 `M/D HH:MM 過ぎ` | `🔴 4/30 15:00 過ぎ` |
| 今日 | `今日 HH:MM` | `今日 15:00` |
| 明日 | `明日 HH:MM` | `明日 09:00` |
| 7日以内 | `M/D (曜) HH:MM` | `5/7 (木) 18:00` |
| それ以降 | `M/D HH:MM` | `5/15 17:00` |
| 期限なし | `—` | — |

#### 優先度の表示ルール

| Reminders優先度 | 表示 |
|---|---|
| 1 (high) | 🔴 high |
| 5 (medium) | 🟡 medium |
| 9 (low) | 🔵 low |
| 0 (none) | — |

### Step 5. サマリー出力

テーブルの末尾に1行サマリーを追加:

```
合計: 未完了 N件 / 完了済み M件 / 期限超過 X件 / 期限3日以内 Y件
```

### Step 6. Daily Log ダッシュボード用スナップショット書き出し（自動）

表示が完了したら、Daily Log ダッシュボード（`http://127.0.0.1:8765`）の `⏰ リマインダー` カードが読む JSON ファイルを更新する。これにより `/show-reminders` を実行するたびに dashboard 側のデータも最新化される。

```bash
# Bashツールで実行（Terminal context なので TCC 通る）
~/bin/daily-log/reminders-snapshot.sh
```

実装メモ:
- daily-log-server は launchd 起動の制約上、TCC（プライバシー制御）が silently 拒否され Reminders DB を直接読めない。Terminal context（Claudian の Bash ツールや手動 cli）から書き出すスナップショットファイルを介して連携する設計。
- スナップショット出力先: `_ kiwami/tools/daily-log/reminders-snapshot.json`
- 失敗時は警告のみで Step 5 までの結果は維持（best-effort）

---

## 出力例

### 引数なし時

```markdown
## 📋 Tsukapon（未完了 4件）

| # | タイトル | 期限 | 優先度 |
|---:|---|---|:-:|
| 0 | 📋 ICA学費表カスタマイズ | 今日 15:00 | 🔴 high |
| 1 | 09:00 🧵 ニューススレッドv2 初試行 | 今日 09:00 | — |
| 2 | 11:00 🐦 day97 投稿①（朝） | 今日 11:00 | — |
| 3 | 22:30 🔄 本日KPI記録 | 今日 22:30 | — |

合計: 未完了 4件 / 期限超過 0件 / 今日中 4件
```

### `--all` 時

```markdown
## 🚨 期限3日以内（全リスト横断）

| # | リスト | タイトル | 期限 | 優先度 |
|---:|---|---|---|:-:|
| 0 | 全て | umikun.netの移管 | 5/6 (火) | — |
| 1 | Tsukapon | 📋 ICA学費表カスタマイズ | 今日 15:00 | 🔴 high |

---

## 📋 Tsukapon（未完了 13件）

…テーブル…

---

## 📂 個人リスト

### 全て（未完了 5件）

…テーブル…
```

---

## 制約・禁止事項

### 🔴 読み取り専用（絶対遵守）

CLAUDE.md「⏰ 絶対ルール」読み取り権限に従い、本スキルは:

- `add` / `complete` / `delete` / `edit` / `new-list` を**一切実行しない**
- `reminders show` / `show-all` / `show-lists` のみ使う（副作用ゼロ）
- 個人リストの内容は**表示のみで vault内ファイルに転記しない**（プライバシー配慮）

### その他

- 表示が長すぎる場合（合計50件超等）は「上位30件のみ表示」等で切り、末尾に「以下省略」を明記
- 完了済みリマインダーはデフォルト非表示（`--include-completed` で明示指定が必要）
- リマインダーの順序を変更する操作は提案しない（並び替えは Reminders App 側で）

---

## 連携先

- 上流: なし（純粋な読み取りスキル）
- 下流: ユーザー操作（必要に応じて `/sync-reminders` で更新、または iPhone・Apple Watch で完了マーク）
- 関連: `/sync-reminders`（書き込み側） / CLAUDE.md「⏰ 絶対ルール」（権限マトリクス）

---

## 入力データ

$ARGUMENTS
