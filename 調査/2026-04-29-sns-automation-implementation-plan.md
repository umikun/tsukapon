---
created: 2026-04-29
tags: [調査, sns自動化, n8n, bluesky, 実装計画]
source: "調査/2026-04-29-postiz-sns-automation-overview.md"
---

# n8n × Bluesky/X/Threads 自動投稿 実装計画書（Phase 1〜3）

> **🔗 関連コンテンツ**
> - 📋 出発点となる調査ノート: [[2026-04-29-postiz-sns-automation-overview]]
> - ⚙️ ローカルn8n環境: [[_ kiwami/README/n8n.md]]
> - 🛠 既存n8nワークフロー参考: [[_ kiwami/tools/n8n-cybozu-chatwork-setup.md]]
> - 🐦 入力対象X日次: [[SNS運用/post/day95.md]]
> - 🧵 入力対象Threads日次: [[SNS運用/threads/Threads-day95.md]]
> - 📅 入力対象アクションプラン: [[SNS運用/action-20260429.md]]

## 🎯 ゴール

X・Threads・Blueskyの3媒体への投稿を、ローカル稼働中のn8nから自動化する。**学習しながら段階的に**作って、いきなり全部動かそうとしない。

## 📐 全体ロードマップ

| Phase | 内容 | 期間 | 所要 | 状態 |
|---|---|---|---|---|
| **Phase 1** | Bluesky 単発自動投稿（朝/夜） | 今週末 | 4〜6時間 | ⬜ 未着手 |
| **Phase 2** | X 単発自動投稿（朝/夜）+ pay-per-use設定 | GW明け | 1日 | ⬜ 未着手 |
| **Phase 3** | Threads 単発自動投稿（要Tech Provider Verification） | 5〜6月 | 2〜3週間 | ⬜ 未着手 |
| **Phase 4** | 連投シリーズ（4連投スレッド）の自動化 | 検証後 | 半日 | ⬜ 未着手 |
| **Phase 5** | 画像添付の自動化 | 検証後 | 半日 | ⬜ 未着手 |

---

## 🚀 Phase 1: Bluesky 単発自動投稿

### スコープ

- **対象**: `SNS運用/threads/Threads-day{N}.md` の `## 投稿①（朝）` と `## 投稿②（夜）`
  - Bluesky上限が300字なので、X版（140字想定）よりThreads版（短文型）の流用が相性◎
- **時刻**: 朝12:00 / 夜22:15（Threadsの投下時刻と同一）
- **画像**: なし（Phase 5で対応）
- **連投**: なし（Phase 4で対応）

### 完成イメージ

```
[毎朝12:00 LaunchAgent経由でMacが起きてる]
  → n8n Schedule Trigger 発火
  → SNS運用/threads/ から最新Threads-day*.md を選定
  → 投稿①（朝）の本文を抽出
  → Bluesky API で投稿
  → ログを _ kiwami/tools/daily-log/sns-posts/2026-04-29.jsonl に追記
  → 失敗時は Chatwork通知
```

---

## 📋 Step 0: 事前準備（30分） ✅ 完了 (2026-04-29)

> ✅ 旧アカ削除 → `chackwill.bsky.social` で新規作成 → App password 発行 完了
>
> **アカウント情報（公開可）**:
> - Handle: `chackwill.bsky.social`
> - DID: `did:plc:zmfjwhfdajd2spph3kiipgzy`
> - createSession 認証テスト: ✅ 成功（2026-04-29）

### 0-1. 旧Blueskyアカウントの完全削除

> ⚠️ **削除は不可逆**。フォロー履歴・投稿は完全に消える。あなたの希望どおり進む前提で進行。

**手順:**

