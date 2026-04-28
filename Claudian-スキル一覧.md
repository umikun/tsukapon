# Claudian スキル & 機能一覧

> このvaultに組み込んだカスタムスキル・自動化・バックグラウンド機能の全体マップ。
> 迷ったらここを見れば、どの機能がどこにあるか一発でわかる。
>
> 🤖 **自動更新**: このファイルは [[CLAUDE.md]] のルール＋ `.claude/hooks/remind-skills-list.sh` により、
> スキル・自動化ファイルが変更されるたびに更新するように運用されている。

最終更新: 2026-04-28（**`/re-daily` Step 11-3 のタイムラインに「早見表」を必須化＋ CLAUDE.md に絶対ルール追加**。`SNS運用/action-YYYYMMDD.md` の `## 🗓 タイムライン（時間軸順）` 直下に時刻×種別×内容のテーブルを必ず挿入する。種別アイコンは 🛠/📝/🐦/🧵/🔄/💰/👥 を使い分け、固定枠/最重要枠は太字。**9時前の投稿アクションは禁止**（運用制約）。リスケ時は早見表・個別セクション・翌日予定の3点を同時更新する整合性ルールも明文化。CLAUDE.md には「📅 絶対ルール: アクションプランファイルには必ず『タイムライン早見表』を冒頭に挿入する」セクションを新設。本日 `action-20260428.md` をテンプレートとして適用済み） / 2026-04-27（**`/re-daily` Step 11-1 を拡張**。本日アクションプラン生成時に `SNS運用/post/day*.md` 直下のX用日次投稿と `SNS運用/threads/Threads-day*.md` 直下のThreads用日次投稿を**必須読込**として追加。両者とも通し番号制（X側 `dayNN.md` ／ Threads側 `Threads-dayNN.md` で同番号対応）で、`ls -t` により直近ファイルを特定し、本文・投下時刻・連投構成をタイムラインに必ず反映する。`SNS運用/post/draft/` 配下しか拾われていなかったため、当日の日次X/Threads投稿が action ファイルに載らない事故を防ぐ） / 2026-04-27（**`/news-thread` スキル新設**。AIニュース「今週の1本」を v2型5投稿スレッド（要約→見解→不安→アクション→誘導）に落とし込む専用スキル。火・金の週2回モデル（[[SNS運用/post/template/news_thread_v2.md]]）の実行装置。入力4パターン対応（直書き／調査ノート起点／note記事起点／対話）、ソース候補は `調査/` `SNS運用/note/` `SNS運用/archive/note/` の3ディレクトリ。9ステップで生成→検証→保存し `SNS運用/post/thread/YYYYMMDD_news_v2_*.md` に出力。テンプレ全ルールを自動検証（140字／関係性キーワード／3アクション15分以内／ハッシュタグ禁止）。連携: `/thread`(note→8投稿)とは別系統で二重実行しない、`/re-daily` Step 9 とも独立） / 2026-04-27（**Daily Log Git Fetcher を新設（launchd 10分ごと） + Daily Log サーバーに `/api/fetch` `/api/fetch-status` 追加 + コミット表示にブランチ名・マージコミット情報を追加**。`git log --source` の `%S` でコミットの所属ブランチ、`%P` でマージ親判定 → サブジェクト解析（GitHub/Bitbucket/通常マージの3形式に対応）＋ 抽出失敗時は `git name-rev` で第2親から逆引き。UIにブランチバッジ4色（紫=ローカル/グレー=リモート/黄=タグ/オレンジ🔀=マージ）＋ 🔄 fetchボタン＋最終fetch時刻表示を追加。fetch本体は `_ kiwami/tools/daily-log/git-fetcher.py`（並列4・タイムアウト15秒）と `~/Library/LaunchAgents/com.user.git-fetcher.plist`（StartInterval=600 + RunAtLoad）の構成。Bitbucket等でWeb上から行ったマージが Daily Log に反映されない問題を解消） / 2026-04-27（**GitHub自動プッシュ plist のスケジュールを元に戻した**。直前の「火・金のみ」変更はユーザー意図の取り違えによる誤操作だったため、`StartCalendarInterval` を再び `Minute=30` 単一辞書（毎日毎時 :30）に戻して `launchctl unload/load`。`plutil -lint` 検証OK） / 2026-04-27（**Tsukapon vault → GitHub 自動プッシュ launchd を追加**。`~/Library/LaunchAgents/com.user.git-push-tsukapon.plist` ＋ `~/bin/git-push-tsukapon.sh` を新設し、毎時 :30 に未コミット変更を `auto: YYYY-MM-DD HH:MM hourly sync` 形式で commit → `origin/main` に push。osxkeychain 認証を流用、ネットワーク到達確認後のみ実行、変更ゼロ＋未push commit ゼロなら no-op で抜ける安全設計。ログ: `/tmp/git-push-tsukapon.log` ／ `/tmp/git-push-tsukapon-error.log`。初回手動キックで commit `5db46f0` の push を確認済み） / 2026-04-27（**`/re-daily` に Step 11「本日アクションプラン生成」を追加**。`SNS運用/analytics/` の WNN戦略メモ・WNN分析レポート・統合運用フロー・当日関連ドラフト（連投シリーズ・Day Oneプロモ・ピン候補等）を読み込み、本日の予定を時系列で1ファイルにまとめて `SNS運用/action-YYYYMMDD.md` に保存。実行手順・コピペ用本文・完了チェックを各アクションごとに詳述し、末尾に翌日予定を簡素に追記。出力ファイルが 4本 → **5本** に増加（note本体／サムネ文言／Article版／Thread版／本日アクション）。Step 10 の検証も5ファイルに更新。完了後ユーザーが手動で `SNS運用/archive/action/` に移動する運用。連動: ① `archive/action/` ディレクトリ作成 ② 本日分 `SNS運用/action-20260427.md` を W18戦略メモのカレンダーから生成（7:30 Day One X案B / 12:30 連投①/ 21:30 Threads案B / 夜 批評リプ + 翌4/28予定）） / 2026-04-27（**週次ファイル命名規則を整理: 「分析レポート」と「戦略メモ」を分離**。① `2026-W16.md` を `W16分析レポート.md` にリネーム（中身は週次分析レポートなので意味を反映）。② `/weekly-analytics` の出力先を `SNS運用/analytics/YYYY-WNN.md` → `SNS運用/analytics/WNN分析レポート.md` に変更。③ 命名規則を明確化: `WNN分析レポート.md` = `/weekly-analytics` 出力（実績の事後分析）／ `WNN戦略メモ.md` = 翌週方針メモ（手動作成）。同週でこの2本がペアになる想定。④ 連動更新: 4ファイルのwikilink書き換え（`W17戦略メモ.md` / `W17-Claude統合運用フロー.md` / `フォロワー改善.md` / `growth-strategy.md`）） / 2026-04-27（**`SNS運用/analytics/source/` を新設して生CSVを集約**。Xアナリティクスからエクスポートした `account_analytics_content_*.csv` ／ `account_overview_analytics_*.csv` の4本を `analytics/` 直下から `analytics/source/` に移動。レポート本文（`WNN分析レポート.md` / `WNN戦略メモ.md`）はwikilinkで `source/` 配下を参照する形に統一。連動更新: ① [[CLAUDE.md]] の「重要なファイル・フォルダ」表に `analytics/source/` 行を追加 ② `.claude/commands/weekly-analytics.md` の入力パターンBにCSV保存場所の注記を追加 ③ 既存ノート3件のCSV参照を新パスに書き換え（`W18戦略メモ.md` / `W16分析レポート.md`(旧 `2026-W16.md`) / `20260427_pin_candidates.md`）) / 2026-04-27（**Daily Log webサーバー の iCloud同期待ち wrapper 導入**。Mac起動直後に launchd が daily-log-server を起動した際、iCloud Drive がまだ index.html をローカル同期しておらず `Operation not permitted` で全リクエスト 500 となる問題を観測。`com.user.daily-log-server.plist` の `ProgramArguments` を bash wrapper に変更し、index.html が読めるまで 5秒×最大24回リトライ → 読めたら本体 Python を exec する方式に。プロセス再起動済み・HTTP 200 復旧確認済み） / 2026-04-27（**ディレクトリ再編 A1+A2 実施**。① ゴミ掃除: `.DS_Store`×8 / `__pycache__` / 重複ファイル `note-20260418 2.md` を `/Volumes/500GB/_trash/_ claude/A1_cleanup_20260427_*` へ退避。② アーカイブ命名統一: `SNS運用/{post,threads,note}/_fin/` → `SNS運用/archive/{post,threads,note}/` に集約（126ファイル移動）。③ 未稼働プラットフォーム集約: `SNS運用/_ 運用待機中/` → `SNS運用/pending/` リネーム。④ 関連スキル更新: `.claude/commands/archive.md`（5箇所）/`reflect.md`（3箇所）/`CLAUDE.md`（1箇所）の旧パス参照を新パスに書き換え。⑤ 全mdファイルの旧パスwikilinkを sed 一括置換（202ファイル / 残存ゼロ確認済み）。`/archive` スキルの移動先決定ロジックを「`SNS運用/{post,threads,note}` 配下なら `SNS運用/archive/{post,threads,note}/`」に変更） / 2026-04-26（`/re-daily` と `/thread` のXスレッド最終投稿の仮URLを `[noteのURL]` プレースホルダーから実URL風の `https://note.com/chackwill/n/abc` に変更。これによりnote公開後の手動差し替え時に視覚的にも"仮URLっぽさ"が出てミスが減る） / 2026-04-25（⭐ NEW: **Hermesエージェントの思想を3点取り込み**。① `/archive` スキル新設（完了ノートを `_fin/` または `_archive/YYYY-MM/` に自動仕分け＋ `archive.md` で時系列ログ化）、② **多階層メモリ** `_ memory/short-term.md` `mid-term.md` `long-term.md` 新設＋ `/remember` スキルで適切な層へ振り分け、③ **自己改善ループ** [[Claudian-スキル候補.md]] バックログ＋ `/reflect` でパターン検出。CLAUDE.md にも「セッション冒頭で多階層メモリを読む」「3回以上のパターンは候補化」の絶対ルール追加） / 2026-04-25（Daily Log スタンドアロン版を大型刷新：横幅フル幅化／カテゴリ・プロジェクト円グラフ／メモ自動保存欄（vault `Daily Log/memo/YYYY-MM-DD.md`）／`oclock.svg` をファビコン化／手動記録機能を削除。サーバには `GET/POST /api/memo/...` と `GET /favicon.svg` を追加） / 2026-04-25（`POST /api/save-md/YYYY-MM-DD` を追加） / 2026-04-24（⭐ NEW: **新規/追加ファイルの自動リンク設置ルール** を [[CLAUDE.md]] に追加。vault内への新規作成・外部コピーに対し、関連ファイルを推定して `🔗 関連コンテンツ` callout を H1 直下に自動挿入。対象外は `.obsidian/` `Clippings/` `調査/` `_ kiwami/tools/daily-log/` `.claude/` 等。Daily Log 一式も引き続き運用中: `_ kiwami/tools/daily-log/` にClockify同期（15分毎）・アクティビティトラッカー（60秒毎）・ローカルWebサーバー（常駐、<http://127.0.0.1:8765>））

