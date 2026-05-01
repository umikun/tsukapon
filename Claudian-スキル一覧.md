# Claudian スキル & 機能一覧

> このvaultに組み込んだカスタムスキル・自動化・バックグラウンド機能の全体マップ。
> 迷ったらここを見れば、どの機能がどこにあるか一発でわかる。
>
> 🤖 **自動更新**: このファイルは [[CLAUDE.md]] のルール＋ `.claude/hooks/remind-skills-list.sh` により、
> スキル・自動化ファイルが変更されるたびに更新するように運用されている。

最終更新: 2026-05-02（**`/re-daily` Step 11-2-ter を全面改訂**。本日タイムラインを「ルーチン枠 10本固定 + 変動枠は空きスロット」の二層構造に再設計。固定枠は X朝=09:00／Threads朝=09:15／朝リプ=09:30／note公開=10:00／X記事転載版公開=10:15（NEW）／昼リプ=13:00／X夜=19:00／Threads夜=19:15／夜リプ=19:30／KPI=21:00 の10本。連投シリーズ・ニューススレッドv2・Day Oneプロモ等の戦略メモ由来タスクは空きスロット（11:00〜12:30 / 14:00〜18:30 / 20:00〜20:30 / 21:30〜22:00）に時系列で詰める。最重要枠は集中ピーク時間帯トップ3 に最も近いスロット、17・18時の脱線パターン警告日はその時間帯に変動枠を優先配置。休養日でも最低6本=KPI＋批評リプ3本＋note/Article公開を残す。旧 X朝=11:00／X夜=20:00 のスロット規定は廃止）/ 2026-05-01（**Daily Log dashboard に「⏰ リマインダー」カードを統合**。launchd で常駐する daily-log-server （`http://127.0.0.1:8765`）に Apple Reminders の状態を表示する仕組みを構築。① **TCC 問題の判明と回避**: launchd-spawned Python サブプロセスから `reminders` CLI / `osascript` を直叩きしても macOS の TCC（プライバシー制御）がサイレントに拒否されて stdout 空で返る現象を特定（`reminders show-lists` rc=0 / stdout="" / stderr=""）。`launchctl asuser` 経由・bash → osascript 経由なども試したが launchd context では TCC ダイアログが表示できず全部タイムアウト。最終的に **スナップショットファイル方式** で回避: Terminal context（Bash tool / 手動 cli）から定期的に `_ kiwami/tools/daily-log/reminders-snapshot.json` を更新し、dashboard はそれを読むだけにする設計。② **`~/bin/daily-log/reminders-snapshot.sh` 新設**: `reminders show-lists` で全リストを取得 → 各リストの未完了リマインダーを `--format json` で取得 → 一時ファイル経由のアトミック書き込みで JSON 出力。出力形式: `{ fetched_at: ISO, lists: { <listName>: [reminders...] } }`。③ **daily-log-server.py に `/api/reminders` 追加**: スナップショットファイルを読み、期限3日以内の緊急枠抽出・期限順ソート・サマリー集計（total_pending / overdue / urgent / list_count）を行ってJSONで返す。鮮度判定（30分超で stale=true）も付与。④ **dashboard UI に「⏰ リマインダー」カード追加**: 期限3日以内の緊急枠を最上部にリスト横断表示、Tsukapon と個人リストをセクション分け、優先度バッジ（🔴 high / 🟡 medium / 🔵 low）、人間に優しい期限表示（過去=🔴 / 今日 / 明日 / 7日以内=`M/D (曜) HH:MM` / それ以降）、🔄リフレッシュボタン、最終更新時刻表示。⑤ **`/show-reminders` `/sync-reminders` スキルにスナップショット書き出しを統合**: 各スキル末尾で `~/bin/daily-log/reminders-snapshot.sh` を自動実行し、Claudian セッションを使うたびに dashboard も最新化される連動性を確保。⑥ **CLAUDE.md「⏰ 絶対ルール」に「Daily Log ダッシュボード連携（スナップショット方式）」サブセクション追加**。dashboard 同期のタイミング3パターンを明文化。⑦ ~/bin と vault側の両方の daily-log-server.py / index.html を同期するワークフローも明記（launchd は `~/bin/daily-log/server/` 側を直接実行するため）） / 2026-05-01（**`/show-reminders` スキル新設**。`/sync-reminders`（書き込み）の対になる**読み取り専用スキル**。`reminders show` / `show-all` の生出力（インデックスと時刻だけのフラット表示）を、期限順ソート＋優先度アイコン＋絵文字プレフィックス分類込みのMarkdownテーブルに整形。入力5パターン: ① 引数なし → `Tsukapon` 未完了を期限順表示、② `--all` → 全リスト統合（期限3日以内の緊急枠を最上部、Tsukaponと個人リストをセクション分け）、③ `--list <name>` または `<name>` → 指定リスト、④ `--today` → 今日期限のみ全リスト横断、⑤ `--include-completed` → 完了済みも併記。期限表示は人間に優しい形式（過去=🔴、今日=`今日 HH:MM`、7日以内=`M/D (曜) HH:MM`、それ以降=`M/D HH:MM`、なし=`—`）、優先度は 🔴 high / 🟡 medium / 🔵 low。サマリー行（未完了N件 / 期限超過X件 / 期限3日以内Y件）を末尾に追加。CLAUDE.md「⏰ 絶対ルール」読み取り権限に厳密準拠 — `add` `complete` `delete` `edit` `new-list` を一切実行しない読み取り専用、個人リスト内容は表示のみで vault内ファイル転記禁止。50件超は上位30件で切る対策あり） / 2026-05-01（**Apple Reminders `Tsukapon` リストのタイトル命名コンベンションを正式化**。CLAUDE.md「⏰ 絶対ルール」に「`Tsukapon` リストのタイトル命名コンベンション」サブセクション追加。vault系自動同期タスクと一般業務TODOが混在するため、先頭の絵文字プレフィックスで出自・種別を識別: ① 自動同期（vault系・時刻あり）= `HH:MM 🧵/🐦/📝/🛠/🔄/💰/👥 内容`、② 一般業務TODO（手動追加）= `📋 内容`、③ 個人用買い物・雑事 = `🛒 内容`、④ 緊急・重要 = `🚨 内容`、⑤ 学習・読書 = `📚 内容`。手動 `add` 時は `📋` 必須、緊急度変更（`📋`→`🚨`）は `edit` の明示指示ルール準拠、vault自動同期形式（`HH:MM 種別 内容`）は `/re-daily` Step 11-6 専用で手動真似禁止（衝突防止）、付け忘れ既存リマインダーは無理に整形しない（ユーザー操作尊重）。これにより iPhone・Apple Watch のリマインダー一覧が「これは vault 自動同期？仕事？個人？」をひと目で判別可能に） / 2026-05-01（**Apple Reminders 連携の権限スコープを「読み取り全リスト・書き込みTsukapon限定」に拡張**。当初の Tsukapon 専用運用では個人の重要リマインダー（umikun.netの移管・請求書・仕事の締切等）が朝のセッション起動時に視界に入らず一元管理にならない不便があったため、CLAUDE.md「⏰ 絶対ルール: Apple Reminders は『読み取り全リスト・書き込みTsukapon限定』で運用する」に書き換え。① 読み取りは `reminders show-all` で全リスト統合 — 「今日のタスク見せて」と聞かれた時に Tsukapon系と個人系をセクション分けして時刻順／期限順に提示、個人タスクの期限が3日以内なら無関係な作業中でも1行で警告。② 書き込み権限マトリクスを明文化（show=全OK、add=Tsukapon自動・他は明示指示時のみ、complete=Tsukaponのみ・他は絶対NG、delete=他リスト絶対NG・Tsukaponも明示指示時のみ、edit=同上、new-list=Tsukapon自動作成のみ）。③「ユーザー明示指示」の判定基準を厳密化 — 対象リマインダー特定済みのみOK、「終わったやつ全部」のような曖昧スコープはNG。④ プライバシー配慮として個人リスト内容を vault内ファイルに転記禁止（ログ・コミット混入防止）。⑤ `/sync-reminders` スキル本体にも「🔴 リスト境界（絶対遵守）」セクションを追加し、`--clear` のスコープを Tsukapon 固定で明文化。リマインダーは `delete` 後の復元手段が事実上ないため、ドメイン消失級の事故を防ぐ防御線として機能） / 2026-05-01（**Apple Reminders 連携を全面導入**。① `reminders-cli` を `brew install keith/formulae/reminders-cli` でインストール。② Reminders に専用リスト `Tsukapon` を新規作成（既存個人リマインダーと混ざらない安全運用）。③ 新スキル [[.claude/commands/sync-reminders.md|/sync-reminders]] を新設 — `SNS運用/action-YYYYMMDD.md` のタイムライン早見表をパースし、各エントリ（`HH:MM 種別アイコン 内容`）を `--due-date` 付きで Reminders に登録、既存タイトル一致なら重複スキップ、`--clear` フラグで未完了一括完了マーク機能付き、9時前枠は CLAUDE.md ルール準拠でスキップ。④ `/re-daily` Step 11-6「Apple Reminders への自動同期」を新設 — Step 10 検証完了直後に `reminders` コマンドで自動同期、リスト不在なら `new-list` 自動作成、失敗してもStep 11全体は止めないbest-effort、完了報告に「⏰ Apple Reminders 同期: N件追加 / M件スキップ」の1行追加。⑤ CLAUDE.md に「⏰ 絶対ルール: セッション冒頭で Apple Reminders の `Tsukapon` リストを取り込む」を新設 — 多階層メモリ読込の直後に `reminders show Tsukapon --format json` を実行、ユーザーが「今日のタスク」等を尋ねた時のみ時刻順箇条書きで応答に反映、通常作業時は頭の中に持つだけで応答に毎回貼らない（情報過多防止）、`reminders` 未インストール時は黙ってスキップ。⑥ `apple-reminders` MCP サーバーを `claude mcp add --scope user` で登録（`mcp-server-apple-events` v1.4.0、FradSer/mcp-server-apple-events、EventKit ネイティブ）— `/Users/fukuokase/bin/apple-events-mcp.sh` という wrapper script で nodebrew の `node` を PATH に追加してから `npx -y mcp-server-apple-events` を起動、これで既存の context7・notion MCP が抱えていた「npx の shebang `#!/usr/bin/env node` が PATH 不在で失敗」問題を回避、`✓ Connected` 確認済。次セッションから `mcp__apple-reminders__reminders_tasks` 等のMCPツールが利用可能。連携先: iPhone・Apple Watch・Mac の Reminders アプリで時刻通知が飛ぶ → vault を開かずに次の行動が分かる体験を実現） / 2026-05-01（**CLAUDE.md に「📋 絶対ルール: コピペして使う部分はコードブロック形式で表示する」を新設**。SNS投稿本文／リプライ・引用RT／プロンプト例・コマンド例・コードスニペット／設定ファイル貼付サンプル／URLやファイルパスの一覧など「そのままコピーして別の場所に貼る」想定のテキストは、必ずコードブロック（``` ```）で囲んで出力する。複数候補は1つにつき1コードブロック、言語指定が自然な場合は `python` `bash` `json` 等を付けてOK、インラインの単一トークンはバッククォート1つで済ませてOK。対象外は通常の説明文・blockquote引用・箇条書きテーブル見出し・wikilink。これにより従来スキル個別に書いていた「コードブロックで出力」指示が vault全体の運用ルールに昇格し、スキル外の素のチャット応答や新規スキル追加時にも自動適用される。既存ファイルの一括書き換えは見送り — 新規作成ファイルから自動準拠の方針）/ 2026-05-01（**投稿本文系スキル5本にコードブロック出力ルールを統一**。投稿コンテンツを生成する `/reply` `/thread` `/news-thread` `/quote-rewrite` `/re-daily` の5スキルで、書き込み部分（投稿本文・返信本文・引用RT書き換え後本文）を**必ずコードブロック（``` ```）で囲んで出力**するルールを明文化。① `/reply`：返信本文をコードブロックで囲んで出力する旨を「出力形式（必須）」セクションで追加。複数案を出す時も各案ごとに独立したコードブロック。② `/thread`：保存ファイルの各投稿本文をコードブロックで囲み、字数等のメモはコードブロックの外。チャット返答時も1投稿1コードブロック。③ `/news-thread`：出力ファイルテンプレ（5/5まで）の `{本文}` を全てコードブロック内に変更。Step 9-3 #2 の表現を「**1投稿につき1コードブロック**で5本独立して出力」に更新。④ `/quote-rewrite`：Step 7 ファイルフォーマットで blockquote だった書き換え後本文をコードブロックに変更。Step 8 のチャット返答も「1本につき1コードブロック」を必須化。⑤ `/re-daily` Step 9（Xスレッド版）：保存先フォーマットに「各投稿の本文は必ずコードブロックで囲む」ルールと出力ファイル例を追記。Step 11 のアクションプラン側はすでに `本文（コピペ用）` コードブロック形式で対応済み）/ 2026-05-01（**`/re-daily` Step 4 に「太字（`**...**`）の使い方ルール」を新設**。note記事で太字が長くなりすぎて強調が拡散する問題を解消するため、以下を必須化: ① 太字は20字以内のキーワード／短いフレーズ限定（文や長い節を太字にしない）、② `**Nつ目: 〜**` の番号付き太字は最大15字でキーワード化（説明文は太字の外）、③ `**💾 〜前夜**` の囲み内も短く、④ 段落中の強調は「キーワード抽出」で行う（`核心は**評価軸の切り替わり**。〜` の形）、⑤ 例外として 5本紹介リストの章タイトル／列挙キーワード（`**物理＋ROI＋規制＋陣取り**`）／末尾固定CTAは20字超を許容、⑥ チェックリスト先頭の太字は10〜15字以内のラベル、⑦ 自己チェック義務化: 書き終えたら `grep -oE '\*\*[^*]+\*\*'` で全太字を抽出し、25字以上が5個以上なら書き直し。本日の `note-20260501.md` を新ルールで全面書き直し済み）/ 2026-04-30（**X公式アーカイブをvault直接統合**。`SNS運用/archive/x-history/` を新設し、Twitter ZIPアーカイブを `tweets.jsonl`（600件）/ `tweets-by-favorite.md`・`tweets-by-retweet.md`（Top30）/ `by-year/{2022,2023,2024,2026}.md` / Articles 12件の個別MD / `likes.jsonl`（956件）/ `social/{followers,following}.jsonl` に展開。実測16MB・600件と判明し、調査ノート [[調査/2026-04-29-birdclaw-x-archive-tool.md]] の Phase B 計画から **Birdclaw 撤退・vault直接統合** に再々設計。Obsidian グローバル検索が FTS5 の代替として成立する規模感のため、ポート3000衝突・WIP リスクを全部回避。2025年が完全空白で運用本格化が2026年からと判明）/ 2026-04-30（**`/re-daily` Step 11 の day*.md / Threads-day*.md 反映ルールを大幅強化**。当日アクションプランに日次X投稿・Threads投稿が漏れる事故が発生したため、以下を絶対必須化: ① Step 11-1 #5・#6 を「🔴 絶対必須・スキップ禁止」に格上げ — `ls -t | head -1` でmtime最新ファイルを確定し、本文内の `## 投稿①（朝）` `## 投稿②（夜）` 等の**全セクションを列挙**して**それぞれ独立したタイムラインエントリ化**を必須化。② Step 11-2-ter 新設「day*.md / Threads-day*.md 投稿の時刻配置ルール」 — デフォルト時刻スロット表（X朝=11:00／Threads朝=11:15／X夜=20:00／Threads夜=20:15）を明文化し、固定枠と被ったら15分ずらすロジックを規定。典型ケースは最低4エントリ追加。③ Step 10 検証に「1-bis. day*.md / Threads-day*.md の反映検証」を追加 — `grep` で action ファイルから両 wikilink を確認し、最低4ヒット未達なら 11-2-ter スロット表に従って自動補完）/ 2026-04-30（**`/reply` `/deep-dive` をグローバル化**。`~/.claude/commands/` 配下にユーザー版を新設し、Tsukapon vault 外（任意のディレクトリ）からも呼び出し可能に。① `/reply`：人格データを絶対パス `/Users/fukuokase/.../Tsukapon/_ kiwami/my-clone/` で参照。iCloud同期遅延で読めない場合は1行報告してルールベースで生成。② `/deep-dive`：`pwd` で環境判定 → vault内なら従来通り `調査/YYYY-MM-DD-{slug}.md` に保存、vault外なら `~/Documents/claudian-research/YYYY-MM-DD-{slug}.md` に保存。vault外モードではwikilinkを使わず通常のMarkdownリンクで書く。プロジェクト版（`.claude/commands/`）はそのまま残し、vault内では従来通りプロジェクト版が優先される二重化構成） / 2026-04-29（**`/re-daily` Step 11 にDaily Log連携を追加**。Step 11-0「Daily Logデータ取り込み」を新設し、`analytics.py daily yesterday` / `weekly current` / `distraction-patterns --days 7` の3コマンドを必須実行。アクションプラン本文の「メインミッション」直後に「📊 Daily Log 連携」セクションを必須挿入: ① 昨日の振り返り（集中度スコア／集中ピーク／触ったファイルTop3）／② 今週の集中ピーク時間帯トップ3 → **本日の最重要枠の配置根拠として時刻提示**／③ 注意すべき脱線パターン（3回以上検出）。早見表のルールに「最重要枠は集中ピーク時間帯トップ1〜2に合わせて配置・太字強調」を明文化。固定枠（10:00 note公開等）は別扱い） / 2026-04-29（**Daily Log データ活用スキル群を新設**。① 共通分析エンジン `_ kiwami/tools/daily-log/analytics.py` を新規作成（activity JSONL のみ採用／Clockify は実時間との乖離があるため不採用）。日次・週次サマリー、集中ピーク抽出、ファイル別時間、note執筆時間、時間帯別ヒートマップ、脱線パターン検出をサブコマンド化。② `/daily-summary` 新設（手動実行）— 引数の日付の作業内容を `_ memory/daily/YYYY-MM-DD.md` に Markdown 出力。集中度スコア・ピーク・触ったファイル Top10・my-clone トーンのジャーナルを含む。③ `/focus-report` 新設 — 直近1週間の曜日別/時間帯別 focus 比率と脱線パターンを `SNS運用/analytics/focus/Wnn-focus-report.md` に出力。3回以上検出したパターンは [[Claudian-スキル候補.md]] に自動エントリ（自己改善ループ連動）。④ `/weekly-analytics` に Step 6.5「Daily Log データ統合」を追加 — note記事ROI（執筆時間 vs エンゲージメント）／投稿時刻×直前30分の集中度／集中ピーク時間帯トップ3 を出力。レポート末尾に「🧠 作業時間分析（Daily Log連携）」セクションを必須化） / 2026-04-28（**スクショ命名規則を絶対ルール化＋ CLAUDE.md に「📸 絶対ルール: スクショ撮影タスクには必ずファイル名を指定する」セクション新設**。アクションプランで「スクショ撮って」と書きっぱなしにせず、**保存ファイル名まで決め切る**運用に変更。命名規則は `W{週番号}-{施策名}-{タイミング}-{連番}.png`（例: `W18-series02-EOD-1of4.png`）、保存先は `SNS運用/analytics/screenshots/` 統一。`/re-daily` Step 11 のアクションプラン生成時にも同ルールが適用される。本日の `action-20260428.md` の12:30連投②セクション・22:30本日KPIセクションを新ルールで全面修正済み（4枚連投／ルーチンB／ピン推移／note誘導の4種類のファイル名を明記） / 2026-04-28（**`SNS運用/全体ダッシュボード.base` を追加**。SNS運用/配下 376本の.mdを横断する大本のダッシュボード。`file.inFolder()` ベースの formula で「プラットフォーム」「サブ種別」「ステータス（active/pending/archived/draft）」を自動判別。7ビュー: 全体プラットフォーム別group／アクティブ更新順／最近7日／アーカイブ／待機中／戦略・分析・アクション／ギャラリーcards）/ 2026-04-28（**obsidian-skills 活用マップと posts.base を新規作成**。① [[Claudian-obsidian-skills活用マップ.md]] を vault root に新設（5スキル × Tsukapon vault 特化の活用ガイド／優先度マップ／見送り案ログを集約）。② [[SNS運用/post/posts.base]] を新設（`day*.md` / `thread/*.md` / `article/X-*.md` を横断する初の Bases ファイル。`file.folder` ベースの formula で種別判定し、6ビュー: 全投稿更新順／デイリー／スレッド／Articles／cards ギャラリー／7日以内更新 list を提供）。③ 「📚 参考データファイル」に「Bases」サブセクションを新設） / 2026-04-28（**`/news-thread` セクションに「実行方法」ブロックを追記**。チャット欄でのスラッシュコマンド呼び出し方を、A: ニュース直書き／B: 調査ノート起点／C: note記事起点／D: 対話モードの4パターン分、コピペ即実行可能な形で明記。曜日自動判定や火金以外の警告挙動などの呼び出し時のコツも追加） / 2026-04-28（**「Daily Log（Cowork artifact）」項目を削除**。Coworkサイドバーで開く artifact 版は使わなくなったため、クイックリファレンス1行・専用セクションを削除し、Clockify同期セクションの参照先を「Daily Log スタンドアロンWebサーバー（<http://127.0.0.1:8765>）」に書き換え。スタンドアロン版本体・launchd 4ジョブ（clockify-sync / activity-tracker / daily-log-server / git-fetcher）・データファイルは無変更で従来どおり稼働） / 2026-04-28（**`/re-daily` Step 11-3 のタイムラインに「早見表」を必須化＋ CLAUDE.md に絶対ルール追加**。`SNS運用/action-YYYYMMDD.md` の `## 🗓 タイムライン（時間軸順）` 直下に時刻×種別×内容のテーブルを必ず挿入する。種別アイコンは 🛠/📝/🐦/🧵/🔄/💰/👥 を使い分け、固定枠/最重要枠は太字。**9時前の投稿アクションは禁止**（運用制約）。リスケ時は早見表・個別セクション・翌日予定の3点を同時更新する整合性ルールも明文化。CLAUDE.md には「📅 絶対ルール: アクションプランファイルには必ず『タイムライン早見表』を冒頭に挿入する」セクションを新設。本日 `action-20260428.md` をテンプレートとして適用済み） / 2026-04-27（**`/re-daily` Step 11-1 を拡張**。本日アクションプラン生成時に `SNS運用/post/day*.md` 直下のX用日次投稿と `SNS運用/threads/Threads-day*.md` 直下のThreads用日次投稿を**必須読込**として追加。両者とも通し番号制（X側 `dayNN.md` ／ Threads側 `Threads-dayNN.md` で同番号対応）で、`ls -t` により直近ファイルを特定し、本文・投下時刻・連投構成をタイムラインに必ず反映する。`SNS運用/post/draft/` 配下しか拾われていなかったため、当日の日次X/Threads投稿が action ファイルに載らない事故を防ぐ） / 2026-04-27（**`/news-thread` スキル新設**。AIニュース「今週の1本」を v2型5投稿スレッド（要約→見解→不安→アクション→誘導）に落とし込む専用スキル。火・金の週2回モデル（[[SNS運用/analytics/news_thread_v2.md]]）の実行装置。入力4パターン対応（直書き／調査ノート起点／note記事起点／対話）、ソース候補は `調査/` `SNS運用/note/` `SNS運用/archive/note/` の3ディレクトリ。9ステップで生成→検証→保存し `SNS運用/post/thread/YYYYMMDD_news_v2_*.md` に出力。テンプレ全ルールを自動検証（140字／関係性キーワード／3アクション15分以内／ハッシュタグ禁止）。連携: `/thread`(note→8投稿)とは別系統で二重実行しない、`/re-daily` Step 9 とも独立） / 2026-04-27（**Daily Log Git Fetcher を新設（launchd 10分ごと） + Daily Log サーバーに `/api/fetch` `/api/fetch-status` 追加 + コミット表示にブランチ名・マージコミット情報を追加**。`git log --source` の `%S` でコミットの所属ブランチ、`%P` でマージ親判定 → サブジェクト解析（GitHub/Bitbucket/通常マージの3形式に対応）＋ 抽出失敗時は `git name-rev` で第2親から逆引き。UIにブランチバッジ4色（紫=ローカル/グレー=リモート/黄=タグ/オレンジ🔀=マージ）＋ 🔄 fetchボタン＋最終fetch時刻表示を追加。fetch本体は `_ kiwami/tools/daily-log/git-fetcher.py`（並列4・タイムアウト15秒）と `~/Library/LaunchAgents/com.user.git-fetcher.plist`（StartInterval=600 + RunAtLoad）の構成。Bitbucket等でWeb上から行ったマージが Daily Log に反映されない問題を解消） / 2026-04-27（**GitHub自動プッシュ plist のスケジュールを元に戻した**。直前の「火・金のみ」変更はユーザー意図の取り違えによる誤操作だったため、`StartCalendarInterval` を再び `Minute=30` 単一辞書（毎日毎時 :30）に戻して `launchctl unload/load`。`plutil -lint` 検証OK） / 2026-04-27（**Tsukapon vault → GitHub 自動プッシュ launchd を追加**。`~/Library/LaunchAgents/com.user.git-push-tsukapon.plist` ＋ `~/bin/git-push-tsukapon.sh` を新設し、毎時 :30 に未コミット変更を `auto: YYYY-MM-DD HH:MM hourly sync` 形式で commit → `origin/main` に push。osxkeychain 認証を流用、ネットワーク到達確認後のみ実行、変更ゼロ＋未push commit ゼロなら no-op で抜ける安全設計。ログ: `/tmp/git-push-tsukapon.log` ／ `/tmp/git-push-tsukapon-error.log`。初回手動キックで commit `5db46f0` の push を確認済み） / 2026-04-27（**`/re-daily` に Step 11「本日アクションプラン生成」を追加**。`SNS運用/analytics/` の WNN戦略メモ・WNN分析レポート・統合運用フロー・当日関連ドラフト（連投シリーズ・Day Oneプロモ・ピン候補等）を読み込み、本日の予定を時系列で1ファイルにまとめて `SNS運用/action-YYYYMMDD.md` に保存。実行手順・コピペ用本文・完了チェックを各アクションごとに詳述し、末尾に翌日予定を簡素に追記。出力ファイルが 4本 → **5本** に増加（note本体／サムネ文言／Article版／Thread版／本日アクション）。Step 10 の検証も5ファイルに更新。完了後ユーザーが手動で `SNS運用/archive/action/` に移動する運用。連動: ① `archive/action/` ディレクトリ作成 ② 本日分 `SNS運用/action-20260427.md` を W18戦略メモのカレンダーから生成（7:30 Day One X案B / 12:30 連投①/ 21:30 Threads案B / 夜 批評リプ + 翌4/28予定）） / 2026-04-27（**週次ファイル命名規則を整理: 「分析レポート」と「戦略メモ」を分離**。① `2026-W16.md` を `W16分析レポート.md` にリネーム（中身は週次分析レポートなので意味を反映）。② `/weekly-analytics` の出力先を `SNS運用/analytics/YYYY-WNN.md` → `SNS運用/analytics/WNN分析レポート.md` に変更。③ 命名規則を明確化: `WNN分析レポート.md` = `/weekly-analytics` 出力（実績の事後分析）／ `WNN戦略メモ.md` = 翌週方針メモ（手動作成）。同週でこの2本がペアになる想定。④ 連動更新: 4ファイルのwikilink書き換え（`W17戦略メモ.md` / `W17-Claude統合運用フロー.md` / `フォロワー改善.md` / `growth-strategy.md`）） / 2026-04-27（**`SNS運用/analytics/source/` を新設して生CSVを集約**。Xアナリティクスからエクスポートした `account_analytics_content_*.csv` ／ `account_overview_analytics_*.csv` の4本を `analytics/` 直下から `analytics/source/` に移動。レポート本文（`WNN分析レポート.md` / `WNN戦略メモ.md`）はwikilinkで `source/` 配下を参照する形に統一。連動更新: ① [[CLAUDE.md]] の「重要なファイル・フォルダ」表に `analytics/source/` 行を追加 ② `.claude/commands/weekly-analytics.md` の入力パターンBにCSV保存場所の注記を追加 ③ 既存ノート3件のCSV参照を新パスに書き換え（`W18戦略メモ.md` / `W16分析レポート.md`(旧 `2026-W16.md`) / `20260427_pin_candidates.md`）) / 2026-04-27（**Daily Log webサーバー の iCloud同期待ち wrapper 導入**。Mac起動直後に launchd が daily-log-server を起動した際、iCloud Drive がまだ index.html をローカル同期しておらず `Operation not permitted` で全リクエスト 500 となる問題を観測。`com.user.daily-log-server.plist` の `ProgramArguments` を bash wrapper に変更し、index.html が読めるまで 5秒×最大24回リトライ → 読めたら本体 Python を exec する方式に。プロセス再起動済み・HTTP 200 復旧確認済み） / 2026-04-27（**ディレクトリ再編 A1+A2 実施**。① ゴミ掃除: `.DS_Store`×8 / `__pycache__` / 重複ファイル `note-20260418 2.md` を `/Volumes/500GB/_trash/_ claude/A1_cleanup_20260427_*` へ退避。② アーカイブ命名統一: `SNS運用/{post,threads,note}/_fin/` → `SNS運用/archive/{post,threads,note}/` に集約（126ファイル移動）。③ 未稼働プラットフォーム集約: `SNS運用/_ 運用待機中/` → `SNS運用/pending/` リネーム。④ 関連スキル更新: `.claude/commands/archive.md`（5箇所）/`reflect.md`（3箇所）/`CLAUDE.md`（1箇所）の旧パス参照を新パスに書き換え。⑤ 全mdファイルの旧パスwikilinkを sed 一括置換（202ファイル / 残存ゼロ確認済み）。`/archive` スキルの移動先決定ロジックを「`SNS運用/{post,threads,note}` 配下なら `SNS運用/archive/{post,threads,note}/`」に変更） / 2026-04-26（`/re-daily` と `/thread` のXスレッド最終投稿の仮URLを `[noteのURL]` プレースホルダーから実URL風の `https://note.com/chackwill/n/abc` に変更。これによりnote公開後の手動差し替え時に視覚的にも"仮URLっぽさ"が出てミスが減る） / 2026-04-25（⭐ NEW: **Hermesエージェントの思想を3点取り込み**。① `/archive` スキル新設（完了ノートを `_fin/` または `_archive/YYYY-MM/` に自動仕分け＋ `archive.md` で時系列ログ化）、② **多階層メモリ** `_ memory/short-term.md` `mid-term.md` `long-term.md` 新設＋ `/remember` スキルで適切な層へ振り分け、③ **自己改善ループ** [[Claudian-スキル候補.md]] バックログ＋ `/reflect` でパターン検出。CLAUDE.md にも「セッション冒頭で多階層メモリを読む」「3回以上のパターンは候補化」の絶対ルール追加） / 2026-04-25（Daily Log スタンドアロン版を大型刷新：横幅フル幅化／カテゴリ・プロジェクト円グラフ／メモ自動保存欄（vault `Daily Log/memo/YYYY-MM-DD.md`）／`oclock.svg` をファビコン化／手動記録機能を削除。サーバには `GET/POST /api/memo/...` と `GET /favicon.svg` を追加） / 2026-04-25（`POST /api/save-md/YYYY-MM-DD` を追加） / 2026-04-24（⭐ NEW: **新規/追加ファイルの自動リンク設置ルール** を [[CLAUDE.md]] に追加。vault内への新規作成・外部コピーに対し、関連ファイルを推定して `🔗 関連コンテンツ` callout を H1 直下に自動挿入。対象外は `.obsidian/` `Clippings/` `調査/` `_ kiwami/tools/daily-log/` `.claude/` 等。Daily Log 一式も引き続き運用中: `_ kiwami/tools/daily-log/` にClockify同期（15分毎）・アクティビティトラッカー（60秒毎）・ローカルWebサーバー（常駐、<http://127.0.0.1:8765>））

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
| 1日の作業内容を自動集計して業務日報を出力 | Daily Log アプリ（スタンドアロン） | <http://127.0.0.1:8765> をブラウザで開く |
| その日の作業を Markdown 業務日報化（集中度スコア＋ピーク＋ジャーナル） | `daily-summary` | `/daily-summary` または `/daily-summary YYYY-MM-DD` |
| 直近1週間の集中傾向と脱線パターンを週次レポート化 | `focus-report` | `/focus-report` または `/focus-report 2026-W18` |
| 本日のアクションプランを Apple Reminders の `Tsukapon` リストに同期（iPhone・Apple Watchで通知） | `sync-reminders` | `/sync-reminders`（自動で本日分） / `/sync-reminders --clear`（未完了一括クローズ） |
| Apple Reminders の内容を見やすく一覧表示（読み取り専用・期限順テーブル） | `show-reminders` | `/show-reminders`（Tsukapon） / `/show-reminders --all`（全リスト統合） / `/show-reminders --today`（今日期限のみ） |

