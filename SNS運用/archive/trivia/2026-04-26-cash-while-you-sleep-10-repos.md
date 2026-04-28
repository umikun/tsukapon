---
created: 2026-04-26
tags: [調査, GitHub, AIエージェント, OSS, リスト系ツイート]
source: Clippings/Post by @heygurisingh on X.md
---

# 「寝てる間に現金を生む10リポ」ツイートを冷静に解剖する

> **TL;DR**
> @heygurisingh の「sleep-money 10 repos」リスト系ツイートは、**全部実在するが半分は"金を生む"より"金を生み出すための補助スキル"**だった。実際にトレードを回すのは AutoHedge と Vibe-Trading の2つだけで、両方とも「研究・バックテスト用、live tradingではない」と公式が明言してる。
> 本物の収益化に近いのは **Cloudflare/agentic-inbox（インフラ実装力）**, **HeyGen/Hyperframes（バズ動画量産）**, **Anil-matcha/Open-Generative-AI（画像/動画SaaSの種）** の3本。残り5本（claude-ads, toprank, context-mode, camofox-browser, FinceptTerminal）は **「使えば金を稼げる」ではなく「金を稼ぐ作業を効率化する」** 道具なので、タイトル詐欺気味。
> あと7番目の「ClawRouter」は表示名で、リポ実体は `mksglu/context-mode`（10k★）。リンク経路が変則なので踏む前に注意。

## 📌 元テキスト（抜粋）

> 寝ている間に現金を生み出す10のGitHubリポジトリ：
> 1. AutoHedge … 2. Vibe-Trading … 3. Claude Ads … 4. Toprank … 5. Fincept Terminal … 6. Agentic Inbox … 7. ClawRouter … 8. Camofox Browser … 9. Open Higgsfield AI … 10. Hyperframes

出典: [[Clippings/Post by @heygurisingh on X.md]]
（投稿主は X リスト系インフルエンサーの @heygurisingh、添付画像2枚あり）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Swarm intelligence | 複数AIエージェントを協調させて1つの判断を出す手法 | multi-agent system, agent swarm |
| Solana | 高速・低手数料のレイヤ1ブロックチェーン。AutoHedgeのデフォ取引先 | Solana DeFi, Jupiter aggregator |
| HKUDS | 香港大 Data Intelligence Lab。多分野の OSS を量産する研究室 | HKUDS GitHub org |
| Claude Skills | Claude Code 上で動くドメイン特化スキル群（YAML+MD定義） | Claude Code skill marketplace |
| DataForSEO | SEO/順位取得APIのデファクト有料プロバイダ | DataForSEO pricing |
| Cloudflare Workers | サーバレスエッジ実行環境。Email Workers, Durable Objects等を含む | Cloudflare Email Workers |
| Stealth headless | Bot検知（Cloudflare/Akamai）回避型ブラウザ自動化 | Camoufox, Patchright, undetected-chromedriver |
| Context window optimization | LLMコンテキストを圧縮してコスト削減（grep/read出力など） | RTK token killer, headroom |
| Higgsfield AI | 動画生成のクローズドSaaS。Open-Higgsfield-AIはそのOSS版 | Higgsfield, Kling, Sora alternatives |
| HTML→Video | HTMLレンダ + GSAP でモーショングラフィックス動画を出力する手法 | Remotion, Hyperframes |

---

## 🧭 背景 / なぜ今これが話題なのか

X（旧Twitter）の英語AI界隈では2025年後半あたりから「**Top N GitHub Repos that ○○**」系の画像付きツイートが定番フォーマットになっている。@heygurisingh はそれを大量生産しているアカウントの1つで、今回の「sleep-money」もパッケージ化された **listicle テンプレ** に乗っている。

このフォーマットの常で、「現金を生む」とタイトルが煽っていても、実際は**リポジトリ単体では1円も生まない**。10本の中身を分類するとこう：

- **直接的にトレードする系**（2本）: AutoHedge, Vibe-Trading
- **広告/SEO業務を効率化する系**（2本）: claude-ads, toprank
- **金融データ閲覧系**（1本）: FinceptTerminal
- **インフラ/開発効率化系**（4本）: agentic-inbox, context-mode, camofox-browser, Hyperframes
- **コンテンツ生成 SaaSの種**（1本）: Open-Higgsfield-AI（→ Open-Generative-AI に改名済）

