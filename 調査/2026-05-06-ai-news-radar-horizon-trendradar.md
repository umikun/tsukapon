---
created: 2026-05-06
tags:
  - 調査
  - AIニュース
  - Horizon
  - TrendRadar
  - 情報過多
  - MCP
source: https://x.com/btcqzy1/status/2051500517700808826
action: 取り込み検討, 投稿ネタ
---

# 「打破AI信息差・第二期」Horizon と TrendRadar を裏取りしてみる

> **🔗 関連コンテンツ**
> - 🧠 Obsidian × Claude Code 全体マップ: [[Claudian-obsidian-skills活用マップ.md]]
> - 📝 関連ネタ（AIエージェントvault化）: [[Clippings/Post by @obsidianstudio9 on X.md]]
> - 📰 ニューススレッド作成スキル: [[. claude/commands/news-thread.md]]
> - 🔁 同シリーズ第1回（TrendRadar回・引用元RT）: 出典URL `https://x.com/btcqzy1/status/2050722...`（vault内クリップなし）

> **TL;DR**
> 中国系アカウント @BTCqzy1 が「打破AI信息差」シリーズで紹介する2ツール、**TrendRadarとHorizonは設計思想が逆方向**。TrendRadarは中国国内11プラットフォーム監視（GitHub★56.7k、ツイートの「5万」主張はほぼ正確）、Horizonは海外硬核ソース監視（HN/Reddit/RSS/Telegram/X/GitHub、★2.2k）の**英中バイリンガル日次ブリーフィング**。両方ともMCP/Docker対応で「セルフホスト型AI情報レーダー」というカテゴリ。海外硬派テック情報を狙うなら **Horizonが正しい選択** で、ツイートの紹介意図は妥当。ただし市場には Particle・ClarityBriefs・Feedly AI 等の商用代替も多く、自前運用コストとの天秤は要検討。

## 📌 元テキスト（抜粋）

> 打破 AI 信息差：第二期
>
> 每天刷 Hacker News、Twitter、Reddit、GitHub，是不是经常被水文、重复内容和噪音淹没？
>
> 分享一个我最近在用的新工具：Horizon，你的海外硬核科技新闻雷达。
>
> 让 AI 替你盯着全球科技圈，你只需要每天早上打开一份简报。

引用元（第一期）:
> 99%的人每天刷信息流，以为自己在获取信息，其实只是被算法喂垃圾。
> 而真正会用 AI 的人，早就开始用工具自动监控全网趋势了。
> 分享一个我最近在用的神器：TrendRadar（git斩获5万星标🌟）