---

## 📦 カスタムスキル（このvault専用）

保存場所: `.claude/commands/`

### 1. [[.claude/commands/re-daily.md|/re-daily]] — note記事リライト＋サムネ文言＋X記事版＋Xスレッド＋本日アクションプラン一気通貫生成 ⭐ UPDATED 2026-05-02（Step 11-2-ter を全面改訂：本日タイムラインを「ルーチン枠 10本固定 + 変動枠は空きスロット」の二層構造に。X朝=09:00／Threads朝=09:15／X記事転載版公開=10:15／X夜=19:00／Threads夜=19:15／批評リプ朝昼夜=09:30/13:00/19:30／KPI=21:00 を毎日固定）

> **2026-05-02 変更点（本日タイムラインの固定スケジュール化）**: アクションプランの時刻配置がブレないよう、Step 11-2-ter を「ルーチン枠 + 変動枠」の二層構造に再設計:
>
> - **A. ルーチン枠（毎日 10本固定）**:
>   - **09:00** 🐦 day{N} 投稿①（朝）
>   - **09:15** 🧵 Threads-day{N} 投稿①（朝）短縮版
>   - **09:30** 👥 朝の批評型リプ（同業者の今朝のポスト）
>   - **10:00** 📝 note公開（+ 仮URL差し替え）
>   - **10:15** 🐦 X記事転載版 公開（← 新規固定枠）
>   - **13:00** 👥 昼の批評型リプ（煽り系インフルエンサー）
>   - **19:00** 🐦 day{N} 投稿②（夜）
>   - **19:15** 🧵 Threads-day{N} 投稿②（夜）短縮版
>   - **19:30** 👥 夜の批評型リプ（海外ポスト和訳＋ツッコミ）
>   - **21:00** 🔄 本日KPI記録
> - **B. 変動枠**: 連投シリーズ／ニューススレッドv2／Day Oneプロモ等の戦略メモ由来タスクは、空きスロット（11:00〜12:30 / 14:00〜18:30 / 20:00〜20:30 / 21:30〜22:00）に時系列で詰める。最重要枠は 11-0 の集中ピーク時間帯トップ3 に最も近いスロットへ
> - **C. 17時・18時の脱線パターン警告**が出ている日は、その時間帯への変動枠配置を優先（脱線アプリを開かせないための予定埋め）
> - **休養日でも最低6本** = KPI＋批評リプ3本＋note/Article公開（投稿系のみスキップ可）
> - 旧 11-2-ter（X朝=11:00／Threads朝=11:15／X夜=20:00／Threads夜=20:15）は廃止

