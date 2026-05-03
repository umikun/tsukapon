---
created: 2026-04-29
tags: [調査, Claude Code, Codex, プロンプトエンジニアリング, 多言語LLM]
source: 直接貼付（X風の意見投稿）
---

# Claude Code / Codex には英語プロンプト一択？ — 「日本語は曖昧で性能が落ちる」論を2026年4月時点で検証する

> **🔗 関連コンテンツ**
> - 🧰 関連調査: [[2026-04-26-obsidian-claude-code-second-brain]]
> - 🧰 Claude Code関連: [[2026-04-28-claude-code-curated-lists-overlap]]
> - 🧠 vault運用ルール: [[CLAUDE.md]]

> **TL;DR**
> 「英語の方が性能が出る」は**半分本当・半分は誤解**。研究レベルでは英語プロンプトが平均的にやや高精度・低コストで、日本語は**トークン効率が悪く（同じ意味で1.5〜3倍のトークンを消費）、長文プロンプトでは品質が劣化しやすい**のは事実。一方、Claude / GPT-5 系の最新モデルでは日本語と英語の精度差は **数%レベル**まで縮小しており、「英語一択」は言いすぎ。実務的には **「設定ファイル・技術仕様は英語、対話と要件整理は日本語」** のハイブリッドが2026年現時点でのベストプラクティス。元投稿の「日本語は語順自由で曖昧」というのは事実だが、その曖昧さは**英語でも厳密に書かない限り再現される**ので、本質は言語の違いではなく**プロンプトの構造化能力**にある。

## 📌 元テキスト（抜粋）

> 自分Claude codeやCodexへの指示は全部英語で投げてるんですけど、同じ人います？
> 英語の方がかなり性能上がるように思う。
> 日本語は語順も自由で解釈も自由なので、導き出される結論も読む人の裁量で自由に変化出来る為、特に技術的な仕様などでは書いた本人すらも意味がわからないと言うことも珍しくないため、特にAIに指示を書く時は英語一択では？

出典: 直接入力（X風の意見投稿）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code | Anthropic製のCLIコーディングエージェント | `Claude Code best practices` |
| Codex (GPT-5 Codex) | OpenAIのコーディング特化モデル／CLI | `GPT-5 Codex prompting guide` |
| トークナイザー | 入力テキストを最小単位（トークン）に分割する仕組み | `tokenizer Japanese efficiency` |
| BPE / Byte Pair Encoding | 多くのLLMが採用するトークン化アルゴリズム | `BPE Japanese tokens` |
| クロスリンガル転移 | ある言語で得た能力を別言語にも転用すること | `cross-lingual transfer LLM` |
| English-centric reasoning | 内部表現が英語ベースに偏る現象 | `LLM English-centric reasoning` |
| 多言語ベンチマーク | 言語別にLLM性能を比較する試験（Swallow / JHumanEval等） | `Swallow LLM leaderboard` |
| プロンプトの構造化 | 役割／文脈／制約／出力形式を明示する書き方 | `structured prompt template` |
| 認識精度 | プロンプト解釈の正確度（Claude Codeで日本語92%／英語96%という指摘あり） | `Claude Code 日本語 精度` |
| 日本語語順の自由度 | SOV基本＋助詞依存で順序入れ替え可能 | `日本語 語順 曖昧性` |

---

## 🧭 背景 / なぜ今この議論が再燃しているのか

「LLMは英語で投げた方が賢い」という言説は、GPT-3時代（2020〜2021年）からエンジニア界隈に根強くある。理由は3層に分けられる。