---

## 🎯 クイックリファレンス

| やりたいこと | 使うスキル | コマンド |
|---|---|---|
| noteのAIニュース記事をリライト + サムネ文言 + X記事版 + Xスレッド + 本日アクションプランまで一括生成 | `re-daily` | `/re-daily 記事パス`（任意で2行目にnote記事URL） |
| note記事をXのスレッドに変換（単体実行） | `thread` | `/thread パス\nタイトル\nURL` |
| AIニュース「今週の1本」をv2型5投稿スレッドに変換（火・金運用） | `news-thread` | `/news-thread`＋【今週の1本】等の入力 |
| X投稿への返信を生成 | `reply` | `/reply`（対象ポストを貼り付け） |
| 週次のX運用分析 | `weekly-analytics` | `/weekly-analytics データ` |
| マークダウン記法の検査・修正 | `md-format` | `/md-format ファイルパス` または選択状態で `/md-format` |
| 引用RT下書きをmy-clone口調＋関係性キーワード反映版に書き換え | `quote-rewrite` | `/quote-rewrite 下書き本文` |
| ペーストした文章を深掘り調査してMDノート化 | `deep-dive` | `/deep-dive 調査したい本文` または選択状態で `/deep-dive` |
| 完了ノートを `SNS運用/archive/` `_archive/` へ仕分け＋時系列ログ化 | `archive` | `/archive フォルダパス` または `/archive`（対話） |
| 重要な気づき・決定を多階層メモリの適切な層に記録 | `remember` | `/remember short/mid/long 本文` または `/remember 本文`（自動振り分け） |
| 最近の作業を振り返って繰り返しパターンをスキル候補化 | `reflect` | `/reflect` または `/reflect today` |
| 1日の作業内容を自動集計して業務日報を出力 | Daily Log（artifact） | Coworkサイドバーの「Daily Log」を開く |