> **2026-05-01 変更点（太字使用ルールの明文化）**: note記事の太字（`**...**`）が長くなりすぎて強調が拡散する問題を解消するため、Step 4「フォーマット整備」に「🔴 太字の使い方ルール（必須・厳守）」セクションを新設:
>
> - **太字は20字以内のキーワード／短いフレーズ限定**（文や長い節を太字にしない）
> - **「Nつ目: 〜」の番号付き太字は最大15字**（フォーマットは `**Nつ目: <短いキーワード>**`、詳細は太字の外）
> - **「💾 〜前夜」の囲み内の太字も短く**（長文を太字にしない）
> - **段落中の強調は「キーワード抽出」で行う**（「核心は**評価軸の切り替わり**。〜」のような形）
> - **例外（20字超を許容）**: 5本紹介リストの章タイトル／列挙キーワード（`**物理＋ROI＋規制＋陣取り**` など）／末尾固定CTA
> - **チェックリスト先頭の太字は10〜15字以内のラベル**
> - **自己チェック**: 書き終えたら全太字を `grep -oE '\*\*[^*]+\*\*'` で抽出し、25字以上が5個以上なら書き直し

> **2026-04-30 変更点（day*.md / Threads-day*.md 反映の強制化）**: 日次X投稿・Threads投稿がアクションプランから漏れる事故を防ぐため、3点を絶対必須化:
>
> - **Step 11-1 #5・#6 を「🔴 絶対必須・スキップ禁止」に格上げ**: `ls -t "SNS運用/post/"day*.md | head -1` でmtime最新の1ファイルを機械的に確定。本文内の `## 投稿①（朝）` `## 投稿②（夜）` 等の**全セクションを列挙**して、**それぞれ独立したタイムラインエントリ化**を必須化（1ファイル＝最低1〜複数エントリ）
> - **Step 11-2-ter 新設**: day*.md / Threads-day*.md 投稿の時刻配置スロット表を明文化
>   - X 朝 = **11:00** 🐦 / Threads 朝 = **11:15** 🧵 / X 夜 = **20:00** 🐦 / Threads 夜 = **20:15** 🧵
>   - 投稿③以降は既存スロットの隙間に15分間隔で挿入。固定枠（10:00 note公開・12:30 連投等）と被ったら15分ずらす
>   - 本文に投下時刻の明示指定（`> 投下: 12:00` 等）があればそれを優先
>   - 典型ケース（X 朝夜 + Threads 朝夜）= 最低4エントリを別建てで追加（既存リプ枠と混ぜない）
> - **Step 10-1-bis 新設**: アクションプランの存在確認後、`grep -E "day{番号}\.md|Threads-day{番号}\.md" "SNS運用/action-YYYYMMDD.md"` で両 wikilink の反映を検証。最低4ヒット未達なら 11-2-ter スロット表に従って自動補完し、早見表・個別セクション・翌日予定の3点を同期更新

