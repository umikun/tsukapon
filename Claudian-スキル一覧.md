# Claudian スキル & 機能一覧

> このvaultに組み込んだカスタムスキル・自動化・バックグラウンド機能の全体マップ。
> 迷ったらここを見れば、どの機能がどこにあるか一発でわかる。
>
> 🤖 **自動更新**: このファイルは [[CLAUDE.md]] のルール＋ `.claude/hooks/remind-skills-list.sh` により、
> スキル・自動化ファイルが変更されるたびに更新するように運用されている。

最終更新: 2026-04-25（Daily Log スタンドアロン版を大型刷新：横幅フル幅化／カテゴリ・プロジェクト円グラフ／メモ自動保存欄（vault `Daily Log/memo/YYYY-MM-DD.md`）／`oclock.svg` をファビコン化／手動記録機能を削除。サーバには `GET/POST /api/memo/...` と `GET /favicon.svg` を追加） / 2026-04-25（`POST /api/save-md/YYYY-MM-DD` を追加） / 2026-04-24（⭐ NEW: **新規/追加ファイルの自動リンク設置ルール** を [[CLAUDE.md]] に追加。vault内への新規作成・外部コピーに対し、関連ファイルを推定して `🔗 関連コンテンツ` callout を H1 直下に自動挿入。対象外は `.obsidian/` `Clippings/` `調査/` `_ kiwami/tools/daily-log/` `.claude/` 等。Daily Log 一式も引き続き運用中: `_ kiwami/tools/daily-log/` にClockify同期（15分毎）・アクティビティトラッカー（60秒毎）・ローカルWebサーバー（常駐、http://127.0.0.1:8765））

---

## 🎯 クイックリファレンス

| やりたいこと | 使うスキル | コマンド |
|---|---|---|
| noteのAIニュース記事をリライト + サムネ文言 + X記事版 + Xスレッドまで一括生成 | `re-daily` | `/re-daily 記事パス`（任意で2行目にnote記事URL） |
| note記事をXのスレッドに変換（単体実行） | `thread` | `/thread パス\nタイトル\nURL` |
| X投稿への返信を生成 | `reply` | `/reply`（対象ポストを貼り付け） |
| 週次のX運用分析 | `weekly-analytics` | `/weekly-analytics データ` |
| マークダウン記法の検査・修正 | `md-format` | `/md-format ファイルパス` または選択状態で `/md-format` |
| 引用RT下書きをmy-clone口調＋関係性キーワード反映版に書き換え | `quote-rewrite` | `/quote-rewrite 下書き本文` |
| ペーストした文章を深掘り調査してMDノート化 | `deep-dive` | `/deep-dive 調査したい本文` または選択状態で `/deep-dive` |
| 1日の作業内容を自動集計して業務日報を出力 | Daily Log（artifact） | Coworkサイドバーの「Daily Log」を開く |

---

## 📦 カスタムスキル（このvault専用）

保存場所: `.claude/commands/`

### 1. [[.claude/commands/re-daily.md|/re-daily]] — note記事リライト＋サムネ文言＋X記事版＋Xスレッド一気通貫生成 ⭐ UPDATED 2026-04-21（サムネ文言生成ステップ追加）

**用途**: 毎日のAIニュースnote記事を、SEO最適化・内容充実化し、**続けてX記事転載版とXスレッド版まで自動生成**する

**入力**:
```
記事ファイルパス
（任意）note記事URL  ← 2行目
```

- URL未指定の場合、Xスレッド側は `[noteのURL]` プレースホルダーを使用（公開後に手動差し替え）

**処理内容**:
- **Step 1〜6**: note本文のリライト
  - 過去記事との重複チェック
  - タイトルのSEO最適化 ＋ **7つの型のいずれかに当てはめる必須**（強い冒頭／具体数字／常識覆し／対比／痛み／今すぐ行動／損失回避）
  - **RT誘発**: 「上司」「同僚」「会社」などの関係性キーワードを検討
  - 冒頭の導入文統合（SEO概要＋挨拶を1ブロックに）。1文目は強い動詞で始める1秒フック
  - 目次セクション統合
  - 各ニュースに「実務観点の感想＋ポイントまとめ＋情報源リンク」
  - **保存誘発**: 各章に **1つ以上のチェックリスト or 番号付きリスト**を必須化、プロンプト例は `コピペ用` コードブロックで明記、章末に「この章を保存して〇〇する時に使って」の保存誘導を1文入れる
  - 有料記事CTAの直前に「まずは無料でnoteフォローしてもらえると〜」のフォロー誘導を追加
  - タグ5つ選定
