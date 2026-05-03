---
created: 2026-05-01
tags: [調査, seo, geo, rust, tauri, log-analysis]
source: "[[Clippings/Post by @Fluyeporlaweb on X.md]]"
---

# 元ポストが紹介していたのは「RustySEO」——Rust+Tauri製の無料テクニカルSEO/GEOツールキット（GPL-3.0、最新v0.3.8 / 2026-04）

> **TL;DR**
> @Fluyeporlawebの投稿が指していたのは、おそらく **mascanho/RustySEO**。Rust+Tauri製のクロスプラットフォーム・デスクトップSEOツールで、**サイトクロール × Nginx/Apacheログ解析 × Core Web Vitals × GEO（Generative Engine Optimization）**を1アプリに統合。GPL-3.0、ローカルLLM（Ollama）/Gemini連携あり、最新は **v0.3.8（2026-04）**。Screaming Frogの代替として無料・OSSで使える希少な選択肢だが、★222程度・実装は活発開発中なので「業務で全面的に置き換える」よりは「**個人代理店の検証用＋ログ解析の入口**」としての導入が現実的。

## 📌 元テキスト（抜粋）

> Rustで構築されたウェブサイトとサーバーログを大規模に監査するためのテクニカルSEOツール  Nginx、Apache、クローリング、分析、最適化がすべて統合
>
> ✅ Rustのおかげで高速なテクニカル監査
> ✅ サーバーログの分析（NginxとApache）
> ✅ サイトのクローリングと最適化
> ✅ GEOとSEOの組み合わせに焦点
> ✅ オープンソース

出典: [[Clippings/Post by @Fluyeporlaweb on X.md]]（@Fluyeporlaweb / 2026-04-30投稿、URL: <https://x.com/Fluyeporlaweb/status/2049845980024242424>）

