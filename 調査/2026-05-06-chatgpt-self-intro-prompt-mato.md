---
created: 2026-05-06
tags:
  - 調査
  - ChatGPT
  - 画像生成
  - プロンプト
  - X運用
  - GW
  - Memory
  - 自己紹介
source: https://x.com/matotoushi/status/2051820472984322312
action: 取り込み検討
---

# まと氏の「わたしってこんな人」自己紹介画像プロンプトを解剖する

> [!summary] TL;DR
> - 「文章を考える必要なし」「画像とプロンプトだけ」で **ChatGPT Memory（過去会話履歴）を読み込ませて自己紹介画像を作る** プロンプト。GW 明けのプロフ更新タイミングを狙った投稿
> - 技術的下回りは **ChatGPT Images 2.0 (GPT Image 2)** + **2025-04 から強化された全履歴参照型 Memory**。3:4 アスペクト・3D モチーフ立体配置・テキスト精度 95% 超は GPT Image 2 で初めて素直に出る
> - **2026-01 に流行した「私をどう扱ってきたか画像にして」系プロンプトの進化形**。Memory 依存型バイラルの第二波。my-clone 文体に翻訳すれば実用度の高いコンテンツ素材になる

---

## 📌 元テキスト（抜粋）

> おっ、🆕版いい感じにできた！
> GWあけから頑張るぞ～！！な方、ぜひこのプロンプトで自己紹介画像作ってみてほしい！
> 文章を考える必要なし！
> プロンプトと画像だけでイケるのはChatGPTとのやりとりを読み込ませるので勝手に作ってくれる楽チンタイプのプロンプトでっす！！
>
> プロンプト▼
> "わたしってこんな人"　という画像を作成してください。
> これまでのChatGPTと私とのやりとりから、そのやりとりに関するモチーフや、いいね、リポスト、🆕アイコン、🆕関する3Dのモチーフを作り、添付した画像のまわりかから立体的に飛び出すように配置します。
> 🆕のデザインを活かして、おしゃれなデザインに仕上げてください。
> アスペクト比は3:4。