- **Step 7**: サムネイル文言を自動生成（`SNS運用/title/title-YYYYMMDD.md`） ⭐ NEW
  - メインサムネ＋各見出しサムネの「メインタイトル（12〜20字）」「サブタイトル（20〜35字）」
  - 7つの型のいずれか＋可能なら関係性キーワード（上司／同僚／会社）
- **Step 8**: X Articles版を自動生成（`SNS運用/post/article/X-YYYYMMDD.md`）
  - 挨拶削除→X向けフック（1文目に関係性キーワード）、太字削除、「だ・である」調統一、note誘導CTA
- **Step 9**: Xスレッド版を自動生成（`thread` スキル準拠）
  - 各章を140字以内に要約、導入→各章→まとめの構成
  - **2投稿目URLは固定**: `https://note.com/chackwill`（noteクリエイタートップ / 当日記事URLは最終投稿のみ）
  - 保存先: `SNS運用/post/thread/YYYYMMDD_note紹介スレッド.md`
- **Step 10**: 完了検証と報告（4ファイル存在確認）

**出力**（1コマンドで4ファイル生成）:
1. `SNS運用/note/note-YYYYMMDD.md`（リライト上書き）
2. `SNS運用/title/title-YYYYMMDD.md`（サムネイル文言）⭐ NEW
3. `SNS運用/post/article/X-YYYYMMDD.md`（X Articles版）
4. `SNS運用/post/thread/YYYYMMDD_note紹介スレッド.md`（Xスレッド版）

**🛡 パイプライン堅牢化（2026-04-21）**:
- 冒頭に **「必須パイプライン宣言」** を追加：Step 1〜10をノンストップで走り切ることを明示
- **Step 6 末尾にリマインド**：「ここはまだ1/4の進捗。Step 7以降を続けること」
- **Step 10（完了検証と報告）を独立化**：`ls` で4ファイル存在を確認してから最終応答
- Step 6 の後に応答を終えて後続ステップをスキップする事故を防止

**連携先**: なし（`thread` の処理を内包）。単体で `thread` を使うケース（過去記事からスレッドだけ作る等）は従来どおり `/thread` を呼ぶ。

---

### 2. [[.claude/commands/thread.md|/thread]] — X スレッド生成（単体実行用） ⭐ UPDATED 2026-04-20

**用途**: note記事をX（旧Twitter）のスレッド形式に変換（`/re-daily` の Step 8 からも呼ばれる）

**入力**（3行）:
```
記事ファイルパス
note記事タイトル
note記事URL（最終投稿に使用）
```

**処理内容**:
- 記事の各章を140字以内に要約
- 8投稿構成（導入→各章触り→まとめ）
- **2投稿目URLは固定**: `https://note.com/chackwill`（noteクリエイタートップ）
- **最終投稿URLは当日記事**: 入力3行目のURL（未指定なら `[noteのURL]` プレースホルダー）
- my-clone人格データで文体調整
- 絵文字を自然に配置（1投稿1〜2個）

**出力**: `SNS運用/post/thread/YYYYMMDD_スレッド概要.md`

**使い分け**:
- 当日のnote記事を丸ごと処理 → `/re-daily`（thread生成も自動）
- 過去記事・別角度で追加スレッドが欲しい場合 → `/thread` を単体実行

---

### 3. [[.claude/commands/reply.md|/reply]] — X返信生成

**用途**: X投稿への返信コメントを生成

**入力**: 対象ポストの本文

**処理内容**:
- my-clone人格データを反映
- 共感ベース・3〜5文・絵文字1〜2個
- 「〜だよね」「〜かもなぁ」系の柔らかい語尾

**出力**: チャット内に返信案を表示

---

### 5. [[.claude/commands/md-format.md|/md-format]] — マークダウン整形 ⭐ NEW 2026-04-20

**用途**: 選択テキストまたはファイル全体のマークダウン記法を検査し、問題を修正する

**入力**（2パターン）:
```
① ファイルパス（ファイル全体を対象）
② 引数なし ＋ <editor_selection>（選択範囲のみを対象）
```

**検査・修正対象**:
- コードブロック（` ``` `）の閉じ忘れ
- 見出しレベルの飛び・前後の空行
- リスト記号の混在・インデントの不整合
- 番号付きリストの順序ずれ
- `**` `*` `` ` `` の閉じ忘れ
- テーブルの列数不一致・区切り行の欠落
- 過剰な空行（3行以上 → 2行に圧縮）
- リンク記法の括弧閉じ忘れ
- Obsidian独自記法（`[[]]` `![[]]` `%%`）・Dataviewブロックは変更しない