---

## 📦 カスタムスキル（このvault専用）

保存場所: `.claude/commands/`

### 1. [[.claude/commands/re-daily.md|/re-daily]] — note記事リライト＋サムネ文言＋X記事版＋Xスレッド＋本日アクションプラン一気通貫生成 ⭐ UPDATED 2026-04-28（Step 11-3 タイムラインに「早見表」テーブルを必須化／9時前の投稿アクション禁止ルールを反映）

> **2026-04-28 変更点**: アクションプラン生成時、`## 🗓 タイムライン（時間軸順）` 直下に **早見表テーブル**（時刻×種別×内容）を必ず挿入する。CLAUDE.md の絶対ルール「📅 アクションプランファイルには必ず『タイムライン早見表』を冒頭に挿入する」と連動。
>
> - 早見表は時間軸の昇順、固定枠/最重要枠は太字
> - 種別アイコン: 🛠 開発／📝 note公開／🐦 X／🧵 スレッド or Threads／🔄 計測／💰 有料／👥 リプ
> - **9時前の投稿アクションは載せない**（運用制約）
> - リスケ時は早見表・個別セクション・翌日予定の3点を同時更新

**用途**: 毎日のAIニュースnote記事を、SEO最適化・内容充実化し、**続けてX記事転載版とXスレッド版まで自動生成**する

**入力**:
```
記事ファイルパス
（任意）note記事URL  ← 2行目
```

- URL未指定の場合、Xスレッド側は仮URL `https://note.com/chackwill/n/abc` を使用（公開後に手動差し替え）

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
- **Step 10**: 完了検証と報告（5ファイル存在確認）
- **Step 11**: 本日アクションプラン生成 ⭐ NEW 2026-04-27（2026-04-27 day*.md／Threads-day*.md 必須読込追加）
  - `SNS運用/analytics/` 配下の **当週WNN戦略メモ／前週WNN分析レポート／W*-Claude統合運用フロー** と、当日の連投シリーズ・Day Oneプロモ・ピン候補ドラフト・テンプレ・フォロワー改善メモを総ざらい
  - **本日該当のX日次投稿** `SNS運用/post/day*.md` 直下（通し番号制）と **Threads日次投稿** `SNS運用/threads/Threads-day*.md` 直下を必ず読み込み、本文・投下時刻・連投構成をタイムラインに含める ⭐ NEW
  - 本日の予定を **時刻順** に並べ、各アクションに「媒体」「元ファイル」「目的」「実行手順5〜10行」「コピペ用本文」「完了チェック」を必須記載
  - 末尾に翌日予定を3〜6行で簡素に追記
  - 保存先: `SNS運用/action-YYYYMMDD.md`（vault直下）。完了後ユーザーが `SNS運用/archive/action/` に手動移動

**出力**（1コマンドで5ファイル生成）:
1. `SNS運用/note/note-YYYYMMDD.md`（リライト上書き）
2. `SNS運用/title/title-YYYYMMDD.md`（サムネイル文言）
3. `SNS運用/post/article/X-YYYYMMDD.md`（X Articles版）
4. `SNS運用/post/thread/YYYYMMDD_note紹介スレッド.md`（Xスレッド版）
5. `SNS運用/action-YYYYMMDD.md`（本日アクションプラン）⭐ NEW 2026-04-27

**🛡 パイプライン堅牢化（2026-04-21 → 2026-04-27 更新）**:
- 冒頭に **「必須パイプライン宣言」** を配置：Step 1〜**11**をノンストップで走り切ることを明示
- **Step 6 末尾にリマインド**：「ここはまだ進捗序盤。Step 7以降を続けること」
- **Step 10（完了検証と報告）**：`ls` で **5ファイル**存在を確認してから最終応答
- Step 6 の後に応答を終えて後続ステップをスキップする事故を防止

**連携先**: なし（`thread` の処理を内包）。単体で `thread` を使うケース（過去記事からスレッドだけ作る等）は従来どおり `/thread` を呼ぶ。

---

### 2-2. [[.claude/commands/news-thread.md|/news-thread]] — AIニュース v2型5投稿スレッド生成（火・金運用） ⭐ NEW 2026-04-27

**用途**: AIニュースを「今週の1本」に絞り、X/Threads向けの **v2型5投稿スレッド**（要約 → 一般論じゃない見解 → 不安喚起 → 具体アクション → note誘導）に落とし込む。火・金の週2回モデル（[[SNS運用/post/template/news_thread_v2.md]]）の実行装置。

**入力**（4パターン対応）:
```
A: ニュース直書き（最頻）
   【今週の1本】〇〇発表 ／ 【ソース】URL ／ 【自分の現場】〜
   （任意）【曜日】tue/fri ／【テーマslug】xxx
B: 調査ノート起点
   【ソース】調査/YYYY-MM-DD-〇〇.md
C: note記事/アーカイブ起点
   【ソース】SNS運用/note/note-YYYYMMDD.md
   または SNS運用/archive/note/ 配下
D: 引数なし（対話モード）
```

