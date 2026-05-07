---
tags: [memory, short-term]
scope: 「今週〜今月」レンジ。揮発しやすい・上書きされてOKな作業記憶
last_updated: 2026-05-08
---

# 🟢 Short-Term Memory（短期記憶）

> **このファイルの役割**
> - 直近1〜4週間で「今やってる作業」「今週決めた小さな方針」「忘れたくない一時的な事実」を置く
> - 上書き・削除OK。古くなった項目は遠慮なく落として `mid-term.md` か `archive.md` に移す
> - Claudianはセッション開始時にこのファイルを必ず読む

---

## 📌 今週のフォーカス（Week of 2026-04-20）

- Hermes Kanban v1.5.0 から「思想だけ取り込む」プロジェクト進行中
  - ✅ Task 1: `/archive` スキル新設
  - 🟡 Task 2: 多階層メモリ（このファイル含む3層）
  - ⏳ Task 3: 自己改善スキル（Claudian-スキル候補.md + `/reflect`）
- Discord構成を2チャンネルに縮小（`#情報収集ログ` + `#モバイルメモ`）
- Threads × アフィの動向観測（直リンクOK / 3-5:1 ratio）

## 🧠 直近の決定・気づき

- **2026-05-07**: **ChatGPT Plus 契約。Claudian との棲み分けが day103 で初稼働**。Claudian は「vault内の構造化作業の自動化エンジン」、ChatGPT Plus は「vault外の素材生成と発散ブレスト」という役割分担。day103 18:00 投下の保存型単発①「CLAUDE.md自動読ませ7行」の添付画像を **GPT-4o native image gen で 2リトライ生成 → vault保存 → X投稿** の動線で完遂。フォント混在問題（英字mono／和文sans）は **CJK等幅フォント明示指定**（Source Han Code JP / HackGen / PlemolJP / Cica）で1回のリトライ解決。動線確立済み・W20以降の標準フローに昇格候補。詳細運用パターンは[[調査/2026-05-07-chatgpt-voice-mode-claudian-workflow.md]]。
- **2026-05-07**: **`/re-daily` Step 7 サムネイル文言生成のフォーマット拡張**。各見出しに**強調語フィールド**（メインタイトル内のゴールド表示部分・1〜5字）を追加、各見出し直下に **AI流し込み用コードブロック**（`- メイン:` `- 強調（ゴールド）:` `- サブ:`）併記、ファイル末尾に **5見出し一括生成用統合ブロック**（背景画像5枚同時アップロード対応）を新設。これにより `title-YYYYMMDD.md` をそのまま ChatGPT/GPT-Image-2 にペースト → 既存背景画像 `SNS運用/サムネイル作成/メインサムネイル背景01-05.jpg` を5枚同時アップロード → 1リクエストで5枚の見出しサムネ生成、という運用が可能に。明日5/8 note公開分から本番運用予定。
- **2026-05-08**: **W19 day103 EOD で KPI致命的後退が確定**。フォロワー 228→223（-5減・5/4プロフ改装後の最大下落幅）／朝投稿 imp 4（通常の1/10）／保存単発① 保存0（24h維持されず）／当日note 3view（上流ファネル枯渇）。**「来た人を取り逃さない」改装は機能、「来る人を増やす」効果は薄い**ことが数字で確定。W19 KPI ②③④の達成は現実的に断念ゾーン。残3日（5/8-5/10）は「**W20への助走として何を学ぶか**」へシフト。詳細は [[SNS運用/post/day103.md]] EOD KPIスナップショット ／ [[SNS運用/analytics/W19戦略メモ.md]] F-2 day-by-day実績ログ参照。
- **2026-05-03**: noteメンバーシップ準備に着手決定。W20（5/11〜）本格着手、W19後半（5/7〜5/10）はウォームアップ（在庫仕分け・仕様調査・戦略.md改訂下書き）。GW中（5/4〜5/6）はネタ集めのみ。ローンチ判定はW22末（W18〜W20のKPI 4項目中3つ達成でGo）。詳細は [[SNS運用/note/_メンバーシップ準備ロードマップ.md]]。戦略.md施策②は5/13に「批評型ロング+ルーチンB集+失敗談+実装ツール」へ改訂予定（旧"ニュース読み放題"は削除）。
- **2026-05-03**: W20後半（5/14〜5/17）に codex-plugin-cc の **Tsukapon vault 導入評価**をスケジュール。note記事公開ではなくツール組み込み。5/14=要件確認・API key、5/15=インストール＆テスト（git-fetcher.py 等に `/codex:adversarial-review`）、5/16=採用判定＋スキル一覧反映 or 見送り。詳細は [[SNS運用/note/_メンバーシップ準備ロードマップ.md]] W20後半タスク参照。
- **2026-05-01**: ICA学費表カスタマイズ作業 完了（クライアントワーク／詳細はユーザー側のローカル記録）。
- **2026-04-30**: マークダウンファイル生成時の絵文字装飾は最小限に。セクション見出しや箇条書き先頭の装飾絵文字（🎯 🟢 📌 🔧 など）は原則使わず、シンプルなプレーンMarkdownで書く。既存ファイルの絵文字（CLAUDE.md・memory・スキル一覧などで運用ルール上の意味を持つもの）は触らない。新規生成・新規追記の文章だけが対象。


