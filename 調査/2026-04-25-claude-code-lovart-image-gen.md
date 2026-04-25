---
created: 2026-04-25
tags: [調査, ClaudeCode, Lovart, 画像生成, ChatGPTImages2.0, AIデザインエージェント]
source: "[[Clippings/Post by @kawai_design on X.md]]"
---

# Claude Code から Lovart 経由で画像生成する技：2026年4月時点でホントに動くのか

> **TL;DR**
> 「Claude Codeで画像生成は無理」は半分本当・半分ウソ。**Lovart Skill を `~/.claude/skills/` に入れてAPIキーを環境変数で渡せば、Claude Codeから `/lovart` 系の指示で画像が生成できる**。元ポストの「ChatGPT Images 2.0を指定すれば日本語も綺麗」は、2026/4/21にOpenAI公式発表されたモデル特性とも整合する。ただし「世界初のAIデザインエージェント」は基本Lovart側のセルフブランディングで、競合（Canva Magic Studio / Adobe Firefly Agent / Figma Make等）も増えている点は冷静に見たい。

## 📌 元テキスト（抜粋）

> Claude Codeで画像生成って できないよね...方法あるの？ と思っている方へ。 あります。 世界初のAIデザインエージェントと言われる「Lovart」をAPI経由で使うことで、Claude Codeから直接画像生成指示をすることが可能になります。"ChatGPT Images 2.0"を指定することで、日本語の描画も綺麗に生成できます。