ポスト内では具体的なツール名が明示されていないが、上記の特徴（**Rust×Nginx/Apacheログ×クロール×GEO×OSS**）に完全一致するのは [mascanho/RustySEO](https://github.com/mascanho/RustySEO) で、添付画像のスクショもこのツールのUIと一致するパターン。以下、RustySEO前提で深掘りする。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| RustySEO | Rust+Tauri製のOSSテクニカルSEO/GEOツールキット | `mascanho/RustySEO`, `GPL-3.0` |
| テクニカルSEO | サイト構造・速度・クロール性などを最適化する領域 | `Core Web Vitals`, `crawl budget` |
| GEO（Generative Engine Optimization） | ChatGPT/Claude/Gemini/Perplexityに引用されるためのコンテンツ最適化 | `AI search`, `citation optimization` |
| サーバログ解析 | Nginx/Apacheのアクセスログから検索ボットの挙動を調べる手法 | `log file analyzer`, `Googlebot crawl` |
| Tauri | Rust製のデスクトップアプリフレームワーク。Electron軽量代替 | `Tauri 2.0`, `webview` |
| Screaming Frog | 業界標準の有料テクニカルSEOクローラ（Java製、UK発、2010〜） | `SEO Spider`, `screamingfrog.co.uk` |
| OnCrawl / Botify | 商用のクロール+ログ解析統合ツール（クラウド・エンタープライズ寄り） | `crawl budget analysis` |
| Core Web Vitals | Googleの体感速度3指標（LCP/INP/CLS） | `web.dev`, `PageSpeed Insights` |
| Ollama | ローカルLLM実行ランタイム。RustySEOがチャットボットで利用 | `ollama.ai`, `local LLM` |
| crawl budget | 検索ボットが1サイトに割り当てる巡回リソース。ログで実測する対象 | `Googlebot rate limit` |

---

## 🧭 背景 / なぜ今これが話題なのか

テクニカルSEO領域は長らく**Screaming Frog SEO Spider**（2010〜、UK発、Java製、GUIデスクトップ）の独壇場で、ライセンス£259/年（無料版は500URLまで）が代理店の標準ツールだった。**OnCrawl**や**Botify**といったクラウドのエンタープライズ系（クロール+ログ解析統合）は月数百〜数千ドル級で、中小代理店・個人にはハードルが高い。

ここに**「OSS×Rust×ログ解析統合」のRustySEO**（mascanho、GitHub上で2024〜2025頃から本格開発、本記事執筆時点★222）が登場。Rust製のため起動・クロールが速く、Tauriで配布が軽い。**v2.x表記の第三者レビュー記事**もあるが、GitHub上の実態は **v0.3.8（2026-04）**——つまり「OSSの第三者紹介はバージョン名を盛りがち」という典型例にも遭遇できる（[reviewnexa.com](https://reviewnexa.com/rustyseo-review-the-free-open-source-seo-tool-that-rivals-premium-software-in-2026/) は「v2.0=Jan2026」と書くが、上流リポジトリは0.3.x系で進行中）。

並行して2025〜2026年は **GEO（Generative Engine Optimization）** がSEO業界の最大のバズワード化。Gartner予測の「**生成AIで従来検索が25%減**」を背景に、ChatGPT/Perplexity/Claude/Geminiから引用されるための最適化が独立スキルになりつつある。RustySEOが「**SEO+GEO同居**」を売りにしているのは、この時流に乗った設計判断と読める。

なお、本vaultにも[[2026-04-26-open-seo-self-hosted-stack]]（every-app/open-seo＝キーワードリサーチ寄り）の調査メモがあり、**「商用SEOツールをOSSで剥がす」流れは2026年に明確に来ている**。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Rustで構築されている | リポジトリの言語比率は TypeScript 80% / Rust 19.5%。Tauri採用なのでフロントはTS/React、コアロジックの一部がRust。「Rustで構築」は**やや盛り気味**（Rust「で」というよりRust「を含むTauri」） | [GitHub mascanho/RustySEO](https://github.com/mascanho/RustySEO) | ⚠️ ほぼ一致（誇張あり） |
| サーバログ解析（Nginx & Apache）対応 | 公式README「Server Log Analysis: Apache and Nginx log parsing and analysis」 | 同上 | ✅ 一致 |
| サイトクロールと最適化 | shallow crawl / deep crawl対応、Core Web Vitals/PageSpeed Insights連携、On-Page SEO（content/keyword density） | 同上 | ✅ 一致 |
| GEOとSEOの組み合わせに焦点 | リポジトリ説明欄「SEO/GEO toolkit」、READMEもGEO項目あり。AIチャットボット連携（Ollama/Gemini）でGEO支援を演出 | 同上 | ✅ 一致 |
| オープンソース | GPL-3.0ライセンス。無料利用可だが派生物のソース開示義務あり（商用組み込みは要注意） | 同上 | ✅ 一致 |
| 「本気でテクニカルSEOを行う代理店にとって大きな利点」 | 機能セット的にScreaming Frog相当の領域をカバーするのは事実。ただし**★222・v0.3.8で発展途上**。代理店業務の主軸に据えるのはまだ早い | 同上 / [ReviewNexa記事](https://reviewnexa.com/rustyseo-review-the-free-open-source-seo-tool-that-rivals-premium-software-in-2026/) | ⚠️ ほぼ一致（期待値要調整） |
| 「Rustのおかげで高速」 | Rust部分はクロール/ログparseの重い処理に効く設計。第三者レビューでv2.xでクロール速度+30%という記述があるが、上流リポジトリのバージョン番号と一致しないので**この数字は鵜呑み厳禁** | [ReviewNexa](https://reviewnexa.com/rustyseo-review-the-free-open-source-seo-tool-that-rivals-premium-software-in-2026/) | 🔍 未確認（数値の出典不明瞭） |

---

## 🌐 最新動向（2026-05-01時点）

- **RustySEO v0.3.8 リリース（2026-04）**: GitHub上のreleasesで確認できる最新版。継続的に小数点リリース中、Windows/macOS両対応 — [GitHub Releases](https://github.com/mascanho/RustySEO/releases), 2026-04
- **OllamaとGemini APIをチャットボットに同時統合**: ローカルLLMとクラウドLLMを切り替えられる構造で、SEO監査結果の解釈をAIに任せる体験を提供 — [GitHub README](https://github.com/mascanho/RustySEO), 2026
- **GEO（Generative Engine Optimization）が2026年のSEO業界主要トレンドに**: Gartner「生成AIで従来検索25%減」予測がバズワード化、SEO/GEO併走戦略が標準化 — [WordStream 2026](https://www.wordstream.com/blog/generative-engine-optimization), [Jasper Blog 2026](https://www.jasper.ai/blog/geo-aeo), 2026
- **OSSテクニカルSEOクローラの選択肢が拡大**: LibreCrawl（Python/Qt）、SiteOne Crawler（PHP）、SEO Reporter（CLI 220+チェック）、RustySEO（Rust+Tauri）が出揃う — [AlternativeTo OSS list](https://alternativeto.net/software/screaming-frog-seo-spider/?license=opensource), 2026
- **ログ解析+クロール統合のOSSは依然希少**: 大半のOSSはクロールのみ。「ログ×クロール一体」を無料で提供しているのはRustySEOがほぼ唯一の現実解。商用はOnCrawl/Botifyが主流 — [Capterra 2026 Screaming Frog比較](https://www.capterra.com/p/185765/Screaming-Frog-SEO-Spider/), [searchatlas blog](https://searchatlas.com/blog/screaming-frog-alternatives/), 2026

---

## 🧩 関連概念・隣接分野

- **Screaming Frog SEO Spider**: テクニカルSEOの業界標準。RustySEOの直接ベンチマーク。GUI/機能/プラグイン/ドキュメント量で本家が圧倒的。ただし有料・閉源
- **OnCrawl / Botify**: クラウドのエンタープライズ系。**ログ×クロール統合**をRustySEOと同じく謳うが、価格帯が桁違い（月数百〜数千ドル）
- **Generative Engine Optimization (GEO)**: 「ChatGPT/Claude/Perplexityにcitation挿入される設計」。従来SEOがクリック獲得最適化なのに対し、**citation獲得最適化**にゴールが変わる
- **Core Web Vitals (LCP/INP/CLS)**: 体感速度の3指標。RustySEOがPageSpeed Insights APIを叩いて取得・レポート化する
- **Tauriエコシステム**: Rust+Webviewのデスクトップアプリ基盤。RustySEOのほか、最近のOSSデスクトップ系（音楽プレイヤー・ノートアプリ等）が雪崩を打って採用中
- **GPL-3.0ライセンスの含意**: SaaS化や閉源製品への組み込みは原則NG（コピーレフト）。**代理店内製ツールに改造する場合、改造ソースの公開義務が発生する点は要注意**
- **本vault関連**: [[2026-04-26-open-seo-self-hosted-stack]] のevery-app/open-seoはキーワード/競合リサーチ寄り、RustySEOはテクニカル/ログ寄り、と**カバー範囲が補完関係**

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: Screaming Frogは年£259、OnCrawl/Botifyは月数百ドル超。**個人事業主や小規模代理店にとって「無料でテクニカルSEO+ログ×GEO一体」のRustySEOは破壊的にコスパが良い**。Rust/Tauriで起動が軽く、ローカル動作なので顧客サイトログを外部送信する必要がない（GDPR/プライバシー的に楽）。
- **否定 / 慎重派の主張**:
  - **★222は実運用基準で見ると小規模**。Issue/PRの捌きスピード、Windowsのコード署名警告、突然の方針転換リスクは現実的。商用代理店の主軸ツールには時期尚早。
  - **「Rust製で爆速」マーケは話半分**: コード比率はTS 80% / Rust 20%。フロントエンドはNext.js+React+Tauri webviewで、Rustが効いているのは限定的なホットパスだけと推察。「Rust=速い」のハロー効果に乗せた紹介が散見される。
  - **第三者レビューがバージョンを盛っている**: ReviewNexa等は「v2.0/2.1/2.2」と書くが、上流リポジトリは v0.3.x系。**SEO業界記事のSEO（自己言及SEO）でAI生成と思しき"水増し"レビューが流通している**疑いがあり、ツール選定時はGitHub releasesを直接見るのが鉄則。
  - **GEOの効果測定がまだ標準化されていない**: 「生成AIに引用された回数」を観測する手段が断片的（Perplexityの引用ログ、Bing Chatの参照リンク、ChatGPTのSearch機能等それぞれ異なる）。GEO機能を売りにするツールは**指標設計の薄さ**を見抜く必要がある。
- **中立的に見るときの補助線**:
  - **「Screaming Frog置き換え」ではなく「ログ解析エントリ＋GEO探索」用途で導入**するのが現実的。クロール本流はScreaming Frogか商用クラウド、ログ初手探索とAI citation仮説検証はRustySEOで、という棲み分け。
  - GPL-3.0なので**社内ツールフォーク改造はOKだが、顧客に納品する有料製品に組み込む場合はコピーレフト要件を社内法務とすり合わせる**。
  - 「**SEO代理店向け**」と謳うツールの**多くは結局フリーミアム・有料アップセル**で、純OSSで利益相反なく開発が継続するモデルは少ない。寄付/Sponsorsの動向もチェックすべき。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] RustySEOのログ解析機能は、巨大ログ（GB級）でもパースできるか／メモリ効率はどうか（実測ベンチが見当たらない）
- [ ] GEO機能の中身が「AIに見つけられやすいFAQ schemaの提案」程度なのか、Perplexity citation実測まで踏み込むのか（要触ってみる）
- [ ] Tauri製クロスプラットフォームアプリの、macOSコード署名警告・Windows SmartScreen警告の現実的な顧客説明コスト
- [ ] [[2026-04-26-open-seo-self-hosted-stack]] の every-app/open-seo（キーワード/競合）と RustySEO（テクニカル/ログ）を組み合わせた**自前SEOスタック**の構築コスト
- [ ] 国内代理店業務で**Screaming Frogから移行可能かのギャップ分析**（プラグイン・GA4連携・カスタム抽出ルール等）
- [ ] AI生成と思しき"水増しレビュー記事"を見抜くチェックリスト化（OSSバージョン番号と上流GitHub releasesの突き合わせは有力指標）

---

## 📚 参考資料

- [GitHub: mascanho/RustySEO](https://github.com/mascanho/RustySEO) — 一次ソース（README・機能・ライセンス・★数）, 取得日 2026-05-01
- [GitHub Releases: mascanho/RustySEO](https://github.com/mascanho/RustySEO/releases) — 実バージョン（v0.3.8 / 2026-04）, 取得日 2026-05-01
- [GitHub: mascanho/rusty-seo](https://github.com/mascanho/rusty-seo) — 同作者の別プロジェクト（CLIクローラ）, 取得日 2026-05-01
- [ReviewNexa: RustySEO Review 2026](https://reviewnexa.com/rustyseo-review-the-free-open-source-seo-tool-that-rivals-premium-software-in-2026/) — 第三者レビュー（バージョン記述に注意）, 取得日 2026-05-01
- [WordStream: GEO vs SEO 2026](https://www.wordstream.com/blog/generative-engine-optimization) — GEO概念整理, 取得日 2026-05-01
- [Jasper Blog: GEO vs AEO vs SEO Guide 2026](https://www.jasper.ai/blog/geo-aeo) — GEO業界トレンド, 取得日 2026-05-01
- [AlternativeTo: OSS Screaming Frog Alternatives](https://alternativeto.net/software/screaming-frog-seo-spider/?license=opensource) — OSS代替候補一覧, 取得日 2026-05-01
- [Capterra: Screaming Frog SEO Spider 2026](https://www.capterra.com/p/185765/Screaming-Frog-SEO-Spider/) — 本家の現状価格・評価, 取得日 2026-05-01
- [Searchatlas: 29 Best Screaming Frog Alternatives 2026](https://searchatlas.com/blog/screaming-frog-alternatives/) — 業界比較, 取得日 2026-05-01
- [元ポスト: @Fluyeporlaweb on X](https://x.com/Fluyeporlaweb/status/2049845980024242424) — 出典ツイート, 取得日 2026-05-01

---

## 🗒 メモ

このClippingsは「**Rust×SEO×OSS×GEO**」という流行ワードを4つ重ねた典型的なX紹介ポストで、**実態に対して紹介テキストがやや盛り気味**なのは押さえておきたい（特に「Rustで構築」は実質Tauri＋一部Rust）。ただし、ログ解析×クロール×GEOの**OSS統合**としては現状ほぼ唯一の選択肢で、SEO代理店業務の周辺ツール選定としては触っておく価値は十分にある。

使い道:

1. **note記事化**: 「**Screaming Frog 代替を本気でOSSにできるか 2026版**——RustySEO・LibreCrawl・SiteOne Crawler・SEO Reporterを全部触ってみた」系の比較レビュー。検索流入が見込める領域
2. **X投稿ネタ**: 「**SEOツール紹介ポストの『vX.X』表記、上流GitHubと食い違ってない？AI生成水増しレビューの見抜き方**」というメタな啓発スレッド（2〜3ポスト）
3. **代理店向け業務提案**: クライアントのNginxアクセスログをローカルRustySEOで分析→クロールバジェット改善提案、というワークフロー検証。ローカル動作なのでログ持ち出し不要なのが営業面の強み
4. **本vault内連携**: [[2026-04-26-open-seo-self-hosted-stack]] と組み合わせて「**自前SEOスタック構築マップ 2026**」をDataview的に作っておくと将来役立つ
