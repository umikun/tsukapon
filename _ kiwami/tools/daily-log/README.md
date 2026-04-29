# Daily Log — ダッシュボード関連ファイル

2種類のフロントエンドからアクセス可能：

1. **Cowork artifact** (ID: `daily-log`): Coworkサイドバーで開く。カレンダー・Gmail・AIサマリー対応
2. **スタンドアロンWebサーバー** (http://127.0.0.1:8765): ブラウザで開く。Activity / Clockify / Markdown の3ソースのみ

---

## 📂 構成

```
_ kiwami/tools/daily-log/
├── README.md                           … このファイル
├── analytics.py                        … 分析エンジン（activity集計、CLI＋Pythonモジュール）⭐ NEW 2026-04-29
├── clockify-sync.py                    … Clockify APIから時間エントリを取得
├── com.user.clockify-sync.plist        … 15分ごとの同期用launchd
├── clockify/                           … Clockify同期データ
│   ├── YYYY-MM-DD.json
│   └── _latest.json
├── activity-tracker.py                 … 最前面アプリ・タイトル・アイドル秒を記録
├── activity-config.json                … アプリ→カテゴリの分類設定（編集可）
├── com.user.activity-tracker.plist     … 60秒ごとのトラッカー用launchd
├── activity/                           … アクティビティ記録（JSONL）
│   └── YYYY-MM-DD.jsonl
├── com.user.daily-log-server.plist     … サーバー常駐用launchd
└── server/                             … スタンドアロンWebサーバー
    ├── daily-log-server.py             … 127.0.0.1:8765 で提供
    └── index.html                      … ブラウザ版ダッシュボード
```

---

## 🧠 analytics.py — 分析エンジン ⭐ NEW 2026-04-29

`activity/*.jsonl` のデータ（1分粒度）を集計し、日次・週次のサマリーや集中ピーク・脱線パターン等を JSON で返す CLI ツール兼 Python モジュール。

**重要**: Clockify データは実時間との乖離があるため**使わない**（2026-04-29 ユーザー判断）。activity tracker のみが信頼できる作業時間データソース。

### CLI サブコマンド

```bash
# 日次サマリー（カテゴリ別時間 / アプリ別 / ファイル別 / 集中ピーク / 時間帯ヒートマップ）
/usr/bin/python3 analytics.py daily 2026-04-29
/usr/bin/python3 analytics.py daily today

# 週次サマリー（曜日別 / 集計値 / 曜日×時間帯ヒートマップ）
/usr/bin/python3 analytics.py weekly 2026-W18
/usr/bin/python3 analytics.py weekly current

# 集中ピーク時間帯（連続focus N分以上、デフォルト30分）
/usr/bin/python3 analytics.py focus-peaks 2026-04-29 --min-minutes 30

# ファイル別時間（Obsidian/Cursorのウィンドウタイトルから抽出）
/usr/bin/python3 analytics.py file-times 2026-04-29

# note記事の執筆時間（titleに 'note-YYYYMMDD' を含む focus 時間を集計）
/usr/bin/python3 analytics.py note-time 2026-W18

# 時間帯別ヒートマップ（曜日×時間帯）
/usr/bin/python3 analytics.py hourly-heatmap 2026-W18

# 脱線パターン検出（同じ (hour, app) が複数日に出現したら検出）
/usr/bin/python3 analytics.py distraction-patterns --days 7 --min-occurrences 3
```

### Python モジュールとして使う

```python
import sys
sys.path.insert(0, "_ kiwami/tools/daily-log")
import importlib.util
spec = importlib.util.spec_from_file_location("analytics", "_ kiwami/tools/daily-log/analytics.py")
analytics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analytics)

s = analytics.summarize_day("2026-04-29")
w = analytics.summarize_week("2026-W18")
peaks = analytics.find_focus_peaks(analytics.load_day("today"))
patterns = analytics.detect_distraction_patterns(days=7)
```

### 利用しているスキル

- `/daily-summary` — 日次業務日報の生成
- `/focus-report` — 週次集中レポート＋脱線パターン検出（自己改善ループ連動）
- `/weekly-analytics` — Step 6.5「Daily Log データ統合」で note記事ROI・投稿時刻×集中度・集中ピーク時間帯を取得

---

## 🔧 Clockify連携のセットアップ（初回のみ）

### 1. APIキーをvault外に配置

```bash
mkdir -p ~/.config/clockify-sync
echo 'NTExNDBkODYtMmM3Zi00YjgwLWJiMWMtMDg4MjdhMjk2Y2Ez' > ~/.config/clockify-sync/api_key
chmod 600 ~/.config/clockify-sync/api_key
```

APIキーは `_ kiwami/name.md` の「API」項目から取得。

### 2. 手動で1回実行して動作確認

```bash
/usr/bin/python3 "/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/clockify-sync.py"
```

### 3. launchdに登録（15分ごと自動実行）

```bash
cp "/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/com.user.clockify-sync.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.clockify-sync.plist
```

---

## 📊 アクティビティトラッカーのセットアップ（初回のみ）

### 1. launchdに登録（60秒ごと自動実行）

```bash
cp "/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/com.user.activity-tracker.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.activity-tracker.plist
```

### 2. アクセシビリティ権限を許可（必須）

初回の osascript 実行時、macOSから **「システム設定 → プライバシーとセキュリティ → アクセシビリティ」**を開いて以下を有効にするよう求められる：

- `/usr/bin/osascript` または `python3`
- あるいは launchd 経由で動く `Python`

設定後は `launchctl list | grep activity-tracker` で `LastExitStatus: 0` が出れば成功。

### 3. カテゴリ分類のカスタマイズ

`activity-config.json` を編集してアプリを増減できる：

- `categories.focus.apps` … 集中カテゴリ（緑）
- `categories.distraction.apps` … 脱線カテゴリ（赤）
- どちらにも無いアプリ → `other`（灰色）
- `idle_threshold_seconds: 180` … アイドル判定（3分）
- `distraction_session_min_minutes: 15` … 脱線アラートの閾値

**アプリ名の確認方法**: `activity/YYYY-MM-DD.jsonl` を覗くとmacOSが報告する実際の名前が分かる（例: Photoshopは `Adobe Photoshop 2024` だったりする）。

---

## 🌐 スタンドアロンサーバーのセットアップ（ブラウザで開きたい場合）

### 1. launchdに登録（常時起動）

```bash
cp "/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/com.user.daily-log-server.plist" ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.user.daily-log-server.plist
```

### 2. ブラウザで開く

[http://127.0.0.1:8765](http://127.0.0.1:8765)

**機能比較**:

| 機能 | Cowork | スタンドアロン |
|---|---|---|
| 活動トラッカー | ✅ | ✅ |
| Clockify | ✅ | ✅ |
| 編集したMarkdown | ✅ | ✅ |
| カレンダー予定 | ✅ | ❌ |
| Gmail送信履歴 | ✅ | ❌ |
| AIサマリー生成 | ✅ | ❌ |
| Markdown出力・コピー | ✅ | ✅ |
| 手動記録（localStorage） | ✅ | ✅ (別保存) |

**ポート変更**: plistの `EnvironmentVariables.DAILY_LOG_PORT` を書き換え → `launchctl unload && load` で反映。

**LAN内の他デバイスからも見たい**: plistの `DAILY_LOG_HOST` を `0.0.0.0` に変更（ただしMac内に閉じたい場合は `127.0.0.1` のままが安全）。

### 3. 動作確認

```bash
# 登録状態
launchctl list | grep daily-log-server

# 疎通
curl -sS http://127.0.0.1:8765/healthz

# ログ
tail -f /tmp/daily-log-server.log
tail -f /tmp/daily-log-server-error.log
```

### 4. 停止

```bash
launchctl unload ~/Library/LaunchAgents/com.user.daily-log-server.plist
```

---

## 📊 動作確認・運用

```bash
# Clockify同期
launchctl list | grep clockify-sync
launchctl start com.user.clockify-sync
tail -f /tmp/clockify-sync.log

# アクティビティトラッカー
launchctl list | grep activity-tracker
launchctl start com.user.activity-tracker
tail -f /tmp/activity-tracker.log

# 今日のアクティビティ生ログを見る
cat "/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/activity/$(date +%Y-%m-%d).jsonl"

# 停止
launchctl unload ~/Library/LaunchAgents/com.user.clockify-sync.plist
launchctl unload ~/Library/LaunchAgents/com.user.activity-tracker.plist
```

---

## 🛑 トラブルシュート

| 症状 | 対処 |
|---|---|
| Clockify `API key file not found` | ~/.config/clockify-sync/api_key をやり直す |
| Clockify `HTTP 401` | APIキーが古い or 無効 |
| Activity tracker が `unknown` ばかり | アクセシビリティ未許可。システム設定 → プライバシー → アクセシビリティで許可 |
| Activity のJSONLに特定アプリが出ない | macOSの実名を確認して activity-config.json に追記 |
| JSONは出ているがダッシュボードに反映しない | ダッシュボード（Coworkサイドバーの Daily Log）を⟳Reloadする |

---

## 🔗 関連

- Daily Log（Cowork artifact）: `daily-log`
- [[../../../Claudian-スキル一覧.md]] の「バックグラウンド機能（自動化）」セクション
- 既存のlaunchdパターン: [[../../../Macで定期的に同期.md]]（rsyncバックアップ）

---

## ⚠️ セキュリティ・プライバシー

- Clockify APIキーは必ず vault外 (`~/.config/`) に置く
- `activity/*.jsonl` にはウィンドウタイトルが含まれる（例: "Safari - 〇〇の明細書"）。
  Google Driveバックアップに含まれても良いかを確認。気になる場合は `.gitignore` 的な除外設定を検討
- `clockify/*.json` には作業内容・プロジェクト名・タグが含まれる