**ソース候補ディレクトリ**（B/C/D で読み込む）:
- `調査/`（`/deep-dive` の出力ノート）
- `SNS運用/note/`（当日〜直近のリライト済みnote）
- `SNS運用/archive/note/`（公開済み過去note）

**処理内容（9ステップ）**:
1. 入力パターン判定とソース確定（D は対話で `ls -t` 直近1週間を提示）
2. 曜日判定と「角度」決定（火: 週末動向 ／ 金: 週中最大トピック）
3. 戦略コンテキスト照合（当週 `WNN戦略メモ.md` ＋ 前週 `WNN分析レポート.md`）
4. **1/5（フック・要約）** 生成: 希少性訴求語＋現場匂わせ＋絵文字1＋断定しない語尾＋20字主題見出し
5. **2/5（一般論じゃない見解）**: 「ほとんどの解説が〇〇で止まってる」批評ポジ＋理由3つ（4つ以上禁止）
6. **3/5（不安喚起）**: 関係性キーワード必須（上司／同僚／会社 等）＋❌3つ＋絵文字1
7. **4/5（具体アクション）**: ✅3つ・全部15分以内・「読む／ブクマ／試す」のいずれか
8. **5/5（誘導）**: noteURL＋プロフ誘導・ハッシュタグ禁止
9. 自動検証5項目（140字／関係性キーワード／3アクション／ハッシュタグなし／`---` 区切り）→ 保存 → コピペ用本文をチャット返却

**出力**: `SNS運用/post/thread/YYYYMMDD_news_v2_{slug}.md`
- H1直下に `🔗 関連コンテンツ` callout（テンプレ／当週戦略メモ／ソース）
- 各投稿に字数・関係性キーワード・採用型のメタ表示
- 末尾に「投稿前チェックリスト」5項目

**v2思想**:
- 5本詰める旧テンプレ（imp 4〜15で全滅）から **「1本×深さ3倍」** へ転換
- ハッシュタグ禁止（bot認識回避）
- 関係性キーワードでRT率を上げる（W17の批評型リプ勝ちパターンの移植）

**既存スキルとの関係**:
- `/thread`（note記事 → 8投稿）とは設計思想が別。火金朝は `/news-thread` 単体で動かす
- `/re-daily` の Step 9 と二重実行しない（`/re-daily` は note起点、`/news-thread` は単独ニュース起点）

**初試行**: 2026-05-01(金)朝 ＝ W18戦略メモのカレンダー記載

**連携先**: [[SNS運用/post/template/news_thread_v2.md]]（テンプレ本体）／ [[SNS運用/analytics/W18戦略メモ.md]]（運用方針）／ `/quote-rewrite`（生成スレッドを引用RTに転用したい場合）

---

### 2. [[.claude/commands/thread.md|/thread]] — X スレッド生成（単体実行用） ⭐ UPDATED 2026-04-26（仮URLを `https://note.com/chackwill/n/abc` に変更）

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
- **最終投稿URLは当日記事**: 入力3行目のURL（未指定なら仮URL `https://note.com/chackwill/n/abc`）
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
- [[note-20260426間違い]] の大量自動化系は取り込まない

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

### 8. [[.claude/commands/archive.md|/archive]] — 完了ノートの自動仕分け＋時系列ログ化 ⭐ NEW 2026-04-25

**用途**: 完了マーカー付きのノートを `SNS運用/archive/{post,threads,note}/` または `_archive/YYYY-MM/` に自動移動し、対象フォルダ直下の `archive.md` にタイムスタンプ付きの集約ログを追記する。Hermes Kanban v1.5.0 の「Smart Card Archive」発想をObsidian vault運用に持ち込んだもの。

**入力**（4パターン対応）:
```
A: /archive SNS運用/post           ← フォルダ指定（標準）
B: /archive SNS運用/post/day60.md  ← 単一ファイル指定
C: /archive                        ← 対話モード（候補一覧から選ばせる）
D: /archive SNS運用/post --dry-run ← ドライラン
```

**完了マーカーの判定ルール（OR条件）**:
- frontmatter フラグ: `archived: true` / `posted: true` / `投稿済み: true` / `status: done|完了|posted`
- 本文末のHTMLコメント: `<!-- ARCHIVE -->` / `<!-- DONE -->`
- ファイル名規則: `day*.md` で本文先頭が「投稿済み」「✅」

**処理内容（7ステップ）**:
1. 対象フォルダ・ファイルの確定（パターン判定）
2. 完了マーカーのスキャン（既に `SNS運用/archive/` `_archive/` 配下のものは除外）
3. 移動先の決定（`SNS運用/{post,threads,note}` 配下なら `SNS運用/archive/{post,threads,note}/`、なければ `_archive/YYYY-MM/`）
4. `mv` で移動（`rm` 禁止 / 失敗時は即停止して報告）
5. `archive.md` への追記（`## YYYY-MM-DD` 見出し配下に `- HH:MM [[wikilink]] — 検出理由`）
6. 確認とクリーンアップ（移動件数 ＝ 追記行数の整合チェック）
7. 完了報告（移動件数・移動先・archive.mdリンク）

**出力**: 各対象フォルダ直下の `archive.md` を新規作成または末尾追記

**安全運用**:
- `rm` 禁止（CLAUDE.md準拠）
- frontmatter は読むだけで書き換えない（事実は archive.md に記録）
- 1度に20件以上はユーザー確認
- `.obsidian/` `.claude/` `_ kiwami/tools/daily-log/` 配下は対象外

**連携先**: 旧来の手動 `_fin/` 退避運用は `SNS運用/archive/{post,threads,note}/` に統合済み（2026-04-27のディレクトリ再編A2にて）。手作業を自動化する立ち位置

---

### 9. [[.claude/commands/remember.md|/remember]] — 多階層メモリへの自動振り分け ⭐ NEW 2026-04-25

