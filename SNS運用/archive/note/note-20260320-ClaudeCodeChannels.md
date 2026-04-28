# 【速報】Claude Codeにスマホからメッセージでコード書かせる「Channels」が爆誕！設定方法を全解説

> **🔗 関連コンテンツ（過去アーカイブ）**
> - 📂 現行note一覧: [[SNS運用/note/note-20260424|最新のnote]]
> - 📝 note運用戦略: [[SNS運用/noteの今後と収益化戦略]]
> - 🎨 サムネ仕様: [[note記事用サムネイルのデザインシステム仕様書]]

みなさん、ちょっと聞いてください！Anthropicが本日（2026/03/20）、**めちゃくちゃアツい新機能**をリリースしました！

その名も**「Claude Code Channels」**！

何がすごいかって、TelegramやDiscordからClaude Code（AIコーディングエージェント）にメッセージを送るだけで、**スマホからコードの開発指示が出せちゃう**んです💦
「パソコンの前にいなくても、移動中にAIにコード書かせておく」っていう、まさに**非同期のAI開発パートナー**が現実になりました！

今日はこの「Claude Code Channels」について、何ができるのか、どうやって設定するのか、公式ドキュメントに基づいて徹底的にまとめてみました！

---

## そもそもClaude Code Channelsって何？

Claude Code Channelsは、Anthropicが2026年3月20日に**リサーチプレビュー（テスト版）**として公開した超注目の新機能です！

ひと言で言うと、**「TelegramやDiscordから、Claude Codeのセッションに外部イベントやメッセージをプッシュできる仕組み」**ですね。

これまでのClaude Codeって、ターミナル（黒い画面）を開いて、パソコンの前に座って使うのが前提でした。つまり「聞いて→待って→結果を見る」っていう**同期型**の使い方だったんですよね。

でもChannelsが登場したことで、スマホのTelegramやDiscordからAIに**「あの機能、先に実装しといて！」**ってメッセージを飛ばすだけで、AIが裏で勝手にコードを書いてくれるようになりました！いわば**「指示を出して→放置→あとで確認」**っていう非同期型のスタイルに進化したわけです！

### なんでこの機能が生まれたの？

実はこれ、2025年11月にリリースされて爆発的に流行ったオープンソースのAIエージェントフレームワーク**「OpenClaw」**の影響がめちゃくちゃ大きいんです。OpenClawはもともとWhatsAppとかDiscordとか、色んなメッセージアプリからAIに仕事をお願いできるマルチチャネル対応が売りだったんですよね。

VentureBeatは今回のChannelsを「OpenClaw killer」って表現してて、Anthropicがそのアプローチを見て公式で同等の機能を組み込んできた形です。ただ、Anthropicらしいのは**AIセキュリティと安全性を最初からガチガチに設計してる**ところ。ここがOpenClawとの差別化ポイントですね！

### 技術的にはどうなってるの？

Channelsの裏側では、Anthropicが2024年に作った**「Model Context Protocol（MCP）」**っていうオープン規格が使われてます。MCPは「AIモデル用のUSB-Cポート」みたいなもんで、AIと外部ツールを安全に繋ぐための共通仕様です。

具体的な仕組みとしては、`--channels`フラグ付きでClaude Codeを起動すると、MCPサーバーがポーリングサービスとして立ち上がって、TelegramやDiscordのメッセージをClaude Codeセッションにプッシュしてくれます。チャンネルは**双方向**で、Claudeがメッセージを読んで、同じチャンネルを通じて返信もしてくれるんです！

ちなみに、Claudeが返信した内容はターミナルには「送信済み」って表示されるだけで、実際の返信テキストはTelegramやDiscord側に表示されます。イベントはセッションが開いてる間だけ届くんで、常時稼働させたい場合はバックグラウンドプロセスか永続ターミナルで動かす必要がありますね！

---

## 使うために必要なもの

セットアップの前に、まず環境を整えましょう！

