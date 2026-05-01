---
created: 2026-05-01
tags: [調査, AIエージェント, Manus, クラウドコンピュータ, OpenClaw, 自動化]
source: "https://x.com/masahirochaen/status/2049882253527077126"
---

# Manus「Cloud Computer」一般開放──"AIに渡す24時間稼働の専用PC"の実態

> **TL;DR**
> Manus（旧シンガポール拠点 → 2025年12月にMeta傘下、ただし**4/27に中国NDRCが買収阻止**を命じた状態）の **Sandbox = Cloud Computer**（2026-01-14発表）が、My Computerデスクトップ展開（3/16）と並走する形でゴールデン・ウィーク期に一般枠を広げている。  
> 24/7稼働・persistent storage・コード実行・スクレイピング・DB操作はAPI上で公式機能として既に存在する。ただし「Slack Bot や定期レポート」は**プロンプト次第のユースケース**であって専用UIではない、料金プランは Free=7日／Pro=21日のファイル保持で **常時稼働≠永続無料**、**OpenClaw との関係は補完というより競合構図**──このあたりは今日の煽りポストには載っていない実態。  
> 「365日動く自動化が身近に」は2026Q1〜Q2の汎用エージェント全体のトレンドそのもの（ChatGPT Agent / Perplexity Personal Computer / Claude Cowork / OpenClaw も同じ路線）。「Manusだから特別」というより「クラウド常駐エージェント市場全体が一斉に成熟した」と読むのが正確。

## 📌 元テキスト（抜粋）

> 【⚡️速報】Manusが24時間稼働の「Cloud Computer」を一般開放
>
> 簡単に言うと、AIに"24時間起きている専用PC"を渡せる機能。
> Manusで簡単にMac mini × OpenClaw的な機能を実装できる。
>
> ・PCを閉じてもBotが止まらない
> ・ファイルや設定が消えずに残る
> ・Slack Botや定期レポートを自動実行
> ・MySQLやスクレイピングにも対応
> ・AWS契約やOS設定なしで使える
>
> 今まで開発者しかできなかった「365日動く自動化」が、かなり身近になる。