1. [bsky.app](https://bsky.app) にログイン
2. **Settings → Account → Delete account**
3. パスワード入力 + メール確認コード入力
4. 削除実行
5. ログアウト確認

### 0-2. 同じメアドで新規アカウント作成

1. シークレットウィンドウで [bsky.app](https://bsky.app) → **Create new account**
2. メアド入力（旧アカと同じ）+ 強いパスワード
3. **ハンドル取得**: `chackwill.bsky.social`（X/noteと統一）が空いていれば取得
4. 取得後すぐログイン

### 0-3. プライバシー設定（必須）

新アカでログイン後、以下を**すぐ**実施:

- [ ] **Settings → Privacy and security → Discoverable by email** を **OFF**
- [ ] **Settings → Privacy and security → Logged-out visibility** を**用途に応じて選択**（公開運用なら ON のまま）
- [ ] プロフィール画像: X/note と同一画像
- [ ] 自己紹介文: X/note と同一トーン（AI/テック発信であることを明記）
- [ ] バナー画像: あれば統一

### 0-4. App Password 発行

1. **Settings → Privacy and security → App passwords**
2. **Add app password**
3. 名前: `n8n-auto-post`
4. 発行された `xxxx-xxxx-xxxx-xxxx` 形式のpasswordを**メモ**（再表示不可）
5. ハンドル `chackwill.bsky.social` と App password をペアでメモ

> 📝 **App password の権限**: 投稿・読み取り権限のみ。DM操作、設定変更、削除は不可。漏洩しても限定的被害なのでn8nに渡してOK。

### 0-5. X/note プロフィール更新

- [ ] X プロフィールに `🦋 chackwill.bsky.social` を追加
- [ ] note プロフィールに同様にBlueskyリンク追加
- [ ] スレッドの誘導文に「Blueskyでも発信中」を入れる検討（Phase 1安定後）

---

## 🏗 Step 1: n8n クレデンシャル登録（10分）

### 1-1. n8n管理画面を開く

```bash
# n8n が起動中か確認
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5678
# 200 が返ればOK
```

ブラウザで [http://localhost:5678](http://localhost:5678) を開く。

### 1-2. Bluesky 用クレデンシャルを2つ作成

**n8n左メニュー → Credentials → Add Credential**

#### クレデンシャル①: `bluesky-handle`

- Type: **Generic Credential Type → Header Auth** ではなく、**Variable** で作る方がシンプル
- 実は n8n の Variables（Settings → Variables）に登録するのが運用上ラク
  - `BLUESKY_HANDLE`: `chackwill.bsky.social`
  - `BLUESKY_APP_PASSWORD`: `xxxx-xxxx-xxxx-xxxx`

> 既存のClockifyワークフローでもVariablesは使ってないので、ここで初めて触る形になる。一度設定すればワークフロー間で使い回せる。

> 📝 **代替案**: Variablesがn8nのプランで使えない場合（無料セルフホスト版で機能制限あり）、**Code Node 内で `process.env.BLUESKY_HANDLE` を読む**方式に切り替える。LaunchAgent の plist に環境変数として書く。

---

## 🔧 Step 2: ワークフロー作成（90分）

### 2-1. 新規ワークフロー追加

n8n管理画面で **Add workflow** → 名前 `sns-bluesky-daily-poster`

### 2-2. ノード構成（全体図）

```
[1] Schedule Trigger（朝12:00）─┐
                                ├→ [3] Code: 今日のファイルパス算出
[2] Schedule Trigger（夜22:15）─┘     ↓
                                    [4] Read File: Threads-day{N}.md
                                      ↓
                                    [5] Code: 投稿①or②の本文抽出
                                      ↓
                                    [6] HTTP Request: Bluesky createSession
                                      ↓
                                    [7] HTTP Request: Bluesky createRecord
                                      ↓
                                    [8] Code: ログ追記
                                      ↓
                                    [Error Trigger → Chatwork通知]
```

### 2-3. 各ノードの詳細設定

#### [1] Schedule Trigger（朝枠）

- **Trigger Interval**: Days
- **Trigger At Hour**: 12
- **Trigger At Minute**: 0
- **Timezone**: Asia/Tokyo
- **Output**: 後続ノードに `slot: 'morning'` を渡せるように、Set Node を間に挟むか、Code Nodeで判定

> 💡 **小技**: Schedule Triggerは出力データを持たないので、後続のCode Nodeで「現在時刻から朝/夜を判定」させると分岐がきれい

#### [2] Schedule Trigger（夜枠）

- 同じ設定で時刻のみ変更
- **Trigger At Hour**: 22
- **Trigger At Minute**: 15

#### [3] Code: 今日のファイルパス算出 + 朝/夜判定

```javascript
// n8n Code Node (JavaScript)
const VAULT_ROOT = '/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon';
const fs = require('fs');
const path = require('path');

// 朝/夜判定: 現在時刻のhourで分岐（12時台 = 朝、22時台 = 夜）
const now = new Date();
const jstHour = (now.getUTCHours() + 9) % 24;
const slot = jstHour < 18 ? 'morning' : 'evening';

// 最新の Threads-day{N}.md を取得（更新日時でソート）
const threadsDir = path.join(VAULT_ROOT, 'SNS運用/threads');
const files = fs.readdirSync(threadsDir)
  .filter(f => /^Threads-day\d+\.md$/.test(f))
  .map(f => ({
    name: f,
    mtime: fs.statSync(path.join(threadsDir, f)).mtime,
  }))
  .sort((a, b) => b.mtime - a.mtime);

if (files.length === 0) {
  throw new Error('Threads-day*.md が見つかりません');
}

const latestFile = path.join(threadsDir, files[0].name);

return [{
  json: {
    slot,                              // 'morning' or 'evening'
    filePath: latestFile,              // 絶対パス
    fileName: files[0].name,           // ファイル名のみ
    runDate: now.toISOString().slice(0, 10),  // YYYY-MM-DD
  },
}];
```

> 💡 既存のClockifyワークフローでも `child_process` と `fs` を使っている（Day One CLI実行のため）。**LaunchAgent の plist に `NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs` が設定済み**なのでそのまま使える。

#### [4] Read File: Threads-day{N}.md

n8nの **"Read Binary File"** ノード を使う。

- **File Path**: `={{ $json.filePath }}`
- **Property Name**: `data`

または **"Execute Command"** ノードで:
- **Command**: `=cat "{{ $json.filePath }}"`

> 📝 **iCloud `.icloud` プレースホルダ問題**: Vaultが iCloud Drive 上にあるため、ファイルが「ダウンロード待ち」状態の可能性がある。事前に `brctl download` で強制同期させる安全策を Step 3 で追加する。

#### [5] Code: 投稿①or②の本文抽出

```javascript
// n8n Code Node (JavaScript)
const slot = $('Code: 今日のファイルパス算出').item.json.slot;
const fileContent = $input.first().binary
  ? Buffer.from($input.first().binary.data.data, 'base64').toString('utf-8')
  : $input.first().json.stdout;  // Execute Command の場合

// セクションヘッダーの正規表現
const headerRegex = slot === 'morning'
  ? /## 投稿①（朝）([\s\S]*?)(?=^##|\Z)/m
  : /## 投稿②（夜）([\s\S]*?)(?=^##|\Z)/m;

const match = fileContent.match(headerRegex);
if (!match) {
  throw new Error(`セクション「投稿${slot === 'morning' ? '①（朝）' : '②（夜）'}」が見つかりません`);
}

// 本文クリーンアップ
function cleanBody(rawSection) {
  return rawSection
    .split('\n')
    .filter(line => !line.trim().startsWith('>'))  // callout（メモ・サムネ文言・画像注釈）除外
    .filter(line => !/^-{3,}$/.test(line.trim()))  // 区切り線除外
    .join('\n')
    .trim();
}

const text = cleanBody(match[1]);

// Bluesky文字数制限（300字）の検証
const grapheme = [...text].length;
if (grapheme > 300) {
  throw new Error(`本文が${grapheme}文字でBluesky上限300字を超過。Threads-dayファイルを短縮してください。`);
}

if (!text || text.length < 10) {
  throw new Error('本文が空 or 短すぎます。Threads-dayファイルの該当セクションを確認してください。');
}

return [{
  json: {
    text,
    grapheme,
    slot,
    sourceFile: $('Code: 今日のファイルパス算出').item.json.fileName,
  },
}];
```

#### [6] HTTP Request: Bluesky createSession

- **Method**: POST
- **URL**: `https://bsky.social/xrpc/com.atproto.server.createSession`
- **Authentication**: なし
- **Body Content Type**: JSON
- **Body**:
  ```json
  {
    "identifier": "{{ $vars.BLUESKY_HANDLE }}",
    "password": "{{ $vars.BLUESKY_APP_PASSWORD }}"
  }
  ```
- **Response**: JSON（accessJwt, refreshJwt, did, handleが返る）

> 💡 **Variables機能が使えない場合**: Body内に直書きするか、Code Nodeで `process.env.BLUESKY_HANDLE` を読んで設定する。直書きはセキュリティ的に避けたい。

#### [7] HTTP Request: Bluesky createRecord（投稿）

- **Method**: POST
- **URL**: `https://bsky.social/xrpc/com.atproto.repo.createRecord`
- **Authentication**: Generic Credential Type → **Header Auth**
  - Header Name: `Authorization`
  - Header Value: `Bearer {{ $('HTTP Request: createSession').item.json.accessJwt }}`
- **Body Content Type**: JSON
- **Body**:
  ```json
  {
    "repo": "{{ $('HTTP Request: createSession').item.json.did }}",
    "collection": "app.bsky.feed.post",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": "{{ $('Code: 本文抽出').item.json.text }}",
      "createdAt": "{{ $now.toISO() }}"
    }
  }
  ```

#### [8] Code: ログ追記

```javascript
// n8n Code Node (JavaScript)
const fs = require('fs');
const path = require('path');

const LOG_DIR = '/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon/_ kiwami/tools/daily-log/sns-posts';

// ディレクトリ作成（再帰）
fs.mkdirSync(LOG_DIR, { recursive: true });

const today = new Date().toISOString().slice(0, 10);
const logFile = path.join(LOG_DIR, `${today}.jsonl`);

const postResult = $('HTTP Request: createRecord').item.json;
const sourceData = $('Code: 本文抽出').item.json;

const logEntry = {
  timestamp: new Date().toISOString(),
  platform: 'bluesky',
  slot: sourceData.slot,
  source_file: sourceData.sourceFile,
  text: sourceData.text,
  text_length: sourceData.grapheme,
  uri: postResult.uri,        // at://did:plc:xxx/app.bsky.feed.post/xxx
  cid: postResult.cid,
  status: 'success',
};

fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n', 'utf-8');

return [{ json: logEntry }];
```

#### [9] Error Trigger（別ワークフロー or Error Workflow設定）

n8nの **Error Workflow** 機能を使う。`sns-bluesky-daily-poster` のSettingsから:

- **Error Workflow**: 既存の Cybozu→Chatwork 通知ワークフローを参考に、新規 `sns-error-notifier` を作る

エラー通知の中身:
```javascript
const errorMessage = `[Bluesky自動投稿エラー] ${$json.execution.error.message}`;
// → ChatworkかDiscordに送信
```

または、簡易的に **Slack/Chatwork通知HTTP Request ノード** を Error Trigger 内に直接置く形でもOK。

---

## 🛡 Step 3: iCloud同期の事前ダウンロード（10分）

vault が iCloud Drive 上にあるため、`Threads-day*.md` が `.icloud` プレースホルダ状態の可能性がある。**毎朝11:30に強制ダウンロード** するLaunchAgentを追加する。

### 3-1. シェルスクリプト作成

ファイル: `~/bin/icloud-download-vault.sh`

```bash
#!/bin/bash
VAULT="/Users/fukuokase/Library/Mobile Documents/iCloud~md~obsidian/Documents/Tsukapon"
brctl download "$VAULT/SNS運用/post" 2>&1 | head -20
brctl download "$VAULT/SNS運用/threads" 2>&1 | head -20
brctl download "$VAULT/SNS運用" 2>&1 | grep -i "action-" | head -5
echo "[$(date)] iCloud download completed" >> /tmp/icloud-download.log
```

実行権限:
```bash
chmod +x ~/bin/icloud-download-vault.sh
```

### 3-2. LaunchAgent plist 作成

ファイル: `~/Library/LaunchAgents/com.icloud.vault-download.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.icloud.vault-download</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/fukuokase/bin/icloud-download-vault.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
    <dict>
      <key>Hour</key>
      <integer>11</integer>
      <key>Minute</key>
      <integer>30</integer>
    </dict>
    <dict>
      <key>Hour</key>
      <integer>21</integer>
      <key>Minute</key>
      <integer>45</integer>
    </dict>
  </array>
  <key>StandardOutPath</key>
  <string>/tmp/icloud-download.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/icloud-download.error.log</string>
</dict>
</plist>
```

### 3-3. 登録

```bash
launchctl load ~/Library/LaunchAgents/com.icloud.vault-download.plist
launchctl list | grep icloud
```

---

## 🌙 Step 4: Macスリープ防止（5分）

夜22:15の投稿を確実に動かすため、**夜の時間帯だけスリープ防止**するLaunchAgentを追加。

### 4-1. シェルスクリプト

ファイル: `~/bin/caffeinate-evening.sh`

```bash
#!/bin/bash
# 21:00〜23:00 の2時間スリープ防止
caffeinate -i -t 7200 &
echo "[$(date)] caffeinate started for 2h" >> /tmp/caffeinate.log
```

### 4-2. LaunchAgent

ファイル: `~/Library/LaunchAgents/com.caffeinate.evening.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.caffeinate.evening</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/fukuokase/bin/caffeinate-evening.sh</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>21</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
</dict>
</plist>
```

```bash
launchctl load ~/Library/LaunchAgents/com.caffeinate.evening.plist
```

> 💡 朝12:00 はほぼ確実に作業中なのでスリープ防止不要。夜だけで十分。

---

## 🧪 Step 5: テスト手順（30分）

### 5-1. ノード単体テスト

n8n管理画面で各ノードを **Execute Node** で順に試す:

1. **Code: ファイルパス算出** → 出力が `slot: 'morning' or 'evening'`、`filePath` が正しいか
2. **Read File** → ファイル内容が取得できるか
3. **Code: 本文抽出** → `text` がプレーンテキストで返ってくるか、文字数チェック通過するか
4. **HTTP createSession** → `accessJwt` と `did` が返ってくるか（**ここで認証エラーならApp password 確認**）
5. **HTTP createRecord** → `uri` と `cid` が返り、Bluesky上に実投稿が出るか
6. **Code: ログ追記** → `_ kiwami/tools/daily-log/sns-posts/YYYY-MM-DD.jsonl` に1行追加されるか

### 5-2. 投稿テスト用の安全策

本番投稿の前に**テスト用テキストでドライラン**する:

```javascript
// Code: 本文抽出 の最後に一時的に追加
return [{
  json: {
    text: '🧪 テスト投稿です。n8n × Bluesky動作確認中。1分以内に削除します。',
    grapheme: 30,
    slot: 'test',
    sourceFile: 'TEST',
  },
}];
```

これで投稿成功を確認したら、Blueskyから手動削除し、テストコードを除去。

### 5-3. ワークフロー全体実行（手動）

n8n画面の **Execute Workflow** で全体を流す。Schedule Trigger は無視されるが、その下のCode Nodeから順に流れる。

### 5-4. Schedule Trigger の発火テスト

ワークフロー右上の **Active トグルをON**。翌日12:00と22:15に自動発火。

最初の数日は **n8n Executions タブ**で実行ログを確認。

---

## 📊 Step 6: ログ確認 & ダッシュボード（任意・後回しOK）

`_ kiwami/tools/daily-log/sns-posts/YYYY-MM-DD.jsonl` を集計するDataviewクエリ:

```dataview
TABLE WITHOUT ID
  this.timestamp AS "時刻",
  this.platform AS "媒体",
  this.slot AS "枠",
  this.text_length AS "文字数",
  this.status AS "状態"
FROM "_ kiwami/tools/daily-log/sns-posts"
SORT this.timestamp DESC
LIMIT 30
```

> ⚠️ Dataviewは `.md` ファイルが対象なので、jsonlを集計するには別ノートを作って `dataviewjs` で読み込む形になる。Phase 1ではログファイル直接 `cat` で十分。

---

## 🔁 Step 7: 段階的な拡張ポイント（Phase 2 以降）

### Phase 2: X 自動投稿の追加

- 既存ワークフローの **HTTP Request: createRecord** を**並列に複製**して X API も叩く
- X API は OAuth 2.0 PKCE 必須（n8nには Twitter v2 専用ノードあり、これ使うのが楽）
- 入力ファイルは `SNS運用/post/day{N}.md` に切り替え（X用本文）
- pay-per-use のため、月次コスト監視（クレカ使用通知 or X Developer Portal の usage 確認）

### Phase 3: Threads 自動投稿の追加

- Meta for Developers で **Tech Provider Verification** を1〜2週間かけて取得
- IG を Business/Creator アカウントに切り替え
- App Review 提出（投稿フローのスクリーンキャスト）
- 通過後、Threads Graph API の2-step（container作成→publish）を HTTP Request 2連で組む

### Phase 4: 連投スレッドの自動化

- 4連投 = 4回の `createRecord` 呼び出し
- 2投目以降は `record.reply.parent.uri` と `record.reply.root.uri` に1投目のuriを入れる
- データ元: `SNS運用/post/draft/YYYYMMDD_*.md` の `## 1/4` 〜 `## 4/4` をパース

### Phase 5: 画像添付

- Bluesky: blob upload API → record.embed.images[].image にblob CID
- X API: media upload v1.1 → media_ids
- Threads: media_url に直接URL指定（要パブリック画像URL）
- 画像保存先: `SNS運用/title/img/YYYYMMDD-{slot}.png` をリネーム規則として導入

---

## 🆘 トラブルシューティング

### ケース1: n8nでファイルが読めない（"ENOENT" エラー）

- `.icloud` プレースホルダ問題。Step 3 のLaunchAgentが動いているか確認
- 手動で `brctl download "SNS運用/threads"` を試す
- それでも読めない場合は iCloud Drive 設定で「このMacにダウンロード」を強制

### ケース2: Bluesky認証エラー（401 Unauthorized）

- App password の `xxxx-xxxx-xxxx-xxxx` 形式が正しいか（ハイフン込みでコピペ）
- ハンドルが `chackwill.bsky.social` の形式（`@` 不要）
- App password を新規発行し直す（古いの無効化）

### ケース3: 文字数制限違反

- Bluesky上限は **graphemes（書記素クラスタ）で300**。絵文字の合成形が多いと予想より長くなる
- Code Node内の `[...text].length` ではなく、より厳密には `Intl.Segmenter` を使う
  ```javascript
  const seg = new Intl.Segmenter('ja', { granularity: 'grapheme' });
  const grapheme = [...seg.segment(text)].length;
  ```

### ケース4: Macスリープ中に発火失敗

- `pmset -g log | grep -i sleep` でスリープ履歴確認
- caffeinate plistが動いてるか: `launchctl list | grep caffeinate`
- 該当時刻にMacが起きてた場合は別原因（n8n停止等）を疑う

### ケース5: 重複投稿

- ワークフローが2回発火 = Schedule Triggerが二重登録されてる可能性
- n8n Executions タブで該当時刻の実行履歴を確認
- 重複防止: ログファイル（jsonl）に当日の同slot投稿があれば skip するCode Nodeを Step 5 と Step 6 の間に追加

---

## 📝 学習メモ（Phase 1 を進めながら埋める）

### ✅ 2026-04-29 セッション1で学んだこと

- **`process.env` ではなく `$env` を使う**: n8n の Code Node では Node.js 標準の `process.env` ではなく、n8n 専用の `$env.VARIABLE_NAME` を使う。`process` オブジェクトはサンドボックスで隠されている
- **環境変数の渡し方**: LaunchAgent の plist 内 `EnvironmentVariables` dict に追加 → `launchctl unload && load` で n8n 再起動 → `$env` 経由で参照可能
- **`plutil -insert` の冪等化**: 既存キーがあるとエラーになるので `plutil -remove ... 2>/dev/null` を先に走らせる
- **HTTP Request ノードの Expression モード**: JSON Body や Header Value で `{{ }}` を使うときは Expression モードに切り替える必要あり（Fixed モードだと文字列扱い）
- **ノード間データ参照**: `{{ $('NodeName').item.json.fieldName }}` 形式で前のノードの出力を参照
- **`$now.toUTC().toISO()`**: n8n 標準の Luxon DateTime オブジェクト。Bluesky API の `createdAt` 用に UTC ISO8601 を返す
- **JSON Body 内の改行問題**: 改行を含む文字列を JSON Body に直接埋めると壊れる → Code Node 内で `JSON.stringify(text).slice(1, -1)` でエスケープ済み版（`textForJson`）を作っておくと安全
- **`fs.readFileSync` 直接利用**: LaunchAgent の `NODE_FUNCTION_ALLOW_BUILTIN=child_process,fs` のおかげで `require('fs')` が使える
- **iCloud `.icloud` プレースホルダ検出**: `fs.readdirSync` で `.Threads-day95.md.icloud` のような隠しファイルが返る → 正規表現で別途検出
- **graphemes の正確な数え方**: `Intl.Segmenter('ja', { granularity: 'grapheme' })` を使う（絵文字や合成文字を1文字として数える）
- **zsh の `read` 構文**: `read -p` は bash 専用、zsh では `read "VAR?prompt"` 形式
- **`heredoc + 変数展開` の挙動**: `<< EOF` で `${VAR}` を含むと、シェル履歴には `${VAR}` が記録され、ファイルには展開後の値が書かれる（パスワードを履歴に残さずファイルに渡せるイディオム）
- **AT Protocol の認証フロー**: createSession で `accessJwt` 取得 → createRecord で `Authorization: Bearer {accessJwt}` ヘッダ付きで叩く2段階

### ⬜ 次セッションで学ぶ予定

- [ ] Schedule Trigger（複数時刻）の設定、Active化
- [ ] LaunchAgent の StartCalendarInterval 配列指定（複数時刻）
- [ ] caffeinate コマンドの活用
- [ ] iCloud `brctl download` コマンド
- [ ] n8n の Error Workflow 機能
- [ ] Code Node からの `fs.appendFileSync` でログ追記

---

## ✅ Phase 1 完了の定義

- [x] 旧Blueskyアカウント削除完了 ✅ 2026-04-29
- [x] 新Blueskyアカウント `chackwill.bsky.social` 作成、プライバシー設定完了 ✅ 2026-04-29
- [x] App password 発行、n8n LaunchAgent環境変数 登録 ✅ 2026-04-29
- [x] curl で createSession + createRecord 動作確認 ✅ 2026-04-29
- [x] n8n から `$env` 経由で BLUESKY_HANDLE / BLUESKY_APP_PASSWORD 取得確認 ✅ 2026-04-29
- [x] n8n ワークフロー `sns-bluesky-daily-poster` の基本パイプライン作成（Manual Trigger → createSession → createRecord）、テスト投稿成功 ✅ 2026-04-29
- [x] ファイル読み込み + 本文抽出（最新Threads-day*.md → 朝/夜セクション抽出） ✅ 2026-04-29
- [x] 抽出本文での投稿テスト成功（Threads-day105.md 朝枠 → Bluesky実投稿確認 → 削除） ✅ 2026-04-29
- [ ] ログ書き出し機能追加（jsonl）
- [ ] Manual Trigger → Schedule Trigger（朝12:00 / 夜22:15）置換
- [ ] iCloud事前ダウンロード LaunchAgent 設置（11:30 / 21:45）
- [ ] caffeinate evening LaunchAgent 設置（21:00〜23:00）
- [ ] Active化、翌日12:00と22:15の自動投稿が成功
- [ ] エラー時のChatwork通知が動く（強制エラーで確認）
- [ ] X/note プロフィールに新Blueskyリンク追加

3日連続で安定稼働を確認できたら **Phase 1 完了**。Phase 2（X追加）に進む。

---

## 📚 参考資料

- [Bluesky AT Protocol Get Started](https://docs.bsky.app/docs/get-started)
- [Bluesky createRecord API](https://docs.bsky.app/blog/create-post)
- [Bluesky create app password](https://docs.bsky.app/docs/api/com-atproto-server-create-app-password)
- [n8n Bluesky workflow template](https://n8n.io/workflows/2562-simple-bluesky-multi-image-post-using-native-bluesky-api/)
- [n8n-nodes-bluesky community node](https://github.com/muench-dev/n8n-nodes-bluesky)
- [既存n8n環境ドキュメント](_%20kiwami/README/n8n.md)
- [既存Cybozu→Chatworkワークフロー](_%20kiwami/tools/n8n-cybozu-chatwork-setup.md)
