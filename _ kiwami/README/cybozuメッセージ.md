# サイボウズOffice 未読メッセージ → Chatwork 通知

> **🔗 関連コンテンツ（ツール手順書）**
> - 📨 サイボウズ未読→Chatwork通知 草案: [[_ kiwami/_tmp/サイボウズOffice 未読メッセージ → Chatwork 通知の概要（案）.md]]
> - ⚙️ n8n × サイボウズ × Chatwork セットアップ: [[_ kiwami/tools/n8n-cybozu-chatwork-setup.md]]
> - 📘 n8n手順: [[_ kiwami/README/n8n.md]]

## 概要

サイボウズOffice（クラウド版・API利用不可）の「未読一覧」ページをPlaywrightで定期監視し、個人宛メッセージの新着があればChatworkのマイチャットに通知する。

- **稼働環境**: 社内Windows機（24h稼働・2段階認証なし）
- **実行方式**: Windowsタスクスケジューラ + Node.js + Playwright
- **n8n不使用**（要件に対してオーバースペックのため）

---

## 構成図

```
[Windowsタスクスケジューラ 5分毎]
        ↓
[Node.js + Playwright スクリプト]
  ├─ ① Cybozu Office にログイン
  ├─ ② 未読一覧ページを取得
  ├─ ③ 個人宛メッセージを抽出
  ├─ ④ 前回スナップショット（JSON）と差分比較
  ├─ ⑤ 新着があれば Chatwork API に POST
  └─ ⑥ 今回のスナップショットを保存
```

---

## 必要なもの

### 環境
- Windows機（社内LANからサイボウズにアクセス可能）
- Node.js 18 以上
- Playwright（Chromium）

### 認証情報
- サイボウズOffice ログインURL
- サイボウズOffice ユーザーID / パスワード
- Chatwork APIトークン（<https://www.chatwork.com/service/packages/chatwork/subpackages/api/token.php>）
- Chatwork マイチャットの room_id

---

## ディレクトリ構成（例）

```
C:\cybozu-watcher\
├─ index.js              # メインスクリプト
├─ .env                  # 認証情報（Git管理外）
├─ state.json            # 前回の未読スナップショット
├─ package.json
└─ logs\
   └─ YYYY-MM-DD.log
```

---

## セットアップ手順

### 1. Node.js インストール
<https://nodejs.org/> から LTS 版をインストール。

### 2. プロジェクト作成
```powershell
mkdir C:\cybozu-watcher
cd C:\cybozu-watcher
npm init -y
npm install playwright dotenv axios
npx playwright install chromium
```

### 3. `.env` 作成
```
CYBOZU_URL=https://{サブドメイン}.cybozu.com/o/
CYBOZU_USER=your_user_id
CYBOZU_PASS=your_password
CHATWORK_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
CHATWORK_ROOM_ID=xxxxxxxx
```

### 4. `index.js`（雛形）
```javascript
require('dotenv').config();
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const axios = require('axios');

const STATE_FILE = path.join(__dirname, 'state.json');

async function fetchUnread() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  // ① ログイン
  await page.goto(process.env.CYBOZU_URL);
  await page.fill('input[name="_account"]', process.env.CYBOZU_USER);
  await page.fill('input[name="_password"]', process.env.CYBOZU_PASS);
  await page.click('button[type="submit"]');
  await page.waitForLoadState('networkidle');

  // ② 未読一覧ページへ遷移（※実際のURL/セレクタは要調査）
  await page.goto(`${process.env.CYBOZU_URL}?page=UnreadIndex`);
  await page.waitForLoadState('networkidle');

  // ③ 個人宛メッセージ抽出（※セレクタは実画面で確認）
  const items = await page.$$eval('.unread-message-item', els =>
    els.map(el => ({
      id: el.dataset.id,
      title: el.querySelector('.title')?.textContent?.trim(),
      from: el.querySelector('.from')?.textContent?.trim(),
      url: el.querySelector('a')?.href,
    }))
  );

  await browser.close();
  return items;
}

function loadState() {
  if (!fs.existsSync(STATE_FILE)) return [];
  return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
}

function saveState(items) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(items, null, 2));
}

async function notifyChatwork(newItems) {
  const body =
    '[info][title]サイボウズ 新着メッセージ[/title]' +
    newItems
      .map(i => `・${i.from}: ${i.title}`)
      .join('\n') +
    '[/info]';

  await axios.post(
    `https://api.chatwork.com/v2/rooms/${process.env.CHATWORK_ROOM_ID}/messages`,
    new URLSearchParams({ body }),
    { headers: { 'X-ChatWorkToken': process.env.CHATWORK_TOKEN } }
  );
}

(async () => {
  try {
    const current = await fetchUnread();
    const previous = loadState();
    const prevIds = new Set(previous.map(i => i.id));
    const newItems = current.filter(i => !prevIds.has(i.id));

    if (newItems.length > 0) {
      await notifyChatwork(newItems);
      console.log(`[${new Date().toISOString()}] ${newItems.length}件通知`);
    }

    saveState(current);
  } catch (e) {
    console.error(e);
    process.exit(1);
  }
})();
```

### 5. 動作確認
```powershell
node index.js
```

### 6. タスクスケジューラ登録
- **プログラム**: `node.exe`
- **引数**: `C:\cybozu-watcher\index.js`
- **開始場所**: `C:\cybozu-watcher`
- **トリガー**: 5分ごとに繰り返し

---

## 事前調査が必要な項目

実装前に以下を実ブラウザのDevToolsで確認する必要があります。

| 項目 | 内容 |
|---|---|
| ログインフォーム | `input` の `name` 属性、送信ボタンのセレクタ |
| 未読一覧URL | `?page=UnreadIndex` 等の実際のパス |
| 未読メッセージのHTML構造 | リストアイテムのクラス名、データ属性 |
| 個人宛の判定方法 | 「宛先」列の表示、アイコン、属性など |
| セッション維持 | ログイン後のCookie有効期限 |

---

## 想定される課題と対策

| 課題 | 対策 |
|---|---|
| ログインCSRFトークン | Playwrightなら自動処理されるので基本問題なし |
| HTML構造の変更 | サイボウズアップデート時にセレクタ調整が必要 |
| 5分間に複数メッセージ | 差分検出で全件まとめて1通知に集約 |
| 一覧ページに未読が多すぎて途切れる | ページング対応 or 件数上限を設ける |
| ブラウザプロセスの残留 | 必ず `browser.close()` を try/finally で |
| 長時間セッション切れ | 毎回ログインする設計で回避済み |

---

## 次のステップ

1. 本方式でGOサイン
2. Windows機にNode.js + Playwright導入
3. 実画面のHTML構造調査（セレクタ特定）
4. スクリプト実装・手動実行テスト
5. タスクスケジューラ登録・本番運用
