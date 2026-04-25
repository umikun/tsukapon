# n8n ワークフロー自動化システム

> **🔗 関連コンテンツ（ツール手順書）**
> - ⚙️ n8n × サイボウズ × Chatwork セットアップ: [[_ kiwami/tools/n8n-cybozu-chatwork-setup.md]]
> - 📝 Chatwork API申請メモ: [[_ kiwami/_tmp/Chatwork API申請.md]]
> - 🛑 停止条件および停止手順: [[_ kiwami/README/停止条件および停止手順.md]]
> - 🧰 SNS運用での日常ツール: [[SNS運用/日常的に使っているツール.md]]

## 概要

Clockifyに登録したタイムエントリを、Googleカレンダー・Day Oneに自動連携するシステム。
n8nをローカル（npm）で動作させ、Zapierの代替として運用する。

```
Clockify → [n8n] → Google Calendar（clockifyカレンダー）
                 → Day One（Jobジャーナル）
```

## システム構成

### インストール情報

| 項目 | 値 |
|------|---|
| n8n バージョン | 2.14.2 |
| インストール方法 | npm グローバル (`npm install n8n -g`) |
| Node.js | v22.17.1 |
| 管理画面URL | http://localhost:5678 |
| データ保存先 | `~/.n8n/` |
| DB | `~/.n8n/database.sqlite` |

### ワークフロー名

`n8n-googlecalender`（ID: TuQn8cgrU8dTl2YP）

### ノード構成

```
Schedule Trigger → HTTP Request → Filter New → Create an event → Code in JavaScript
（3分間隔）       （Clockify API）  （重複防止）   （Google Calendar）  （Day One登録）
```

#### 1. Schedule Trigger
- 3分間隔で実行（Every 3 Minutes）

#### 2. HTTP Request
- **Method**: GET
- **URL**: `https://api.clockify.me/api/v1/workspaces/684043134d7e18788e95a3d5/user/684043134d7e18788e95a3d4/time-entries`
- **認証**: Header Auth（X-Api-Key）
- **Query Parameters**:
  - `page-size`: `10`（最新10件取得、複数エントリの取りこぼし防止）
  - `hydrated`: `true`（プロジェクト詳細を含む）
- **Retry on Fail**: 有効（Max Tries: 3、Wait: 3000ms）

#### 3. Filter New（Code）
- 前回処理したエントリIDを `/tmp/n8n_clockify_last_id.txt` に保存
- Clockify APIは新しい順で返すため、前回IDの位置を探し、それより新しいエントリだけを次のノードへ渡す
- タイマー実行中（end=null）のエントリは除外
- 複数の新規エントリがあれば全件を次のノードへ渡す
- コードは `tools/n8n-fix-filter-new.js` に保存

#### 4. Create an event（Google Calendar）
- **カレンダー**: clockify
- **Summary**: `【clientName：projectName】description`
- **Location**: clientName
- **Description**: 作業時間（例: 2:00）
- **Start/End**: Clockifyのタイムエントリの開始・終了時刻
- **Execute Once**: OFF（複数エントリを全件処理）

#### 5. Code in JavaScript（Day One登録）
- Day One CLI (`/usr/local/bin/dayone`) を使用
- `$("Filter New").all()` でClockifyデータを直接参照（Google Calendarの出力ではなく）
- **Execute Once**: OFF（複数エントリを全件処理）
- **ジャーナル**: Job
- **タグ**: clientName
- **フォーマット**:
  ```
  【clientName：projectName】description

  > Start：April 3, 2026 at 12:00 PM
  > End：April 3, 2026 at 2:00 PM
  > 作業時間：2.0h

  Location：ウィズハイム天神山
  ```
- コードは `tools/n8n-fix-code-in-javascript.js` に保存

## 起動方法

### 自動起動（LaunchAgent）

Mac起動時にn8nが自動的に起動するよう、LaunchAgentで設定済み。

