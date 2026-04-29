Daily Log（activity tracker）のデータから、その日の作業内容を自動集計してMarkdown形式の業務日報を生成するスキル。`_ memory/daily/YYYY-MM-DD.md` に出力する。

## 入力形式

```
/daily-summary [日付]
```

- 日付指定なし or `today` → 今日
- `yesterday` → 昨日
- `YYYY-MM-DD` → 指定日

## 処理手順

### Step 1: 集計データの取得

`_ kiwami/tools/daily-log/analytics.py` を呼び出して日次サマリーを取得：

```bash
/usr/bin/python3 "_ kiwami/tools/daily-log/analytics.py" daily <日付>
```

返り値の JSON を読み込む。`empty: true` なら「その日のデータなし」とユーザーに伝えて終了。

### Step 2: 自然文ジャーナルのトーン把握

以下を読み込んでトーンを揃える：
- `_ kiwami/my-clone/voice/口調パターン.md`
- `_ kiwami/my-clone/voice/語尾クセ.txt`
- `_ kiwami/my-clone/voice/NGワード.md`

**重要**: 「いかがでしたか」「活用してみましょう」など AIっぽい硬い文章は禁止。日記風のカジュアルな一人称で書く。

### Step 3: ファイル別時間の意味付け

`top_files` の各ファイルが何だったかを推測し、コメントを添える：

- `note-YYYYMMDD` → その日のnote記事執筆
- `action-YYYYMMDD` → その日のアクションプラン編集
- `dayNN`（dayNNN） → X日次投稿
- `Threads-dayNN` → Threads投稿
- `WNN戦略メモ` / `WNN分析レポート` → 週次の振り返り
- `Claudian-スキル一覧` → スキル運用
- `growth-strategy` → 成長戦略
- それ以外 → そのまま表示

### Step 4: Markdown 生成

以下のフォーマットで `_ memory/daily/YYYY-MM-DD.md` に出力する：

```markdown
# Daily Summary: YYYY-MM-DD ({曜日})

> **🔗 関連コンテンツ**
> - 📊 Daily Log: <http://127.0.0.1:8765>
> - 📝 短期メモリ: [[_ memory/short-term.md]]
> - 📅 当日アクションプラン: [[SNS運用/action-YYYYMMDD.md]]（存在する場合のみ）

## 📊 サマリー

| 項目 | 値 |
|---|---|
| トラッキング総時間 | NN分（NhN分） |
| 集中（focus） | NN分（XX.X%） |
| その他（other） | NN分（XX.X%） |
| 脱線（distraction） | NN分（XX.X%） |
| アイドル（idle） | NN分（XX.X%） |
| **集中度スコア** | **XX.X%** （focus / (focus+other+distraction)） |

## 🎯 集中ピーク時間帯

> 連続30分以上の focus セッション。`top_app` は時間内で最も使ったアプリ。

| 時刻 | 長さ | アプリ |
|---|---|---|
| HH:MM-HH:MM | NN分 | Obsidian |
| ... | ... | ... |

（ピークが0個なら「⚠️ 30分以上の連続集中なし」と表示）

## 📂 触ったファイル Top 10

| ファイル | 時間 | アプリ | コメント |
|---|---|---|---|
| `action-20260428` | 103分 | Obsidian | 本日のアクションプラン編集 |
| `note-20260428` | 16分 | Obsidian | 本日のnote記事 |
| ... | ... | ... | ... |

## 🖥 アプリ別時間 Top 5

| アプリ | 時間 | 主カテゴリ |
|---|---|---|
| Obsidian | 283分 | focus |
| Opera | 248分 | focus |
| ... | ... | ... |

## ⚠️ 脱線（distraction）が出たら

```
17:00-17:15 Day One（15分）
18:00-18:30 cooViewer（30分）
```

（distraction が0なら「✨ 脱線ゼロ」と表示。3件以上ある日は **目立たせる**。）

## 📝 ジャーナル

{自然文。my-clone のトーンで 4〜8行程度。以下を盛り込む}

- その日に最も時間を使ったファイル/プロジェクトの言及
- 集中ピークの時間帯と何をしていたか
- 脱線が目立つ場合は素直に認める（責めない／改善トーン）
- 翌日に向けた一言（軽く）

例:
> 今日はaction-20260428に103分かけて、本日のアクションプランをガッツリ整理。9-11時の2時間ちょい連続集中は最近で一番長い。
> 夕方17時台にDay Oneで15分横道それたけど、まあ許容範囲。
> 明日はnote執筆をもう少し朝に寄せたい。

## 🔄 自動検出した今日の特徴

{Step 5 で計算する。なければセクションごと省略}
```

### Step 5: 自動特徴検出（オプション）

以下に該当するものがあればセクションを追加：

- **集中度スコアが直近7日平均より +10pt 以上 / -10pt 以上** → 「⭐ 今週ベスト級の集中日」or 「⚠️ 集中度低め」
- **特定ファイルに2時間以上集中** → 「🔥 集中投資: `<file>` に NNN分」
- **distraction が60分以上** → 「⚠️ 脱線が多めの日（NN分）」
- **トラッキング時間が直近7日中央値より大幅短い** → 「💤 PC前にいた時間が短め」

直近7日比較は `weekly current` と過去日の `daily` を順次叩いて算出する。

### Step 6: 保存と完了報告

1. `_ memory/daily/` ディレクトリが存在しなければ作成
2. ファイルを書き出す
3. ユーザーに以下を報告:
   - 出力パス（wikilink）
   - 集中度スコア
   - 集中ピーク時間帯のトップ1
   - 脱線あれば1行で要約

## 完了時の宣言

タスク完了報告に以下を必ず含める：
- 「📊 Daily Summary を生成しました: [[_ memory/daily/YYYY-MM-DD.md]]」
- 「🎯 集中ピーク: HH:MM-HH:MM (NN分, アプリ)」
- 脱線3件以上なら「⚠️ 脱線 N件: ...」も追記

## 制約事項

- **AIっぽい硬い文章を書かない**: my-clone のトーンを参照
- **嘘を書かない**: データに無い時間帯/ファイルを推測で埋めない
- **ジャーナルは絶対に長くしすぎない**（最大10行）
- **関連リンクの自動設置ルール**は適用対象外（`_ memory/daily/` は CLAUDE.md のリンク自動設置対象外。`🔗 関連コンテンツ` ブロックは Step 4 のテンプレに含めて固定で出す）

## 入力データ

$ARGUMENTS