> **2026-04-29 変更点（Daily Log 連携）**: Step 11-0「Daily Logデータ取り込み」を新設。`analytics.py daily yesterday` / `weekly current` / `distraction-patterns --days 7` を必須実行し、アクションプラン本文の「メインミッション」直後に「📊 Daily Log 連携」セクションを必ず挿入する：
>
> - **昨日の振り返り**: 集中度スコア／集中ピーク時間帯／触ったファイル Top3（用途コメント付き）
> - **今週の集中ピーク時間帯トップ3**: hour 別に集計 → 本日の最重要枠の配置時刻提示
> - **注意すべき脱線パターン**: 直近7日3回以上検出を警告表示（検出ゼロなら✨表記）
> - 早見表のルール拡張: **最重要枠は集中ピーク時間帯トップ1〜2に合わせて配置・太字強調**（固定枠は別扱い）
> - データ取得不能時は「データなし」と明記してスキップ（推測で埋めない）

> **2026-04-29 変更点**: アクションプランの「note公開後の実URL差し替え」タスク生成ルールを Step 11-2-bis として明文化。対象は **Thread版** と **day*.md / Threads-day*.md（grepヒット時のみ）** に限定し、**X記事転載版（`SNS運用/post/article/X-YYYYMMDD.md`）は構造上noteURLを含まないため常に対象外**とする。「念のため確認」のチェック項目も書かない。
>
> - 背景: Article版は本日note記事の中身を転載した独立コンテンツで、末尾プロモURLは神プロンプト記事への固定リンク。毎日不要なチェック工数が発生していた
> - 実装: Article版生成直後に `Grep` で `note\.com/chackwill/n/abc` を検索 → ヒットしたファイルのみリスト化（Article版は結果に関わらず除外）

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
- **Step 11**: 本日アクションプラン生成 ⭐ UPDATED 2026-04-30（day*.md / Threads-day*.md の反映を絶対必須化＋時刻スロット規定）
  - `SNS運用/analytics/` 配下の **当週WNN戦略メモ／前週WNN分析レポート／W*-Claude統合運用フロー** と、当日の連投シリーズ・Day Oneプロモ・ピン候補ドラフト・テンプレ・フォロワー改善メモを総ざらい
  - 🔴 **本日該当のX日次投稿** `SNS運用/post/day*.md`（mtime最新を `ls -t | head -1` で確定）と **Threads日次投稿** `SNS運用/threads/Threads-day*.md`（X側day番号と同番号を優先）を必ず読み込み、本文内の `## 投稿①（朝）` `## 投稿②（夜）` 等**全セクションを独立タイムラインエントリ化**（投下時刻明示なしなら X朝=11:00／Threads朝=11:15／X夜=20:00／Threads夜=20:15 をデフォルト適用）
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