- **2026-04-25**: HermesエージェントはClaudianの代替ではなく「設計思想の輸入元」と位置付け
- **2026-04-25**: X 2026-01改定により「リプ欄インプ稼ぎ」は収益化対象外 → @09pauai 流の戦略は古い
- **2026-04-25**: OpenAuthはAuth0/Clerk互換ではない（user管理なし）。代替は Stack Auth / Logto / SuperTokens / Better Auth
- **2026-04-26**: 人格データ [[_ kiwami/my-clone/brain/プロフィール.md]] 確定 → **収益化活動は2026年3月開始、4月時点で実績なし**。SNS発言・返信・記事の口調は「実績語り」ではなく「**観察・試行錯誤・駆け出し2ヶ月目の生身**」ベースで書く。"X年やってきた"系の架空キャリア表現はNG。
- **2026-04-28**: **obsidian-skills 5本導入完了**（kepano公式 / 配置: vault内 `.claude/skills/`）。`obsidian-markdown` `obsidian-bases` `defuddle` `json-canvas` `obsidian-cli` の5スキル。
  - **CLAUDE.md スリム化の現実**: 234行/11,764byte → 253行/12,934byte（**+19行/+1,170byte**）。sutero記事の「半分以下」削減はObsidian記法説明が大量にあるCLAUDE.md向けで、Tsukapon は既に行動ルール100%構成のため不適用。今回は**スキル責務の明示化**（外部スキル参照ルール section追加）が主成果
  - **環境整備**: `~/.zshenv` に nodebrew PATH を追記（Claude Code非対話シェルから node を見えるようにするため）。バックアップは `~/.zshenv.bak-20260428`
  - **既知の症状**: ① Obsidianインストーラ古い（v1.5.11）→ `obsidian` 小文字バイナリ無し → `~/.local/bin/obsidian` シンボリックリンクで対応（インストーラ更新時は削除）／② `defuddle-cli@0.7.0` deprecated警告だが実体は `defuddle@0.1.0` 入っていて動作問題なし
  - **バックアップ管理**: `CLAUDE.md.bak-20260428` を1週間（〜2026-05-05）保持予定。問題なければ `/Volumes/500GB/_trash/_ claude/` へ退避
  - **詳細記録**: [[Claudian-スキル一覧.md]] の「## 🧩 外部スキル（obsidian-skills）」セクション参照

## 🔧 試行中の運用変更

- `_fin/` への手動退避 → `/archive` で自動化
- セッション冒頭で `_ memory/` 3ファイルを読むルール追加（CLAUDE.md側に反映）
- **2026-05-07〜 試行中：ChatGPT Plus × Claudian の素材生成ワークフロー**
  - 散歩・スキマ時間 → ChatGPT Advanced Voice Mode でブレスト → 帰宅後コピペで vault 投入 → Claudianの `/thread` `/reply` `/news-thread` 等で整形
  - サムネ生成 → ChatGPT GPT-4o image gen で背景持ち込み×テキスト配置型に切替（既存 `SNS運用/サムネイル作成/` 資産活用）
  - 投稿添付画像 → 「Claude Code Tips」シリーズのブランド統一（ダークネイビー＋ゴールド＋macOS風カード）
  - **観察期間**: 〜2026-05-31（W20-W22）。3週間で「投稿数1.5倍」「保存型単発の保存数1件以上」の2つで効果判定
  - 効果あり → mid-term.md に昇格 / W21からの標準ワークフロー化
  - 効果なし → ChatGPT Plus は「ブレスト・音声」専用に縮小、画像はFireflyに戻す

## ⏰ 期限・宿題

