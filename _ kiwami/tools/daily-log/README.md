# Daily Log — ダッシュボード関連ファイル

2種類のフロントエンドからアクセス可能：

1. **Cowork artifact** (ID: `daily-log`): Coworkサイドバーで開く。カレンダー・Gmail・AIサマリー対応
2. **スタンドアロンWebサーバー** (http://127.0.0.1:8765): ブラウザで開く。Activity / Clockify / Markdown の3ソースのみ

---

## 📂 構成

```
_ kiwami/tools/daily-log/
├── README.md                           … このファイル
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
