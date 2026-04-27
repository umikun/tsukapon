---
tags: [memory, short-term]
scope: 「今週〜今月」レンジ。揮発しやすい・上書きされてOKな作業記憶
last_updated: 2026-04-26
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

- **2026-04-25**: HermesエージェントはClaudianの代替ではなく「設計思想の輸入元」と位置付け
- **2026-04-25**: X 2026-01改定により「リプ欄インプ稼ぎ」は収益化対象外 → @09pauai 流の戦略は古い
- **2026-04-25**: OpenAuthはAuth0/Clerk互換ではない（user管理なし）。代替は Stack Auth / Logto / SuperTokens / Better Auth
- **2026-04-26**: 人格データ [[_ kiwami/my-clone/brain/プロフィール.md]] 確定 → **収益化活動は2026年3月開始、4月時点で実績なし**。SNS発言・返信・記事の口調は「実績語り」ではなく「**観察・試行錯誤・駆け出し2ヶ月目の生身**」ベースで書く。"X年やってきた"系の架空キャリア表現はNG。

## 🔧 試行中の運用変更

- `_fin/` への手動退避 → `/archive` で自動化
- セッション冒頭で `_ memory/` 3ファイルを読むルール追加（CLAUDE.md側に反映）

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
- **調査ノート**: [[調査/2026-04-26-kawai-claude-md-design-skills.md]]
- **発火トリガー（いずれか1つ満たしたらユーザーに再提案）**:
  - [ ] サムネ／note執筆／threadなど**複数スキルの出力で世界観のズレ**をユーザーが指摘した時
  - [ ] [[CLAUDE.md]] が肥大化し、新ルール追加時にコンテキスト圧迫を感じた時
  - [ ] [[SNS運用/note記事用サムネイルのデザインシステム仕様書.md]] を**他スキルから明示参照したい**シーンが3回以上発生した時
  - [ ] KAWAI / DESIGN.md 関連の発信を**新たに3本以上クリップ**した時（潮流加熱の合図）
  - [ ] ユーザー側から「**ブランド統一**」「**デザインシステム**」「**スキル間で世界観**」のキーワードが出た時
- **再提案時に出すミニ施策（最小コスト版）**:
  1. CLAUDE.md に1行追記:「サムネ生成・note執筆系スキルは [[SNS運用/note記事用サムネイルのデザインシステム仕様書.md]] のブランド定義を毎回参照すること」
  2. 試行記録を本ファイルの「試行中の運用変更」に追加し、観察期間を切る
- **発火しない条件**: ユーザーが「もうこの案は完全に却下」と明示した時 → 本エントリを ⚪見送り として削除

---

## 📝 メモの書き方

- 日付つきで時系列に積む
- 1ヶ月以上前の項目は `mid-term.md` に格上げ or 落とす
- 「これ恒久ルールだな」と思ったら `long-term.md` に昇格