つまり**収益化の接続線は人間側の手数**にある。「AutoHedge を git clone して放置すれば寝てる間に資産が増える」と読んだ人は1ドルも稼げないので、ツイートの煽りを一段冷ます必要がある。

そしてもう1つ重要な点：**金融系2本（AutoHedge / Vibe-Trading）はどちらも公式に "research / simulation only, NOT live trading, NOT investment advice" と明記**している（[Vibe-Trading解説](https://tradersunion.com/news/editors-picks/show/1519525-vibe-trading-myth-or-model/), 2026-04時点）。AutoHedge の +12-18% という数字も backtest 値で、live で再現される保証はない（[BrightCoding解説](https://www.blog.brightcoding.dev/2025/11/26/autohedge-build-your-autonomous-ai-hedge-fund-in-minutes-2025-guide), 2025-11）。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| ① AutoHedge = 自動で稼ぐ | 実体は **autonomous agent framework**（MIT, ★1,578）。デフォルトで Solana のみ。**backtestベース**で +12-18%等の数字が出回るが live保証なし | [GitHub The-Swarm-Corporation/AutoHedge](https://github.com/The-Swarm-Corporation/AutoHedge), [BrightCoding](https://www.blog.brightcoding.dev/2025/11/26/autohedge-build-your-autonomous-ai-hedge-fund-in-minutes-2025-guide) | ⚠️ ほぼ一致（誇張あり） |
| ② Vibe-Trading = 個人トレード | **HKU研究室製**（MIT, ★2,811, Python）。**research/simulation/backtest限定**, live tradeしないと公式明記 | [GitHub HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading), [TradersUnion](https://tradersunion.com/news/editors-picks/show/1519525-vibe-trading-myth-or-model/) | ❌ 要注意（"trading"だが live ではない） |
| ③ Claude Ads = 広告で稼ぐ | 実体は **Claude Code用skill**（MIT, ★3,191）。Google/Meta/YouTube/LinkedIn/TikTok/Microsoft/Apple Adsの**監査・最適化チェック250+項目**。広告"運用代行業務の効率化"ツール | [GitHub AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | ⚠️ ほぼ一致（自分で出稿が必要） |
| ④ Toprank = SEO自動化 | **Claude Code skills for SEO/SEM/Google Ads**（MIT, ★1,042, Python）。SEOコンサル・自社サイト運用の補助 | [GitHub nowork-studio/toprank](https://github.com/nowork-studio/toprank) | ⚠️ ほぼ一致（同上） |
| ⑤ Fincept Terminal = 金融データ | 実在（★15,165）, 投資調査・経済データ閲覧UI。**Bloomberg Terminal風の閲覧アプリ**で、稼ぐツールではない | [GitHub Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) | ❌ 要注意（"閲覧"であって"運用"じゃない） |
| ⑥ Agentic Inbox = AI受信箱 | **Cloudflare公式**（Apache-2.0, ★1,456, TypeScript）。Cloudflare Workers上で動くAI付きセルフホストメール。**SaaS化・社内ツール化の素材として濃い** | [GitHub cloudflare/agentic-inbox](https://github.com/cloudflare/agentic-inbox) | ✅ 一致（マネタイズ材料あり） |
| ⑦ ClawRouter | **リポ実体は `mksglu/context-mode`**（★10,233, TypeScript）。Claude/Cursor/Gemini等のコンテキスト圧縮プロキシ。"ClawRouter"は別名/プロダクト名扱い | [GitHub mksglu/context-mode](https://github.com/mksglu/context-mode) | ⚠️ ほぼ一致（命名混乱あり） |
| ⑧ Camofox Browser = ステルス自動化 | 実在（MIT, ★3,161, JS）。Cloudflare/bot検知回避のPuppeteer/Playwright互換。**スクレイピング受託で稼ぐ用途** | [GitHub jo-inc/camofox-browser](https://github.com/jo-inc/camofox-browser) | ✅ 一致（業務委託の道具） |
| ⑨ Open Higgsfield AI | URLは生きてるが**リポ名が `Anil-matcha/Open-Generative-AI` に変更済**（★8,571）。200+モデル対応の画像/動画生成SaaS雛形 | [GitHub Anil-matcha/Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) | ⚠️ ほぼ一致（リダイレクト） |
| ⑩ Hyperframes = 動画生成 | **HeyGen公式**（Apache-2.0, ★11,008, TypeScript）。`HTML書く → 動画レンダ`。AIエージェント連携前提で、**ショート動画量産→アフィ/広告**の構成と相性◎ | [GitHub heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | ✅ 一致（量産の足回りになる） |

> 集計: ✅3本 / ⚠️5本 / ❌2本。「現金を生む」と直接言える完全該当は **3本だけ**。

---

## 🌐 最新動向（2026-04-26時点）

- **AutoHedge** が Solana特化で push 続いてる（最終 push 2026-04-13）。バックテスト数字 +12-18% は伸びてるが live track recordなし — [SourcePulse](https://www.sourcepulse.org/projects/2315995), 2026-04
- **Vibe-Trading v0.1.5** がリリース済（.env bootstrap, runtime data-source fallback, 12 LLM provider対応）。HKUのもう1つ `HKUDS/AI-Trader` が同系統で派生中 — [GitHub HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading), 2026-04
- **mksglu/context-mode（=ClawRouter）★10k超え**は2026-04-26時点で当日 push、コンテキスト圧縮系の本命候補に上昇。RTK（[[調査/2026-04-26-rtk-token-killer-cli-proxy.md]]）と並べて検討する価値あり — [GitHub mksglu/context-mode](https://github.com/mksglu/context-mode), 2026-04
- **HeyGen Hyperframes** は2026年Q1ローンチ後一気に★11k突破。HTML→Videoの教育キット（`nateherkai/hyperframes-student-kit`★231）や `agno-agi/vibe-video` のような派生も生まれている — [GitHub heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), 2026-04
- **Cloudflare agentic-inbox** はEmail Workers + AI agentの公式実装例。セルフホスト型 Superhuman/HEY代替を目指すSaaSプロジェクトが派生しはじめている — [GitHub cloudflare/agentic-inbox](https://github.com/cloudflare/agentic-inbox), 2026-04
- **Anil-matcha のリポ改名**（Open-Higgsfield-AI → Open-Generative-AI）はSora/Veo/Klingまで対応モデルを拡張したから、というのが推測。Higgsfieldだけ追従してる人はリンク切れ注意 — [GitHub Anil-matcha/Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI), 2026-04

---

## 🧩 関連概念・隣接分野

- **コンテキスト圧縮プロキシ**: ClawRouter/context-mode と RTK は同じカテゴリ。AIコーディング代金の最大支出ポイントを叩く道具で、2026年に一気に10k★級が複数出てきた — [[調査/2026-04-26-rtk-token-killer-cli-proxy.md]]
- **OSS-as-SaaS-代替**: Open-Generative-AI / agentic-inbox / context-mode はいずれも「有料SaaSをセルフホスト版で撃つ」型。同じ系譜で Open-SEOがいる — [[調査/2026-04-26-open-seo-self-hosted-stack.md]]
- **Claude Code Skill 経済圏**: claude-ads / toprank はどちらも Skill単位での配布。Skill marketplace まわりは別途調査済 — [[2026-04-24-claude-code-plugin-marketplace]]
- **Stealth Browser/スクレイピング**: camofox-browser は Camoufox（Firefox派生）/Patchright/undetected-chromedriver と同枠。受託・データプロバイダの足回り
- **Agent + Email**: agentic-inbox は Cloudflare Email Workers + Durable Objects の組み合わせ事例で、SaaS発射台として濃い

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側（リスト発信者の論調）**: 「OSSを並べて知らせれば、誰かが組み合わせて副収入を作る。情報の存在自体が価値」
- **否定 / 慎重派**:
  - **タイトル詐欺問題**: 10本中7本は"稼ぐツール"でなく"作業を速くする道具"。読者が「git clone → 寝る → 起きたら入金」を期待すると100%裏切られる
  - **金融系のリスク**: AutoHedge/Vibe-Tradingの数字はいずれもbacktest。Solana / 暗号資産でlive運用すれば**元本毀損は当然あり得る**。各国で投資助言業との接点を踏みかねない
  - **ステルスブラウザの法務**: camofox-browser系は**利用規約違反/不正アクセス禁止法のグレーゾーン**を踏みやすい。"稼ぐ"前提で使うなら案件選定が必須
  - **★数バブル**: ★10k級でも**実装の薄いハイプ系**が混じる。issuesと commit historyで活性度を見るべき
- **中立的に見る補助線**: 「**収益化の道筋を自分で描けるか**」だけが判断基準。AutoHedge を起点に Solana 自動運用業を構築する／Hyperframes を起点に1日10本のショート動画SaaSを建てる、みたいに**人間の事業デザイン**を1本足せれば、リスト中の道具は本当に役立つ

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] AutoHedge / Vibe-Trading で**live trade 接続まで持っていく**最小構成はどう書くか（&法的責任の境界）
- [ ] Cloudflare agentic-inbox を**SaaSの軸**にする場合、Workers / Durable Objects / R2のコスト試算
- [ ] mksglu/context-mode（ClawRouter）と RTK の **A/B 比較**（圧縮率・互換性・遅延）
- [ ] Hyperframes + Claude Code でショート動画**量産パイプライン**を組んだ場合の単価試算
- [ ] @heygurisingh 系の listicle 投稿が **note記事の横展開素材**として使えるか（"私が試した5つだけ" 切り口）

---

## 📚 参考資料

- [GitHub The-Swarm-Corporation/AutoHedge](https://github.com/The-Swarm-Corporation/AutoHedge) — AutoHedge本体・★1,578・MIT・最終push 2026-04-13、取得日 2026-04-26
- [BrightCoding: AutoHedge 2025 Guide](https://www.blog.brightcoding.dev/2025/11/26/autohedge-build-your-autonomous-ai-hedge-fund-in-minutes-2025-guide) — 性能数値とlive保証なしの注意、取得日 2026-04-26
- [SourcePulse: AutoHedge stats](https://www.sourcepulse.org/projects/2315995) — リポ活性度の追跡、取得日 2026-04-26
- [GitHub HKUDS/Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) — Vibe-Trading本体・★2,811・MIT、取得日 2026-04-26
- [TradersUnion: Vibe trading – myth or model](https://tradersunion.com/news/editors-picks/show/1519525-vibe-trading-myth-or-model/) — research/simulation限定であることの裏取り、取得日 2026-04-26
- [GitHub AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) — Claude Code skill, 250+ ads checks、取得日 2026-04-26
- [GitHub nowork-studio/toprank](https://github.com/nowork-studio/toprank) — SEO/SEM Claude skills、取得日 2026-04-26
- [GitHub Fincept-Corporation/FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) — 金融閲覧端末、取得日 2026-04-26
- [GitHub cloudflare/agentic-inbox](https://github.com/cloudflare/agentic-inbox) — Cloudflare公式・Workers + AI、取得日 2026-04-26
- [GitHub mksglu/context-mode](https://github.com/mksglu/context-mode) — ClawRouter実体、★10,233、取得日 2026-04-26
- [GitHub jo-inc/camofox-browser](https://github.com/jo-inc/camofox-browser) — stealth headless、取得日 2026-04-26
- [GitHub Anil-matcha/Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — Open-Higgsfield-AI改名後、取得日 2026-04-26
- [GitHub heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — HTML→Video公式、取得日 2026-04-26

---

## 🗒 メモ

このリストは note記事の素材としては**そのままだとAIっぽくて弱い**。けど切り口を変えれば化ける：

- **「実際に試したのは2本だけ」リライト**: 10本まとめではなく「自分で動かして黒字化に近づいた/挫折した本数を正直に書く」型。ホンネ系の方がX/Threadsで伸びる
- **「タイトル詐欺見抜き方」記事**: 「"寝てる間に稼ぐ"系ツイートに騙されない3つのフィルタ」みたいな批評型。RT誘発に強い
- **「AIコーディング代を90%削る組み合わせ」**: ClawRouter（context-mode）+ RTK の2本立てで実コスト計測 → これは別ノートで深掘り価値あり

@heygurisingh のフォーマット自体は learn する価値ある（**画像2枚 + 番号付き10個 + URL**）。X案で「私が試した10個のうち実際に金になった3つ」みたいに**減算型listicle**にすると差別化できる。
