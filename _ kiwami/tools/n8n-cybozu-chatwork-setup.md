# サイボウズOffice → n8n → Chatwork 通知連携セットアップ

> **🔗 関連コンテンツ（本命セットアップ）**
> - 📘 n8n手順: [[_ kiwami/README/n8n.md]]
> - 📨 サイボウズメッセージ手順: [[_ kiwami/README/cybozuメッセージ.md]]
> - 🛑 停止条件および停止手順: [[_ kiwami/README/停止条件および停止手順.md]]
> - 📝 Chatwork API申請メモ: [[_ kiwami/_tmp/Chatwork API申請.md]]
> - 📨 サイボウズ未読→Chatwork通知 草案: [[_ kiwami/_tmp/サイボウズOffice 未読メッセージ → Chatwork 通知の概要（案）.md]]

## 概要

サイボウズOffice（クラウド版）の「未読一覧」を n8n で定期監視し、新着通知を Chatwork に自動転送する。

```
[10分おき] → [サイボウズにログイン] → [未読一覧取得] → [HTML解析・重複排除] → [Chatwork送信]
```

## 前提

- サイボウズOffice クラウド版（https://linkstaff.cybozu.com/）
- サイボウズOfficeの「お知らせ」はメール通知の対象外のため、未読一覧ページをスクレイピングする方式
- メール通知で対応可能なのは「予定」「電話メモ」「ワークフロー」の3つのみ
- n8n 構築済み

## 事前準備

### 1. Chatwork APIトークンの取得（管理者の承認が必要）

1. Chatwork にブラウザでログイン
2. 右上の自分のアイコン → **「サービス連携」**
3. 左メニューの **「API Token」**
4. パスワードを入力 → **「表示」**
5. 表示されたトークンをコピーして安全に保管

### 2. Chatwork ルームIDの確認

1. Chatwork で転送先のチャットルームを開く
2. URL を確認 → `chatwork.com/#!/rid123456789`
3. `rid` のあとの数字がルームID

### 3. サイボウズOfficeのログイン情報

- ログインID
- パスワード

## n8n ワークフローの設定

### ワークフローのインポート

1. n8n で **Add workflow** → 右上メニュー → **Import from File**
2. `tools/n8n-cybozu-chatwork.json` を選択

### 各ノードに値を直接設定

Variables 機能が使えないため、各ノードに直接値を入力する。

#### 「サイボウズにログイン」ノード

- `_account` の value → サイボウズのログインID
- `_password` の value → サイボウズのパスワード

#### 「Chatworkへ送信」ノード

- URL 内の `{{$vars.CHATWORK_ROOM_ID}}` → 実際のルームID（数字）に置換
- Headers の `{{$vars.CHATWORK_API_TOKEN}}` → 実際のAPIトークンに置換

## テスト手順

### Step 1: ログイン確認

1. 「サイボウズにログイン」ノードを単体実行
2. レスポンスの headers に `set-cookie` が含まれていれば成功
3. 失敗する場合 → ログインID/パスワード、またはログインURLのパラメータ名を確認

### Step 2: 未読一覧取得確認

1. 「未読一覧を取得」ノードまで実行
2. HTML が取得できていれば成功
3. ログインページにリダイレクトされる場合 → Cookie の受け渡しを確認

### Step 3: HTML解析の調整

1. 取得した HTML の構造を確認
2. 「未読を解析・重複排除」ノードの正規表現を実際のHTML構造に合わせて修正
3. 未読アイテムが正しく抽出されるまで調整

### Step 4: Chatwork送信確認

1. 全ノードを通しで実行
2. Chatwork のルームにメッセージが届けば成功

## トラブルシューティング

| 問題 | 対処 |
|------|------|
| ログインできない | ログインURLやパラメータ名（`_account`, `_password`）がサイボウズの仕様と合っているか確認。ブラウザの開発者ツールで実際のログインリクエストを確認する |
| 未読一覧のHTMLが取れない | Cookie の受け渡し式 `$node['サイボウズにログイン'].json.headers['set-cookie']` が正しく動作しているか確認 |
| 通知が重複送信される | 「未読を解析」ノードの Static Data（重複排除用）がリセットされていないか確認 |
| Chatwork送信エラー | APIトークン、ルームID、APIのレート制限（5分間に100リクエスト）を確認 |

## 関連ファイル

- `tools/n8n-cybozu-chatwork.json` — n8n ワークフロー定義
