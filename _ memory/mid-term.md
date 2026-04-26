---
tags: [memory, mid-term]
scope: 「今四半期〜半年」レンジ。運用方針・現在進行中の戦略
last_updated: 2026-04-25
---

# 🟡 Mid-Term Memory（中期記憶）

> **このファイルの役割**
> - 3〜6ヶ月続く「運用方針」「現在の戦略」「定常的な前提」を置く
> - `short-term` から昇格してきたもの、`long-term` ほど不変ではないもの
> - 四半期ごとに見直し（古くなった項目は `archive.md` 行き、一段上がる項目は `long-term` 行き）

---

## 🎯 現在の運用戦略（2026 Q2）

### SNS運用方針

- **メインプラットフォーム**: X（旧Twitter）
- **収益化基準**: Verified + Home Timeline の有機的インプレッション（2026-01改定後）
- **コンテンツ軸**:
  - 日次X投稿（`SNS運用/post/day*.md`）
  - 週次note記事 → リライト → スレッド化 → 引用RT展開
- **避けるパターン**: リプ欄スパム、AI定型文、「いかがでしたか」調

### サブプラットフォーム観測

- **Threads**: アフィ直リンクOK / 3-5:1 ratio / 様子見ステージ
- **note**: 長文ハブ。X導線として機能
- **Discord**: 2チャンネル運用（情報ログ + モバイルメモ）に縮小済み

## 🧠 Claudian運用方針

- **人格データ**: `_ kiwami/my-clone/` を文体ソースに
- **スキル拡張ルール**: `.claude/commands/` 追加 → 必ず `Claudian-スキル一覧.md` 更新
- **メモリ階層**: short / mid / long の3層構造（このファイル含む）
- **自動化境界線**: `rm` 禁止 / `mv` のみ / `_fin/` `_archive/` で物理隔離

## 🛠 現役のスキル（2026 Q2）

| スキル | 用途 | 頻度 |
|---|---|---|
| `/deep-dive` | 外部情報の調査ノート化 | 高 |
| `/re-daily` | note → X記事 → スレッド一気通貫 | 中 |
| `/thread` | 長文 → スレッド分解 | 中 |
| `/reply` | 返信下書き | 中 |
| `/quote-rewrite` | 引用RTの口調統一 | 中 |
| `/md-format` | Markdown整形 | 中 |
| `/weekly-analytics` | 週次データ分析 | 週1 |
| `/archive` | 完了ノート自動仕分け | 日次 |

## 📊 現在の運用前提（変更したらここを更新）

- 外部バックアップ: 1時間ごと launchd → Google Drive
- 削除はすべて `/Volumes/500GB/_trash/_ claude/` 行き
- 自動リンク（🔗 関連コンテンツ）はvault新規ファイル作成時に必ず検討
- daily-log: `_ kiwami/tools/daily-log/` で自動収集中

---

## 📝 メモの書き方

- 「3ヶ月以上はこの方針でいく」と判断した項目だけ
- 短期メモから昇格したら、元のshort-term側からは消してよい
- 不変ルール（鉄則・哲学）になったら `long-term.md` に昇格