**用途**: AIニュースを「今週の1本」に絞り、X/Threads向けの **v2型5投稿スレッド**（要約 → 一般論じゃない見解 → 不安喚起 → 具体アクション → note誘導）に落とし込む。火・金の週2回モデル（[[SNS運用/analytics/news_thread_v2.md]]）の実行装置。

**実行方法**:

Claudianのチャット欄で `/news-thread` をスラッシュコマンドとして呼び出し、続く本文として下記4パターンのいずれかを貼り付ける（同じメッセージ内に書く）。

```
# パターンA: ニュース直書き（最頻 — 火金朝の通常運用）
/news-thread
【今週の1本】OpenAI が o4-mini を発表
【ソース】https://openai.com/blog/...
【自分の現場】社内でo3 → o4-mini に切替検証始まってる
【曜日】fri          ← 任意。省略時は date +%u で自動判定
【テーマslug】o4-mini ← 任意。ファイル名用。省略時は自動生成
```

```
# パターンB: 調査ノート起点（/deep-dive の出力を使う）
/news-thread
【ソース】調査/2026-04-26-claude-code-100-best-repos.md
【自分の現場】煽りに引きずられた人を週3で見てる
```

```
# パターンC: note記事/アーカイブ起点（過去ネタの再構成）
/news-thread
【ソース】SNS運用/note/note-20260427.md
# または SNS運用/archive/note/ 配下のパス
```

