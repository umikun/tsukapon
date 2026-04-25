---
created: 2026-04-24
tags: [調査, OpenChronicle, MCP, AIメモリ, macOS, Claude]
source: "[[Clippings/Post by @L_go_mrk on X.md]]"
---

# OpenChronicle──Mac作業文脈を"画面録画なし"で自動記憶するOSS。Claude Desktop×MCPで使える代わりにv0.1アルファ

> **TL;DR**
> OpenChronicle（Einsia/OpenChronicle、MIT）は、**OpenAI Codexの"Chronicle"（2026-04-20公開）に対する開かれたオルタナティブ**。Rewind/Screenpipe系と違い **画面スクショを撮らずAccessibility Tree(AX) イベントだけで作業文脈を抽出**する設計で、ローカル完結＋Markdown+SQLite保存。Claude DesktopとはMCP経由（`http://127.0.0.1:8742/mcp`）で接続できる。ただし **v0.1.0の早期アルファでmacOS 13+専用、`git clone` + `bash install.sh` が必要**で、「入れるだけ」とは言えない。機密業務で使う前に、アプリ除外設定の有無を自分で確認する必要がある。

## 📌 元テキスト（抜粋）

> このツール、入れるだけで「自分の作業内容をAIが自動で覚えてくれる」らしくて便利そう。
> ・「先週あの資料どこに保存したっけ？」「昨日のあの話なんだっけ？」にClaudeが答えられるようになる
> ・作業ログを自分で書かなくても、作業履歴が自動で構造化されて残っていく
> ・ClaudeがあなたのMac作業文脈を理解した上で回答するので「毎回背景説明する手間」が消える
> ・OpenAI・Anthropic・Ollamaなど好きなAIと組み合わせて使える
> ・全て自分のMacの中で完結するので、機密情報を扱う業務でも安心して使える
> ※macOSのみ対応、v0.1のアルファ版です。