**用途**: 重要な気づき・決定・運用変更を、時間レンジに応じて `_ memory/short-term.md` / `mid-term.md` / `long-term.md` の3層に振り分けて追記する。Hermesエージェントの「多階層メモリ」発想をObsidian vault運用に持ち込んだもの。

**入力**（4パターン対応）:
```
A: /remember short 本文       ← 階層指定
B: /remember 本文             ← 自動振り分け（キーワード判定 → ユーザー確認）
C: 引数なし＋<editor_selection> または <browser_selection>
D: /remember                  ← 対話モード
```

**階層の判定ガイド**:
| 層 | レンジ | 例 |
|---|---|---|
| short | 1〜4週間 | 今週のフォーカス、試行中の運用、期限あり宿題 |
| mid | 3〜6ヶ月 | 四半期方針、現役スキル、定常的な前提 |
| long | 半年以上〜恒久 | 行動原則、文体の根、絶対禁止事項、価値観 |

**処理内容（6ステップ）**:
1. 入力の確定（階層 / 本文 / 出典）
2. 対象ファイルの特定（`_ memory/{tier}-term.md`）
3. 追記位置の決定（適切なセクション見出しを判定）
4. 追記の実行（日付プレフィックス付き、出典があれば末尾に wikilink / URL）
5. 階層昇格・降格の検討（古い項目があれば一行だけ提案。**勝手に動かさない**）
6. 完了報告（書き込み先＋プレビュー）

**出力**: `_ memory/{tier}-term.md` の該当セクションに追記。frontmatter `last_updated` を今日の日付に更新

**制約**:
- 既存項目を書き換えない（追記のみ）
- ユーザー指定階層は尊重（自動振り分けで上書きしない）
- `_ memory/` 配下は自動リンクルール（`🔗 関連コンテンツ`）の対象外

**連携先**: `/reflect`（パターン検出で気づいた項目を流す）、CLAUDE.md（セッション冒頭で3層を読み込む鉄則）

---

### 10. [[.claude/commands/reflect.md|/reflect]] — 自己改善ループ：作業パターン検出 ⭐ NEW 2026-04-25

**用途**: 最近の会話・作業を振り返り、繰り返し現れる作業パターン（命名規則・配置先・処理フロー）を検出して [[Claudian-スキル候補.md]] に追記する。Hermesエージェントの「自己改善スキル」発想をObsidian vault運用に持ち込んだもの。

**入力**（3パターン対応）:
```
A: /reflect                            ← 現在のセッション対象（デフォルト）
B: /reflect today / week / last-3-sessions  ← 範囲指定
C: /reflect "毎回〜している"            ← 観察したパターンを直接記録
```

**処理内容（7ステップ）**:
1. 対象範囲の確定
2. パターン抽出（ファイル操作・会話・改善ポイント の3軸）
3. 既存候補との突合（`Claudian-スキル候補.md` を読んで重複チェック）
4. ステータス遷移（1〜2回 → 🟡観察中 / 3回以上 → 🟢候補確定）
5. 既存スキルへの再帰チェック（拡張で済むなら新スキルにせず `_ memory/short-term.md` に改善案として書く）
6. 追記の実行（候補ファイル更新）
7. レポート提示（新規 / 更新 / 候補確定 件数＋ハイライト）

**出力**: [[Claudian-スキル候補.md]] への追記

**安全運用**:
- 勝手にスキルを実装しない（候補追加までで止める）
- ⚪見送り判定済みのパターンは再提案しない（ループ防止）
- 1回で10件以上の新規候補が出たら絞り込みを確認
- パターン検出は**観察**であって**評価**ではない

**連携先**: [[Claudian-スキル候補.md]]（書き込み先）、`/remember`（気づきのメモリ化）、CLAUDE.md（自己改善ループの鉄則の根拠）

---

### 4. [[.claude/commands/weekly-analytics.md|/weekly-analytics]] — 週次分析 ⭐ NEW

**用途**: X運用の週次データを分析し、次週の改善アクションを提案

**入力**（3パターン対応）:
- A: データ直接貼り付け
- B: データファイルパス（または `SNS運用/analytics/source/*.csv` の生CSVパス）
- C: 空入力（対話モードで質問）

**データソース**:
- 生CSV保存場所: `SNS運用/analytics/source/`（Xアナリティクスからエクスポートした `account_analytics_content_*.csv` / `account_overview_analytics_*.csv`）
- レポート本文からは `[[SNS運用/analytics/source/...csv]]` でwikilink参照

**処理内容**:
- エンゲージメント率・保存率・プロフアクセス率を計算
- TOP3 / WORST3 を抽出、型・時間帯・フックを分析
- 4指標で総合判定（良好/要改善）
- 来週のアクション3つを具体的に提示
- WORST3のBefore/Afterリライト
- 他スキル連携提案（re-daily / thread へ流す内容）

**出力**: `SNS運用/analytics/WNN分析レポート.md`（例: `W16分析レポート.md`）

**命名規則の使い分け（2026-04-27〜）**:
- `WNN分析レポート.md` … 本スキル出力（実績の事後分析）
- `WNN戦略メモ.md` … 翌週方針メモ（手動作成・別ドキュメント）
- 同週でこの2本がペアになる想定

**連携先**: `re-daily`（分析結果をnote記事に反映）、`thread`（伸びた投稿のスレッド化）

---

## 🧩 外部スキル（obsidian-skills）

⭐ **NEW 2026-04-28** — Obsidian CEO kepano公式の Agent Skills セットを当vaultに導入

- **配置**: `.claude/skills/`（vault内、当vault専用）
- **ソース**: <https://github.com/kepano/obsidian-skills>
- **導入記事**: [[Clippings/ObsidianでClaudeCodeを使い始めたら、次に入れるべき「obsidian-skills」｜sutero（ステロ）.md]]
- **CLAUDE.md からの参照**: 「## 🧩 外部スキル参照ルール」セクションで明示済み

### 5スキル一覧