**出力**:
- 修正差分をチャット内に表示（修正理由付き）
- ファイルに上書き保存
- 修正0件の場合も「問題は見つかりませんでした」と報告

---

### 6. [[.claude/commands/quote-rewrite.md|/quote-rewrite]] — 引用RT下書きのmy-clone口調書き換え ⭐ NEW 2026-04-23

**用途**: 複数の引用RT下書きをmy-clone人格の口調に書き換え、冒頭に関係性キーワード（上司／会社／同僚／部下／取引先）を差し込んで、X規約・安全運用ルール準拠の最終版として保存する。W17統合運用フローの「朝の引用RT下書き生成」工程をスキル化したもの。

**入力**（3パターン対応）:
```
A: 【1番への引用RT下書き】〜 の番号ラベル付き複数下書き
B: フリーテキスト（1本のみ）
C: 【引用元URL】＋【下書き】形式
```

**処理内容（8ステップ）**:
1. 人格データ・運用ルールの読み込み（[[_ kiwami/my-clone/voice/口調パターン.md]] / [[_ kiwami/my-clone/voice/NGワード.md]] / [[CLAUDE.md]] / [[SNS運用/Threads運用.md]] / 最新のW番号統合運用フロー）
2. 下書き解析（N本切り出し・訴求把握・AI臭／属性主張スキャン）
3. my-clone口調への書き換え（です・ます基調＋感嘆符1〜2個＋カジュアル崩し＋絵文字ワンポイント、自己属性主張／男言葉／AI定型句／断言誇大系を除去）
4. 関係性キーワードの差し込み（冒頭1文目、3本以上は異なるキーワードを振り分け）
5. 7つの型の判定（2つの型の掛け合わせ推奨）
6. 文字数チェック（140字以内／90字未満なら体験談・数字で補強）
7. 出力ファイル生成（`SNS運用/post/draft/YYYYMMDD_quote_draft.md`、同日複数回は時刻付きセクションで共存）
8. チャット最終報告（本文コピペ用／字数・キーワード・型／wikilink／次のアクション）

**出力**: `SNS運用/post/draft/YYYYMMDD_quote_draft.md`
- W番号テーマ・運用ルール・投稿前チェック欄を自動付与
- 各下書きごとに「字数／関係性キーワード／採用型」を明記
- 末尾に5項目の投稿前チェックリストを必須付与

**安全運用の絶対ルール**:
- 自動投稿は絶対に提案しない（「手動で投稿ボタン」明記）
- 同じ関係性キーワードの連投禁止（複数本時は分散）
- 1日3本以内の推奨を出力内に記載
- [[Clippings/Post by @kuso_inc on X.md]] の大量自動化系は取り込まない

**連携先**: [[SNS運用/analytics/W17-Claude統合運用フロー.md]]（本スキルは"朝の④B引用RT下書き生成"の実行装置）

---

### 7. [[.claude/commands/deep-dive.md|/deep-dive]] — ペースト文章の深掘り調査ノート生成 ⭐ NEW 2026-04-23

**用途**: ペーストされた文章・エディタ選択・ブラウザ選択を対象に、WebSearch+WebFetchで背景・最新動向・ファクトチェック・反対意見・関連概念を調査し、1枚のマークダウン調査ノートに仕上げる。「読んだけど腹落ちしてない」テキストを投入して、理解を厚くするための調査スキル。

**入力**（3パターン対応）:
```
A: /deep-dive 調査したい本文をそのまま貼り付け（複数段落OK）
B: 引数なし ＋ <editor_selection>（選択範囲のみを対象。出典としてファイルパスも記録）
C: 引数なし ＋ <browser_selection>（ブラウザの選択を対象。URL/タイトルを出典に記録）
```

**処理内容（8ステップ）**:
1. 対象テキストの取得と正規化（入力パターン判定・`topic_slug` 生成・出典情報の記録）
2. 構造解析（主題／キーワード／主張／暗黙の前提／疑問点／時制情報の抽出）
3. 調査計画の策定（背景・最新動向・ファクトチェック・反対意見・関連概念の5観点でクエリ3〜6本）
4. 外部情報の収集（WebSearch＋WebFetchで一次情報優先。URLと取得日を必須記録、内部知識だけでの断定禁止）
5. 調査ノートの組み立て（TL;DR／元テキスト抜粋／キーワード早見表／背景／ファクトチェック表／最新動向／関連概念／反対意見／残る疑問／参考資料／メモの11セクション構成）
6. 保存（`調査/YYYY-MM-DD-{topic_slug}.md`、同日衝突時は `-2`, `-3` で回避）
7. チャット内サマリ提示（wikilink＋TL;DR＋ハイライト3点＋次アクション案）
8. 自己検証（ソースURL最低3本／ファクトチェック🔍未確認の比率／元テキスト曲解なし／AI定型文なし）