- **Claude Code**: バージョン **2.1.80以上**（必須！古いと動きません）
- **claude.aiアカウント**: ログインできる状態にしておいてください。**Console（API）やAPIキー認証は非対応**なんで注意です！
- **Bunランタイム**: JavaScriptの高速ランタイム。プリビルドのチャンネルプラグインはBunスクリプトなんで必須です。`bun --version`で確認して、入ってなければ[bun.sh](https://bun.sh)からインストールしてください！
- **組織ユーザーの場合**: Team/Enterpriseプランでは管理者がChannelsを**明示的に有効化**する必要があります。[claude.ai → Admin settings → Claude Code → Channels](https://claude.ai/admin-settings/claude-code)から設定できるんで、IT部門に確認してみてくださいね！

---

## まずは手軽に試したい人向け：fakechatデモ

いきなりTelegramやDiscordのBot設定するの面倒…って人のために、Anthropicが公式で**「fakechat」**っていうデモチャンネルを用意してくれてます！localhostでチャットUIが立ち上がって、ブラウザからChannelsの動きを体験できるんですよね。認証も外部サービスの設定も一切不要なんでめっちゃお手軽です！

```bash
# プラグインをインストール
/plugin install fakechat@claude-plugins-official

# Claude Codeを再起動（--channelsフラグ付き）
claude --channels plugin:fakechat@claude-plugins-official
```

起動したら http://localhost:8787 にアクセスして、メッセージを打ってみてください。Claude Codeのセッションにイベントが届いて、Claudeが処理して返信してくれます！動作確認ができたら、本番のTelegramやDiscordに進みましょう！

---

## セットアップ手順：Telegram編（5ステップ）

スマホで一番手軽に始められるのがTelegramです！順番にやっていきましょう。

### ステップ1：Telegram Botを作る

Telegramを開いて、**「BotFather」**っていう公式Botに話しかけます！

1. BotFatherに `/newbot` と送信
2. Botの表示名を入力（例：「MyClaude」）
3. ユニークなユーザー名を入力（末尾に `bot` が必要。例：`my_claude_dev_bot`）
4. BotFatherが**Botトークン**をくれるので、これをコピーして大切に保管！

このトークンが鍵になるんで、絶対に人に教えちゃダメですよ💦

### ステップ2：Claude Codeにプラグインをインストール

Claude Codeのターミナルで以下のコマンドを実行します！

```bash
/plugin install telegram@claude-plugins-official
```

公式プラグインなんで安心ですね！ちなみに`claude-plugins-official`マーケットプレイスは自動で追加されますが、もしなければ先に `/plugin marketplace add anthropics/claude-plugins-official` を実行してください。

### ステップ3：Botトークンを設定

さっきコピーしたトークンを使って設定します。

```bash
/telegram:configure <あなたのBotトークン>
```

トークンはプロジェクトの`.claude/channels/telegram/.env`に保存されます。シェル環境変数`TELEGRAM_BOT_TOKEN`として事前に設定しておく方法もありますよ！

### ステップ4：Channelsモードで再起動

一度Claude Codeを終了して、Channelsを有効にして再起動します！

```bash
claude --channels plugin:telegram@claude-plugins-official
```

### ステップ5：アカウントをペアリング＆アクセス制限

ここがセキュリティ上めっちゃ大事なステップです！

1. TelegramでさっきのBotにメッセージを送る
2. Botが**ペアリングコード**を返してくる
3. Claude Code側で以下のコマンドを実行してペアリング承認：

```bash
/telegram:access pair <ペアリングコード>
```

4. **必ず**アクセスポリシーを許可リスト方式に設定：

```bash
/telegram:access policy allowlist
```

これであなたのTelegramアカウントだけが許可リストに登録されて、他の人からのメッセージは全部無視されるようになります。知らない人のメッセージでAIが動いちゃったら大変なんで、この設定は絶対にやっておきましょう！

---

## セットアップ手順：Discord編（7ステップ）

チームでの開発にはDiscordが便利ですね！こちらもやっていきましょう。

### ステップ1：Discord Botを作る

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリックしてBotを作成
3. **「Bot」セクション**でユーザー名を作って、「Reset Token」でトークンをコピー！

### ステップ2：Message Content Intentを有効化

Botの設定画面で**「Privileged Gateway Intents」**までスクロールして、**Message Content Intent**を有効にします！これを忘れるとメッセージが届かないんで注意です。

### ステップ3：BotをDiscordサーバーに招待

**OAuth2 > URL Generator**で`bot`スコープを選んで、以下の権限を付与します：

- View Channels
- Send Messages
- Send Messages in Threads
- Read Message History
- Attach Files
- Add Reactions

生成されたURLを開いてBotをサーバーに追加してください！ちなみに「Administrator」権限を付けちゃうのは楽だけど、最小権限の原則でこの6つだけにしておくのがおすすめです。

### ステップ4：Claude Codeにプラグインをインストール

```bash
/plugin install discord@claude-plugins-official
```

### ステップ5：Botトークンを設定

```bash
/discord:configure <あなたのBotトークン>
```

トークンは`.claude/channels/discord/.env`に保存されます。

### ステップ6：Channelsモードで再起動

```bash
claude --channels plugin:discord@claude-plugins-official
```

ちなみに**複数チャンネルを同時に有効化**することもできて、スペース区切りで渡せます：

```bash
claude --channels plugin:telegram@claude-plugins-official plugin:discord@claude-plugins-official
```

### ステップ7：アカウントをペアリング＆アクセス制限

1. Discord上でBotにDMを送信
2. Botが返してきたペアリングコードを確認
3. Claude Codeで承認＆ポリシー設定：

```bash
/discord:access pair <ペアリングコード>
/discord:access policy allowlist
```

これで接続完了です！

---

## 実際にどう使うの？ユースケース3選！

セットアップが終わったら、あとはスマホからメッセージするだけ！具体的にどんな使い方ができるか紹介しますね。

### ユースケース1：移動中の「Vibe Coding」

電車の中とか、カフェでちょっと思いついたときに、TelegramからClaude Codeに**「あのAPIのエンドポイント、バリデーション追加しておいて」**ってメッセージするだけ！家に帰ったらコードが出来上がってるなんて、最高すぎませんか💦

### ユースケース2：外部イベントへのリアルタイム反応

CI/CDパイプラインの結果とか、エラー通知をChannels経由でClaude Codeに流しておけば、AIが自動でバグ修正に取り掛かってくれるなんて使い方も！「テスト落ちたよ！」っていうアラートをそのままAIに流すイメージですね。公式ドキュメントでも「CI results, chat messages, and monitoring events」をプッシュする使い方が想定されてます。

### ユースケース3：チーム開発でのタスク依頼

Discordのチャンネルを使って、チームメンバーがClaude Codeのエージェントに直接タスクを投げられます。「このPRのレビューお願い！」みたいな感じで、AIをチームの一員として使えるようになるのが面白いですよね！許可リストでメンバー管理もできるんで、セキュリティ面も安心です。

---

## セキュリティの仕組みを深掘り

Channelsのセキュリティ、個人的にかなりしっかり設計されてるなって思ったんで、もうちょっと詳しく書いておきますね。

**1. 送信者の許可リスト（Allowlist）**
承認済みのチャンネルプラグインはすべて送信者の許可リストを持ってて、リストに登録されたIDからのメッセージだけを受け付けます。それ以外のメッセージは**無言で破棄**されるんで、悪意のある第三者がBotにメッセージ送っても何も起きません。

**2. セッションごとの有効化**
`--channels`フラグで起動時に明示的に指定したプラグインだけがチャンネルとして動作します。`.mcp.json`に書いてあるだけじゃチャンネルメッセージは届かないんで、意図しない有効化が防がれてます。

**3. 組織レベルの制御**
Team/Enterpriseプランでは管理者が`channelsEnabled`設定で組織全体の利用を制御できます。デフォルトでは無効になってるんで、勝手に使われちゃう心配はないですね。

**4. 権限プロンプト**
ターミナルを離れてる間にClaudeが権限の確認が必要な操作に当たった場合、ローカルで承認するまでセッションが一時停止します。完全に無人で動かしたい場合は`--dangerously-skip-permissions`フラグが使えますが、信頼できる環境でだけ使ってくださいね💦 名前に「dangerously」って入ってるくらいなんで。

---

## 自分だけのチャンネルも作れる！

TelegramとDiscordは最初の2つで、今後対応プラットフォームは増えていく予定です。でも待てない！って人は、**自分でカスタムチャンネルを作る**こともできます！公式ドキュメントの[Channels reference](https://code.claude.com/docs/en/channels-reference)にビルド方法が載ってるんで、社内のSlackやTeamsに繋ぎたい人はチェックしてみてください。

開発中のカスタムチャンネルは`--dangerously-load-development-channels`フラグで読み込めます。

---

## 注意点まとめ

いくつか気をつけておきたいポイントもあります！

- **リサーチプレビュー段階**: まだ正式リリースじゃないんで、`--channels`フラグの仕様やプロトコルはフィードバックに基づいて変わる可能性があります。使えるプラグインもAnthropicが管理する許可リストに含まれるものだけです。
- **Claude Codeは起動したまま**: イベントはセッションが開いてる間だけ届きます。PCを閉じちゃうとメッセージが届かなくなるんで、常時稼働させたい場合はバックグラウンドプロセスか永続ターミナルで動かしましょう！
- **認証方式の制限**: claude.aiログインのみ対応で、ConsoleやAPIキー認証は使えません。
- **組織での利用制限**: Team/Enterpriseアカウントの場合、管理者がChannelsを明示的に許可しないと使えません。Pro/Maxプラン（組織なし）ならデフォルトで利用可能です。
- **セキュリティ**: ペアリング後は必ず`/xxxxx:access policy allowlist`で許可リスト方式にしておきましょう。知らない人からのメッセージでAIが動いちゃったら大変なんでね！
- **バグ報告**: 問題があれば[Claude Code GitHubリポジトリ](https://github.com/anthropics/claude-code/issues)でフィードバックできます。

---

## 関連機能もチェック！

Channelsと合わせて使えるClaude Codeの関連機能もあるんで、ちょっと紹介しておきますね。

- **Remote Control**: チャンネル経由でイベントを転送するんじゃなくて、スマホからローカルのClaude Codeセッションを直接操作する機能。Channelsとはアプローチが違うけど、「外出先からClaude Codeを使う」っていう目的は同じです！
- **Scheduled tasks**: プッシュイベントに反応するChannelsに対して、タイマーベースで定期的にポーリングする仕組み。CI/CDの監視とかと組み合わせると便利ですよ。

---

## まとめ：「AIにメッセージで仕事を頼む」時代が来た！

Claude Code Channels、個人的にめちゃくちゃワクワクしてます！

だって考えてみてください。今まで「AIにコードを書いてもらう」って、PCの前に座ってプロンプトを打ち込んで、結果を待って…っていう作業だったじゃないですか。それが**「電車の中からTelegramでメッセージ一本」**で済むようになるんですよ💦

しかもこれ、OpenClawが先に「マルチチャネル＋非同期」のスタイルを見せつけたことで、Anthropicが公式で対抗してきた流れだと思うんですよね。AI業界の競争のおかげで、僕らユーザーはどんどん便利なツールを手に入れられてます！

個人的に一番評価したいのは**セキュリティ設計の丁寧さ**です。許可リスト方式、セッションごとの明示的な有効化、組織レベルの制御、権限プロンプトの一時停止…「便利だけど危ない」じゃなくて「便利で安全」を目指してるのがAnthropicらしいなと。一昨日のnoteで書いたNVIDIAのNemoClawも、昨日のOpenShellも、今週はずっと「AIエージェントのセキュリティ」が大テーマになってますが、Channelsもその流れにしっかり乗ってますね。

今はまだリサーチプレビューの段階ですが、これが正式リリースされたら**開発者の働き方が根本的に変わる**と思ってます。「パソコンの前にいる時間＝開発時間」っていう概念が崩れて、いつでもどこでもAIと一緒にコードを書ける世界。もうSFじゃないですね！

気になった方はぜひ試してみてください！Claude Codeのバージョンを2.1.80以上にアップデートして、まずはfakechatデモで試すところからスタートしてみるのがおすすめです！

---

### この記事のタグ

#AI, #ClaudeCode, #Anthropic, #プログラミング, #AIエージェント, #開発効率化, #Telegram, #Discord, #MCP

---

**参考情報源：**
- [Claude Code公式ドキュメント - Channels](https://code.claude.com/docs/en/channels)
- [VentureBeat - Anthropic just shipped an OpenClaw killer called Claude Code Channels](https://venturebeat.com/orchestration/anthropic-just-shipped-an-openclaw-killer-called-claude-code-channels)
- [claude-plugins-official GitHub](https://github.com/anthropics/claude-plugins-official)