出典: [[Clippings/Post by @masahirochaen on X.md]]（[元ポスト](https://x.com/masahirochaen/status/2049882253527077126)）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Manus** | 2025年Q1にシンガポール発の汎用AIエージェント。クラウド型で「依頼してPC閉じてOK」を最初に広めた。2025-12にMeta買収合意、2026-04-27に中国NDRCが買収阻止 | Manus AI Agent / Meta Acquisition / NDRC block |
| **Cloud Computer (Sandbox)** | Manusが各タスクごとに割り当てる隔離仮想マシン。永続ストレージ・ブラウザ・コード実行・ネットワーク全部入り | Manus Sandbox / E2B virtual computer |
| **My Computer** | 2026-03-16発表のManus Desktop版。ローカルPC（Mac/Win11）にエージェントを下ろす版 | Manus Desktop / Local AI Agent |
| **OpenClaw** | 2026年に登場したMITライセンスのオープンソース汎用AIエージェント。ローカル動作が前提 | OpenClaw open source / OpenClaw vs Manus |
| **E2B** | Manus が Sandbox 実装に使っているクラウド仮想マシン基盤の裏方 | E2B Manus / E2B virtual computer |
| **persistent file system** | エージェントが書いたファイルが次のセッションでも残る仕組み（=「設定が消えない」の根拠） | Manus persistent storage |
| **Zero Trust** | Manus Sandboxのセキュリティ設計思想。ユーザーとManusが完全制御、他タスクへの干渉ゼロ | Manus Zero Trust security |

---

## 🧭 背景 / なぜ今これが話題なのか

### Q1 2025: Manus 登場 → "PC閉じてOK"の衝撃

Manus は 2025年Q1 にシンガポールのスタートアップから登場した汎用AIエージェント。当初は招待制クローズドβで、「依頼を投げたあとPCを閉じても、クラウド側で勝手にタスクを完走させる」UXがX/Twitterで爆発的に広まった。これが「クラウド常駐エージェント」というジャンルを認知させた起点。

### 2025-05: 一般開放第1波

2025年5月に招待制を解除、メール／Google／Apple／Microsoftアカウントでサインアップ可能に。ここで「個人ユーザーが自分のクラウドPCを持てる」フェーズに入った。

### 2025-12: Meta が約20億ドルで買収合意

Big Techの「エージェントAI囲い込み」競争の象徴的ディール。OpenAI（ChatGPT Agent）・Google（Gemini系）・Microsoft（Copilot）に対抗するMetaの一手。

### 2026-01-14: Sandbox（Cloud Computer）正式発表

買収後初の大きなプロダクト発表。「タスク単位で隔離仮想マシンを払い出す」アーキテクチャを公式化。Free 7日／Pro 21日のファイル保持枠も同時にアナウンス。

### 2026-03-16: My Computer（Desktop版）公開

クラウドオンリー → ローカル統合へ。OpenClaw（MITライセンスのOSS）との直接競合構図が表面化。

### 2026-04-27: 中国 NDRC が Meta 買収を阻止

中国国家発展改革委員会が Meta–Manus 買収の取引撤回を要求。Manus のロードマップ（Sandboxの他社クラウド展開、My Computerの中国市場対応など）に**直撃中**。

### 2026-04-30〜05-01: 一般開放の波

X上で「Cloud Computer 一般開放」と日本語で速報が出回っているのは、買収阻止の混乱を受けて Manus 側が**北米・東南アジアで Sandbox 機能の解放を加速**している流れに見える（2026-05-12の「open registration」アナウンスが控えている）。今日のポストはその第1波。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 24時間稼働の「Cloud Computer」を一般開放 | Sandbox は 2026-01-14 発表、24/7稼働は仕様。一般開放は 2025-05 に第1波、2026-05-12 に open registration の追加発表予定 | [Adwaitx Sandbox記事](https://www.adwaitx.com/meta-manus-sandbox-cloud-ai-execution/) / [Manus公式blog](https://manus.im/blog/manus-sandbox) | ⚠️ ほぼ一致（"今日が一般開放スタート"ではなく、"段階開放の最新フェーズ"） |
| AIに"24時間起きている専用PC"を渡せる | 各タスクに**isolated VM**を払い出し、sleep/wake/recycle で運用される。完全に常時稼働ではなくスリープあり | [Manus公式blog](https://manus.im/blog/manus-sandbox) | ⚠️ ほぼ一致（"常時on"ではなく"on-demand wake"） |
| PCを閉じてもBotが止まらない | クラウド側で動くため正しい。「PCを切ってもタスク継続、完了通知が届く」のがManusの売り | [WorkOS紹介](https://workos.com/blog/introducing-manus-the-general-ai-agent) | ✅ 一致 |
| ファイルや設定が消えずに残る | persistent file system 仕様あり。ただし**Free 7日／Pro 21日**の inactivity recycle で消える | [Adwaitx](https://www.adwaitx.com/meta-manus-sandbox-cloud-ai-execution/) | ⚠️ ほぼ一致（条件付き永続） |
| Slack Botや定期レポートを自動実行 | 汎用エージェントなのでプロンプトでSlack APIや定期実行は組める。ただし**専用UI/テンプレートが公式提供**ではない | [Manus公式blog](https://manus.im/blog/manus-sandbox) | 🔍 部分一致（できるがプロンプト次第） |
| MySQLやスクレイピングにも対応 | Sandboxにブラウザ・コード実行環境・ネットワーク全部入り、DB接続/スクレイピングは技術的に可能 | [Manus公式blog](https://manus.im/blog/manus-sandbox) | ✅ 一致 |
| AWS契約やOS設定なしで使える | Sandbox自体がManus提供のVM、ユーザーはクラウド契約不要 | [Adwaitx](https://www.adwaitx.com/meta-manus-sandbox-cloud-ai-execution/) | ✅ 一致 |
| Mac mini × OpenClaw的な機能を実装できる | OpenClawはローカル常駐、Manus Sandboxはクラウド常駐。**機能領域は近いが媒体が逆**（"Mac mini ≒ ローカル24/7マシン" と "Cloud Computer = クラウド24/7マシン"） | [Trendingtopics: Meta Manus OpenClaw](https://www.trendingtopics.eu/meta-manus-openclaw-my-computer/) | ⚠️ 比喩的な一致（厳密にはローカルvsクラウドの媒体違い） |
| 「今まで開発者しかできなかった」365日動く自動化 | n8n / Zapier / Make / Lambda + cron 等で非開発者向けの常時自動化は数年前から存在。「ノーコードで多目的に動く」点は新しい | 一般的常識 + [Taskade Manus Review](https://www.taskade.com/blog/manus-ai-review) | ⚠️ 誇張気味（「初めて」ではなく「より汎用化」が正確） |

---

## 🌐 最新動向（2026-05-01時点）

- **2026-04-27 中国NDRCが Meta–Manus 買収阻止を命令**：取引撤回要求、Manusのプロダクトロードマップに不確実性 — [Cybernews Manus Review](https://cybernews.com/ai-tools/manus-ai-review/), 2026-04
- **2026-05-12 open registration拡大予告**：北米・東南アジア向けのフルパブリック化アナウンスが控えている — [Manus Wikipedia](https://en.wikipedia.org/wiki/Manus_(AI_agent)), 2026-05
- **2026-03-16 My Computer（Desktop版）公開**：Mac/Win11対応、ローカル展開でOpenClawと正面衝突 — [Tech Startups](https://techstartups.com/2026/03/18/metas-ai-startup-manus-launches-desktop-app-that-lets-agents-control-your-computer/), 2026-03
- **OpenClaw vs Manus 比較記事が急増**：MITライセンス vs サブスク型の対立軸が市場で確立 — [Skywork比較](https://skywork.ai/skypage/en/manus-ai-openclaw-comparison/2048613475022925825), 2026-04
- **競合常駐エージェントが横並びで成熟**：Perplexity Personal Computer・Claude Cowork・ChatGPT Agent・Genspark が同四半期に類似機能をリリース — [Manus公式 best-agents](https://manus.im/blog/best-ai-agents-for-desktop), 2026-04
- **E2B（Sandbox基盤）の認知度が上昇**：「Manusの中身はE2B」が技術者層に広まり、自前で同等環境を構築する動きも出てきている — [E2B Blog](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers), 2026-04

---

## 🧩 関連概念・隣接分野

- **OpenClaw**: 2026年登場のMITライセンスOSS汎用AIエージェント。Manus My Computer の直接の競合。**ローカル動作が前提でクラウド料金がゼロ**な点が、Manusの有料Sandboxに対する強烈な対抗軸
- **E2B Cloud**: Manus Sandboxのバックエンドとされる "Sandbox as a Service"。AIエージェント開発者にとっての「Manusじゃなくても同じ仮想PC」を作れる技術スタック
- **ChatGPT Agent / Perplexity Personal Computer / Claude Cowork**: Manusと同種のクラウド常駐 or ハイブリッド型エージェント。**サブスク$20帯**で並ぶため、選定軸は「ファイルアクセス vs DB操作 vs 文書処理」の得意領域
- **Mac mini 自宅サーバー型 + Claude Code / OpenClaw 常駐**: 投稿主が比喩で出している「Mac mini × OpenClaw」。**ローカル電気代 + 自分管理**で月額ゼロにできる代替案。Manusに対する"自前主義"のカウンター
- **MCP（Model Context Protocol）**: Anthropic提唱の標準。MyComputer / OpenClaw 系のローカルエージェントが**ローカルファイル・APIへ安全に接続するための共通プロトコル**として2026年に普及中

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（投稿主寄り）**: 「365日動く自動化が一般人の手に降りてきた、コード書けない人でも Slack Bot / 定期レポート / DB操作が組める」
- **否定 / 慎重派の主張**:
  - **本当に新しいのか問題**: n8n, Zapier, Make, AWS Lambda + cron で非開発者向けの常時自動化は2020年代前半から存在する。「初めて身近に」は煽り
  - **コスト構造の罠**: Free 7日／Pro 21日のファイル保持で「常時稼働＆永続保存」は**有料前提**。月$20帯の他SaaSと並ぶため、選定では「Manusでなければならない理由」を要求される
  - **ロックイン懸念**: Manusタスクで作ったファイル・設定はSandbox上にしか残らない。Pro解約で21日後に消える＝ベンダーロックイン
  - **規制リスク**: 2026-04-27 NDRCのMeta買収阻止で、中国市場・中国データを扱う運用は不確実。日本企業でも「中国規制の影響を受けるエージェントを業務で使うべきか」は議論余地あり
  - **OpenClaw との比較で割高**: ローカルで完結するOpenClawはMITライセンスで実質無料。**「クラウドが必要な理由」**（複数端末からの参照／PCオフ時の継続実行）が無いユースケースなら、OpenClawの方が経済的
- **中立的に見るときの補助線**:
  - 「**自分が動かしたいタスクは"PCをオフにしている時間帯"も実行が必要か？**」── Yesなら Manus / ChatGPT Agent、Noなら OpenClaw / Claude Code でローカル常駐
  - 「**そのタスクは21日以内に終わる単発か？**」── Yesなら Free Sandbox、定常自動化なら Pro必須＋ロックイン覚悟
  - 「**Slack Bot等を作るなら**」── 専用UIがある Make / n8n の方が安定運用しやすい。Manusは"汎用力で曖昧なタスクをこなす"のが本領

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Manus Sandbox の Free と Pro 以外の上位プラン（Team / Enterprise）の料金とファイル保持期間
- [ ] NDRC 買収阻止後の Manus の独立運営シナリオ（Meta 機能統合の解除はどこまで進むのか）
- [ ] OpenClaw を Mac mini に常駐させて、Manus Cloud Computer と同等の作業をした場合の**実コスト比較**（電気代・ハード償却含む）
- [ ] Slack Bot や定期レポートを Manus で組んだ場合の**運用安定性**（cron相当の信頼性／エラー時のリトライ／ログ収集）
- [ ] 日本のSaaSベンダー（Notion AI / kintone / freee）が同様の「クラウド常駐エージェント」を出してくる可能性（2026下期予想）
- [ ] MCP（Model Context Protocol）を経由してローカル＋クラウドのエージェントを連携させる構成（Manus Sandbox + Claude Code の合わせ技）

---

## 📚 参考資料

- [Meta's Manus Unveils Cloud Sandbox for AI Agent Execution - AdwaitX](https://www.adwaitx.com/meta-manus-sandbox-cloud-ai-execution/) — Sandbox発表日(2026-01-14)・Free/Pro料金プラン裏取り, 取得日 2026-05-01
- [Understanding Manus sandbox - your cloud computer (Manus公式)](https://manus.im/blog/manus-sandbox) — 機能仕様・Zero Trust設計・ファイル保持期間の一次情報, 取得日 2026-05-01
- [Meta's AI startup Manus launches desktop app - Tech Startups](https://techstartups.com/2026/03/18/metas-ai-startup-manus-launches-desktop-app-that-lets-agents-control-your-computer/) — My Computer Desktop版(2026-03-16)裏取り, 取得日 2026-05-01
- [Zuckerberg's $2 Billion Bet: How Manus Is Chasing OpenClaw's Shadow - TrendingTopics](https://www.trendingtopics.eu/meta-manus-openclaw-my-computer/) — Meta買収背景・OpenClaw競合構図, 取得日 2026-05-01
- [Manus AI Review 2026: Features, Pricing, 7 Alternatives - Taskade](https://www.taskade.com/blog/manus-ai-review) — 機能評価・代替プロダクト比較, 取得日 2026-05-01
- [Manus AI Review in 2026 - Cybernews](https://cybernews.com/ai-tools/manus-ai-review/) — NDRC買収阻止情報の裏取り, 取得日 2026-05-01
- [Introducing Manus: The general AI agent - WorkOS](https://workos.com/blog/introducing-manus-the-general-ai-agent) — Manusのコンセプト・"PC閉じてOK"のUX紹介, 取得日 2026-05-01
- [Manus AI vs OpenClaw - Skywork比較](https://skywork.ai/skypage/en/manus-ai-openclaw-comparison/2048613475022925825) — Manus vs OpenClaw 機能比較, 取得日 2026-05-01
- [How Manus Uses E2B to Provide Agents With Virtual Computers - E2B Blog](https://e2b.dev/blog/how-manus-uses-e2b-to-provide-agents-with-virtual-computers) — Sandboxのバックエンド技術解説, 取得日 2026-05-01
- [Manus (AI agent) - Wikipedia](https://en.wikipedia.org/wiki/Manus_(AI_agent)) — 2026-05-12 open registration予告など年表整理, 取得日 2026-05-01

---

## 🗒 メモ

- **note・X記事化のフック候補**:
  - 「Manus Cloud Computer 一般開放」を**「OpenClaw vs Manus / Mac mini自前 vs クラウド常駐」の選定フレーム**に落とす記事は、AI実務者層に刺さる。**「自分のタスクはPCを閉じる時間帯に動かす必要があるか？」**が選定の唯一の軸
  - **NDRCの買収阻止**を絡めて「Manusに業務依存していいのか？データ主権リスク」の角度で書くと、4/30 note記事 #2「マルチベンダー人質回避」とつながる
- **本日note(5/1)との接続**: 5/1 note は「AIマネーが物理レイヤーに動いた5本」だったが、**Manus Cloud Computer 一般開放は"AIマネーがソフトレイヤーで再びユーザー向けに降りてきた"角度**で並走する話題。来週の連投シリーズ候補
- **W18戦略メモのE項目「note記事を批評型に寄せる」適用案**: 「365日動く自動化が身近に」を素直に賛美せず、**"既存ツールでもできた話"＋"ロックイン＋ファイル保持期限＋規制リスク"の3点を冷静に並べる**批評型noteで書くと、4/26リプ型と同じパターンに乗せられる
- **Day Oneプロモへの接続**: 「自分のジャーナルを Manus Sandbox に置くのは安全か？」は神プロンプト記事で扱える小ネタ。Day One的な"自分の記録は自分で持つ"思想とManusのクラウド常駐は**思想が逆**なので、対比コンテンツとして面白い

🔗 自動リンクを設置しました（[[Clippings/Post by @masahirochaen on X.md]] を 出典 リンクで参照）。