**出力**: `調査/YYYY-MM-DD-{topic_slug}.md`
- フロントマターに `created` / `tags` / `source` を自動付与
- 各「最新動向」項目にURLと年月を必須付与
- 参考資料セクションにソースURL＋取得日を記載

**命名規則**: 日本語テーマでも英語slug優先（例: 「MCP Serverの最新動向」→ `mcp-server-trends`）

**制約**:
- ソースURLのない断定は書かない（内部知識で補うときは "一般に〜" 等のヘッジ語）
- チャット内だけで完結せず、必ずファイル保存
- Obsidian独自記法（`[[]]`）でvault内関連ノートへリンク
- AIっぽい硬い結び（「いかがでしたか」等）は書かない

**連携先**: `re-daily`（調査結果をnote記事に反映）、`thread`（調査ノートから単体でスレッド化）、`quote-rewrite`（調査したトピックを引用RT用に再構成）

---

### 4. [[.claude/commands/weekly-analytics.md|/weekly-analytics]] — 週次分析 ⭐ NEW

**用途**: X運用の週次データを分析し、次週の改善アクションを提案

**入力**（3パターン対応）:
- A: データ直接貼り付け
- B: データファイルパス
- C: 空入力（対話モードで質問）

**処理内容**:
- エンゲージメント率・保存率・プロフアクセス率を計算
- TOP3 / WORST3 を抽出、型・時間帯・フックを分析
- 4指標で総合判定（良好/要改善）
- 来週のアクション3つを具体的に提示
- WORST3のBefore/Afterリライト
- 他スキル連携提案（re-daily / thread へ流す内容）

**出力**: `SNS運用/analytics/YYYY-WNN.md`

**連携先**: `re-daily`（分析結果をnote記事に反映）、`thread`（伸びた投稿のスレッド化）

---

## 📚 参考データファイル（スキルが読む資料）

### 人格・ブランド

| ファイル | 役割 | 保存場所 |
|---|---|---|
| `my-clone/` | 文体・人格データ（全スキルが参照） | `_ kiwami/my-clone/` |

### 運用戦略

| ファイル | 役割 |
|---|---|
| [[SNS運用/post/フォロワー改善.md]] | フォロワー獲得のCTA・ハッシュタグ戦略 |
| [[SNS運用/post/Xへ記事転載.md]] | X Articles（記事転載）の戦略・変換ルール |

### 過去記事アーカイブ

| 場所 | 内容 |
|---|---|
| `SNS運用/note/note-YYYYMMDD.md` | 毎日のnote記事（リライト対象） |
| `SNS運用/post/day*.md` | 日次X投稿のドラフト |
| `SNS運用/post/article/X-YYYYMMDD.md` | XのArticles版 |
| `SNS運用/post/thread/` | Xスレッド保存先 |
| `SNS運用/analytics/` | 週次分析レポート |

---

## ⚙️ バックグラウンド機能（自動化）

### 📋 スキル一覧の自動更新（hook + CLAUDE.md）

**仕組み**: 2層のセーフティネットで、スキル/自動化ファイル変更時に本ファイルの更新を強制する。

| 層 | ファイル | 役割 |
|---|---|---|
| 宣言ルール | [[CLAUDE.md]] | Claudeが毎セッション冒頭で読むルールブック |
| 実行時hook | `.claude/hooks/remind-skills-list.sh` | PostToolUse hookで更新リマインダーを発火 |
| hook登録 | `.claude/settings.json` | hookを `Write\|Edit` ツールの後に実行するよう設定 |

**発火条件**（Write/Edit したファイルが以下に該当すると発動）:

- `.claude/commands/*.md` — カスタムスキル追加/編集
- `~/Library/LaunchAgents/*.plist` — launchd自動化追加/編集
- `~/bin/*.sh` — シェル自動化追加/編集
- `.mcp.json` — MCPサーバー設定変更

**発火時の挙動**: Claudeに「Claudian-スキル一覧.mdを更新せよ」というsystem-reminderが注入される。完了報告に「📋 スキル一覧を更新しました」を含めるよう義務付け。

---

### 🔗 新規/追加ファイルの自動リンク設置（CLAUDE.md絶対ルール）