- **plistファイル**: `~/Library/LaunchAgents/com.n8n.server.plist`
- **RunAtLoad**: ログイン時に自動起動
- **KeepAlive**: クラッシュ時に自動再起動
- **環境変数**: `NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs` を設定済み
- **ログ**: `/tmp/n8n.log`, `/tmp/n8n-error.log`

```bash
# LaunchAgent停止（n8nを止めたい時）
launchctl unload ~/Library/LaunchAgents/com.n8n.server.plist

# LaunchAgent起動
launchctl load ~/Library/LaunchAgents/com.n8n.server.plist
```

### 手動起動

LaunchAgentを使わず手動で起動する場合：

```bash
NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs n8n start &
```

**重要**: `NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs` が必要。
この環境変数がないとDay One CLIの実行（child_process）とファイル書き込み（fs）が制限される。

### n8n 停止

```bash
# LaunchAgent経由の場合
launchctl unload ~/Library/LaunchAgents/com.n8n.server.plist

# 手動起動の場合
pkill -f "n8n"
```

### 起動確認

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5678
# 200 が返れば起動中
```

### デバッグモードで起動

問題発生時はLaunchAgentを停止してからデバッグモードで手動起動する：

```bash
launchctl unload ~/Library/LaunchAgents/com.n8n.server.plist
NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs N8N_LOG_LEVEL=debug n8n start > /tmp/n8n-debug.log 2>&1 &
```

ログ確認：
```bash
tail -f /tmp/n8n-debug.log
```

## 認証情報

### Clockify API
- Header Auth: `X-Api-Key`
- ワークスペース名: kiwami
- ワークスペースID: `684043134d7e18788e95a3d5`
- ユーザーID: `684043134d7e18788e95a3d4`

### Google Calendar OAuth2
- Google Cloud Console でOAuthクライアントを作成済み
- リダイレクトURI: `http://localhost:5678/rest/oauth2-credential/callback`
- カレンダー: clockify

### Day One CLI
- パス: `/usr/local/bin/dayone`
- インストール: `sudo bash /Applications/Day\ One.app/Contents/Resources/install_cli.sh`

## トラブルシューティング

### ワークフローが自動実行されない

1. n8nが起動しているか確認
   ```bash
   pgrep -f "n8n" && echo "running" || echo "not running"
   ```

2. ワークフローがPublish済みか確認
   ```bash
   sqlite3 ~/.n8n/database.sqlite "SELECT name, active FROM workflow_entity;"
   ```

3. デバッグモードで起動してログを確認

### 重複登録が発生する

`/tmp/n8n_clockify_last_id.txt` を削除してリセット：
```bash
rm /tmp/n8n_clockify_last_id.txt
```
※リセット後の最初のポーリングでは、最新10件が全て新規として処理される点に注意。
不要な重複が発生した場合はGoogle Calendar・Day Oneから手動削除が必要。

### エントリが登録されない（取りこぼし）

1. page-sizeが`10`になっているか確認（`1`だと複数エントリの取りこぼしが発生する）
2. Filter New / Code in JavaScript の Execute Once が OFF になっているか確認
3. Clockify APIのタイムアウト → HTTP Requestの Retry on Fail が有効か確認
4. タイマー実行中のエントリは意図的に除外される。タイマーを停止してから確認

### Day One CLIが動かない

```bash
/usr/local/bin/dayone --version
```
バージョンが表示されない場合は再インストール：
```bash
sudo bash /Applications/Day\ One.app/Contents/Resources/install_cli.sh
```

### Google Calendar認証エラー

n8n管理画面（http://localhost:5678）でGoogle Calendar credentialを再認証する。
Google Cloud ConsoleのリダイレクトURIが `http://localhost:5678/rest/oauth2-credential/callback` になっているか確認。

## 旧システムからの移行

| 項目 | 旧（Zapier） | 新（n8n） |
|------|-------------|-----------|
| 実行環境 | クラウド | ローカル（Mac） |
| コスト | 有料 | 無料 |
| 連携先 | Google Calendar のみ | Google Calendar + Day One |
| データ | 外部サーバー経由 | ローカル完結 |