| スキル | 用途 | 追加セットアップ | 使用頻度 |
|---|---|---|---|
| `obsidian-markdown` | Wikiリンク・コールアウト・frontmatter等のObsidian記法 | なし | ⭐ マスト |
| `obsidian-bases` | .baseファイルの作成・編集（DB的ビュー） | なし | 中（読書/買物リスト） |
| `defuddle` | WebページをクリーンMarkdownに変換 | `npm install -g defuddle-cli`（v0.1.0で動作確認済） | ⭐ マスト |
| `json-canvas` | .canvasファイルの作成・編集 | なし | 低（保険） |
| `obsidian-cli` | Obsidian CLI操作（vault読書き・検索） | Obsidian設定でCLI ON ＋ `~/.local/bin/obsidian` シンボリックリンク作成（インストーラ古い場合のみ） | 低（保険） |

### 既知の運用ノート（2026-04-28）

- **obsidian-cli**: 公式インストーラがv1.5.11と古いため `obsidian`（小文字）コマンドが入っていない。`/Applications/Obsidian.app/Contents/MacOS/Obsidian`（大文字）が実体なので `~/.local/bin/obsidian` にシンボリックリンクを作成して対応中。インストーラ更新時はリンク削除予定
- **defuddle**: `defuddle-cli@0.7.0` は deprecated 警告が出るが、実体は新パッケージ `defuddle@0.1.0` がインストールされる。動作問題なし
- **CLAUDE.md スリム化**: sutero記事の「半分以下」削減はObsidian記法説明が大量にあるCLAUDE.md向け。Tsukaponは既に行動ルール100%構成のため**スキル責務の明示化のみ**（+19行/+1,170byte）に留めた。Sonnet/Haiku でのスキル呼び忘れ事故防止が主成果

### 連携先（自動ルーティング）

| ユーザーの指示 | 自動で呼ばれるスキル |
|---|---|
| 「このURL要約して」「このページ読んで」（`.md` 以外） | `defuddle` |
| 「.mdのURL」「Markdownファイルを読んで」 | WebFetch（defuddleではない） |
| Wikiリンク／コールアウト／frontmatter作成依頼 | `obsidian-markdown` |
| 「読書リスト作って」「買物リスト DB化」 | `obsidian-bases` |
| 「マインドマップ作って」「.canvas編集」 | `json-canvas` |
| vault検索／一括読み書き／プラグイン操作 | `obsidian-cli` |

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
- `SNS運用/pending/` 配下 25ファイル（Instagram/YouTube/note-sub/fonts）
- `SNS運用/note/` 配下 49ファイル（日次/アーカイブ/有料記事）
- `SNS運用/threads/` 配下 79ファイル（root/archive/profile/固定自己紹介）

---

### 🚀 GitHub 自動プッシュ（launchd）⭐ NEW 2026-04-27

**内容**: Tsukapon vault の未コミット変更を毎時 `:30` に自動コミット → `origin/main` へ push する。GitHubリポジトリ: `https://github.com/umikun/tsukapon`

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.git-push-tsukapon.plist` | launchd登録（`StartCalendarInterval` Minute=30） |
| `~/bin/git-push-tsukapon.sh` | git add → commit → push スクリプト |

**動作仕様**:
- ネットワーク到達確認: `curl https://github.com` を5秒タイムアウトで叩き、失敗時は `[skip]` で静かに終了
- 変更検出: `git status --porcelain` ＋ `git rev-list @{u}..HEAD` で **「作業ツリー変更ゼロ ＆ 未push commit ゼロ」なら何もしない**
- コミットメッセージ規約: `auto: YYYY-MM-DD HH:MM hourly sync`
- 認証: グローバル設定の `credential.helper = osxkeychain` を流用（事前に手動 push 1回でキーチェーンに保存しておく必要あり）
- ロケール: `LANG/LC_ALL=en_US.UTF-8` を明示し、launchd 環境での日本語ファイル名失敗を回避
- 実行タイミング: `RunAtLoad=false`（plist再読み込みのたびに走らないようにする）

**rsync同期との関係**: rsync同期は Google Drive へのバックアップ（24h）、git push は GitHub への履歴管理。同じ vault に対して二重に冗長化されている。

**ログ**:
- 成功ログ: `/tmp/git-push-tsukapon.log`
- エラーログ: `/tmp/git-push-tsukapon-error.log`（git の正常な push 進捗も stderr 経由で混ざる）
- launchd 標準出力: `/tmp/git-push-tsukapon.launchd.log`

**確認コマンド**:
```bash
# ステータス確認
launchctl list | grep git-push-tsukapon

# 手動実行（即座に1回 push）
launchctl start com.user.git-push-tsukapon

# ログ監視
tail -f /tmp/git-push-tsukapon.log

# 停止 / 再読み込み
launchctl unload ~/Library/LaunchAgents/com.user.git-push-tsukapon.plist
launchctl load   ~/Library/LaunchAgents/com.user.git-push-tsukapon.plist
```

**トラブル時のチェック**:
- push が失敗する → osxkeychain にトークンが保存されているか: `git credential-osxkeychain get <<< $'protocol=https\nhost=github.com\n'`
- `Operation not permitted` 系 → vault の iCloud 同期完了前に走った可能性。次の :30 で自動復旧
- `[skip] github.com unreachable` が連続 → ネットワーク不安定 or DNS問題

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