**宣言場所**: [[CLAUDE.md]] の「🔗 絶対ルール: 新規・追加ファイルには可能な限りObsidianリンクを自動設置する」セクション

**発火条件**:
- vault内に `.md` を新規作成した時（Write / Bash heredoc 経由も対象）
- 外部から vault に `.md` がコピー/移動されてきた時
- ユーザーが「追加した」「コピーしてきた」と宣言した時
- フォルダ単位の一括取り込みを検知した時

**対象外**: `.obsidian/` / `_ kiwami/tools/daily-log/` / `Clippings/` / `調査/` / `.claude/` / 既に `🔗 関連コンテンツ` ブロックを持つファイル

**挙動**: H1直下に `> **🔗 関連コンテンツ**` callout を挿入。フルパス wikilink（`[[folder/sub/file]]`）で同名衝突を回避。関連ファイルが1つも見つからない場合は**設置せず**、完了報告で「🔗 自動リンク未設置（理由）」を宣言。

**関連タスクでの実績**:
- `SNS運用/_ 運用待機中/` 配下 25ファイル（Instagram/YouTube/note-sub/fonts）
- `SNS運用/note/` 配下 49ファイル（日次/アーカイブ/有料記事）
- `SNS運用/threads/` 配下 79ファイル（root/_fin/profile/固定自己紹介）

---

### 🔄 自動バックアップ（launchd）

**内容**: Tsukapon vault を1時間ごとにGoogle Driveへrsync同期

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.rsync-sync.plist` | launchd登録ファイル |
| `~/bin/rsync-tsukapon.sh` | rsync実行スクリプト |

**同期先**: `/Volumes/500GB/GoogleDrive/Tsukapon`

**除外対象**: `.DS_Store`, `.Trash`, `.obsidian/workspace*.json`

**ログ**:
- 成功ログ: `/tmp/rsync-sync.log`
- エラーログ: `/tmp/rsync-sync-error.log`

**確認コマンド**:
```bash
# ステータス確認
launchctl list | grep rsync-sync

# 手動実行
launchctl start com.user.rsync-sync

# ログ監視
tail -f /tmp/rsync-sync.log

# 停止
launchctl unload ~/Library/LaunchAgents/com.user.rsync-sync.plist
```

参考ドキュメント: [[Macで定期的に同期.md]]

---

### ⏱ Clockify 時間エントリ同期（launchd）⭐ NEW 2026-04-24

**内容**: Clockifyの時間エントリを15分ごとにAPI経由で取得し、`_ kiwami/tools/daily-log/clockify/YYYY-MM-DD.json` に日付別保存。**Daily Log ダッシュボード（Cowork artifact）** が参照するデータソース。

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.clockify-sync.plist` | launchd登録ファイル（雛形は `_ kiwami/tools/daily-log/`） |
| `_ kiwami/tools/daily-log/clockify-sync.py` | Clockify API取得＆JSON出力スクリプト |
| `~/.config/clockify-sync/api_key` | APIキー（vault外。permission 600） |
| `_ kiwami/tools/daily-log/clockify/YYYY-MM-DD.json` | 日付別の時間エントリデータ |
| `_ kiwami/tools/daily-log/clockify/_latest.json` | 最終同期時刻メタデータ |

**出力項目**: 開始時刻／終了時刻／説明／プロジェクト名＆カラー／タグ／所要時間／進行中フラグ

**ログ**:
- 成功ログ: `/tmp/clockify-sync.log`
- エラーログ: `/tmp/clockify-sync-error.log`

**確認コマンド**:
```bash
# ステータス確認
launchctl list | grep clockify-sync

# 手動実行
launchctl start com.user.clockify-sync

# ログ監視
tail -f /tmp/clockify-sync.log

# 停止
launchctl unload ~/Library/LaunchAgents/com.user.clockify-sync.plist
```

**セットアップ手順**: [[_ kiwami/tools/daily-log/README.md]]

---

### 📊 アクティビティトラッカー（launchd）⭐ NEW 2026-04-24