```
# パターンD: 引数なし（対話モード）
/news-thread
```
→ 直近1週間の `調査/` `SNS運用/note/` `SNS運用/archive/note/` を `ls -t` で列挙してくれるので、番号で選択する。

**呼び出し時のコツ**:
- スレッド本体だけ欲しい時は `/news-thread` 単体で完結（note記事は不要）
- 火・金以外に実行すると「本来は火金運用」と警告が出るが、続行可能
- コマンドは1回の送信で完結する。Step 1〜9 はノンストップで走り切る設計

**入力フォーマット（4パターンの仕様まとめ）**:
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

**連携先**: [[SNS運用/analytics/news_thread_v2.md]]（テンプレ本体）／ [[SNS運用/analytics/W18戦略メモ.md]]（運用方針）／ `/quote-rewrite`（生成スレッドを引用RTに転用したい場合）

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

### 3. [[.claude/commands/reply.md|/reply]] — X返信生成 🌐 **グローバル化済み 2026-04-30**

**用途**: X投稿への返信コメントを生成

**入力**: 対象ポストの本文

**処理内容**:
- my-clone人格データを反映
- 共感ベース・3〜5文・絵文字1〜2個
- 「〜だよね」「〜かもなぁ」系の柔らかい語尾

**出力**: チャット内に返信案を表示

**呼び出し可能な場所**: 🌐 **どのディレクトリからでもOK**
- vault内（Tsukapon）: `.claude/commands/reply.md`（プロジェクト版／優先）
- vault外: `~/.claude/commands/reply.md`（ユーザー版／フォールバック）
  - 人格データは絶対パス `/Users/fukuokase/.../Tsukapon/_ kiwami/my-clone/` を参照
  - iCloud同期遅延で読めなかった場合は1行報告してルールベースで生成

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

### 7. [[.claude/commands/deep-dive.md|/deep-dive]] — ペースト文章の深掘り調査ノート生成 ⭐ NEW 2026-04-23 / 🌐 **グローバル化済み 2026-04-30**

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

**呼び出し可能な場所**: 🌐 **どのディレクトリからでもOK**
- vault内（Tsukapon）: `.claude/commands/deep-dive.md`（プロジェクト版／優先）
  - 保存先: `調査/YYYY-MM-DD-{topic_slug}.md` （vault相対）
  - Obsidian wikilink で関連ノート連携
- vault外: `~/.claude/commands/deep-dive.md`（ユーザー版／フォールバック）
  - 保存先: `~/Documents/claudian-research/YYYY-MM-DD-{topic_slug}.md`
  - 通常のMarkdownリンク `[text](path)` で書く（wikilinkは解決されないため）
  - frontmatter `source:` に「直接貼付（vault外）」と環境を明記

**環境判定ロジック**: `pwd` の結果が Tsukapon vault（`/Users/fukuokase/.../Tsukapon`）配下かどうかで保存先を自動切り替え

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

### 11. [[.claude/commands/daily-summary.md|/daily-summary]] — Daily Log 日次業務日報 ⭐ NEW 2026-04-29

**用途**: activity tracker の生データから、その日の作業内容を集計して Markdown の業務日報を生成。集中度スコア・集中ピーク時間帯・触ったファイル・my-clone トーンのジャーナルを含む。

**入力**:
```
/daily-summary             ← 今日（デフォルト）
/daily-summary today
/daily-summary yesterday
/daily-summary 2026-04-28
```

**処理内容**:
1. `_ kiwami/tools/daily-log/analytics.py daily <日付>` を呼び出して JSON 取得
2. `_ kiwami/my-clone/voice/` のトーンを読み込み（口調パターン・語尾クセ・NGワード）
3. ファイル名から作業内容を意味付け（note-YYYYMMDD → 当日note記事 等）
4. Markdown 生成: サマリー表 / 集中ピーク表 / 触ったファイル Top10 / アプリ別 Top5 / 脱線一覧 / **my-clone トーンの自然文ジャーナル 4-8行**
5. 自動特徴検出: 集中度スコア±10pt差、特定ファイルへ2時間以上集中、distraction 60分以上、トラッキング短時間 等
6. 保存と完了報告

**出力**: `_ memory/daily/YYYY-MM-DD.md`

**重要な仕様**:
- **Clockify データは使わない**（実時間との乖離があるため。activity tracker のみ採用）
- 手動実行のみ（launchd 自動起動はしない / 2026-04-29 ユーザー判断）
- ジャーナルは AI 文体禁止／my-clone トーン徹底／最大10行

**連携先**: `/focus-report`（週次集計の素材）、`/weekly-analytics`（短時間で伸びた記事の執筆プロセス再現性抽出）、`/remember`（特筆すべき気づきは多階層メモリへ昇格）

---

### 12. [[.claude/commands/focus-report.md|/focus-report]] — Daily Log 週次集中レポート＋脱線パターン検出 ⭐ NEW 2026-04-29

**用途**: 直近1週間の activity データから、曜日別・時間帯別の集中傾向を可視化。**3回以上繰り返す脱線パターンを検出した場合、自動的に [[Claudian-スキル候補.md]] にエントリ追加**（自己改善ループ連動）。

**入力**:
```
/focus-report             ← 今週（current）
/focus-report last        ← 先週
/focus-report 2026-W18
```

**処理内容**:
1. `analytics.py weekly <週>` と `analytics.py distraction-patterns --days 7` を呼ぶ
2. **集中ピーク時間帯トップ3**を hour 別に集計 → 来週の最重要枠配置の根拠
3. 曜日別 focus 比率テーブル
4. 時間帯ヒートマップ（24×7）を 5段階の絵文字（🟩🟨🟧🟥⬜）で可視化
5. 3回以上検出した脱線パターンを抽出 → [[Claudian-スキル候補.md]] に追記（重複チェック・⚪見送り判定済みは再追加しない）
6. 来週への提言3つ（集中ピーク時間帯への配置 / 脱線対策 / 集中度低曜日のテコ入れ）

**出力**: `SNS運用/analytics/focus/Wnn-focus-report.md`

**重要な連動**:
- **自己改善ループ**: 脱線パターン3回以上 → 候補ファイル自動エントリ（CLAUDE.md「🔁 自己改善ループ」絶対ルール）
- **タイムライン早見表の根拠**: 集中ピーク時間帯トップ3 を `/re-daily` Step 11 のアクションプランで「最重要枠の配置時刻」として参照する想定

**連携先**: [[Claudian-スキル候補.md]]（脱線パターン書き込み先）、`/weekly-analytics`（同週の Step 6.5 で同データを使う）、`/re-daily`（タイムライン早見表の最重要枠の根拠提供）

---

### 4. [[.claude/commands/weekly-analytics.md|/weekly-analytics]] — 週次分析 ⭐ UPDATED 2026-04-29（Step 6.5 Daily Log 統合追加）

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
- **Step 6.5 Daily Log データ統合 ⭐ NEW 2026-04-29**:
  - `analytics.py note-time` でnote記事の執筆実時間 → エンゲージメント率と並べて ROI 判定
  - 投稿時刻 × 直前30分の focus 比率で「集中時に書いた投稿 vs 慌ただしく書いた投稿」のパフォーマンス差
  - 集中ピーク時間帯トップ3 → 来週の最重要枠配置時刻の提案