出典: [[Clippings/Post by @kawai_design on X.md]] / [元ポスト](https://x.com/kawai_design/status/2047790182221676817)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code | AnthropicのターミナルAIエージェント。テキストとツール実行が主、生成画像は出力しない | Claude Code MCP Skill |
| Lovart | プロンプトから画像・動画・3D・ロゴ等を一括生成するAIデザインエージェント | Lovart AI Design Agent |
| AIデザインエージェント | 複数の生成モデル（Flux/Ideogram/Runway等）をオーケストレーションするレイヤー | AI Design Agent autonomy |
| ChatGPT Images 2.0 | 2026/4/21にOpenAIが正式発表した画像生成モデル。日本語等非ラテン文字に強い | gpt-image-2 OpenAI 日本語 |
| Claude Code Skill | `.claude/skills/` 配下に置いて拡張するスキル機構（コマンド + プロンプト + ツール） | Claude Code skill custom |
| Access Key / Secret Key | LovartのAPI認証ペア。`~/.zshrc` 等で環境変数化が推奨 | Lovart API key 環境変数 |
| Nano Banana 2 | Lovartが採用する最新画像モデルの呼称（Gemini系派生） | Lovart Nano Banana |

---

## 🧭 背景 / なぜ今これが話題なのか

**2024-2025: 「画像生成は別ツール」が常識**
ChatGPT・Midjourney・Stable Diffusionそれぞれの画面に行って指示する世界観。Claude Codeはコード生成・ファイル操作の文脈で広まり、画像はスコープ外とみなされてきた。

**2025年5月前後: Lovartが「世界初のAIデザインエージェント」を掲げて登場**
Product Huntや海外メディアで取り上げられ、「プロンプトから複数モデル（ChatGPT・Runway・Ideogram・Flux 等）を自動オーケストレーションして、ロゴ・バナー・動画・3Dまで一気通貫で出す」という打ち出し方が話題に（[Lovart公式](https://www.lovart.ai/)）。同社のキャッチが日本のメディアにそのまま輸入され、「世界初」の枕詞が普及した。

**2025年後半-2026年初頭: Claude Code Skill 機構の成熟**
Anthropicが Claude Code に Skill / MCP プラグイン機構を整備。`~/.claude/skills/` 配下に置くだけで自然言語コマンドから外部API呼び出しができるようになった。これに乗っかる形でLovart側が公式 [`lovartai/lovart-skill`](https://github.com/lovartai/lovart-skill)（記事中で言及）を提供。

**2026年4月21日: OpenAIが ChatGPT Images 2.0 を発表**
日本語など非ラテン文字の描画品質を大幅改善、Thinkingモード搭載、最大2K解像度、複数枚同時生成、Image Arenaで Text-to-Image / Single-Image Edit / Multi-Image Edit 全カテゴリ1位（[OpenAI公式](https://openai.com/index/introducing-chatgpt-images-2-0/) / [k-tai.watch.impress 2026-04](https://k-tai.watch.impress.co.jp/docs/news/2103621.html)）。API（`gpt-image-2`）は2026年5月予定。

**2026年4月24-25日: Kawai氏のnote記事 → Xポストで日本語界隈に拡散**
[KAWAI氏のnote 2026-04-24](https://note.com/kawaidesign/n/n7839f35455a4) で「Claude Code × Lovart 連携 → ChatGPT Images 2.0 で日本語もキレイ」というワークフローが公開され、それを縮約したのが今回の元ポスト。タイミング的に **OpenAI発表のわずか3日後**にLovart経由で取り回す手順を出した形。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Claude Codeで画像生成はできない」 | 単体ではテキスト出力が中心。画像生成にはMCP/SkillまたはAPI連携が必要。"画像を直接出力する"機能は持っていない、という意味では正しい | 一般的なClaude Code仕様 / [zenn taimo](https://zenn.dev/taimo/articles/5fe1fb0ef62bca) | ⚠️ ほぼ一致（厳密にはMCP経由なら可） |
| 「Lovartは世界初のAIデザインエージェント」 | Lovart自身が "World's First AI Design Agent" を公式に謳い、Product Hunt・各種レビューでもこの表現が踏襲されている。**自称起点だが業界呼称として定着済み** | [Lovart公式](https://www.lovart.ai/) / [Product Hunt](https://www.producthunt.com/products/lovart) / [Filmora 2026レビュー](https://filmora.wondershare.com/video-editor-review/lovart-ai-review.html) | ⚠️ 自称由来だが定着 |
| 「LovartをAPI経由でClaude Codeから直接画像生成可能」 | `git clone`/`npx skills add` で `~/.claude/skills/lovart` を導入、Access Key・Secret Keyを環境変数化、Claude Code内 `/lovart` で実行できる手順が複数記事で公開済み | [花果 note](https://note.com/mizuhiki_kaka/n/n48d164c6cc00) / [KAWAI note](https://note.com/kawaidesign/n/n7839f35455a4) | ✅ 一致 |
| 「ChatGPT Images 2.0を指定すれば日本語描画が綺麗」 | OpenAIは2026/4/21に「日本語・韓国語・中国語・ヒンディー・ベンガル語の描画を大幅強化」と公式アナウンス。Image Arenaで主要3カテゴリ1位 | [OpenAI公式 2026-04-21](https://openai.com/index/introducing-chatgpt-images-2-0/) / [Impress Watch 2026-04](https://www.watch.impress.co.jp/docs/news/2103570.html) | ✅ 一致 |
| 「Lovart内で "ChatGPT Images 2.0" をモデル指定できる」 | Lovartは公式に "all top AI models" を統合し、ChatGPT系・Runway・Ideogram・Fluxを切り替え可能とする。ChatGPT Images 2.0 名義での選択UIに関しての一次ソースは未確認 | [Lovart Nano Banana記事](https://www.lovart.ai/blog/lovart-nano-banana-2-ai-design-agent) | 🔍 部分的に未確認（モデル切替自体は確認済み・最新モデル名対応の明示は要追加調査） |

---

## 🌐 最新動向（2026-04時点）

- **ChatGPT Images 2.0 正式発表（API "gpt-image-2" は5月予定）** — 日本語含む非ラテン文字の描画が大幅改善、Thinkingモード搭載、Image Arena 3冠 — [OpenAI公式](https://openai.com/index/introducing-chatgpt-images-2-0/), 2026-04
- **Claude Code に公式 Lovart Skill (`lovartai/lovart-skill`) が登場** — `npx skills add lovartai/lovart-skill` 1発で導入、APIキーは環境変数管理が推奨 — [花果 note](https://note.com/mizuhiki_kaka/n/n48d164c6cc00), 2026-04
- **KAWAI氏が Claude Code × Lovart の日本語向けハンズオンnoteを公開** — 元ポストの引用元。`~/.zshrc`へのキー保存・SNS流出注意までケア — [KAWAI note](https://note.com/kawaidesign/n/n7839f35455a4), 2026-04-24
- **Lovart 自体が "Nano Banana 2" 等の最新モデルへ随時更新** — 単一ベンダーではなく、Flux/Ideogram/Runway/ChatGPT系を統合する"指揮者"型 — [Lovart Blog](https://www.lovart.ai/blog/lovart-nano-banana-2-ai-design-agent), 2026
- **国内制作会社の社内勉強会でも Claude Code + Chrome DevTools MCP + Lovart の3点セットが定番化** — Web制作 + ビジュアル生成のハイブリッドワークフローとして紹介 — [株式会社デザインファミリー](https://www.design-family.jp/dezifami/blog/ai-usecases-production-team/), 2026

---

## 🧩 関連概念・隣接分野

- **MCP (Model Context Protocol)**: Claude Codeから外部ツール（DB・API・ローカルファイル）を呼び出す共通プロトコル。Lovart Skill もこの思想の延長線上にある
- **Claude Code Skill**: コマンド + プロンプト + 必要ツールをパッケージ化して `~/.claude/skills/<name>/` に配置する仕組み。今回の `/lovart` もこれ
- **AIデザインエージェントの群雄割拠**: Canva Magic Studio、Adobe Firefly Agent、Figma Make、Galileo AIなどが類似機能を提供。Lovartの優位は「複数モデルの自動使い分け × チャットUI」
- **gpt-image-2 / Nano Banana 2 / Flux / Ideogram**: 個別の画像生成モデル。Lovartはこれらを内部で使い分けるオーケストレーター
- **環境変数によるAPIキー管理**: `~/.zshrc` や direnv、1Password CLI などでセッション履歴に鍵を残さない運用パターン

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（元ポスト寄り）**:
  - チャットUIの中で "画像も含めて完結" できるのは作業分断が減って明確に速い
  - Lovart 1ツールでロゴ・バナー・動画・3Dまで広範カバー
  - ChatGPT Images 2.0 採用で日本語ロゴ・看板・LP用画像の品質課題が一気に下がる
- **否定 / 慎重派の主張**:
  - 「世界初」は基本マーケコピー。Canva Magic Studio や Adobe Firefly Agent も2025-2026にエージェント化を進めており、機能差は縮みつつある（[Filmoraレビュー 2026](https://filmora.wondershare.com/video-editor-review/lovart-ai-review.html)）
  - **二重課金**：Lovart有料プラン + 内部で呼ぶ各モデル（ChatGPT/Runway等）のクレジット消費 → 単純な画像生成だけなら gpt-image-2 直叩きの方が安い
  - APIキーをClaude Codeのセッション履歴経由で漏らすリスク（[KAWAI note](https://note.com/kawaidesign/n/n7839f35455a4) も注意喚起）
  - Skill は野良配布も多く、`~/.claude/skills/` への導入は**実行コードの取り込み**でもあるのでサプライチェーン視点で要警戒
- **中立的に見るときの補助線**:
  - 「速さ重視で1ツールに寄せたい」なら Lovart × Claude Code が最短
  - 「コスト最適化したい」なら Claude Code に直接 `gpt-image-2` API を叩く軽量MCPを書く方が筋が良い
  - 「商用利用」なら各モデルのライセンス（特に画像著作権）を**Lovartではなく内部呼び出し先のモデル基準**で確認する必要

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Lovart の UI / API で "ChatGPT Images 2.0" を**明示的に指名できる**のか、それとも内部ルーティングだけか
- [ ] OpenAI公式 `gpt-image-2` API（2026年5月予定）が出たあとの**Lovart経由 vs 直叩き**のコスト比較
- [ ] Claude Code Skill のサプライチェーン管理（公式署名・サンドボックス化）の現状
- [ ] 競合（Canva Magic Studio Agent、Adobe Firefly Agent、Figma Make）と Lovart の機能差を実機検証
- [ ] 日本語ロゴ・看板系での「ChatGPT Images 2.0 vs Ideogram vs Flux」実測比較

---

## 📚 参考資料

- [OpenAI: Introducing ChatGPT Images 2.0](https://openai.com/index/introducing-chatgpt-images-2-0/) — 日本語含む非ラテン文字描画強化・Thinking・2K対応の一次情報, 取得日 2026-04-25
- [Impress Watch: "思考"する画像生成モデル「ChatGPT Images 2.0」](https://www.watch.impress.co.jp/docs/news/2103570.html) — 日本語メディアでの公式発表報道, 取得日 2026-04-25
- [k-tai Watch: OpenAI、次世代画像生成「ChatGPT Images 2.0」公開](https://k-tai.watch.impress.co.jp/docs/news/2103621.html) — 公開タイミングと日本語強化の裏取り, 取得日 2026-04-25
- [Lovart 公式トップ](https://www.lovart.ai/) — "World's First AI Design Agent" 自称・複数モデル統合の謳い文句, 取得日 2026-04-25
- [Lovart Blog: Nano Banana 2](https://www.lovart.ai/blog/lovart-nano-banana-2-ai-design-agent) — 採用モデルと位置付け, 取得日 2026-04-25
- [Product Hunt: Lovart](https://www.producthunt.com/products/lovart) — "World's First AI Design Agent" としてのローンチ実績, 取得日 2026-04-25
- [花果｜Claude Code×lovart連携 (note)](https://note.com/mizuhiki_kaka/n/n48d164c6cc00) — `npx skills add lovartai/lovart-skill` / Access Key + Secret Key / 環境変数の手順, 取得日 2026-04-25
- [KAWAI｜Claude CodeとLovartで画像生成 (note)](https://note.com/kawaidesign/n/n7839f35455a4) — 元ポストの引用元。`~/.zshrc` 保存と SNS 流出注意の言及, 取得日 2026-04-25
- [株式会社デザインファミリー: 制作課のAI活用事例](https://www.design-family.jp/dezifami/blog/ai-usecases-production-team/) — 国内制作現場での Claude Code + Lovart 採用事例, 取得日 2026-04-25
- [Filmora: Lovart AI Review 2026](https://filmora.wondershare.com/video-editor-review/lovart-ai-review.html) — 2026年時点での競合比較・評価, 取得日 2026-04-25
- [Qiita: GPT-Image-2入門 — 推論モード・2K解像度・マルチ生成](https://qiita.com/kai_kou/items/9d5085048be780b78d90) — gpt-image-2 直叩きでの実装観点, 取得日 2026-04-25

---

## 🗒 メモ

- このネタはまさに自分の vault の使い方と相性が良い：[[Claudian-スキル一覧.md]] の延長として「画像生成系スキル」枠を作ると即戦力
- note記事タイトル候補:「Claude Codeで画像生成は無理」は半分ウソ：Lovart Skillと ChatGPT Images 2.0 でつくる実用ワークフロー
- X短尺投稿候補: ①セットアップ3行（git clone / env / `/lovart`）/ ②Lovart vs gpt-image-2直叩きのコスト感 / ③APIキー流出を防ぐ `~/.zshrc` パターン
- セキュリティ観点：Skill導入はコード実行を伴うので、信頼できる配布元（公式GitHub Org）からのみ入れる方針を CLAUDE.md に追記しておくと安全
- 関連: [[_ kiwami/my-clone]] / Webデザイン業務との接続用に [[SNS運用/post/フォロワー改善.md]] でクリエイティブ活用例を補強