**内容**: 最前面アプリ名・ウィンドウタイトル・アイドル秒を60秒ごとに記録。activity-config.jsonのカテゴリ定義に従って`focus` / `distraction` / `other` / `idle` に自動分類し、`_ kiwami/tools/daily-log/activity/YYYY-MM-DD.jsonl` に追記。

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.activity-tracker.plist` | launchd登録ファイル（雛形は `_ kiwami/tools/daily-log/`） |
| `_ kiwami/tools/daily-log/activity-tracker.py` | osascript + ioreg でデータ取得 → JSONL追記 |
| `_ kiwami/tools/daily-log/activity-config.json` | アプリ→カテゴリ分類設定（編集可） |
| `_ kiwami/tools/daily-log/activity/YYYY-MM-DD.jsonl` | 1分1行の活動記録 |

**必要なmacOS権限**: アクセシビリティ（初回実行時に求められる）。画面収録は不要。

**データ形式**: `{"ts":"15:30","app":"Cursor","title":"...","idle":0,"cat":"focus"}`

**ログ**:
- 成功ログ: `/tmp/activity-tracker.log`
- エラーログ: `/tmp/activity-tracker-error.log`

**確認コマンド**:
```bash
launchctl list | grep activity-tracker
launchctl start com.user.activity-tracker
tail -f /tmp/activity-tracker.log
launchctl unload ~/Library/LaunchAgents/com.user.activity-tracker.plist
```

**セットアップ手順**: [[_ kiwami/tools/daily-log/README.md]]

---

### 🌐 Daily Log スタンドアロンWebサーバー（launchd）⭐ NEW 2026-04-24

**内容**: Coworkを介さずブラウザからダッシュボードを開くための常駐HTTPサーバー。`http://127.0.0.1:8765` でスタンドアロン版UIを配信。エンドポイントは `/api/activity/...` `/api/clockify/...` `/api/files/...` `/api/commits/...`（GET：git-repos.json で指定したローカルリポジトリの自分のコミット一覧）、`/api/memo/...`（GET/POST：vault `Daily Log/memo/YYYY-MM-DD.md` のCRUD）、`/api/save-md/...`（POST：vault直下 `Daily Log/YYYY-MM-DD.md` に業務報告を上書き）、`/favicon.svg`（vault直下 `oclock.svg` を配信）。UIは横幅フル＋カテゴリ/プロジェクト円グラフ＋メモ自動保存欄＋アプリ別ファイル/タイトル＋コミット一覧を備えるビジュアル強化版（手動記録機能は削除済み）。コミット監視対象は `_ kiwami/tools/daily-log/git-repos.json` で管理。

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.daily-log-server.plist` | launchd登録ファイル（KeepAlive=true で常時起動） |
| `_ kiwami/tools/daily-log/server/daily-log-server.py` | Python標準ライブラリのみのHTTPサーバー |
| `_ kiwami/tools/daily-log/server/index.html` | スタンドアロン版ダッシュボードHTML |

**アクセス**: [http://127.0.0.1:8765](http://127.0.0.1:8765)

**Cowork版との機能差（ブラウザ版で使えないもの）**:
- カレンダー予定（MCPコネクタ依存のため）
- Gmail送信履歴（同上）
- AIサマリー生成（`window.cowork.sample()` 依存）

**ログ**:
- 成功ログ: `/tmp/daily-log-server.log`
- エラーログ: `/tmp/daily-log-server-error.log`

**確認コマンド**:
```bash
launchctl list | grep daily-log-server
curl -sS http://127.0.0.1:8765/healthz
tail -f /tmp/daily-log-server.log
launchctl unload ~/Library/LaunchAgents/com.user.daily-log-server.plist
```

**セットアップ手順**: [[_ kiwami/tools/daily-log/README.md]]

---

### 📊 Daily Log（Cowork artifact）⭐ NEW 2026-04-24

**artifact ID**: `daily-log`（Coworkサイドバーの「Daily Log」）

**統合ソース（1日分のデータを5つのソースから自動取得）**:

| ソース | 取得元 | 表示 |
|---|---|---|
| 📊 Activity | `_ kiwami/tools/daily-log/activity/YYYY-MM-DD.jsonl`（launchd 60秒） | 24h活動タイムライン・集中/脱線時間・アプリランキング・15分以上の脱線アラート |
| ⏱ Clockify | `_ kiwami/tools/daily-log/clockify/YYYY-MM-DD.json`（launchd 15分） | 時間エントリ・合計稼働時間・進行中マーク |
| 📅 Google Calendar | MCP connector (OAuth) | 選択日の会議・予定 |
| ✉ Gmail | MCP connector (OAuth) | `from:me` でその日送信したスレッド |
| 📝 Markdown | `Tsukapon/` 配下を workspace bash で find | その日に編集した `.md` ファイル |

**機能**:
- 前日・翌日・今日ボタンで日付切替 → 4ソースすべて連動再取得
- 手動記録フォーム（時刻・カテゴリ・内容）で任意の作業ログを追加可能（ブラウザlocalStorageに保存）
- 「AIで一日のサマリーを生成」ボタン → `window.cowork.sample()` で3セクション構成の業務報告を生成
- Markdown形式で全ソース統合出力 → クリップボードにコピーしてそのまま提出可能

**参考**: セットアップ全体像は [[_ kiwami/tools/daily-log/README.md]]

---

## 🔌 Claude Code組み込みスキル（プラグイン経由）

これらはプラグインで追加されたもので、このvault専用ではない。

### SNS運用系

| スキル名 | 用途 | トリガー |
|---|---|---|
| `sns-persona-writer` | my-clone人格でSNS投稿生成 | 「投稿を作って」系 |
| `x-mastery-mentor` | X運営メンター（6人のトップクリエイター手法） | 「X運営」「ツイート」系 |
| `note-publish-monetize` | note記事の収益化最適化 | note記事作成時 |

### 開発系

| スキル名 | 用途 |
|---|---|
| `base` | コアワークフロー管理 |
| `code-review` | コードレビュー |
| `claude-api` | Claude APIアプリ構築 |
| `simplify` | コード簡潔化 |

### 画像・設定系

| スキル名 | 用途 |
|---|---|
| `generate-image` | Nano Banana 2で画像生成 |
| `update-config` | settings.json設定 |
| `keybindings-help` | キーボードショートカット設定 |

### 記憶・検索系

| スキル名 | 用途 |
|---|---|
| `claude-mem:mem-search` | 過去セッションの記憶検索 |
| `claude-mem:troubleshoot` | claude-memの診断 |

### スケジューリング系

| スキル名 | 用途 |
|---|---|
| `loop` | 定期的にスキルを実行（例: `/loop 5m /foo`） |
| `schedule` | クーロン形式で遠隔エージェント実行 |

---

## 🧩 標準スキル（Claude Code本体）

| スキル名 | 用途 |
|---|---|
| `/init` | CLAUDE.md を生成 |
| `/review` | PRレビュー |
| `/security-review` | セキュリティ監査 |

---

## 🌐 MCPサーバー（外部連携）

| サーバー | 用途 | 状態 |
|---|---|---|
| `claude-in-chrome` | Chrome自動操作（ページ読取・クリック・入力・GIF録画） | ✅ |
| `claude_ai_Gmail` | Gmailの下書き作成・ラベル管理 | ✅ |
| `claude_ai_Google_Calendar` | カレンダーの予定作成・更新 | ✅ |
| `claude_ai_Google_Drive` | Google Driveアクセス | ⚠️ 要認証 |
| `claude_ai_Atlassian` | Atlassian連携 | ⚠️ 要認証 |
| `context7` | ライブラリの最新ドキュメント参照（ハルシネーション対策） | ✅ グローバル登録済み |

### Context7の使い方

Context7は**ライブラリ/フレームワークの最新ドキュメント**をリアルタイムで取得するMCPサーバー。コード書く時に「最新のReact 19のAPIで」「Next.js App Routerの最新仕様で」と指定すると、訓練データ以降の変更も反映される。

- **提供**: Upstash社（無料）
- **スコープ**: `user`（グローバル）→ 全プロジェクトで利用可能
- **登録先**: `~/.claude.json` のトップレベル `mcpServers`
- **起動コマンド**: `/Users/fukuokase/.nodebrew/current/bin/npx -y @upstash/context7-mcp@latest`
- **追加方法**（再登録時・グローバル）:
  ```bash
  claude mcp add -s user context7 -- /Users/fukuokase/.nodebrew/current/bin/npx -y @upstash/context7-mcp@latest
  ```

### 🔐 MCPトークンの安全な管理

機密情報（APIトークン等）は `~/.claude.json` に平文で書かず、**`~/.zshrc` の環境変数**経由で渡す。

**例: Notion MCP（移行済み）**

```bash
# ~/.zshrc
export NOTION_TOKEN="ntn_..."
```

```json
// ~/.claude.json の mcpServers.notion
{
  "command": "/Users/fukuokase/.nodebrew/current/bin/npx",
  "args": ["-y", "@notionhq/notion-mcp-server"],
  "env": {}   // ← 空にする。環境変数から継承される
}
```

**仕組み**: Claude Codeを対話シェルから起動すると `~/.zshrc` が読み込まれて環境変数がセットされる → MCPサブプロセスが親プロセスの環境を継承する。

**注意点**:
- `.zshrc` は**インタラクティブシェル専用**。cronやlaunchdから起動する場合は `.zshenv` の方が確実
- `~/.zshrc` 自体はGitHub等に絶対コミットしないこと

---

### MCPスコープの基礎知識

| スコープ | 保存先 | 有効範囲 | 用途 |
|---|---|---|---|
| `local` | `~/.claude.json` のプロジェクト別 | 単一プロジェクト | 個人のプロジェクト固有設定 |
| `user` | `~/.claude.json` トップレベル | **全プロジェクト** | 個人で広く使いたいMCP |
| `project` | プロジェクトの `.mcp.json` | チーム共有可 | git管理してチームで共有 |

---

## 🔄 スキル連携フロー（ワークフロー）

### 毎日のSNS運用フロー（2026-04-19〜: `/re-daily` に統合）

```
朝: ニュースソースを読んで下書き
  ↓