出典: [[Clippings/Post by @L_go_mrk on X.md]] / [@L_go_mrk 2026-04-23](https://x.com/L_go_mrk/status/2047271011817836876) / [Einsia/OpenChronicle (GitHub)](https://github.com/Einsia/OpenChronicle)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| OpenChronicle | Macの作業文脈をLLMに渡すためのローカルOSS | `Einsia OpenChronicle MCP` |
| OpenAI Chronicle | OpenAIが2026-04-20に公開した、Codex用の画面キャプチャ型メモリ機能 | `OpenAI Codex Chronicle screen context` |
| MCP (Model Context Protocol) | Anthropicが策定した、LLMが外部ツール/データにアクセスする共通規格 | `Anthropic MCP Claude Desktop` |
| Accessibility Tree (AX) | macOSが各アプリに公開する"UI構造情報"。VoiceOver等が使う | `macOS accessibility API AX tree` |
| LiteLLM | OpenAI/Anthropic/Ollama等を統一APIで叩くPythonライブラリ | `LiteLLM proxy providers` |
| Screenpipe | Rewind後継のOSS。画面録画＋音声をローカル保存 | `screenpipe open source rewind alternative` |
| Rewind / Limitless | 元祖の"Mac全画面録画AI"。MetaがLimitlessを2025-12に買収、Mac版終了 | `Rewind Limitless Meta acquisition` |
| 憲法AI / Constitutional AI | Anthropic流の"AIが安全原則に沿って自己修正"する手法 | `Anthropic constitutional AI paper` |

---

## 🧭 背景 / なぜ今これが話題なのか

**2026年4月に入って、「Macの作業文脈をAIに食わせる」市場が一気に動いた**。順を追って整理する。

- **〜2025年**: Rewind AIが"Mac全画面を常時録画→後から検索"カテゴリを作った。2025年中にLimitlessへリブランド、**2025-12にMetaが買収してMac版アプリは終了**。ユーザーは行き場を失った。
- **2026-04-20**: OpenAIが「Chronicle」をCodex for Macに投入。**画面スクショを定期取得→クラウド送信して文脈化**する方式で、Sam Altman が "telepathy-like" とまで表現した。ただし **ChatGPT Pro限定、EU/UK/CH不可、暗号化なしのクラウド処理**という点で即座に批判が出ている。
- **2026-04-23**: X上で [@L_go_mrk](https://x.com/L_go_mrk/status/2047271011817836876) がOSSの「OpenChronicle」を紹介。**名前はOpenAI Chronicleへの当てつけ**に近く、READMEも "Open-source, local-first memory for any tool-capable LLM agent" と位置づけている。
- **並行して**: 既存のOSS [Screenpipe](https://screenpi.pe/) がRewind難民の受け皿として広がっている（MIT、$400一括、画面+音声キャプチャ）。

つまり、**OpenChronicleは「OpenAI Chronicleの反対側」**に立つ位置取りで、同じ"Mac作業文脈記憶"でも **スクショを撮らない／クラウドに送らない／MCPでClaudeにも渡せる** ことを売りにしている。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「入れるだけ」で使える | 実際は `git clone` → `bash install.sh`、Xcode Command Line Tools と macOS 13+ が前提。一般ユーザーにはハードル高め | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ⚠️ ほぼ一致（ただし"入れるだけ"は誇張） |
| Claudeが過去作業に答えられる | MCPエンドポイント `http://127.0.0.1:8742/mcp` を立て、Claude DesktopをMCPクライアントとして接続する設計。理屈としては成立 | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ✅ 一致（ただし手動設定が要る） |
| 作業ログを書かなくても自動で構造化 | `user-` / `project-` / `tool-` / `topic-` / `person-` / `org-` / `event-YYYY-MM-DD.md` などのMarkdownに分類保存されるのは事実 | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ✅ 一致 |
| OpenAI・Anthropic・Ollamaと組み合わせ可 | LiteLLM経由。Ollama / LM Studio / OpenAI / Anthropic / その他LiteLLM対応プロバイダ全般が使えるとREADMEに記載 | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ✅ 一致 |
| Mac内で完結、機密業務でも安心 | ローカル保管・クラウド送信なしは事実。ただし**どのLLMプロバイダを選ぶかで"安心"の意味が変わる**（OpenAI API指定ならクラウド送信される） | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ⚠️ 条件付き一致 |
| v0.1のアルファ版 | README冒頭に "Status: v0.1.0 · macOS only · early alpha" と明記、GitHub releasesは未作成 | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | ✅ 一致 |
| 画面録画やスクショなしで文脈取得 | AX Treeイベント（フォーカス要素・可視テキスト・URL等）から抽出。スクショ方式ではない──元ツイートには明言なしだが**設計上の最大の差別化ポイント** | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | 🔍 元ツイートは未言及／事実は確認済 |
| アプリ単位の除外設定 | READMEに明示なし。AXは全アプリに対して有効化される前提なので、**1Password等も覗かれうる可能性**。実装確認要 | [Einsia/OpenChronicle README](https://github.com/Einsia/OpenChronicle) | 🔍 未確認（要追加調査） |

---

## 🌐 最新動向（2026-04-24時点）

- **OpenAI「Chronicle」**がCodex for Macに正式投入。画面スクショ→クラウド処理でCodexに文脈を渡す方式。EU/UK/CHは対象外、暗号化なしで **プライバシー懸念が報道多数** — [Help Net Security](https://www.helpnetsecurity.com/2026/04/21/openai-chronicle-codex-screen-context-memories/), 2026-04
- **TheNextWeb が批判的記事**: "Cloud processing, no encryption" と明記、ChatGPT Proの月額前提で一般にはハードル高い — [The Next Web](https://thenextweb.com/news/openai-codex-chronicle-screen-context-mac), 2026-04
- **Altman が "telepathy-like" と表現**し、逆にUXと監視性の両義性で議論化 — [The Hans India](https://www.thehansindia.com/technology/tech-news/openai-adds-chronicle-memory-to-codex-altman-calls-it-telepathy-like-1067938), 2026-04
- **OpenChronicleがその対抗馬として登場**: MITライセンス・ローカル完結・MCP対応でClaude Desktopにも繋がる — [GitHub Einsia/OpenChronicle](https://github.com/Einsia/OpenChronicle), 2026-04
- **Rewind→Limitless→Meta買収→Mac版終了** の余波で、OSS系メモリ層（Screenpipe、OpenChronicle、[mcp-memory-service](https://github.com/doobidoo/mcp-memory-service)）が一気に注目される状況 — [Screenpipe Blog 2026](https://screenpi.pe/blog/best-rewind-ai-alternative-2026), 2026-04
- **AIメモリ×MCP**が1つのジャンルとして形成されつつある。[Plurality.network のまとめ](https://plurality.network/blogs/best-universal-ai-memory-extensions-2026/)でも2026年のキー領域として扱われている — 2026-04

---

## 🧩 関連概念・隣接分野

- **MCP (Model Context Protocol)**: OpenChronicleは「データ源」としてMCPを話す。Claude Desktop / Claude Code / 各種MCPクライアントに共通接続できるのは、この規格のおかげ。**[[Claudian-スキル一覧.md]]** でも日々MCPサーバを繋いでいる前提と整合する。
- **AX (Accessibility) API**: macOSが全アプリに公開するUIツリー。VoiceOverのためのものが、いまやAI文脈抽出の主戦場に。**スクショ方式より軽量・精度も高い**（テキストが構造化済みだから）。
- **LiteLLM**: 1本のAPIでOpenAI/Anthropic/Ollama/LM Studioに切り替えるためのラッパ。**"LLMプロバイダ中立"のプロジェクトはほぼこれを使う**。
- **ローカルLLM（Ollama / LM Studio）**: OpenChronicleの"機密情報でも安心"説を成立させるにはここが必須。クラウドAPI指定なら結局送信される。
- **Screenpipe**: 画面+音声をローカル保存する対抗OSS。**OpenChronicle（AXベース）vs Screenpipe（スクショ+音声）** は捕捉対象・容量・精度でトレードオフ関係。
- **[[調査/2026-04-23-claude-obsidian-llm-wiki.md]]**: claude-obsidianがObsidian vault内の"知識"を扱うのに対し、OpenChronicleは "Mac上の作業行動"を扱う。**組み合わせて使うと「思考(vault)＋行動(Mac)」の両輪メモリ**になる。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（元ツイート）**: ローカル完結＋MCPで好きなLLMに繋げる。機密業務でも安心。プロンプトで背景説明する手間が消える。
- **否定 / 慎重派の主張**:
  - **v0.1.0アルファ＋コミット15本程度** で、セキュリティ監査・エッジケース対応は未成熟。業務Mac（特に法人支給機）に入れるのは時期尚早。
  - **AXは全アプリの内容をデフォルトで拾う設計**。アプリ除外設定の実装状況がREADMEで不明で、**パスワードマネージャ・医療情報・クライアント契約書** まで索引化される可能性がある。
  - **"ローカル完結"はLLMプロバイダの選択次第**。OpenAI APIをLiteLLMで指定した瞬間にプロンプト内容（＝作業文脈）はOpenAIへ流れる。本当にローカル運用するにはOllama/LM Studioが前提。
  - **LLMの"記憶"そのものが幻覚を誘発**する可能性。過去ログから"それっぽく"答えさせると、事実と矛盾する出力を自信満々で出す事故が増える。
- **中立的に見るときの補助線**:
  - **目的が"個人の試験運用"か"業務常用"か** で評価が分かれる。試験運用なら今入れて損はない。業務常用ならv0.3くらいまで待って、**アプリ除外・暗号化・監査ログ** の実装を確認する方が無難。
  - **OpenAI Chronicle / Screenpipe / OpenChronicle** の三極で捉え、"どこでスクショを撮るか／何をローカルにするか" の設計哲学を比較するのが一番分かりやすい。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] アプリ単位の **除外リスト** は実装されているか（`docs/config.md` を直接読む必要あり）
- [ ] AX イベントは **どの粒度** で保存されるか（キー入力単位？フォーカス変更単位？）
- [ ] **ファイル容量** はどれくらい増えるか（1日あたりMB？GB？）
- [ ] Claude Desktop 以外の **MCPクライアント**（Cursor / Zed / Claude Code / Continue.dev など）での動作報告はあるか
- [ ] Ollama ローカルLLMだけで運用したときの **検索精度・応答速度** の実測値
- [ ] 日本語アプリ（Notion Mac / Obsidian / Craft 等）の **AXテキスト抽出精度**
- [ ] [[調査/2026-04-23-claude-obsidian-llm-wiki.md]] との **組み合わせ運用**（行動ログ × 知識vault をClaudeに同時に渡す）が現実的か

---

## 📚 参考資料

- [Einsia/OpenChronicle (GitHub)](https://github.com/Einsia/OpenChronicle) — README本体・機能・MCPエンドポイント・AX採用の裏取り, 取得日 2026-04-24
- [Post by @L_go_mrk on X](https://x.com/L_go_mrk/status/2047271011817836876) — 元ツイート, 取得日 2026-04-24
- [9to5Mac: Codex Chronicle for Mac](https://9to5mac.com/2026/04/20/codex-for-mac-gains-chronicle-for-enhancing-context-using-recent-screen-content/) — OpenAI Chronicleの仕様確認, 取得日 2026-04-24
- [Help Net Security: OpenAI Chronicle privacy concerns](https://www.helpnetsecurity.com/2026/04/21/openai-chronicle-codex-screen-context-memories/) — OpenAI側のプライバシー批判論点, 取得日 2026-04-24
- [The Next Web: OpenAI Chronicle cloud processing](https://thenextweb.com/news/openai-codex-chronicle-screen-context-mac) — クラウド送信・暗号化なしの報道, 取得日 2026-04-24
- [Kingy AI: Inside OpenAI's Chronicle](https://kingy.ai/ai/codex-gets-a-memory-inside-openais-chronicle-the-screen-watching-agent-trying-to-end-context-resetting/) — 設計思想の解説, 取得日 2026-04-24
- [Screenpipe Blog: Best Rewind Alternative 2026](https://screenpi.pe/blog/best-rewind-ai-alternative-2026) — Rewind→Limitless→Meta買収の経緯, 取得日 2026-04-24
- [Screenpipe (公式)](https://screenpi.pe/) — 対抗OSSの機能・価格比較, 取得日 2026-04-24
- [OpenTools: OpenAI Codex Chronicle](https://opentools.ai/news/openai-codex-chronicle-watches-your-screen-to-build-ai-context) — 補強, 取得日 2026-04-24
- [Plurality: Best AI Memory Extensions of 2026](https://plurality.network/blogs/best-universal-ai-memory-extensions-2026/) — ジャンル全体の俯瞰, 取得日 2026-04-24

---

## 🗒 メモ

- **使い道**: 明日以降の [[SNS運用/note/]] の素材として強い。**「OpenAI Chronicle vs OSSのOpenChronicle」**というシンプルな対比軸は、X投稿／引用RT向きのフックになる（関係性KWは「会社の機密」）。
- **刺さりそうな切り口**: 「**画面録画しない派**」という新しいサブカテゴリが成立しうる。Screenpipe（撮る派）とOpenChronicle（撮らない派）の2軸で記事化すると、稟議通過しやすいOSS選び方ガイドになる。
- **Tsukapon vault との接続**: [[調査/2026-04-23-claude-obsidian-llm-wiki.md]] とセットで、**claude-obsidian（vault側）＋OpenChronicle（Mac作業側）＋MCP（接続層）＋Claude Desktop（UI）** の4層構成を描くと、"Claudianの次の進化系"の絵が描ける。
- **自分用の判断**: 業務Macで即導入はしない。**個人のサブMac or 仮想環境でv0.1を試し、v0.3くらいまで待ってから本番機に入れる** のが現実解。AXのアプリ除外が入るかを最初に確認すべき。