1. **データ偏り**：2024年1月時点でWeb全体の英語コンテンツ比率は **50%超**、日本語は **約4%**（[LILT, 2024](https://lilt.com/blog/multilingual-llm-performance-gap-analysis)）。学習データの量がそのまま流暢さと知識量に効く。
2. **トークン化効率**：英語は「単語＝ほぼ1トークン」だが、日本語は **1文字あたり1〜3トークン** を消費するケースが多い。同じ「こんにちは、これは簡単な例です。」が**日本語15トークン／英語7トークン**程度（[株式会社AX, 2025](https://a-x.inc/blog/llm-token-count/)）。長いコンテキスト窓を浪費し、コストもかさむ。
3. **English-centric reasoning**：MultiChallengeベンチマークの研究では、**多言語LLMの失敗の70〜80%がトークナイザーの非効率さと内部推論が英語ベースに偏ることに起因**するとされる（[arxiv 2024](https://arxiv.org/html/2404.11553v1)）。

加えて、**コーディングエージェントの台頭（2024〜2026年）** で問題が再注目されている：
- Claude Code（2024年後半リリース）／GPT-5 Codex（2025年）は**長文の仕様書・差分・ログ・テスト出力**をやり取りするため、トークン効率が直接的に開発体験に効く。
- コードのキーワード（`function`, `interface`, `null` 等）は元々英語で、関連知識も英語ドキュメント中心に学習されている。**英語仕様書 → 英語コード**の流れがモデルの内部表現と素直に噛み合う。
- Anthropic公式の[Claude Code Best Practices](https://code.claude.com/docs/ja/best-practices) は2026年4月時点で「言語選択」については明示的に言及しておらず、コミュニティの経験則に委ねられている状態。

つまりこの議論は「**英語学習データの偏り＋トークン効率＋コーディング特有の英語親和性**」の3点が重なって起きており、元投稿の感覚は完全に的外れではない。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 英語プロンプトの方が性能が上がる | 平均的には正しいが**差は近年縮小**。Claude Code環境での実測では英語**約96%** vs 日本語**約92%**の認識精度差にとどまる | [とつブログ](https://www.m-totsu.com/910/), [zenn](https://zenn.dev/totsu_ai_lab/articles/claude-code-japanese) | ⚠️ ほぼ一致（差は4%前後） |
| 日本語は語順自由・解釈自由なので技術仕様に向かない | 言語学的に語順自由度は高い（SOV基本＋助詞で語順入替可）。ただし**英語でも要件定義の曖昧さが事故るのは同じ**で、言語よりも**構造化能力**が支配的 | [Stanford HAI policy paper](https://hai.stanford.edu/assets/files/hai-taf-pretoria-white-paper-mind-the-language-gap.pdf) | ⚠️ ほぼ一致（前段は事実、後段の「英語一択」は言い過ぎ） |
| AIへの指示は英語一択 | 公式・ベンチマーク双方で「英語一択」とまでは言われていない。Anthropic公式ベストプラクティスは言語選択に中立 | [Claude Code Docs](https://code.claude.com/docs/ja/best-practices) | ❌ 要注意（過剰な一般化） |
| 日本語はトークンを多く消費する | 正しい。英語比1.5〜3倍が一般的 | [Qiita: トークンから見る言語の不思議](https://qiita.com/dennis_wang/items/d132f5114df6e4a7fdc8) | ✅ 一致 |
| Claude Sonnet 4.5は日本語のトークン効率が悪い | 正しい。Legalscape実測で**1トークン≒1文字**と低効率（PLaMo 2.1 Primeが優位） | [Legalscape Tech Blog 2025-10](https://tech.legalscape.co.jp/entry/2025/10/28/150459) | ✅ 一致 |
| GPT-4系も非英語プロンプトで性能差が出る | 出るが軽微。**Hindi/中国語以外では平均的にロバスト**。CodeLLaMaのような小型モデルでは差が顕著 | [arxiv 2408.09701](https://arxiv.org/html/2408.09701v2) | ✅ 一致 |
| 日本語は書いた本人すら意味がわからなくなる | 個人の体感ベースで、研究レベルでの定量化はない。**プロンプトを構造化していない場合**に起こりやすいのは事実 | （根拠なし） | 🔍 未確認（経験則） |

---

## 🌐 最新動向（2026年4月時点）

- **「英語/日本語ハイブリッド運用」がエンジニアコミュニティで定着**：設定ファイル・コード規約・型定義は英語、要件整理・レビュー対話は日本語、という使い分けが推奨されている — [zenn: Claude Code 日本語で使うコツ](https://zenn.dev/totsu_ai_lab/articles/claude-code-japanese), 2026-XX
- **Claude Sonnet 4.5の日本語トークナイザーが「1文字≒1トークン」と低効率**：PLaMo 2.1 Primeなど国産モデルとの実コスト差が議論に — [Legalscape Tech Blog](https://tech.legalscape.co.jp/entry/2025/10/28/150459), 2025-10
- **多言語ポストトレーニング研究で「単一の非英語を加えると英語性能も改善する」結果**：英語独占主義への反論として注目 — [arxiv 2604.13286 "English is Not All You Need"](https://arxiv.org/html/2604.13286), 2026-XX
- **Swallow LLM Leaderboard v2が稼働中**：JHumanEval（コード生成）・M-IFEval-Ja（指示追従）など日本語コード生成の専用ベンチが整備されつつある — [Swallow Leaderboard](https://swallow-llm.github.io/leaderboard/about.en.html), 2025-XX
- **国産LLM（PLaMo, Rakuten AI, Swallow）が日本語タスクで一部Claude/GPTに肉薄**：日本語ネイティブ運用の選択肢が広がる — [Rakuten Open LLM ranks top in Japanese](https://rakuten.today/blog/rakutens-open-llm-tops-performance-charts-in-japanese.html), 2025-XX

---

## 🧩 関連概念・隣接分野

- **プロンプト構造化テンプレート（CRISPE / RTF / RACE）**: 「言語の問題」と思われがちな曖昧さの大半は、役割／文脈／制約／出力形式を明示するテンプレ運用で解消できる。
- **`CLAUDE.md` / `AGENTS.md`方式**: プロジェクトに常駐するルールブックで、英語と日本語のどちらで書いても効果が出る。当vaultの[[CLAUDE.md]]もこの形式。
- **Few-shot プロンプティング**: 入力例＋期待出力例をペアで2〜3個渡すと、言語に依存せず精度が劇的に上がる。日本語の曖昧さ問題を回避する最短ルート。
- **コードコメント言語ルール**: 多国籍チームでは「**識別子・コメント・コミットメッセージ＝英語**、議論・要件＝現地語」の分離が定石。AIエージェントへの投げ方も同じ思想で整理できる。
- **国産LLM（PLaMo, Rakuten AI 7B, Swallow）**: 日本語のトークナイザーが最初から最適化されており、同じ日本語入力でも消費トークンが半分以下になる。**コスト最適化目的**なら有力。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側（英語一択派）の主張**: 学習データ量・トークン効率・コード命名規則すべてが英語有利。仕様書を書く頭の体操が**そのまま英語ドキュメントを読むトレーニング**になり、副次的にエンジニアスキルも上がる。日本語のあいまいさで詰まった経験を持つ人が共感しやすい。
- **否定 / 慎重派の主張**:
  - 「英語で正確に書ける」のは**英語の構造化スキル**があるからで、日本語が苦手なわけではない。**自分の母語より雑な英語で書いて精度が落ちるリスク**が普通にある。
  - Claude Sonnet 4.5・GPT-5・Gemini 2.5 Pro クラスでは日本語精度差は数%レベル。**コードベースが日本語コメント中心**なら、日本語プロンプトの方が文脈マッチが良いケースもある。
  - 英語にすることで「**書いた本人も読み返せない**」事故が逆に増える（チームレビューで詰む）。
  - PLaMo等の国産LLM、もしくは大手モデルでも日本語トークナイザー改善が進んでおり、**コスト面の優位性も縮小傾向**。
- **中立的に見るときの補助線**:
  1. **「英語が得意か」より「構造化が得意か」を先に問う**。テンプレ（役割／文脈／制約／例／出力形式）を埋められるなら、言語はどちらでも8割の戦いが終わっている。
  2. **長文・複雑な仕様書 → 英語**、**短文・対話・要件すり合わせ → 日本語** のハイブリッドが2026年4月時点の合理解。
  3. **`CLAUDE.md` / `AGENTS.md` を英語で固定し、対話は日本語**——ロール定義は精度差が効きやすいので英語、日々のやり取りは思考速度が出る母語、という分業が現実的。
  4. 「自分が日本語で書いた指示が読み返せない」と感じるなら、それは**プロンプトを書く前段の整理力**の問題。先に箇条書きで構造化してから本文化する。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Claude Code / Codex で**同一仕様の英語プロンプト vs 日本語プロンプト**を投げて、生成コードの**コンパイル成功率／テストパス率／レビュー指摘数**を実測する個人ベンチ
- [ ] PLaMo / Rakuten AI 7B / Swallow をローカルで動かして、日本語トークン効率がどれだけ違うかをコスト試算（自vaultでの運用妥当性）
- [ ] `CLAUDE.md` を英語で書いた場合 vs 日本語で書いた場合で、**ルール遵守率**にどれくらい差が出るか（[[CLAUDE.md]] の絶対ルールの遵守度をログ化する仕組みがあると一発で測れる）
- [ ] 「英語プロンプト派」が実は**ChatGPT / Claudeの公式英語ドキュメントを読み込んだだけ**で、日本語ドキュメントが整備されたら同じ精度が出る可能性
- [ ] Few-shot 2〜3例 + 日本語プロンプト と zero-shot 英語プロンプト の比較（言語より構造化が支配的という仮説の検証）

---

## 📚 参考資料

- [LILT: Why LLM Performance Drops in Non-English Languages](https://lilt.com/blog/multilingual-llm-performance-gap-analysis) — 英語以外で精度が落ちる構造的理由, 取得日 2026-04-29
- [Stanford HAI: Mind the Language Gap](https://hai.stanford.edu/assets/files/hai-taf-pretoria-white-paper-mind-the-language-gap.pdf) — 低リソース言語のLLM課題マップ, 取得日 2026-04-29
- [arxiv 2404.11553: Quantifying Multilingual Performance of LLMs](https://arxiv.org/html/2404.11553v1) — 英語中心の推論バイアス定量化, 取得日 2026-04-29
- [arxiv 2408.09701: Multilingual Prompt-Based Code Generation](https://arxiv.org/html/2408.09701v2) — 多言語プロンプトでのコード生成精度比較, 取得日 2026-04-29
- [arxiv 2604.13286: English is Not All You Need](https://arxiv.org/html/2604.13286) — 多言語ポストトレーニングの効果検証, 取得日 2026-04-29
- [Swallow LLM Leaderboard](https://swallow-llm.github.io/leaderboard/about.en.html) — 英語/日本語ベンチマーク統合リーダーボード, 取得日 2026-04-29
- [zenn: Claude Code 日本語で使うコツ](https://zenn.dev/totsu_ai_lab/articles/claude-code-japanese) — 認識精度英96%／日92%の出典, 取得日 2026-04-29
- [とつブログ: Claude Code 日本語で使うコツと注意点](https://www.m-totsu.com/910/) — 英語/日本語ハイブリッド運用の実践論, 取得日 2026-04-29
- [Claude Code Best Practices（公式）](https://code.claude.com/docs/ja/best-practices) — Anthropic公式ガイド（言語中立）, 取得日 2026-04-29
- [Codex Prompting Guide（OpenAI公式）](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide) — Codexプロンプト設計ガイド, 取得日 2026-04-29
- [Legalscape Tech Blog: 日本語トークナイザー効率比較](https://tech.legalscape.co.jp/entry/2025/10/28/150459) — Sonnet 4.5の日本語効率の悪さの実測, 取得日 2026-04-29
- [Qiita: なぜ日本語はAIにとって"高価"なのか](https://qiita.com/dennis_wang/items/d132f5114df6e4a7fdc8) — トークン化の言語依存解説, 取得日 2026-04-29
- [株式会社AX: LLMトークン数カウント](https://a-x.inc/blog/llm-token-count/) — 日英トークン数の実例, 取得日 2026-04-29

---

## 🗒 メモ

- **コンテンツ化の角度（X / note）**:
  - 「英語一択 vs 日本語OK」を**二項対立にせず**、「**英語にしたら精度が上がった人と、構造化を覚えたら精度が上がった人を区別する**」という切り口が刺さりそう。
  - スレッド化なら5本構成案：
    1. 「英語の方がAI性能上がる」は半分本当
    2. データの偏り＋トークン効率の事実（数字）
    3. ただし最新モデルでは差は4%前後
    4. 本当の差は「言語」より「構造化能力」
    5. 結論：仕様＝英語、対話＝日本語のハイブリッドが今のところ最強
- **自vault運用への持ち込み**:
  - [[CLAUDE.md]] のルール記述部分は日本語のまま運用しているが、**役割定義・絶対ルール部分だけ英語化**してA/Bテストする価値がある（個人ベンチ案）
  - 国産LLM（PLaMo）でCLAUDE.mdを処理させる実験は、トークンコスト削減の選択肢として一度回しておきたい
- **キャッチー仮タイトル候補**:
  - 「『英語で投げた方が性能上がる』は半分しか合ってない」
  - 「Claude CodeとCodexに英語で指示すると賢くなる、の本当の理由」
  - 「日本語が雑なんじゃない、構造化できてないだけ」