**内容**: Coworkを介さずブラウザからダッシュボードを開くための常駐HTTPサーバー。`http://127.0.0.1:8765` でスタンドアロン版UIを配信。エンドポイントは `/api/activity/...` `/api/clockify/...` `/api/files/...` `/api/commits/...`（GET：git-repos.json で指定したローカルリポジトリの自分のコミット一覧。`%S`(source ref) ＋ `%P`(parents) で各コミットに **branch名** と **マージコミット情報**(`is_merge`/`merged_from`/`merged_into`) を付与）、`/api/fetch`（POST：全リポジトリを並列 `git fetch` 実行）、`/api/fetch-status`（GET：直近fetch結果の取得）、`/api/memo/...`（GET/POST：vault `Daily Log/memo/YYYY-MM-DD.md` のCRUD）、`/api/save-md/...`（POST：vault直下 `Daily Log/YYYY-MM-DD.md` に業務報告を上書き）、`/favicon.svg`（vault直下 `oclock.svg` を配信）。UIは横幅フル＋カテゴリ/プロジェクト円グラフ＋メモ自動保存欄＋アプリ別ファイル/タイトル＋コミット一覧（**ブランチバッジ：紫=ローカル/グレー=リモート/黄=タグ/オレンジ🔀=マージ**）＋ 🔄fetchボタン＆最終fetch時刻表示を備えるビジュアル強化版（手動記録機能は削除済み）。コミット監視対象は `_ kiwami/tools/daily-log/git-repos.json` で管理。

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.daily-log-server.plist` | launchd登録ファイル（KeepAlive=true で常時起動／Mac起動時に bash wrapper で iCloud 同期完了を最大120秒待ってから本体起動） |
| `_ kiwami/tools/daily-log/server/daily-log-server.py` | Python標準ライブラリのみのHTTPサーバー |
| `_ kiwami/tools/daily-log/server/index.html` | スタンドアロン版ダッシュボードHTML |

**アクセス**: [http://127.0.0.1:8765](http://127.0.0.1:8765)

**Cowork版との機能差（ブラウザ版で使えないもの）**:
- カレンダー予定（MCPコネクタ依存のため）
- Gmail送信履歴（同上）
- AIサマリー生成（`window.cowork.sample()` 依存）

**ログ**:
- 成功ログ: `/tmp/daily-log-server.log`（wrapper の `[wrapper] index.html readable on attempt N` も出力）
- エラーログ: `/tmp/daily-log-server-error.log`

**起動シーケンス（2026-04-27 改修）**:
1. launchd が plist の `ProgramArguments` を実行（bash wrapper）
2. wrapper が `index.html` の読み取りを5秒間隔で最大24回（=120秒）リトライ
3. 読み取り成功で `exec /usr/bin/python3 daily-log-server.py` に切り替え
4. iCloud 同期未完了状態で起動して 500 エラーを返す問題を予防

**既知のトラブル**:
- 2026-04-27: iCloud 同期完了前に launchd が起動 → `Operation not permitted: index.html` で全リクエスト 500。手動 `launchctl unload && load` で復旧。再発防止として上記 wrapper を導入

**確認コマンド**:
```bash
launchctl list | grep daily-log-server
curl -sS http://127.0.0.1:8765/healthz
tail -f /tmp/daily-log-server.log    # wrapper のリトライ動作も確認可能
launchctl unload ~/Library/LaunchAgents/com.user.daily-log-server.plist
launchctl load   ~/Library/LaunchAgents/com.user.daily-log-server.plist  # 手動再起動
```

**セットアップ手順**: [[_ kiwami/tools/daily-log/README.md]]

---

### 🔄 Daily Log Git Fetcher（launchd）⭐ NEW 2026-04-27

**内容**: Daily Log の「コミット」表示は **ローカルの git log** を読むため、Bitbucket/GitHub上で行ったマージや他端末からのpushがローカルに `git fetch` されるまで反映されない。これを解消するために、`git-repos.json` に登録された全リポジトリを **10分ごとに並列 `git fetch --all --prune`** するバックグラウンドジョブ。Daily Log UIの 🔄 ボタンからも同じスクリプトを即時実行できる。

| ファイル | 役割 |
|---|---|
| `~/Library/LaunchAgents/com.user.git-fetcher.plist` | launchd登録ファイル（`StartInterval=600` ＋ `RunAtLoad=true`） |
| `_ kiwami/tools/daily-log/git-fetcher.py` | fetch本体（雛形） |
| `~/bin/daily-log/git-fetcher.py` | launchd/サーバーから呼ばれる稼働コピー |

**動作**:

- ThreadPoolExecutor で **最大4並列** fetch、各リポジトリ **15秒** タイムアウト
- 失敗してもexit 0（launchdを止めない）
- 結果を `/tmp/daily-log-git-fetcher.json` にJSON保存
  - サーバーの `GET /api/fetch-status` がこのファイルを返し、UIが「fetch: 2分前」のように表示
- 認証切れ・ネットワーク不通リポジトリは個別に `error` フィールド付きで記録

**手動トリガー**:

- Daily Log UI の **🔄 fetch ボタン**（`POST /api/fetch` を叩いて同期実行・完了後にコミット欄を自動再描画）
- CLI: `python3 ~/bin/daily-log/git-fetcher.py`（テキスト出力）／ `--json` オプションでJSON

**ログ**:

- 標準出力: `/tmp/git-fetcher.log`
- エラー: `/tmp/git-fetcher-error.log`
- 直近結果(JSON): `/tmp/daily-log-git-fetcher.json`

**確認コマンド**:

```bash
launchctl list | grep git-fetcher
cat /tmp/daily-log-git-fetcher.json | jq '.ok, .total, .failed'
launchctl kickstart -k gui/$(id -u)/com.user.git-fetcher  # 即時実行
launchctl unload ~/Library/LaunchAgents/com.user.git-fetcher.plist
launchctl load   ~/Library/LaunchAgents/com.user.git-fetcher.plist
```

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

### 毎日のSNS運用フロー（2026-04-19〜: `/re-daily` に統合 / 2026-04-27 アクションプラン追加）

```
朝: ニュースソースを読んで下書き
  ↓
/re-daily でnote記事化＋本日の運用指示を一本化（1コマンドで5ファイル生成）
  ├─ 本体             → SNS運用/note/note-YYYYMMDD.md
  ├─ サムネ文言       → SNS運用/title/title-YYYYMMDD.md
  ├─ X記事版          → SNS運用/post/article/X-YYYYMMDD.md
  ├─ Xスレッド        → SNS運用/post/thread/YYYYMMDD_note紹介スレッド.md
  └─ 本日アクション   → SNS運用/action-YYYYMMDD.md  ⭐ NEW 2026-04-27
  ↓
note公開後、スレッドファイル内の仮URL https://note.com/chackwill/n/abc を実URLに置換
  （※ 初回から URL を入力2行目で渡せば置換不要）
  ↓