- 他スキル連携提案（re-daily / thread / focus-report / daily-summary へ流す内容）

**出力**: `SNS運用/analytics/WNN分析レポート.md`（例: `W16分析レポート.md`） + 末尾に「🧠 作業時間分析（Daily Log連携）」セクション

**命名規則の使い分け（2026-04-27〜）**:
- `WNN分析レポート.md` … 本スキル出力（実績の事後分析）
- `WNN戦略メモ.md` … 翌週方針メモ（手動作成・別ドキュメント）
- 同週でこの2本がペアになる想定

**連携先**: `re-daily`（分析結果をnote記事に反映）、`thread`（伸びた投稿のスレッド化）、`focus-report`（同週の集中傾向データ）、`daily-summary`（短時間で伸びた記事の執筆プロセス再現性抽出）

---

### 14. [[.claude/commands/show-reminders.md|/show-reminders]] — Apple Reminders 一覧表示（読み取り専用） ⭐ NEW 2026-05-01

**用途**: `reminders` CLI の生出力を、期限順ソート＋優先度アイコン＋絵文字プレフィックス分類込みのMarkdownテーブルに整形して表示。`/sync-reminders`（書き込み）の対になる読み取り専用スキル。

**入力**（5パターン対応）:
- A: 引数なし → `Tsukapon` の未完了を期限順表示
- B: `--all` → 全リスト統合（期限3日以内の緊急枠を最上部、Tsukaponと個人リストをセクション分け）
- C: `--list <name>` または `<name>` → 指定リスト
- D: `--today` → 今日期限のみ全リスト横断
- E: `--include-completed` → 完了済みも併記（取り消し線）

**期限表示ルール**:

| 状態 | 表示 |
|---|---|
| 過去 | `🔴 M/D HH:MM 過ぎ` |
| 今日 | `今日 HH:MM` |
| 明日 | `明日 HH:MM` |
| 7日以内 | `M/D (曜) HH:MM` |
| それ以降 | `M/D HH:MM` |
| 期限なし | `—` |

**優先度表示**: 🔴 high / 🟡 medium / 🔵 low / `—` none

**サマリー**: 末尾に「未完了N件 / 完了済みM件 / 期限超過X件 / 期限3日以内Y件」を1行で

**前提**:
- `reminders-cli` がインストール済み

**禁止事項（CLAUDE.md「⏰ 絶対ルール」読み取り権限準拠）**:
- `add` / `complete` / `delete` / `edit` / `new-list` を**一切実行しない**
- 個人リスト内容は表示のみで vault内ファイル転記禁止（プライバシー配慮）

**連携先**: `/sync-reminders`（書き込み側） / CLAUDE.md「⏰ 絶対ルール」（権限マトリクス）

---

### 13. [[.claude/commands/sync-reminders.md|/sync-reminders]] — Apple Reminders 同期 ⭐ NEW 2026-05-01

**用途**: `SNS運用/action-YYYYMMDD.md` のタイムライン早見表を macOS Reminders の `Tsukapon` リストに時刻付きで登録。iPhone・Apple Watch・Mac の3端末で時刻通りに通知が飛ぶようにする。

**入力**（3パターン対応）:
- A: 引数なし → 本日の `action-$(date +%Y%m%d).md` を自動取得
- B: ファイルパス指定 → `/sync-reminders SNS運用/action-20260501.md`
- C: `--clear` → 未完了リマインダー一括完了マーク（朝の整理用）

**処理内容**:
- `reminders show-lists` で `Tsukapon` リスト存在確認、不在なら `new-list` で自動作成
- アクションプラン本文から `## 🗓 タイムライン（時間軸順）` 直下の早見表テーブルをパース
- 各行から `HH:MM` / 種別アイコン / 内容を抽出
- リマインダータイトル形式: `HH:MM 🧵 内容`（重複防止のためタイトル完全一致でスキップ）
- `--due-date "YYYY-MM-DD HH:MM"` でアクションプラン日付＋時刻の期限設定
- 9時前枠は CLAUDE.md「📅 タイムライン早見表」ルール準拠でスキップ
- 失敗時は `stderr` 報告で続行（処理を止めない）

**前提**:
- `reminders-cli` がインストール済み（`brew install keith/formulae/reminders-cli`）
- macOS のリマインダーアクセス許可付与済み
- Reminders に `Tsukapon` リスト存在（無ければ自動作成）

**出力**: macOS Reminders `Tsukapon` リストへのリマインダー追加 + チャットへ「N件追加 / M件スキップ / X件失敗」報告

**連携先**: `/re-daily` Step 11-6（アクションプラン保存直後に自動呼び出し）/ CLAUDE.md「⏰ 絶対ルール: セッション冒頭で Apple Reminders 取り込み」（読み出し側）

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
| [[SNS運用/analytics/フォロワー改善.md]] | フォロワー獲得のCTA・ハッシュタグ戦略 |
| [[SNS運用/analytics/Xへ記事転載.md]] | X Articles（記事転載）の戦略・変換ルール |
| [[Claudian-obsidian-skills活用マップ.md]] ⭐ NEW 2026-04-28 | obsidian-skills 5本のTsukapon vault特化活用ガイド |

### Bases（DB的ビュー）

| ファイル | 役割 |
|---|---|
| [[SNS運用/全体ダッシュボード.base]] ⭐ NEW 2026-04-28 | SNS運用/配下376本を「プラットフォーム×ステータス」で横断する大本のダッシュボード（7ビュー） |
| [[SNS運用/post/posts.base]] ⭐ NEW 2026-04-28 | X投稿（day/thread/article）の横断ダッシュボード |

### 過去記事アーカイブ

| 場所 | 内容 |
|---|---|
| `SNS運用/note/note-YYYYMMDD.md` | 毎日のnote記事（リライト対象） |
| `SNS運用/post/day*.md` | 日次X投稿のドラフト |
| `SNS運用/post/article/X-YYYYMMDD.md` | XのArticles版 |
| `SNS運用/post/thread/` | Xスレッド保存先 |
| `SNS運用/analytics/` | 週次分析レポート |
| [[SNS運用/archive/x-history/README.md]] ⭐ NEW 2026-04-30 | **X公式アーカイブ取り込み版**。tweets.jsonl（600件）/ いいね・リポストTop30 / 年次ダンプ / Articles12件 / likes.jsonl（956件）。Birdclaw撤退判断＋vault直接統合の最終形（→ [[調査/2026-04-29-birdclaw-x-archive-tool.md]] Phase B 完了記録） |

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

**内容**: Clockifyの時間エントリを15分ごとにAPI経由で取得し、`_ kiwami/tools/daily-log/clockify/YYYY-MM-DD.json` に日付別保存。**Daily Log スタンドアロンWebサーバー（<http://127.0.0.1:8765>）** が参照するデータソース。

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

### ⏰ Apple Reminders 連携 ⭐ NEW 2026-05-01 / ⭐ UPDATED 2026-05-01（権限スコープを「読み取り全リスト・書き込みTsukapon限定」に拡張 + Daily Log dashboard 連携追加）

**Daily Log dashboard 連携（スナップショット方式）:**

`http://127.0.0.1:8765` の dashboard 上に「⏰ リマインダー」カードが追加され、Tsukapon/個人リストの状態を可視化できる。仕組みは launchd の TCC 制約を回避するスナップショットファイル方式:

| ファイル | 役割 |
|---|---|
| `~/bin/daily-log/reminders-snapshot.sh` | reminders-cli を呼び出して `_ kiwami/tools/daily-log/reminders-snapshot.json` に書き出すスクリプト |
| `_ kiwami/tools/daily-log/reminders-snapshot.json` | dashboard が読むキャッシュファイル（30分超で stale=true 表示） |
| `daily-log-server.py` の `/api/reminders` | スナップショットを読んで期限順ソート・緊急枠抽出して返す |
| dashboard の「⏰ リマインダー」カード | UI 表示。緊急枠（期限3日以内）→ Tsukapon → 個人リスト の順 |

**スナップショット更新タイミング**:
- `/show-reminders` 実行時 → Step 6 で自動更新
- `/sync-reminders` 実行時 → Step 6 で自動更新
- ユーザーが手動で `~/bin/daily-log/reminders-snapshot.sh` 実行