出典: [Post by @BTCqzy1 on X (2026-05-05)](https://x.com/btcqzy1/status/2051500517700808826)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Horizon** | Thysrael製OSS。HN/Reddit/RSS等から英中バイリンガル日報を自動生成する個人ニュースレーダー | `Thysrael Horizon AI news radar` |
| **TrendRadar** | sansan0製OSS。中国国内11プラットフォームの熱点をAI分析・推送 | `sansan0 TrendRadar 舆情` |
| **MCP (Model Context Protocol)** | Anthropic発のAIツール接続規格。Horizon/TrendRadar共に対応 | `MCP Anthropic protocol` |
| **AI信息差（AI情報格差）** | AIを使う人と使わない人の間に開く情報入手スピードの差を指すスローガン | `AI 信息差 自媒体` |
| **海外硬核（科技）** | 中国語圏での「英語圏のディープなテック情報」を指すスラング | `海外硬核 hacker news 中文` |
| **日報ブリーフィング** | 1日分のニュースをAIで要約・配信する形態。NotebookLMやClaude Projectsでも実装可 | `daily AI briefing newsletter` |
| **フィルターバブル** | パーソナライズで自分の好みだけが見える状態。情報レーダーが対抗策として登場 | `filter bubble Pariser` |
| **HelloGitHub** | 中国の人気OSS紹介プラットフォーム。両ツール共に掲載 | `HelloGitHub trending` |

---

## 🧭 背景 / なぜ今これが話題なのか

**「AI信息差」という中国語圏のミーム（2023〜）。** 中国IT/SNS界隈では「AIを使う人 vs 使わない人」の情報入手速度の差を **「AI信息差」** と呼ぶ。GPTショック以降にミームとして定着し、「AIで○○を自動化して情報差を埋めろ」系コンテンツがX中華圏・知乎・小紅書で量産されている。@BTCqzy1の「打破AI信息差」シリーズもこの文脈の一環で、**第一期がTrendRadar（国内向け）、第二期がHorizon（海外向け）** という構成。

**TrendRadarの急成長（2025年〜）。** sansan0が2025年6月頃から開発、半年強で **GitHub★56.7k**（2026-05時点）に到達。中国OSSとしては破格の伸びで、HelloGitHubでも上位常連。監視対象は知乎・抖音・bilibili・华尔街见闻・贴吧・百度・财联社・澎湃・凤凰・头条・微博 の **国内11プラットフォーム**。MCP連携（v3.0.0〜）で17個の智能分析ツールを Claude Desktop 等から呼べる構成は、2025年後半のMCP普及波に乗った典型例。

**Horizonの立ち位置（2025年末〜）。** Thysraelが開発するMITライセンスOSS。コミット履歴は134個、★2.2k と TrendRadar より小規模だが、**ターゲットが明確に「海外硬核」**（Hacker News / Reddit / RSS / Telegram / X / GitHub）。AIスコアリング・重複統合・コミュニティコメント要約・**英中バイリンガル日報**生成・GitHub Pages公開・メール配信・Webhook（Feishu/Slack/Discord）が一通り揃う。Docker / GitHub Actionsで「サーバ無し運用」可能。

**情報過多問題への構造的対応（2024〜2026）。** 「ニュース流し読み疲れ」を解決するAI日報ツールは欧米でも市場が立ち上がり、2025年で **$14.83B → 2033年予想 $29.77B** の成長予測。商用では Particle / ClarityBriefs / Ground News / Feedly AI / Claude Projects + Schedules、OSS自前派では Horizon / TrendRadar / trendFinder（ericciarla）等。**「フィードを集めて読む」から「AIに読ませて要点だけ受け取る」へ** のパラダイムシフトが確実に進行中。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| **Horizon = 海外硬核科技ニュース雷達** | 公式READMEで HN/Reddit/RSS/Telegram/X/GitHub から海外ソース収集する設計と明記。英中バイリンガル日報出力 | [GitHub - Thysrael/Horizon](https://github.com/Thysrael/Horizon) | ✅ 一致 |
| **「AIが代わりに全球科技圈を盯著」** | AIスコアリング・重複排除・背景情報リサーチ・コメント要約まで自動化される設計 | [Horizon on HelloGitHub](https://hellogithub.com/en/repository/Thysrael/Horizon) | ✅ 一致 |
| **「毎朝1通のブリーフィングを開くだけ」** | メール配信 / GitHub Pages / Webhook の3経路で配信。GitHub Actionsスケジュール化が推奨 | [GitHub - Thysrael/Horizon](https://github.com/Thysrael/Horizon) | ✅ 一致 |
| **TrendRadarが「git斩获5万星标」** | 2026-05時点で **★56.7k（forks 23.9k）**。「5万」は事実上正確（やや控えめな表現） | [GitHub - sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) | ✅ 一致 |
| **「TrendRadarで全網トレンドを自動監視」** | 監視対象は **国内11プラットフォーム中心**（知乎/抖音/bilibili等）。**HN/Reddit/Twitter等の海外は標準では含まれない**（RSS追加で間接的） | [GitHub - sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) | ⚠️ ほぼ一致（"全網"は中国全網寄り） |
| **「99%の人は算法に喂垃圾されている」** | フィルターバブル研究では「短期暴露の二極化効果は限定的」とする2024 PNAS論文もあり、**強い断言には学術的に異論あり** | [PNAS: Short-term exposure to filter-bubble recommendation systems...](https://www.pnas.org/doi/10.1073/pnas.2318127122) | ⚠️ 修辞的誇張 |

🔍 未確認: 0件（主要な検証対象はすべて裏取り完了）

---

## 🌐 最新動向（2026-05-06時点）

- **TrendRadarが半年で★56.7kへ急成長 — フォークも23.9k** — sansan0/TrendRadarのGitHubページで★56.7k / fork 23.9kを直接確認。MCP対応（v3.0〜）後から伸びが加速。 — [GitHub sansan0/TrendRadar](https://github.com/sansan0/TrendRadar), 2026-05
- **Horizonは「海外硬核ニッチ」を狙うMITライセンスOSSとして登場** — Thysrael/Horizonが英中バイリンガル日報を生成する個人ニュースレーダーとして公開。★2.2k、Docker / uv / GitHub Actions対応。 — [GitHub Thysrael/Horizon](https://github.com/Thysrael/Horizon), 2026-05
- **AIニュース要約市場は$14.83B（2025）→ 2033年に倍増予測** — News Aggregator Tool Marketは年率7.2%成長、AI個人化ブリーフィングが牽引。 — [News Aggregator Market 2026-2032](https://www.openpr.com/news/4475720/news-aggregator-tool-market-2026-2032-ai-powered-content), 2026-04
- **Particleが「10分日報」型でAIニュース市場の本命に** — ニュースレター + RSSを10分ダイジェストに圧縮、月30時間節約と謳う商用代表格。 — [Best AI News Aggregators in 2026 (Readless)](https://www.readless.app/blog/best-ai-news-aggregators-2026), 2026
- **ClarityBriefsが「フィード不要・自然言語で興味を伝える」型を提示** — 8.7万ソース x 89言語をAIが横断スキャンしてダッシュボード配信。Feedly的フィード組立が不要に。 — [Best Feedly Alternative 2026 (ClarityBriefs)](https://claritybriefs.com/blog/best-feedly-alternative-2026), 2026
- **Claude Projects + 定期実行で「自前AI日報」が個人レベルで成立** — Claude Co-work Projectsを使えば興味分野を記憶させた永続アシスタント＋スケジュール配信が組める。Horizon/TrendRadarの「セルフホスト派」と並ぶ第3の道。 — [How to Use Claude Co-work Projects... (MindStudio)](https://www.mindstudio.ai/blog/claude-cowork-projects-personalized-news-brief), 2026
- **MCPプロトコルがAIニュースツールの標準コネクタに** — Horizon・TrendRadar共にMCP対応で、Claude Desktop等から自然言語クエリが可能。「ツール → MCP → LLM」の三層が定型化。 — [TrendRadar README](https://github.com/sansan0/TrendRadar), 2026-05

---

## 🧩 関連概念・隣接分野

- **HelloGitHub**: 中国OSSコミュニティの登竜門。両ツールとも掲載。海外発OSSの中華圏での発見経路として重要。
- **Claude Projects（コワークプロジェクト）**: 興味・好みを永続記憶するAIアシスタント。Horizonの「セルフホスト型」と対をなす「商用クラウド型AI日報」アプローチ。
- **trendFinder（ericciarla製）**: 同系統のOSS。Twitter/Slack/Webhook統合がやや軽め。HorizonとTrendRadarの中間ポジション。
- **Feedly AI / Inoreader**: 旧世代のRSSリーダーがAIサマリ機能を後付け。「フィード設計の自由度」では依然強い。
- **MCP（Model Context Protocol）**: Anthropic発、2024年末リリース。ツール側がMCPサーバを実装すればLLMから自然言語で叩ける。Horizon/TrendRadar/Obsidian Skills...と2026年は普及期。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（ツイート発信者の立場）**:
  - HN/Reddit/RSSを毎日刷るより、AIに前処理させた方が時間効率が劇的に高い
  - セルフホストOSSなら**API/サブスク料金不要**でカスタマイズ自由度が高い
  - MCP対応により「読む」だけでなく「LLMに分析を投げる」拡張性がある
- **否定 / 慎重派の主張**:
  - **「AI日報疲れ」リスク**: 自分で読む時間が減る代わりに「AIが選んだ世界」に閉じこもる新しいフィルターバブル。研究者からは2025年以降、**LLM要約に最適化された情報摂取が認知バイアスを増幅する**懸念が指摘される — [Restraining filter bubbles (Wiley, 2025)](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24988?af=R)
  - **TrendRadarで「海外硬核」は基本不可**: ツイート文脈で「全網トレンド」と書かれていても、TrendRadarは中国国内向けが本籍。「海外硬核科技」を狙うなら**Horizonか英語圏ツール**が筋。
  - **セルフホストの隠れコスト**: Docker・GitHub Actions・APIキー管理・LLM料金（OpenAI/Anthropic）が累積。2026年の商用ツール（Particle / ClarityBriefs等）は月$5〜$15で収まる場面が多く、「無料OSS」は時間コストを払って自由度を買う取引。
  - **「99%の人は喂垃圾されている」断定への学術的反論**: PNAS 2024論文は「短期暴露の二極化効果は限定的」と結論。**フィルターバブル説は社会通念ほど強固でない**ことが直近の研究の流れ。([PNAS](https://www.pnas.org/doi/10.1073/pnas.2318127122))
- **中立的に見るときの補助線**:
  - **「自前/商用/Claude Projects」の3択** で考えると整理しやすい
    - 自前OSS派（Horizon / TrendRadar）: コスト低だが運用負荷あり、自由度最大
    - 商用派（Particle / ClarityBriefs / Brevio）: 月額数ドル、即動く、ロックインあり
    - LLMベンダ純正派（Claude Projects + Schedule）: 既存ツール環境に統合、汎用LLMの応用力を活かせる
  - 「中国ローカル情報を見たい」 → **TrendRadar**、「海外英語圏を見たい」 → **Horizon or 商用** が役割分担としては正しい
  - 個人の **Personal AI OS** を組むという文脈なら、これらニュースレーダーは「**入力レイヤー**」の1コンポーネントに過ぎず、Obsidian Vault / Claude Code / MCP との **接続性**で評価するのが筋

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] HorizonをObsidian vaultと連携させた事例（GitHub Pages出力をvaultに自動コピー → Obsidian Skillsで再要約 etc.）
- [ ] TrendRadarのMCPサーバを Claude Code から叩いて「中国国内トレンドを毎日 vault のデイリーノートに流す」フロー設計
- [ ] Particle / ClarityBriefsとの**コスト比較**（自前運用の月額LLM料金 vs 商用月額の損益分岐点）
- [ ] @BTCqzy1の「打破AI信息差」シリーズ第3期以降の予告（noteやZhihu連携の有無）
- [ ] 中国国内OSSが英語圏でも採用されるパスウェイ（HelloGitHub→Hacker News→海外コミュニティの流入経路）

---

## 📚 参考資料

- [GitHub - Thysrael/Horizon](https://github.com/Thysrael/Horizon) — Horizonの一次情報（README・スター数・機能リスト）, 取得日 2026-05-06
- [Horizon on HelloGitHub (English)](https://hellogithub.com/en/repository/Thysrael/Horizon) — 英語サマリ, 取得日 2026-05-06
- [GitHub - sansan0/TrendRadar](https://github.com/sansan0/TrendRadar) — TrendRadarの一次情報（★56.7k / 11プラットフォーム / MCP対応）, 取得日 2026-05-06
- [TrendRadar Tutorial (Decision Crafters)](https://www.decisioncrafters.com/trendradar-ai-powered-news-monitoring-tutorial/) — 第三者ガイドによる機能紹介, 取得日 2026-05-06
- [TrendRadar 本地部署教程 (少数派)](https://sspai.com/post/105506) — 中華圏での代表的なTrendRadarデプロイ記事, 取得日 2026-05-06
- [Best AI News Aggregators in 2026 (Readless)](https://www.readless.app/blog/best-ai-news-aggregators-2026) — 商用代替ツール7選比較, 取得日 2026-05-06
- [Best Feedly Alternative 2026 (ClarityBriefs)](https://claritybriefs.com/blog/best-feedly-alternative-2026) — フィード不要型の最新潮流, 取得日 2026-05-06
- [News Aggregator Tool Market 2026-2032 (OpenPR)](https://www.openpr.com/news/4475720/news-aggregator-tool-market-2026-2032-ai-powered-content) — 市場規模と成長率, 取得日 2026-05-06
- [How to Use Claude Co-work Projects (MindStudio)](https://www.mindstudio.ai/blog/claude-cowork-projects-personalized-news-brief) — Claude Projects型の代替アプローチ, 取得日 2026-05-06
- [Restraining filter bubbles (Wiley, 2025)](https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24988?af=R) — フィルターバブル対策の学術論文, 取得日 2026-05-06
- [PNAS: Short-term exposure to filter-bubble systems (2024)](https://www.pnas.org/doi/10.1073/pnas.2318127122) — フィルターバブル説への反証研究, 取得日 2026-05-06

---

## 🗒 メモ

- 自分のvault運用に直接活かすなら **Horizon の GitHub Pages 出力 → Tsukapon vault `Clippings/` に自動取り込み** が筋が良い。Obsidian Skillsで再要約してX投稿ネタの一次素材にする運用は[[. claude/commands/news-thread.md|/news-thread]] と相性良し。
- 「打破AI信息差」シリーズは中華圏で **再現性高いコンテンツフォーマット**。日本語版でも「**AI情報差を埋める道具・第N回**」シリーズで note / X に展開できる。差別化軸は「**Claude Code + Obsidian Vault でセルフホスト型情報レーダー**」あたり。
- ツイートで「海外硬核」を強調しているのは、第一期のTrendRadar（国内）に対する**カバレッジ補完の意図**。シリーズ構成は秀逸 → 自分が書くなら同じ構造で「**国内（日本語ニュース）→海外（英語ハードコア）→専門領域（論文/特許）**」の3部作にすると流用が効く。
- TrendRadarの監視対象に**日本国内プラットフォームは含まれない**点は要注意。日本語コンテンツを追うなら別途RSS/Custom実装が必要。今後の調査として「**TrendRadarをforkしてはてブ・Zenn・Qiita・X日本タイムラインを足したフォーク**」が候補になりうる。
- @BTCqzy1の発信スタイルは「**断言＋ツール推し**」型で、フォロワー獲得に強いが、学術的厳密さは緩い（フィルターバブル断言など）。自分の語り口は「**根拠を持って違いを示す**」方向で差別化したい。