出典: [まと｜AI×デザイン @MatoToushi](https://x.com/matotoushi/status/2051820472984322312) — 2026-05-06 09:24 JST、261 likes / 14 RT / 14 replies、画像2枚（1066×1199, 3:4 縦）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **ChatGPT Memory（全履歴参照）** | 2025-04-10 から強化された機能。保存メモリだけでなく**全過去会話**から好み・興味を引いてくる | "ChatGPT memory all chats" 2025 |
| **GPT Image 2 / Images 2.0** | OpenAI の最新画像生成。3:1〜1:3 の柔軟なアスペクト比、ネイティブ 2K、テキスト精度 95%超 | "GPT Image 2" "Images 2.0" |
| **自己紹介画像トレンド** | プロフ画像・固定ポスト画像として "私はこういう人" を視覚化する文化 | プロフ画像 ChatGPT 流行 |
| **「私をどう扱ってきたか」プロンプト** | 2026-01 に X/Instagram で爆発的にバズった先行事例。Memory 参照型の元祖 | itmedia 2026-01 ChatGPT 私を |
| **🆕（添付画像）** | プロンプト中の `🆕` は文字通りの絵文字ではなく **添付したアイコン/写真** を指す変数的記号 | (まと氏独自記法) |
| **GW（ゴールデンウィーク）** | 2026年は 4/29〜5/6。投稿当日の 5/6 はちょうど GW 最終日で「明日から本番」の心理 | 2026 GW 日程 |

---

## 🧭 背景 / なぜ今これが話題なのか

**1. 著者は「AI×デザイン」のミドル女性層インフルエンサー**
@MatoToushi は **フリーランスデザイナー20年・二児の母・画像生成研究者** を自称、**約7万フォロワー**規模。煽り系（@heynavtoor 等）とは一線を画して **「試しました→こうでした」型の率直な実験報告** で支持を集めるタイプ。本人もずんだもん他のプロンプトに乗っかったり、パーソナルカラー診断表生成プロンプトを共有したりしている（[過去ツイート 1](https://x.com/MatoToushi/status/2046851180765323544), [2](https://x.com/MatoToushi/status/2046831688320434651)）。

**2. 投稿タイミングが GW 最終日 = プロフ更新需要のピーク**
2026 年の GW は **4/29〜5/6**。投稿は **5/6 09:24 JST**（=GW 最終日朝、明日から仕事復帰のタイミング）。「GW 明けから頑張る人」へ向けた **プロフィール画像・固定ポスト画像 リフレッシュ需要** に正面から打ち込んでいる。バズ設計としてタイミングが正しい。

**3. 直接の元ネタは 2026-01 の「私をどう扱ってきたか画像にして」バズ**
2026-01-19 頃から X/Instagram で **「これまで私があなたをどう扱ってきたかを画像にしてください」** というプロンプトが急拡散（[ITmedia](https://www.itmedia.co.jp/aiplus/articles/2601/22/news140.html), [Togetter](https://togetter.com/li/2654471)）。これは **ChatGPT Memory が貯めた個人ごとの会話履歴を画像で可視化する** 第一波。今回のまと氏の「わたしってこんな人」は **同じ Memory 参照型プロンプト** の派生で、自分側を主人公に据えた**第二波**と読める。

**4. 技術的下回り: GPT Image 2 が"立体的に飛び出す 3D" を素直にこなせるようになった**
ChatGPT Images 2.0（GPT Image 2、[OpenAI 公式](https://openai.com/index/introducing-chatgpt-images-2-0/)）は **3:1〜1:3 のアスペクト比対応・ネイティブ 2K・テキスト精度 95%超**。多言語（日本語含む）対応で **物理・ライティング・素材の理解が深まり**、Isometric 3D / Pop-out 3D の指示が以前よりずっと素直に通る。プロンプト末尾の `アスペクト比は3:4` が安定して効くのは GPT Image 2 環境での前提。

**5. ChatGPT Memory が"全履歴参照"に進化したから成立する**
2025-04-10 のアップデートで ChatGPT は **保存メモリだけでなく全過去会話を横断参照** するようになった（[OpenAI](https://openai.com/index/memory-and-new-controls-for-chatgpt/), [TechCrunch](https://techcrunch.com/2025/04/10/openai-updates-chatgpt-to-reference-your-other-chats/)）。「やりとりに関するモチーフを作って」が **会話履歴の少ない 2024 年以前なら成立しなかった**プロンプト。今のタイミングだから刺さる。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 文章を考える必要なし | プロンプト本文は固定で、ユーザーは画像 1 枚添付するだけで OK。本人の言う通り | プロンプト本文 | ✅ 一致 |
| ChatGPT が過去のやりとりを読み込んで自動でモチーフを作る | 2025-04-10 から ChatGPT Memory は全過去会話を横断参照。Free/Plus/Pro 全てで利用可（2025-07 以降） | [OpenAI Memory Blog](https://openai.com/index/memory-and-new-controls-for-chatgpt/), [Axios 2025-07](https://www.axios.com/2025/07/11/chatgpt-memory-update) | ✅ 一致 |
| 3:4 アスペクトで立体的に飛び出す 3D モチーフが安定して出る | GPT Image 2 は 3:1〜1:3 を含む柔軟なアスペクト対応、3D・物理表現も改善 | [OpenAI Images 2.0](https://openai.com/index/introducing-chatgpt-images-2-0/), [Morphic](https://morphic.com/resources/how-to/chatgpt-images-2.0-prompts) | ✅ 一致 |
| 楽チンタイプ（≒誰でも同じ品質で出る） | Memory 参照型なので **会話履歴の濃さに比例**して結果が変わる。新規アカウントや Memory OFF だと薄いモチーフしか出ない | [OpenAI Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq) | ⚠️ ほぼ一致（ハードル無し、品質差は出る） |
| 「いいね、リポスト、🆕アイコン」の意味 | 文脈から「SNS の UI モチーフ＋添付画像（🆕）のアイコン」を意図。本文では `🆕` が**変数的記号**として使われている | プロンプト本文の文脈読解 | 🔍 未確認（本人の意図はリプ欄等で要確認） |

---

## 🌐 最新動向（2026-05-06 時点）

- **2026-05-06 09:24 JST**: まと氏が「わたしってこんな人」自己紹介画像プロンプトを公開、GW 明けタイミングで拡散中 — [元ツイート](https://x.com/matotoushi/status/2051820472984322312), 2026-05
- **2026-04-23**: Anthropic Claude が Spotify / Instacart 等の Lifestyle 連携を発表。AI×日常 の文脈は ChatGPT 一強から多軸化へ — [Spotify Newsroom](https://newsroom.spotify.com/2026-04-23/claude-integration/), 2026-04
- **2026-Q1**: ChatGPT Memory がさらに改善され、**1年前の会話まで具体的に参照可能 + Sources リンク表示** に進化 — [TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/after-todays-big-memory-upgrade-chatgpt-can-now-remember-conversations-from-a-year-ago-and-link-you-directly-to-them), 2026-Q1
- **2026-01-19〜**: 「私をどう扱ってきたか画像にして」が X/Instagram で爆発的に拡散、ChatGPT Memory 参照型バイラルの第一波 — [ITmedia](https://www.itmedia.co.jp/aiplus/articles/2601/22/news140.html), 2026-01
- **2025-07-11**: ChatGPT Memory が **Free / Plus / Pro 全プランに開放** 。バイラルプロンプトの裾野が広がる前提が整う — [Axios](https://www.axios.com/2025/07/11/chatgpt-memory-update), 2025-07
- **2025-05-21**: Simon Willison が Memory への慎重論を公開。「個人 dossier」化への懸念 — [simonwillison.net](https://simonwillison.net/2025/May/21/chatgpt-new-memory/), 2025-05

---

## 🧩 関連概念・隣接分野

- **GPT Image 2 / ChatGPT Images 2.0**: 3:4 縦・3D・テキスト精度 95% 超を一発で出せる現行モデル。プロンプトが安定して効く前提条件
- **ChatGPT Memory（全履歴参照型）**: 2025-04-10 で大幅強化。保存メモリ＋全過去会話を横断。**個人 dossier 化**として批判もあるが、バイラルプロンプトの土台
- **「私をどう扱ってきたか画像にして」型バイラル**: 2026-01 の先行事例。**自分の AI 利用履歴を視覚化する** 系プロンプトの先駆け
- **isometric / pop-out 3D デザイン**: Threads / Instagram で 2025〜2026 にかけて流行中の視覚スタイル。アイコン周辺に小物を立体配置する構図
- **GW × プロフ画像更新文化**: 日本独自の「連休明けに新しい自分を出す」需要。2026 年 GW は 4/29〜5/6 で、5/6 投稿はピンポイント
- **Personal Color Diagnosis / 診断系プロンプト**: 同著者が以前バズらせた[パーソナルカラー診断表プロンプト](https://x.com/MatoToushi/status/2046831688320434651)。「自分を可視化する」系で同じシリーズの延長線

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - 煽り系（"$XXX/h を代替"）と違って **正直な実験報告型**。「いい感じにできた」「楽チンタイプ」と等身大の言葉で書かれていて、**プロンプト自体が即実用品**
  - GW 明けタイミング × プロフ画像需要 × Memory 機能 × GPT Image 2 という **4 要素が同時に揃った瞬間**を捉えており、コンテンツ設計として完成度が高い
  - 「文章を考える必要なし」という UX 約束は事実上守られていて、ハードルを下げる訴求として強い

- **否定 / 慎重派の主張**:
  - **Memory 依存度が品質を決める**: 会話履歴が少ないアカウント・Memory OFF・新規アカウントでは「楽チン」とは言えない結果しか出ない。「誰でも同じ品質」のニュアンスはミスリードを生み得る
  - **プライバシー懸念**: 過去会話の内容（仕事・健康・関係性等の機密）が画像に滲み出るリスク。**業務利用 ChatGPT では絶対やってはいけない**プロンプト
  - **`🆕` の使い方が曖昧**: プロンプト中の `🆕` がどう機能するかリプ欄補足なしでは初見ユーザーが混乱する。「添付画像を🆕に置き換えて読む」式の暗黙ルールがある
  - **GPT Image 2 / Plus 以上前提**: ChatGPT Free でも画像生成自体は使えるが、3:4 や 3D の安定度は Plus 以上で Images 2.0 にアクセスする方が確実。「無料でできる」と誤読されると不満につながる

- **中立的に見るときの補助線**:
  - プロンプト本体は **「Memory が濃い人ほど結果が映える」 性質**を持つ。逆に言えば、これは ChatGPT 課金者・ヘビーユーザーにとっての**ご褒美コンテンツ**として読める
  - my-clone 文体に翻訳するなら「Memory 機能の濃淡で結果が変わる」「Plus 以上推奨」という**前提条件の透明化**を一言入れるだけで、信頼性が一段上がる

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] プロンプト中の `🆕` 記号の正確な使い方 — まと氏のリプ欄や引用RTで本人の補足を拾う
- [ ] 同プロンプトが **Claude Sonnet 4.6 + 画像生成** や **Gemini 3.x** で同等の出力を出せるか — モデル横断ベンチマーク
- [ ] ChatGPT Memory がまだ薄いユーザー（新規 or Memory OFF）でも刺さる**変奏版**プロンプト — 「以下の質問に答えてからこの画像を作って」型に組み替えると Memory 依存度を下げられる
- [ ] 自己紹介画像トレンドの**次の波**: 「私をどう扱ってきたか」(2026-01) → 「わたしってこんな人」(2026-05) の次に来るのは何か（"この1年の私" / "理想の私" / "AI から見た私" など）
- [ ] **業務利用 ChatGPT で同プロンプトを実行した場合のセキュリティリスク**：会社の Enterprise アカウントだと Memory が無効化されている／会話が学習に使われない設定になっているケースが多く、結果がそもそも出ない可能性

---

## 📚 参考資料

- [まと氏 元ツイート（@MatoToushi 2026-05-06）](https://x.com/matotoushi/status/2051820472984322312) — プロンプト本文と添付画像, 取得日 2026-05-06
- [Introducing ChatGPT Images 2.0 — OpenAI](https://openai.com/index/introducing-chatgpt-images-2-0/) — GPT Image 2 の仕様（3:1〜1:3 アスペクト・2K・95% テキスト精度）, 取得日 2026-05-06
- [ChatGPT Images 2.0 prompt library — Morphic](https://morphic.com/resources/how-to/chatgpt-images-2.0-prompts) — 3D / 立体表現の作例, 取得日 2026-05-06
- [Memory and new controls for ChatGPT — OpenAI](https://openai.com/index/memory-and-new-controls-for-chatgpt/) — 全履歴参照型 Memory の仕様, 取得日 2026-05-06
- [OpenAI updates ChatGPT to reference your past chats — TechCrunch](https://techcrunch.com/2025/04/10/openai-updates-chatgpt-to-reference-your-other-chats/) — 2025-04-10 アップデートの一次解説, 取得日 2026-05-06
- [ChatGPT memory expanded to free users — Axios](https://www.axios.com/2025/07/11/chatgpt-memory-update) — Free 開放のタイミング, 取得日 2026-05-06
- [ChatGPT can now remember conversations from a year ago — TechRadar](https://www.techradar.com/ai-platforms-assistants/chatgpt/after-todays-big-memory-upgrade-chatgpt-can-now-remember-conversations-from-a-year-ago-and-link-you-directly-to-them) — Memory の長期化, 取得日 2026-05-06
- [ChatGPT「私があなたをどう扱ってきたか」遊びが流行 — ITmedia](https://www.itmedia.co.jp/aiplus/articles/2601/22/news140.html) — 2026-01 の先行バイラルの一次報道, 取得日 2026-05-06
- [Togetter — ChatGPT「私をどう扱ってきたか」まとめ](https://togetter.com/li/2654471) — バイラル拡散の経緯, 取得日 2026-05-06
- [I really don't like ChatGPT's new memory dossier — Simon Willison](https://simonwillison.net/2025/May/21/chatgpt-new-memory/) — Memory 強化への慎重論, 取得日 2026-05-06
- [まと氏 過去ツイート（パーソナルカラー診断表プロンプト）](https://x.com/MatoToushi/status/2046831688320434651) — 同シリーズの先行作, 取得日 2026-05-06

---

## 🗒 メモ

- **my-clone 文体への翻訳路線**: 「文章を考える必要なし」の UX 約束はそのまま使える。ただし**「Memory 機能の濃淡で結果が変わる」「ChatGPT Plus 以上推奨」**を一文添えると、my-clone の "鵜呑みにせず実測する" キャラと整合する
- **自分でも試す価値あり**: 自分の ChatGPT Memory には Tsukapon 運用・Daily Log・ Hermes Kanban 等の濃いコンテキストが貯まっているので、「わたしってこんな人」の出力は面白いはず。**vault 内 Asset として `_ kiwami/my-clone/` 配下に作品を保存**してプロフィール画像更新の候補にする
- **シリーズ展開のヒント**: 「私をどう扱ってきたか」(自分→AI) → 「わたしってこんな人」(私の周りに飛び出すモチーフ) と来たので、**第三波の予測**:
  - 「**この1年の私**」(時系列タイムライン視覚化)
  - 「**AIから見た私の理想形**」(逆視点・憧れ・向上心の可視化)
  - 「**私の脳内マップ**」(思考クラスタ可視化)
- **note 記事化の素材として強い**: 「まと氏のプロンプトを試してみた + Memory 機能の制約も検証 + 改良版プロンプト」型で 1 本書けば、批評ポジションを取りつつ実用情報も提供できる。GW 明けの note トラフィック狙いとしてタイミングが一致
- **業務利用注意**: クライアント案件で同プロンプトをそのまま渡すのは ⚠️。Enterprise アカウントだと Memory 無効でそもそも結果が出ない。提案前に**「私的アカウントで」**の前置きが必要