サムネ文言を Firefly/Photoshop テンプレに流し込んで、メイン＋各見出しバナーを作成
  ↓
action-YYYYMMDD.md のタイムラインに沿って X / Threads / プロフ操作 / 批評リプを実行
  ↓
全アクション完了後、action-YYYYMMDD.md を SNS運用/archive/action/ に手動移動
  ↓
返信が来たら /reply で返信案生成
```

### 火・金朝のニューススレッド運用フロー（2026-04-27〜: `/news-thread` 導入）

```
火/金 朝
  ↓
今週の1本（火: 週末動向 / 金: 週中最大トピック）を選定
  ↓
/news-thread で v2型5投稿スレッド生成（要約→見解→不安→アクション→誘導）
  → SNS運用/post/thread/YYYYMMDD_news_v2_{slug}.md
  ↓
note公開後、5/5 投稿の仮URL https://note.com/chackwill/n/abc を実URLに置換
  （※ 当日noteを 【ソース】SNS運用/note/note-YYYYMMDD.md で渡せば抽出される）
  ↓
X/Threads に手動投稿
  ↓
週末の振り返りで脱落率（1/5 vs 5/5 imp比）・3/5 RT率・5/5 リンクCTR を計測
```

### 週次改善ループ

```
日曜夜: Xアナリティクスからデータをコピー
  ↓
/weekly-analytics で分析
  → SNS運用/analytics/WNN分析レポート.md
  ↓
改善案を踏まえて来週のテーマ決定
  ↓
SNS運用/analytics/WNN戦略メモ.md（手動作成）に方針を書く
  ↓
/re-daily に反映（来週のnote記事の方向性）
```

### 自己改善ループ（Hermesエージェント発想・2026-04-25導入）

```
セッション中の作業
  ↓
/reflect で繰り返しパターン検出
  → Claudian-スキル候補.md に追記（🟡観察中 → 🟢候補確定）
  ↓
3回到達 or ユーザー明示依頼 → 🔵実装決定
  ↓
.claude/commands/ に新スキル作成
  ↓
Claudian-スキル一覧.md に自動追記（CLAUDE.md鉄則）
  ↓
候補ファイルで ✅実装済み にマーク
```

### 多階層メモリ運用（Hermesエージェント発想・2026-04-25導入）

```
セッション冒頭: CLAUDE.md鉄則により _ memory/ 3層を読み込み
  ├─ short-term.md  → 今週のフォーカス・直近の決定
  ├─ mid-term.md    → 四半期方針・現役スキル
  └─ long-term.md   → 行動原則・価値観
  ↓
重要な気づき発生 → /remember で適切な層に振り分け
  ↓
3ヶ月以上揺るがない項目 → 上位層に昇格
古くなった項目 → 削除 or archive.md 行き
```

### 完了ノートのアーカイブフロー（Hermesエージェント発想・2026-04-25導入）

```
日次X投稿・note・調査ノートに完了マーカー付与
  （frontmatter `posted: true` / `<!-- ARCHIVE -->` / 本文先頭「投稿済み」 等）
  ↓
/archive フォルダパス で一括処理
  ├─ SNS運用/{post,threads,note} 配下なら → SNS運用/archive/{post,threads,note}/ へ mv
  └─ なければ → _archive/YYYY-MM/ を作成して mv
  ↓
対象フォルダ直下 archive.md にタイムスタンプ付き履歴を追記
```

### バックアップ（24時間常時稼働）

```
vault変更 → launchd（1時間ごと） → rsync → Google Drive同期
                                ↘
                                  毎時 :30 → git auto-commit → GitHub push  ⭐ NEW 2026-04-27
```

---

## 📝 保存場所のまとめ

| データ種類 | パス |
|---|---|
| vaultルール（最優先） | `CLAUDE.md` |
| カスタムスキル定義 | `.claude/commands/` |
| **外部スキル（obsidian-skills 5本）** ⭐ NEW 2026-04-28 | `.claude/skills/` |
| 自動化hook | `.claude/hooks/` |
| harness設定（hook登録先） | `.claude/settings.json` |
| 多階層メモリ（短期/中期/長期） | `_ memory/` ⭐ NEW |
| スキル候補バックログ（自己改善） | `Claudian-スキル候補.md` ⭐ NEW |
| 完了ノートのアーカイブログ | 各フォルダ直下 `archive.md` ⭐ NEW |
| note記事（原稿） | `SNS運用/note/` |
| note記事のサムネイル文言 | `SNS運用/title/` |
| 深掘り調査ノート | `調査/` |
| 日次X投稿 | `SNS運用/post/day*.md` |
| XのArticles記事 | `SNS運用/post/article/` |
| Xスレッド | `SNS運用/post/thread/` |
| 週次分析レポート（実績の事後分析・`/weekly-analytics` 出力） | `SNS運用/analytics/WNN分析レポート.md` |
| 週次戦略メモ（翌週方針・手動作成） | `SNS運用/analytics/WNN戦略メモ.md` |
| 週次分析の生CSV | `SNS運用/analytics/source/` |
| 本日アクションプラン（`/re-daily` Step 11 出力） | `SNS運用/action-YYYYMMDD.md` ⭐ NEW |
| 完了済みアクションプランの集約先 | `SNS運用/archive/action/` ⭐ NEW |
| 人格データ | `_ kiwami/my-clone/` |
| Daily Log ツール一式（スクリプト・plist・データ） | `_ kiwami/tools/daily-log/` |
| Clockify APIキー（vault外） | `~/.config/clockify-sync/api_key` |
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
- [[.claude/commands/news-thread.md]]
- [[.claude/commands/reply.md]]
- [[.claude/commands/weekly-analytics.md]]
- [[.claude/commands/md-format.md]]
- [[.claude/commands/quote-rewrite.md]]
- [[.claude/commands/deep-dive.md]]
- [[.claude/commands/archive.md]]
- [[.claude/commands/remember.md]]
- [[.claude/commands/reflect.md]]

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
