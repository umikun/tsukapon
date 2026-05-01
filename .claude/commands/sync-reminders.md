アクションプラン（`SNS運用/action-YYYYMMDD.md`）の **タイムライン早見表** を Apple Reminders の `Tsukapon` リストに同期するスキルです。

---

## 目的

`/re-daily` で生成されるアクションプランの時間軸エントリ（早見表の各行）を、macOS Reminders に時刻付きリマインダーとして登録する。これによりiPhone・Apple Watch・Macで通知が飛び、vault を開かずに次の行動が分かる状態を作る。

---

## 入力形式

### A. 引数なし（最頻パターン）

```
/sync-reminders
```

→ 本日の `SNS運用/action-YYYYMMDD.md`（`date +%Y%m%d`）を自動で読み込む

### B. ファイル指定

```
/sync-reminders SNS運用/action-20260501.md
```

→ 指定されたアクションプランを使う

### C. 削除モード（リスト全クリア）

```
/sync-reminders --clear
```

→ `Tsukapon` リストの未完了リマインダーを全て complete マークして整理。新しい1日の朝に走らせる用。

---

## 前提

- `reminders-cli` がインストール済み（`brew install keith/formulae/reminders-cli`）
- macOS のリマインダーアクセス許可が `reminders` コマンドに付与済み
- Reminders アプリに `Tsukapon` リストが存在（無ければ自動作成）

---

## 処理手順

### Step 1. 入力モードの判定

- `--clear` を含むなら削除モードへ（Step 5 にジャンプ）
- 引数なし → 本日のアクションプラン `SNS運用/action-$(date +%Y%m%d).md` を対象
- ファイルパス指定 → そのファイルを対象
- 対象ファイルが存在しなければ「ファイルなし」と1行報告して終了

### Step 2. リスト存在確認

```bash
reminders show-lists | grep -q "^Tsukapon$" || reminders new-list "Tsukapon"
```

### Step 3. 早見表のパース

アクションプラン本文から `## 🗓 タイムライン（時間軸順）` セクションを探し、その直下の `> **早見表**` 配下のテーブル行を取得する：

```
> | HH:MM | 種別アイコン | 内容 |
```

各行から以下を抽出する:

| 項目 | 抽出方法 |
|---|---|
| 時刻 | テーブル1列目から `HH:MM`（`**HH:MM**` の太字も剥がす） |
| 種別アイコン | テーブル2列目（🛠/📝/🐦/🧵/🔄/💰/👥） |
| 内容 | テーブル3列目（`**...**` の太字記号は剥がす） |
| 日付 | アクションプランファイル名 `action-YYYYMMDD.md` から取得 |

### Step 4. 既存リマインダーとの突き合わせ

```bash
reminders show Tsukapon --format json
```

を実行し、既に同じタイトルのリマインダーがある場合は **スキップ**（重複防止）。タイトル比較は完全一致。

リマインダーのタイトル形式は以下に固定する:

```
HH:MM {種別アイコン} {内容}
```

例: `09:00 🧵 ニューススレッドv2 初試行（W18の最大試行枠）`

### Step 5. 追加 or 削除

#### 追加モード（通常）

各行について:

```bash
reminders add Tsukapon "HH:MM 🧵 内容" --due-date "YYYY-MM-DD HH:MM"
```

- `--due-date` は **「アクションプランの日付」+「早見表の時刻」** を組み合わせて生成
- 失敗時はエラー行を `stderr` に流し、続行（処理を止めない）

#### 削除モード（`--clear`）

```bash
# 未完了リマインダーのインデックスを取得して全complete
indices=$(reminders show Tsukapon --format json | jq -r 'to_entries[] | select(.value.isCompleted == false) | .key')
for i in $indices; do
  reminders complete Tsukapon "$i"
done
```

※ 逆順で complete しないとインデックスがずれる場合があるため `sort -rn` で逆順処理する

### Step 6. Daily Log ダッシュボード用スナップショット書き出し

書き込み（add/complete）が終わったら、Daily Log ダッシュボードの `⏰ リマインダー` カードが読むスナップショットファイルを更新する。

```bash
~/bin/daily-log/reminders-snapshot.sh
```

スナップショット出力先: `_ kiwami/tools/daily-log/reminders-snapshot.json`。失敗しても Step 7 へ進む（best-effort）。

### Step 7. 完了報告

チャットへ以下を返す:

| 項目 | 内容 |
|---|---|
| 対象ファイル | `[[SNS運用/action-YYYYMMDD.md]]` |
| 追加件数 | N件（時刻順リスト付き） |
| スキップ件数 | M件（重複） |
| 失敗件数 | 0件（あれば内訳） |
| Daily Log 同期 | スナップショット更新 ✓ or 失敗（理由） |

iPhone/Apple Watch を見れば、本日の予定が時刻通り通知されることを1行で添える。

---

## 制約・禁止事項

### 🔴 リスト境界（絶対遵守）

CLAUDE.md「⏰ 絶対ルール: Apple Reminders は『読み取り全リスト・書き込みTsukapon限定』」を厳守する：

- **書き込み（add / complete / uncomplete / delete / edit）は `Tsukapon` リストに限定**
- 個人リスト（`全て` 等）には**絶対に書き込まない**。誤って書き込むと請求書・ドメイン移管等の重要タスクを破壊するリスクあり（リマインダーには「ゴミ箱」がなく復元不能）
- `--clear` モードのスコープは `Tsukapon` リスト固定。他リストに広げない
- `new-list` は `Tsukapon` 不在時の自動作成のみ。他のリストは作らない

### その他

- `reminders` コマンドを使う。`osascript` 直叩きは権限ダイアログ問題を避けるため非推奨
- 既存リマインダーの**タイトルを変更**しない（完了→未完了の切替や削除はユーザー操作に任せる。`--clear` 以外で削除はしない）
- 9時前の時刻枠は**スキップ**（CLAUDE.md「📅 タイムライン早見表」ルール準拠）
- 通知音やスヌーズ等の細かい設定は触らない（OS側の通知設定を尊重）
- 個人リストの内容を vault内ファイルに転記しない（プライバシー配慮）

---

## 連携先

- 入力: `SNS運用/action-YYYYMMDD.md`（`/re-daily` Step 11 出力）
- 出力: macOS Reminders `Tsukapon` リスト
- 上流: `/re-daily` Step 11 完了直後に自動呼び出し（オプション）
- 下流: 朝のセッション起動時に CLAUDE.md ルールで `reminders show Tsukapon` を読む

---

## 入力データ

$ARGUMENTS
