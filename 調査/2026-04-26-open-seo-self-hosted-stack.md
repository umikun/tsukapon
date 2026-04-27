---
created: 2026-04-26
tags: [調査, SEO, OSS, セルフホスト, DataForSEO]
source: https://x.com/ErickSky/status/2047879737545036172
---

# OpenSEO（every-app/open-seo）— Semrush/Ahrefsの"セルフホスト＋従量課金"代替を冷静に見る

> **TL;DR**
> OpenSEOは**MIT・TypeScript製**のSEOダッシュボードで、データは外部の**DataForSEO API**から取ってくる従量課金型。Semrush/Ahrefsの月$129〜$140を、検索1回$0.002〜キーワード調査1回$0.035 で置き換えられる可能性がある。ただし**「100%無料」は誤訳に近い**（DataForSEOの最低$50デポジットが必要）。**ロードマップ上の"AI可視性/GEO/MCP統合"はまだ未実装**で、Erickの煽りとは温度差がある。「自分のドメインで小〜中規模に運用する個人/小規模代理店」が一番コスパに乗れる構図。

## 📌 元テキスト（抜粋）

> SEOやウェブサイトのオーナーたちは、このリポジトリをバズらせるでしょう。文字通り、年間数千ドルの節約になるからです。
>
> [Open-SEO]
> ✅ キーワード調査 / ✅ 順位追跡 / ✅ バックリンク / ✅ 完全なSEO監査 / ✅ AIによる可視性
> ✅ 100%セルフホスト可能でGRATIS（DataForSEOのAPIだけ有料、使いたい場合のみ）
> ✅ 毎日の更新

