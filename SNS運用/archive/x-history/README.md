---
created: 2026-04-30
tags: [x-archive, sns運用, archive, content-recycle]
source: twitter-archive-202604
---

# X 過去投稿アーカイブ（2026-04-30 取り込み）

> **🔗 関連コンテンツ**
> - 🔬 取り込み判断の根拠: [[調査/2026-04-29-birdclaw-x-archive-tool.md]]
> - 📋 SNS運用全体像: [[Claudian-スキル一覧.md]]
> - 📊 週次分析（実績ベース）: [[SNS運用/analytics/フォロワー改善.md]]
> - 🎭 人格データ（過去投稿の発掘先）: `_ kiwami/my-clone/`
> - 📁 親フォルダ: [[SNS運用/archive/]]

## 📦 取り込みサマリー

| 項目 | 件数 / サイズ |
|---|---|
| ZIP元サイズ | 16MB（想定 5〜15GB の **約1/300**） |
| ツイート | **600件**（うち本投稿 269 / リプ 331） |
| Articles（X長文） | **12件**（個別MDに展開済） |
| いいね | **956件** |
| フォロワー | 214人 |
| フォロー中 | 195人 |
| DM | 0件（エクスポートで除外された可能性） |
| vault化後の総サイズ | 1.2MB |

### 年次内訳

| 年 | 件数 | 本投稿 | リプ |
|---|---:|---:|---:|
| 2022 | 6 | 6 | 0 |
| 2023 | 3 | 2 | 1 |
| 2024 | 30 | 30 | 0 |
| 2025 | **0** | 0 | 0 |
| 2026 | 561 | 231 | 330 |

> 💡 **2025年が完全に空白**。2026年（=今）が運用本格化のタイミングで、過去の重みは小さい。
> 「過去の自分」のリミックスより、「2026年の自分」の動線整理の方が価値が高い構造。

## 📂 ファイル構成

```
SNS運用/archive/x-history/
├── README.md                       ← このファイル
├── tweets/
│   ├── tweets.jsonl                ← 全600件のJSONL（grep/jq用の一次データ）
│   ├── tweets-by-favorite.md       ← いいね数 Top30 ランキング
│   ├── tweets-by-retweet.md        ← リポスト数 Top30 ランキング
│   └── by-year/
│       ├── 2022.md / 2023.md / 2024.md / 2026.md
├── articles/
│   ├── _index.md                   ← Articles 12件の一覧
│   └── {article_id}_{title}.md     ← 各Articles本文（frontmatter付き）
├── likes/
│   └── likes.jsonl                 ← 956件のいいね履歴
└── social/
    ├── followers.jsonl             ← 214人のフォロワーaccountId
    └── following.jsonl             ← 195人のフォロー中accountId
```

## 🔍 使い方（Birdclaw不要の手動運用）

### 全文検索

**Obsidian グローバル検索**（`Cmd+Shift+F`）でこのフォルダ配下を検索すれば、Birdclaw FTS5の代替として十分機能する。日本語の形態素もObsidian内蔵検索で問題なし。

### 過去のヒット作発掘（コンテンツリサイクル）

```bash
# いいね数 上位を確認
open "SNS運用/archive/x-history/tweets/tweets-by-favorite.md"

# JSONLから条件抽出（CLI）
jq 'select(.favorite_count >= 5)' SNS運用/archive/x-history/tweets/tweets.jsonl
```

### 過去投稿の引用RT素材化

`tweets-by-favorite.md` / `tweets-by-retweet.md` の上位から、再利用可能なテーマを抽出 → 引用RT or リライトで再投下。
[[SNS運用/analytics/フォロワー改善.md]] のコンテンツリサイクル戦略と接続。

### 批評型ポジションの一貫性チェック

`by-year/2026.md` を読み返して、自分の主張軸がブレていないか四半期1回確認。

## ⚠️ 既知の制約

| 制約 | 詳細 | 影響 |
|---|---|---|
| **impression数なし** | Twitter公式アーカイブには `impression_count` が含まれない | 「バズった = いいね数で代替判定」になる。impressionが必要なら週次分析CSVを別途参照 |
| **DM 0件** | `direct-messages.js` は126KBあるが標準フィールドで取得できなかった | DM必要時は raw `direct-messages.js` を別途処理 |
| **再申請24時間ルール** | Xアーカイブは申請から24-48h、ダウンロードリンク7日で失効 | 次回更新は最短でも明日以降 |
| **2025年空白** | エクスポート漏れではなく、運用が止まっていた期間 | この期間のデータは取得不可 |

## 🚪 次回更新時の手順

ZIP配置 → このREADMEと同じ Python 変換スクリプト再実行で全ファイル上書き再生成。
スクリプト本体は [[調査/2026-04-29-birdclaw-x-archive-tool.md]] の Phase B 完了記録に集約予定。

## 📝 取り込み履歴

- **2026-04-30**: 初回取り込み（このバッチ）
  - 申請: 2026-04-29 / 到着: 2026-04-30 13:51（約24時間）
  - 取り込み判断: Birdclaw撤退・vault直接統合（[[調査/2026-04-29-birdclaw-x-archive-tool.md]] Phase B 再々設計）
  - ZIP元: `~/Downloads/twitter-2026-04-30-db699524b3e1fd4186ad3150284c7b266801e1c67040b00018dbef6aad99687a.zip`
  - ZIPバックアップ先: `/Volumes/500GB/GoogleDrive/Tsukapon/x-archive/`