- [ ] Threads運用、最低3週は様子見してからno+X連動の是非判断
- [ ] OpenAuthを実プロジェクトで触るなら Better Auth と比較
- [ ] **Daily Log: Bitbucket認証情報をosxkeychainにキャッシュ**（2026-04-27 ユーザー実施予定）
  - **背景**: Daily Logのgit-fetcher が全Bitbucketリポ（37本）でfetch失敗。`could not read Password for 'https://t-ohsumi@bitbucket.org': Device not configured` エラー。原因はSourceTreeが独自にOAuthトークンを管理しており、CLI gitの `git-credential-osxkeychain` からは資格情報が見えないこと。keychainには `t-ohsumi` ユーザー用のCLI git向けエントリが存在しない（`umikun` 用は別途あるが remote URL は `t-ohsumi@bitbucket.org/...` を指定）。
  - **暫定対応 (2026-04-27 ③ 実装済み)**: git-fetcher 側で auth エラーを `kind="auth"` 分類し、UI側で「失敗」と区別して 🔑バッジ表示。実害なしの状態で運用継続中。
  - **本対応の手順（① — 推奨1回だけ手動でやればOK）**:
    1. Bitbucket Web → 個人設定 → **App passwords** → Create app password
       - 名前例: `cli-fetch-tsukapon-mac`
       - 権限: **Repositories: Read** のみで十分（write不要）
    2. ターミナルで任意の1リポジトリへ `cd` して fetch 実行:

       ```bash
       cd "/Users/fukuokase/__ work/__Gitwork/【dentist】_master"
       git fetch
       # Username: t-ohsumi
       # Password: <生成した app password を貼り付け>
       ```

    3. 成功すれば `osxkeychain` に永続キャッシュされる → 以降全Bitbucketリポで自動認証
    4. 検証: Daily Log UIで 🔄 fetch ボタン → `🔑37` が `🔑0` になればOK
  - **参考**:
    - 関連スキル: [[Claudian-スキル一覧.md]] の「🔄 Daily Log Git Fetcher」セクション
    - git-fetcher本体: `_ kiwami/tools/daily-log/git-fetcher.py`
    - 状態確認: `cat /tmp/daily-log-git-fetcher.json | jq '.ok, .auth, .failed'`

## 👀 通知トリガー（条件マッチで提案する待機案件）

### KAWAI流 CLAUDE.md 統合運用（DESIGN.md×全スキル"同じ記憶"化）

- **保留判断日**: 2026-04-26（ユーザー明示見送り）
- **調査ノート**: [[2026-04-26-kawai-claude-md-design-skills]]
- **発火トリガー（いずれか1つ満たしたらユーザーに再提案）**:
  - [ ] サムネ／note執筆／threadなど**複数スキルの出力で世界観のズレ**をユーザーが指摘した時
  - [ ] [[CLAUDE.md]] が肥大化し、新ルール追加時にコンテキスト圧迫を感じた時
  - [ ] [[note記事用サムネイルのデザインシステム仕様書]] を**他スキルから明示参照したい**シーンが3回以上発生した時
  - [ ] KAWAI / DESIGN.md 関連の発信を**新たに3本以上クリップ**した時（潮流加熱の合図）
  - [ ] ユーザー側から「**ブランド統一**」「**デザインシステム**」「**スキル間で世界観**」のキーワードが出た時
- **再提案時に出すミニ施策（最小コスト版）**:
  1. CLAUDE.md に1行追記:「サムネ生成・note執筆系スキルは [[note記事用サムネイルのデザインシステム仕様書]] のブランド定義を毎回参照すること」
  2. 試行記録を本ファイルの「試行中の運用変更」に追加し、観察期間を切る
- **発火しない条件**: ユーザーが「もうこの案は完全に却下」と明示した時 → 本エントリを ⚪見送り として削除

---

## 📝 メモの書き方

- 日付つきで時系列に積む
- 1ヶ月以上前の項目は `mid-term.md` に格上げ or 落とす
- 「これ恒久ルールだな」と思ったら `long-term.md` に昇格

## CLAUDE.md の現状サイズ
【before】234   11764 CLAUDE.md

ls -la .claude/skills/ 2>/dev/null || echo "NOT EXIST（新規作成必要）"
total 0
drwxr-xr-x@ 2 fukuokase  staff   64 Apr 15 13:21 .
drwxr-xr-x@ 9 fukuokase  staff  288 Apr 28 09:56 ..