出典: [[Clippings/Post by @ErickSky on X.md]]
リダイレクト先: [every-app/open-seo on GitHub](https://github.com/every-app/open-seo)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| OpenSEO | every-appが公開した OSS の SEO ダッシュボード | `every-app/open-seo` |
| DataForSEO | 大手SEO SaaSの裏側でも使われている**SEOデータAPI卸** | `DataForSEO pricing` `SERP API` |
| セルフホスト | 自分のサーバーやPC上で動かすこと（SaaSの逆） | `Docker compose` `Cloudflare Workers` |
| 従量課金（Pay-as-you-go） | サブスクではなく使った分だけ払う | `DataForSEO PAYG` |
| サイト監査 (SEO Audit) | クロールしてSEO上の技術的問題を洗い出す | `SEO crawl` `technical SEO` |
| バックリンク分析 | 自サイトに貼られた外部リンクを把握する | `referring domains` `backlink profile` |
| AI可視性 (AI Visibility) | ChatGPT/Perplexityなど**生成AIに引用される度合い** | `GEO` `LLM visibility` `AEO` |
| GEO (Generative Engine Optimization) | 生成AI検索に向けたSEOの新潮流 | `Generative Engine Optimization` |
| MCP | Anthropicの Model Context Protocol（AI⇄ツールの規格） | `Claude MCP` `MCP server` |
| SEOnaut | OpenSEOと並ぶOSSのSEO監査ツール（音/監査寄り） | `StJudeWasHere/seonaut` |

---

## 🧭 背景 / なぜ今これが話題なのか

### SEOツール市場の "課金疲れ" が限界に来てる

2026年時点で SEO の二強 Semrush / Ahrefs はそれぞれ **Semrush Pro $139.95/月、Ahrefs Lite $129/月** が入口で、本格運用すると Guru/Standard $249/月コースに上がる。複数クライアントを抱える代理店だと Business $499.95/月が現実的なライン。「年間数千ドル」は十分現実の数字。

### "DataForSEO の卸売りを直接叩く" 文化が普及

Semrush も Ahrefs も実態は **DataForSEO のような SEO データ API の集約 + UI** に近い。だから **「UIだけ自前で作って、データは DataForSEO から直接買う」** 構成にすれば、サブスク料金の中に乗っている UI/サポート/マーケコストを丸ごと外せる、というのが OpenSEO 系プロジェクトの根本アイデア。

### LLMの「AI可視性」需要が燃料

2026年に入ってから、ChatGPT/Perplexityの引用順位を測る **GEO (Generative Engine Optimization)** が SEO 業界の最大トピックになっている。Semrush/Ahrefsもここに大型機能を投入中で、価格はさらに上振れ傾向。**「AIで世界変わる前に固定費を畳みたい」** 層が OSS 代替に流れる流れ。

### every-app の "Own your X" 文脈

リポジトリ名は `every-app/open-seo`。every-appの他のプロジェクトと同じく **「Own your ◯◯（自分の◯◯を持とう）」** がトーン。Vercel/SaaS依存への反動として 2025〜26年に強まっている**「Build it yourself」コミュニティ**の流れにのってる。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「年間数千ドルの節約」 | Semrush Pro $139.95×12 = $1,679/年, Ahrefs Lite $129×12 = $1,548/年。Guru/Standardなら $3,000/年超。**「数千ドル」は妥当〜やや控えめ** | [Semrush Pricing](https://aiproductivity.ai/blog/semrush-pricing/) | ✅ 一致 |
| 「キーワード調査」 | リポジトリREADMEに**実装済みとして記載** | [every-app/open-seo](https://github.com/every-app/open-seo) | ✅ 一致 |
| 「順位追跡」 | リポジトリREADMEに**実装済み**とあるが、daniliants（2025末頃のレビュー）は **「rank tracking is the biggest gap」** と書いていた。**最近実装された可能性が高い** | [Daniliants Review](https://daniliants.com/insights/github-every-appopen-seo-own-your-seo-research-keywords-and-competit/), [GitHub README](https://github.com/every-app/open-seo) | ⚠️ ほぼ一致（時期で食い違い） |
| 「バックリンク」 | 実装済み。ただし**DataForSEOのBacklinks サブスク有効化**＋**追加$100/月のミニマムコミット**が別途要 | [DataForSEO Backlinks Pricing](https://dataforseo.com/help-center/backlinks-api-pricing-explained) | ⚠️ ほぼ一致（コスト注記あり） |
| 「完全なSEO監査」 | サイト監査機能あり。ただし**SEOnautのような技術監査専用OSS**ほどクロール設定は深くない | [SEOnaut](https://github.com/stjudewashere/seonaut) | ⚠️ ほぼ一致 |
| 「AIによる可視性」 | リポジトリの**ロードマップに「AI SEO, GEO, LLM visibility」と明記**＝**未実装** | [GitHub README](https://github.com/every-app/open-seo) | ❌ 要注意（まだ未実装） |
| 「100%セルフホスト可能でGRATIS」 | アプリ本体は無料・MIT。ただし**DataForSEOは$50最低デポジットから**。ローカル動作と"完全無料"を混同しないこと | [DataForSEO Pricing](https://dataforseo.com/pricing) | ⚠️ ほぼ一致（誤読注意） |
| 「毎日の更新」 | データ更新は**DataForSEO側のクロール周期**＋**自分でcron回す設定**に依存。アプリ自体は手動でも回る | [DataForSEO API v3](https://dataforseo.com/pricing) | 🔍 未確認（運用次第） |
| MIT・TypeScript・1.6kスター | GitHub上で確認 | [GitHub repo](https://github.com/every-app/open-seo) | ✅ 一致 |

---

## 🌐 最新動向（2026-04-26時点）

- **OpenSEO本体が "rank tracking" を後追い実装済み**。2025末のレビューでは「未実装」だったが、2026年初頭には READMEの実装機能リストに入っている — [GitHub README](https://github.com/every-app/open-seo), 2026-04
- **AI可視性 / GEO / Claude向けMCPサーバー** がロードマップに正式記載。同じく `every-app` が他リポジトリで MCP 系も触っているのでセットで来る可能性 — [GitHub README](https://github.com/every-app/open-seo), 2026-04
- **SEOmonitorが LLM Switcher（複数AIモデルの引用順位を一括追跡）を Rank Tracker ヘッダーに正式導入** — 商用側のGEO競争が激化 — [SEOmonitor Help Center](https://help.seomonitor.com/en/articles/14060942-what-s-new-in-rank-tracker-march-2026), 2026-03
- **DataForSEOは2026年も $0.0006/query（Standard）の最安値レーンを維持**。Backlinksは$100/月ミニマムコミット制（n8n / Make.com経由なら回避可） — [DataForSEO Backlinks Pricing](https://dataforseo.com/help-center/backlinks-api-pricing-explained), 2026-04
- **"open-source SEO tools" 検索のSEO記事自体が量産中** — OpenSEO・SEOnaut・Matomo SEO・Yoastなどを並べる比較記事が2026年に入ってから爆増中で、「OSSだけでSEO業務を回す」が一般化フェーズ — [Best Open Source SEO Tools 2026](https://seojuice.com/blog/top-open-source-tools-for-seo/), 2026-Q1

---

## 🧩 関連概念・隣接分野

- **DataForSEO**: そもそもの "卸" API。OpenSEO/Semrush/Ahrefsその他、ほとんどの中小SEO SaaSが裏で使っている。**OpenSEOを使うかどうかに関わらず、ここを直接叩く発想を持つだけで月数万円浮く**業界の盲点
- **SEOnaut（[StJudeWasHere/seonaut](https://github.com/stjudewashere/seonaut)）**: OSSのSEO監査ツール。クロール深掘り・robots.txt無視・パスワード保護ステージング対応など**監査専用としてはOpenSEOより強い**。役割分担で併用するのがアリ
- **GEO / AEO（Generative/Answer Engine Optimization）**: ChatGPT/Perplexity/Google AI Overviewでの引用最適化。2026年のSEO最重要テーマで、OpenSEOロードマップ最大の目玉
- **MCP (Model Context Protocol)**: Claude などのAIエージェントが SEO データを直接読みに行ける規格。OpenSEO のロードマップに「Claude向けMCP統合」と明記されており、**実装されればCursor/Claude CodeからSEO作業が直接回せる**世界が来る
- **n8n / Make.com**: DataForSEOのBacklinks API最低コミットを回避できる経路。OpenSEOを使わずとも、これらでSEO自動化パイプラインだけ作る選択肢もある — 関連: [[調査/2026-04-26-create-agent-tui-openrouter.md]]（自前ツール文脈）

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「サブスクSEOは個人・中小には過剰課金。データAPIを直接叩いて自分のUIで回せば、機能の80%は$10〜30/月で済む」「AI時代にデータと運用ロジックを自社内に持つことの戦略的価値はむしろ上がる」
- **否定 / 慎重派の主張**:
  - **学習コスト＞節約金額になりがち**: Docker、API key発行、cronセット、cost monitoring……「やっと動かしたけど結局Semrush復帰した」は OSS SEO ツール定番のオチ
  - **データ品質はSemrush/Ahrefs独自クロールの方が深い**部分が残る（特に被リンクのインデックスサイズ）
  - **サポート不在**: 解析がおかしいときに頼れる人がいない。クライアントワークでは商用ツールの方が説明責任を担保しやすい
  - **「無料」表記の誤読リスク**: チームメンバーやクライアントに「無料だから」と提案して、後から月の DataForSEO 請求で揉める事故
- **中立的に見るときの補助線**:
  - **「個人サイト1〜3本＋月20-50キーワード追跡」規模なら間違いなくOpenSEOが安い**（年$50〜200のレンジ）
  - **「クライアント10社・キーワード数千・週次レポート義務」規模はSemrush/Ahrefs残留が安全**
  - **両刀使いも現実解**：商用は1ライセンスだけ残し、追加キーワード/競合監視はOpenSEOで増設

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] OpenSEO の rank tracking、**実際の頻度（毎日 / 毎時 / オンデマンド）**は？ DataForSEOコストとの関係は？
- [ ] Cloudflare Workers版で動かしたとき、**Workers KV/R2の使用量**はどれくらい乗ってくるか
- [ ] 「**MCPサーバー化されたOpenSEO**」が出たら、Claude CodeからそのままSEO業務スキル化できる。タイムラインは？
- [ ] **日本語キーワード**でのDataForSEO精度（特に Yahoo!Japan / モバイル / 音声検索）はどこまで信頼できるか
- [ ] every-app の他リポジトリ（`open-X`シリーズ）はあるか — 同じ思想で **「Own your CRM」「Own your Analytics」** あたりが出てそう

---

## 📚 参考資料

- [every-app/open-seo (GitHub)](https://github.com/every-app/open-seo) — リポジトリ本体・README・ロードマップ確認, 取得日 2026-04-26
- [OpenSEO レビュー by Daniliants](https://daniliants.com/insights/github-every-appopen-seo-own-your-seo-research-keywords-and-competit/) — 2025末〜2026初頭の機能評価、rank trackingが当時未実装だった証拠, 取得日 2026-04-26
- [DataForSEO Pricing (公式)](https://dataforseo.com/pricing) — $50最低デポジット・$0.0006/query〜の料金体系, 取得日 2026-04-26
- [DataForSEO Backlinks Pricing](https://dataforseo.com/help-center/backlinks-api-pricing-explained) — Backlinks APIの$100/月ミニマムコミットとn8n/Make.com経由での回避策, 取得日 2026-04-26
- [Semrush Pricing 2026](https://aiproductivity.ai/blog/semrush-pricing/) — Pro $139.95 / Guru $249.95 / Business $499.95 の確認, 取得日 2026-04-26
- [SEMrush vs Ahrefs Pricing 2026](https://brightseotools.com/post/SEMrush-vs-Ahrefs-Pricing-Full-Cost-Breakdown) — Ahrefs Lite $129 / Standard $249 の確認, 取得日 2026-04-26
- [SEOnaut (StJudeWasHere/seonaut)](https://github.com/stjudewashere/seonaut) — OSS技術監査ツールとの役割比較, 取得日 2026-04-26
- [SEOmonitor What's New (March 2026)](https://help.seomonitor.com/en/articles/14060942-what-s-new-in-rank-tracker-march-2026) — 商用側のLLM対応最新動向, 取得日 2026-04-26
- [Best Open Source SEO Tools 2026](https://seojuice.com/blog/top-open-source-tools-for-seo/) — OSS SEOツール市場の俯瞰, 取得日 2026-04-26
- [Post by @ErickSky on X (vault内)](https://x.com/ErickSky/status/2047879737545036172) — 元投稿。クリッピング: [[Clippings/Post by @ErickSky on X.md]], 取得日 2026-04-26

---

## 🗒 メモ

- このネタは**「SaaSサブスク疲れ」「OSSセルフホスト」「AI時代の自前化」**3つのトレンドが交差する位置にあるので、note記事化しやすい。タイトル候補：「**Semrushを年$1,500で契約してる人へ。OpenSEOは$0だけど"完全無料"ではない理由**」あたりが**型⑦損失回避**として刺さりそう
- ただし**コンテンツ被り注意**: [[調査/2026-04-23-oss-saas-alternatives.md]] と関連性が強い。同記事で OpenSEO を1ケースとして引用する形にした方が記事の体系性が出る
- **個人運用フィット度チェック**: [[SNS運用]] 配下の自分の運用なら、月キーワード20本程度の規模感。**OpenSEO + DataForSEO最低デポジット$50** で年$50〜100で回せそうだが、Semrush系を実際に使ってないなら**そもそも乗り換え動機がない**ので、自分に必要かは別問題
- **GEO（生成AI可視性）が来てから検討の方が賢い**: 今のOpenSEOにAI可視性はまだ無い。商用のSemrush/SEOmonitorも追加課金中。**ロードマップに名指しされている`AI SEO + MCP`機能の実装待ち**でちょうどいいタイミングで参入できる
- 人格データ整合: [[_ kiwami/my-clone/brain/プロフィール.md]] の「実績なし・駆け出し2ヶ月目」と整合的に語るなら、**「自分はまだ試してない、でもツール選定の罠ポイントだけ整理した」**スタンスが正解。レビュー口調はNG
