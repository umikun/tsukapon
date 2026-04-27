# Discord運用方針（vault連携前提）

## ⚠️ 方針変更：自分用Discordサーバーは「外部一次情報インボックス」に縮小

このvault（Tsukapon）と機能が重複していたため、**自分専用サーバーは2チャンネル運用に絞る**。
ストック・編集・公開はすべてvault側に集約する。

### vault と重複していたチャンネル → 廃止

| 廃止チャンネル | vault での代替 |
|---|---|
| #ネタ帳 | `Clippings/`（Web Clipperで直接保存） |
| #下書き | `SNS運用/note/` ／ `SNS運用/post/` ／ `SNS運用/post/thread/` |
| #x投稿アーカイブ | `SNS運用/post/day*.md` |
| #競合分析 | `SNS運用/analytics/`（Dataviewで集計可） |
| #画像ストック | vault内 `attachments/` などの画像フォルダ |
| #ツール・プロンプト | `.claude/commands/` ＋ [[Claudian-スキル一覧.md]] |
| #一般 | [[CLAUDE.md]] ＋ [[Claudian-スキル一覧.md]] |

### 残すチャンネル（Discord独自の強みだけ活かす）

| 残すチャンネル | 役割 |
|---|---|
| #情報収集ログ | 参加した外部Discord（Cursor / Anthropic 等）で拾った一次情報のURL＋一行メモ |
| #モバイルメモ | 出先・スマホで思いついたネタ・スクショの仮置き場 |

### vault への流し込み導線

1. 週1回、#情報収集ログ を見返して `/deep-dive` で残すべきものを `調査/` 化
2. #モバイルメモ は翌日PCで `Clippings/` または `SNS運用/post/` に転記して空にする
3. 転記済みのDiscordメッセージは削除してOK（vaultが正本）

---

## 🌐 参加すべき外部Discord（一次情報の宝庫）

招待リンクからの参加は外部サイトの利用規約・コミュニティルール承認が伴うため、自分で参加する。
以下、AI・副業ネタを仕入れるのに有力な公式・主要コミュニティの入口リスト。

**AI開発ツール系（一次情報の宝庫）**

- Cursor 公式: https://discord.gg/cursor （アップデート/Tipsが最速）
- Anthropic（Claude） 公式: https://www.anthropic.com/discord
- OpenAI 開発者: https://discord.gg/openai
- Vercel（v0含む）: https://vercel.com/discord
- LangChain: https://discord.gg/langchain
- Hugging Face: https://hf.co/join/discord
- Replicate: https://discord.gg/replicate

**画像/デザイン系（バナー素材ネタの源）**

- Midjourney 公式: https://discord.gg/midjourney
- Stability AI: https://discord.gg/stablediffusion

**国内AI系コミュニティ**

「ChatGPT × ◯◯」「AIラボ」「プロンプトエンジニア部」など、X検索で「Discord 招待 AI 副業」「Discord AI コミュニティ 日本」と調べると、note執筆者が運営する公開コミュニティが多数見つかる。有料サロンより無料Discordの方が更新が速いことも多い。

参加後は `通知設定 → @mention のみ` にして、サーバーアイコン右クリックで「全部既読」運用がおすすめ。

---

## 💡 ROM徹底＋ネタ抽出の運用フロー（Discord → vault）

1. 各外部Discordで気になる発言を見つけたら、メッセージ右上「…」→「リンクをコピー」
2. 自分用サーバーの **#情報収集ログ** にURL貼付＋一行メモ（例：「Cursor 0.x.x の◯◯機能、note記事化候補」）
3. 週1で見返して、深掘りするものは Claudian に `/deep-dive` を投げて `調査/` に格上げ
4. 企画化できそうなら `SNS運用/post/` または `SNS運用/note/` で下書き
5. 投稿後は `SNS運用/post/day*.md` がアーカイブを兼ねるので、Discord側は転記後に削除して身軽に保つ

Discord検索は `from:@自分` `in:#情報収集ログ` `has:link` などフィルタが強力なので、**vaultに転記する前の一時保管**としては優秀。ただし長期ストックには向かない（検索やリンク連携でvaultに勝てない）ので、必ず流し込むこと。

---

## 📌 残骸（参考用：旧サーバー構成）

> 以下は方針変更前の構成メモ。自分用サーバーを縮小する際の削除対象リスト。
>
> | 旧チャンネル | 用途 |
> |---|---|
> | #一般 | サーバー全体のガイド・使い方メモ |
> | #ネタ帳 | X/Discordで拾ったnote・Xネタをそのままストック |
> | #下書き | note記事/X投稿の下書き置き場 |
> | #競合分析 | 似ジャンルアカウントのURLやヒット記事を保存 |
> | #x投稿アーカイブ | 送信済みX投稿＋反応メモ（個人年表） |
> | #画像ストック | Adobe Firefly／バナー候補／スクショ |
> | #ツール・プロンプト | 使えるプロンプト・AIツールのリンク／設定レシピ |
> | #情報収集ログ | 各Discordで拾った一次情報のメモ（→ 残す） |