dashboard 上の `🔄` ボタンは **API を叩くだけで JSON 自体は更新しない**（launchd context は TCC で reminders を読めないため）。最新化したい時は Claudian セッションで `/show-reminders` を1回実行するか、Terminal から手動でスクリプトを叩く運用。



**内容**: macOS Reminders を「本日の行動指示の通知レイヤー＋一元管理ハブ」として組み込み。アクションプラン（`SNS運用/action-YYYYMMDD.md`）の早見表を `Tsukapon` リストに同期し、iPhone・Apple Watch・Mac の3端末で時刻通知を受けられる状態にする。読み出し側はセッション起動ルールで**全リスト統合**で自動取り込み（vault系タスク＋個人タスクをまとめて把握）。書き込みは事故防止のため `Tsukapon` リスト限定。

**権限マトリクス（CLAUDE.md「⏰ 絶対ルール」準拠）:**

| 操作 | 全リスト（個人） | `Tsukapon` | 備考 |
|---|---|---|---|
| `show` / `show-all`（読み取り） | 🟢 OK | 🟢 OK | 副作用ゼロ |
| `add` | 🟡 ユーザー明示指示時のみ | 🟢 OK | デフォルトは Tsukapon |
| `complete` | 🔴 NG | 🟢 OK | 個人タスクの誤完了は痛い |
| `uncomplete` | 🟡 ユーザー明示指示時のみ | 🟢 OK | リカバリー用 |
| `delete` | 🔴 **絶対NG** | 🟡 明示指示時のみ | 復元不能 |
| `edit` | 🔴 NG | 🟡 明示指示時のみ | 改ざん事故防止 |
| `new-list` | — | 🟢 不在時自動作成のみ | 他リストは作らない |

| ファイル / 仕組み | 役割 |
|---|---|
| `reminders-cli`（`/usr/local/bin/reminders`） | macOS Reminders 操作CLI（`brew install keith/formulae/reminders-cli`） |
| Reminders リスト `Tsukapon` | 本vault専用リスト（既存個人リマインダーと混ざらない） |
| [[.claude/commands/sync-reminders.md|/sync-reminders]] | アクションプラン → Reminders 同期スキル（`/re-daily` Step 11-6 から自動呼び出し） |
| `~/bin/apple-events-mcp.sh` | `apple-reminders` MCP サーバー起動 wrapper（nodebrew node を PATH に追加して `npx -y mcp-server-apple-events` を起動） |
| `~/.claude.json` の `mcpServers.apple-reminders` | MCP登録（user スコープ） |
| CLAUDE.md「⏰ 絶対ルール: セッション冒頭で Apple Reminders の `Tsukapon` リストを取り込む」 | 読み出し側ルール — `reminders show Tsukapon --format json` を毎セッション冒頭で実行 |
| CLAUDE.md `/re-daily` Step 11-6「Apple Reminders への自動同期」 | 書き込み側ルール — アクションプラン保存直後に同期 |

**動作フロー**:

1. 朝 `/re-daily 記事パス` 実行
2. Step 1〜10 で 5ファイル生成（note本体／サムネ文言／Article版／Thread版／action-YYYYMMDD.md）
3. **Step 11-6 が `reminders` で `Tsukapon` リストに自動同期**（早見表の各行を時刻付きで登録）
4. iPhone・Apple Watch・Mac で時刻通知が届く
5. ユーザーが各端末でリマインダーを完了マーク
6. 翌朝のセッション冒頭で Claudian が `reminders show Tsukapon` を読み、未完了タスクを把握

**確認コマンド**:

```bash
# CLI から
reminders show Tsukapon
reminders show Tsukapon --format json | jq .
reminders new-list "Tsukapon"  # 万一消した時の再作成

# MCP サーバー稼働確認
claude mcp list | grep apple-reminders
```

**既知の制約**:

- macOS のリマインダーアクセス許可ダイアログを最初に承認する必要あり（CLI / MCP 両方）
- 9時前の時刻枠は `/sync-reminders` 側でスキップ（CLAUDE.md「📅 タイムライン早見表」運用制約）
- リマインダーの完了マークは ユーザー操作を尊重。Claudian は明示指示時のみ完了処理する

**トラブルシュート**:

- `reminders not found` → `brew install keith/formulae/reminders-cli`
- MCP `✗ Failed to connect` → wrapper script の実行権限と PATH を確認（`chmod +x ~/bin/apple-events-mcp.sh`）
- リスト表示が空 → 初回権限ダイアログを承認する（`システム設定 → プライバシーとセキュリティ → リマインダー`）

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
| `apple-reminders` ⭐ NEW 2026-05-01 | macOS Reminders（リマインダー）の add / list / complete / delete / 期日設定 / リスト指定 / サブタスク / 繰り返し / 位置情報 / Calendar も同梱（mcp-server-apple-events v1.4.0、EventKit ネイティブ）。`/sync-reminders` スキルとは別系統で、ネイティブ MCPツール `mcp__apple-reminders__*` として呼べる | ✅ ユーザースコープ登録済み |

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

### Apple Reminders MCP の使い方 ⭐ NEW 2026-05-01

`apple-reminders` MCPは **macOS Reminders を Claudian から直接読み書き** するためのMCPサーバー。`/sync-reminders` スキル（CLI叩く方）と用途が重なるが、**ネイティブMCPツール感覚で使える**点が違う（`mcp__apple-reminders__reminders_tasks` 等）。

- **提供**: [FradSer/mcp-server-apple-events](https://github.com/FradSer/mcp-server-apple-events)（v1.4.0、2026-03-10更新、EventKit ネイティブ統合）
- **スコープ**: `user`（グローバル）→ 全プロジェクトで利用可能
- **登録先**: `~/.claude.json` のトップレベル `mcpServers.apple-reminders`
- **起動コマンド**: `/Users/fukuokase/bin/apple-events-mcp.sh`（wrapper script）
- **wrapper の中身**:
  ```bash
  #!/bin/bash
  export PATH="/Users/fukuokase/.nodebrew/current/bin:$PATH"
  exec npx -y mcp-server-apple-events "$@"
  ```
  これで `npx` の shebang `#!/usr/bin/env node` が PATH 不在で失敗する問題を回避（既存の context7・notion MCP も同根。今後の MCP 追加時は wrapper 経由が安全）
- **追加方法**（再登録時・グローバル）:
  ```bash
  claude mcp add --scope user apple-reminders /Users/fukuokase/bin/apple-events-mcp.sh
  ```
- **権限**: 初回起動時に macOS が「リマインダーへのフルアクセス」許可ダイアログを出す。許可しないと EventKit が動かない
- **対応機能**: `reminders_tasks`（add/list/complete/delete/期日/優先度/リスト指定）/ `reminders_lists`（リスト管理）/ `reminders_subtasks` / 繰り返し / 位置情報トリガ / タグ / Calendar 同梱

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
- [[.claude/commands/reply.md]] 🌐 グローバル版あり: `~/.claude/commands/reply.md`
- [[.claude/commands/weekly-analytics.md]]
- [[.claude/commands/md-format.md]]
- [[.claude/commands/quote-rewrite.md]]
- [[.claude/commands/deep-dive.md]] 🌐 グローバル版あり: `~/.claude/commands/deep-dive.md`
- [[.claude/commands/archive.md]]
- [[.claude/commands/remember.md]]
- [[.claude/commands/reflect.md]]

**🌐 グローバル版（vault外でも使えるユーザー版）の編集場所**:
- `~/.claude/commands/reply.md` — 人格データを絶対パスで参照
- `~/.claude/commands/deep-dive.md` — 保存先を環境判定で切替（vault内→`調査/`、vault外→`~/Documents/claudian-research/`）

vault内ではプロジェクト版（`.claude/commands/`）が優先されるため、両者は独立して編集可能。vault外で挙動を変えたいときだけユーザー版を編集する。

### スキルが動かない

1. `.claude/commands/` にファイルがあるか確認
2. Claude Codeを再起動してスキル一覧を再ロード
3. 入力形式（`$ARGUMENTS`）が正しいか確認

---

## 🔗 関連ドキュメント

- [[Macで定期的に同期.md]] — launchd同期の設定手順
- [[HOME.md]] — vaultのエントリポイント（もしあれば）
- [[SNS運用/analytics/フォロワー改善.md]] — X運用改善プラン
- [[SNS運用/analytics/Xへ記事転載.md]] — X Articles戦略