/re-daily でnote記事化（1コマンドで4ファイル生成）
  ├─ 本体         → SNS運用/note/note-YYYYMMDD.md
  ├─ サムネ文言   → SNS運用/title/title-YYYYMMDD.md  ⭐ NEW
  ├─ X記事版      → SNS運用/post/article/X-YYYYMMDD.md
  └─ Xスレッド    → SNS運用/post/thread/YYYYMMDD_note紹介スレッド.md
  ↓
note公開後、スレッドファイル内の [noteのURL] プレースホルダーを実URLに置換
  （※ 初回から URL を入力2行目で渡せば置換不要）
  ↓
サムネ文言を Firefly/Photoshop テンプレに流し込んで、メイン＋各見出しバナーを作成
  ↓
投稿 → フォロワー改善.md のCTAを各投稿に反映
  ↓
返信が来たら /reply で返信案生成
```

### 週次改善ループ

```
日曜夜: Xアナリティクスからデータをコピー
  ↓
/weekly-analytics で分析
  → SNS運用/analytics/YYYY-WNN.md
  ↓
改善案を踏まえて来週のテーマ決定
  ↓
/re-daily に反映（来週のnote記事の方向性）
```

### バックアップ（24時間常時稼働）

```
vault変更 → launchd（1時間ごと） → rsync → Google Drive同期
```

---

## 📝 保存場所のまとめ

| データ種類 | パス |
|---|---|
| vaultルール（最優先） | `CLAUDE.md` |
| カスタムスキル定義 | `.claude/commands/` |
| 自動化hook | `.claude/hooks/` |
| harness設定（hook登録先） | `.claude/settings.json` |
| note記事（原稿） | `SNS運用/note/` |
| note記事のサムネイル文言 | `SNS運用/title/` ⭐ NEW
| 深掘り調査ノート | `調査/` ⭐ NEW |
| 日次X投稿 | `SNS運用/post/day*.md` |
| XのArticles記事 | `SNS運用/post/article/` |
| Xスレッド | `SNS運用/post/thread/` |
| 週次分析レポート | `SNS運用/analytics/` |
| 人格データ | `_ kiwami/my-clone/` |
| Daily Log ツール一式（スクリプト・plist・データ） | `_ kiwami/tools/daily-log/` ⭐ NEW |
| Clockify APIキー（vault外） | `~/.config/clockify-sync/api_key` ⭐ NEW |
| バックアップ先 | `/Volumes/500GB/GoogleDrive/Tsukapon/` |

---

## 🛠 メンテナンス・拡張

### 新しいスキルを追加したい

1. `.claude/commands/新スキル名.md` を作成
2. 冒頭にスキルの説明（Claudeがトリガーに使う）
3. `$ARGUMENTS` で入力を受け取る
4. **このファイル（`Claudian-スキル一覧.md`）への追記は自動リマインダー発動** → CLAUDE.mdルールに従ってClaudeが自動追記する

### 既存スキルを編集したい

該当ファイルを直接編集:
- [[.claude/commands/re-daily.md]]
- [[.claude/commands/thread.md]]
- [[.claude/commands/reply.md]]
- [[.claude/commands/weekly-analytics.md]]
- [[.claude/commands/md-format.md]]
- [[.claude/commands/quote-rewrite.md]]
- [[.claude/commands/deep-dive.md]]

### スキルが動かない

1. `.claude/commands/` にファイルがあるか確認
2. Claude Codeを再起動してスキル一覧を再ロード
3. 入力形式（`$ARGUMENTS`）が正しいか確認

---

## 🔗 関連ドキュメント

- [[Macで定期的に同期.md]] — launchd同期の設定手順
- [[HOME.md]] — vaultのエントリポイント（もしあれば）
- [[SNS運用/post/フォロワー改善.md]] — X運用改善プラン
- [[SNS運用/post/Xへ記事転載.md]] — X Articles戦略
