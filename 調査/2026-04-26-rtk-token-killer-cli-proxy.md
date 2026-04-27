---
created: 2026-04-26
tags: [調査, ClaudeCode, トークン削減, OSS, CLI]
source: https://x.com/nicos_ai/status/2048112597795308032
---

# RTK（Rust Token Killer）— Claude Codeとターミナルの間に挟む"出力圧縮プロキシ"を冷静に見る

> **TL;DR**
> RTK は Rust 製の単一バイナリで、AIコーディングエージェントが `gh pr diff` `curl` `cat` `grep` 系を呼ぶ前に**自動でラップして出力を 60〜90% 圧縮**する PreToolUseフック。Apache-2.0 OSS、`brew install rtk` で入る。Claude Code・Cursor・Codex・Gemini CLI・Copilot・Windsurf・Cline 等に対応し、**実測ベースでも平均80%超のトークン削減**が報告されている。「Claude Code が90%安くなる」は嘘ではないが、**コマンド種類によって効果はバラつく**（`grep` は39%、`read` は23% という現実値もある）。料金よりむしろ**コンテキスト枯渇を遅らせる効果**のほうが体感に効く可能性が高い。

## 📌 元テキスト（抜粋）

> このツールはClaude Codeを90%安くします。
> AIとターミナルの中間に位置し、コマンドの出力がコンテキストに到達する前に圧縮します。
> Claude Code、Cursor、Gemini、Codex、Copilotと互換性があります。
> 100%オープンソース。

出典: [[Clippings/Post by @nicos_ai on X.md]]
リダイレクト先: [rtk-ai/rtk on GitHub](https://github.com/rtk-ai/rtk)

> 添付スクリーンショット（`rtk gain` 出力）で読み取れた実数：
> - Total commands: **15,720**
> - Input tokens: 146.3M
> - **Tokens saved: 130.0M（88.9%）**
> - 内訳: `rtk gh pr diff` 72.0% / `rtk curl -s` 100% / `rtk read` 22.7% / `rtk grep` 39.1% / `rtk eslint` 94.6%

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| RTK | Rust Token Killer。CLI出力をAIに渡す前に圧縮するプロキシ | `rtk-ai/rtk` |
| PreToolUseフック | Claude Code等が "ツール実行前" に差し込める処理 | `Claude Code hooks` `PreToolUse` |
| トークン | LLMの料金・コンテキスト長の単位。1トークン≒英語0.75単語 | `LLM token` `context window` |
| プロキシ | 間に挟まって入出力を変換する仕組み | `CLI proxy` `wrapper command` |
| Headroom | RTKの**APIレイヤー版相棒**。セッション全体を圧縮 | `headroom claude code` |
| プレフィックスキャッシュ | 同一プロンプト前半をキャッシュして安くする仕組み | `Anthropic prompt caching` |
| Apache-2.0 | 商用利用OK・特許保護ありのOSSライセンス | `Apache 2.0 license` |
| Claude Code | Anthropic公式のCLIコーディングエージェント | `Claude Code` `claude.ai/code` |
| ccusage / claude-code-headroom | Claude Codeコスト可視化系の代表ツール | `ccusage npm` |

---

## 🧭 背景 / なぜ今これが話題なのか

### Claude Code が "コンテキスト料金課金"の代表格になった

2024〜25年にかけてClaude Code・Cursor・Codexが普及した結果、**「ファイル読む・diff取る・grep 走らせる」だけでコンテキストが何十万トークンも食う**問題が一般化した。Anthropicの料金体系は入力/出力トークンに比例するため、`gh pr diff` 1回で数千円飛ぶ事故報告が2025年後半から急増。

### 圧縮ミドルウェア層が "層" として確立

2026年に入って、**LLMとCLIの間に挟むトークン削減ミドルウェア**が一気にカテゴリ化した。代表が **RTK（コマンドレベル圧縮）** と **Headroom（セッションレベル圧縮）** で、両者は競合ではなく**スタックを組む補完関係**として認知されている。

### "Single Rust Binary, Zero Dependencies" が刺さる文脈

2026年OSS界のトレンドは `uv` `bun` `ruff` `biome` などに象徴される **「Rust/Goで書かれた単一バイナリ・依存ゼロ・即動く」** 系。RTKもこの系譜で、**`brew install rtk` で1秒、設定不要で透過的に動く**点が初動拡散の鍵。

### Hacker Newsで35.7k★、1ヶ月で爆発

GitHub上で 35,700 stars / 2,200 forks（2026-04-26時点）、最新リリース v0.37.2（2026-04-20）。Hacker News掲載後の数日で大量の実測ツイートが流れ、**「24.6M tokens saved (83.7%)」「7,081コマンドで83.6%削減」**といった数字が次々共有されている。今回の `@nicos_ai` ツイートもその波の1つ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Claude Codeを90%安くする」 | 公称60-90%削減。実測平均は80〜89%が多い。**ただしコマンド依存**で `grep` 39%、`read` 23%まで落ちることも | [GitHub README](https://github.com/rtk-ai/rtk), [Andrew Patterson実測](https://andrewpatterson.dev/posts/token-savings-rtk-headroom/) | ⚠️ ほぼ一致（90%は最良ケース） |
| 「AIとターミナルの中間に位置」 | 正確。**PreToolUseフック**でBashコマンドを傍受し `rtk` equivalent に書き換えてから実行 | [GitHub README](https://github.com/rtk-ai/rtk) | ✅ 一致 |
| 「コマンド出力がコンテキストに到達する前に圧縮」 | 正確。4つの戦略（フィルタリング・グルーピング・トランケーション・重複排除）で出力を圧縮してからAIに返す | [Ginbok技術解説](https://ginbok.com/blog/rtk-the-token-killer-that-sits-between-your-ai-and-the-terminal) | ✅ 一致 |
| 「Claude Code, Cursor, Gemini, Codex, Copilot 互換」 | 正確。さらに **Windsurf / Cline / Roo Code / Kilo Code / OpenCode / Google Antigravity** にも対応 | [GitHub README](https://github.com/rtk-ai/rtk) | ✅ 一致（むしろ広い） |
| 「100%オープンソース」 | リポジトリは公開、ライセンスは **Apache-2.0（README）/ MIT（バッジ）** で表記揺れあるが商用OK系 | [GitHub LICENSE](https://github.com/rtk-ai/rtk) | ⚠️ ほぼ一致（ライセンス表記要確認） |
| Single Rust binary | 正確。zero dependencies | [GitHub README](https://github.com/rtk-ai/rtk) | ✅ 一致 |
| ローカル実行・phone home無し | 「doesn't phone home or require any accounts」と公式記載 | [Hacker News thread](https://news.ycombinator.com/item?id=46974740) | ✅ 一致 |

---

## 🌐 最新動向（2026-04-26時点）

- **RTK v0.37.2 リリース**（2026-04-20）。バグ修正と対応CLIの追加が活発。週次〜隔週リリースペース — [GitHub Releases](https://github.com/rtk-ai/rtk), 2026-04
- **Headroom（APIレイヤープロキシ）との"二段圧縮"構成が定着**。実測で **RTK 13.3億トークン + Headroom 1.9億トークン = 計15.2億トークン削減 / 月（コスト換算 約$3,800削減）** の事例 — [Andrew's Blog](https://andrewpatterson.dev/posts/token-savings-rtk-headroom/), 2026-04
- **MCP化フォーク `alexiyous/rtk-mcp-server` が登場**。Claude Desktop からシェルツール出力を直接圧縮するMCPサーバー化。RTK本体に取り込まれる可能性も — [GitHub](https://github.com/alexiyous/rtk-mcp-server), 2026-04
- **YouTubeチュートリアル「Claude Code + RTK : Saves 90% Tokens」**が拡散中。日本語圏ではまだ少数派 — [YouTube](https://www.youtube.com/watch?v=CncyYt9ozAQ), 2026-04
- **OpenClaw（OSS版CursorクローンOSS）からも統合提案 Issue #37057** が立ち上がっており、エコシステムとして広がる兆し — [openclaw/openclaw#37057](https://github.com/openclaw/openclaw/issues/37057), 2026-04

---

## 🧩 関連概念・隣接分野

- **Headroom**: RTKの相棒。RTKが**コマンド出力レベル**で圧縮するのに対し、Headroomは**APIリクエスト全体**を圧縮＋プレフィックスキャッシング活用。**両刀使いで月$3,000超のコスト削減事例**あり
- **ccusage / claude-code-headroom**: Claude Codeの**コスト可視化**ツール。RTKを入れる前に「自分が月いくら払ってるか」を測る入口
- **Anthropic Prompt Caching**: 同一プロンプト前半の自動キャッシュ機能。**RTKの圧縮で内容がブレるとキャッシュヒット率が落ちる**懸念があるので、Headroom併用が推奨される理由でもある
- **MCP (Model Context Protocol)**: Claude等のAIエージェントが外部ツール/データソースを呼ぶ標準。RTKもMCPサーバー化フォークが登場済み — 関連: [[調査/2026-04-26-create-agent-tui-openrouter.md]] の文脈とつながる
- **claude-code-router**: 「タスクごとに最適モデルにルーティング」する別アプローチ。RTKが"出力削減"でコスト下げるのに対し、こっちは"安いモデルに振る"でコスト下げる — 役割が違うので**併用も可能**

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - 「設定不要で透過的、入れて損ない」「平均89%圧縮 = エージェントの集中力UP＋セッション寿命UP＋月数千ドル削減の三方良し」「Single Rust binary なので保守も軽い」
- **否定 / 慎重派の主張**:
  - **「90%」は cherry-picked**: 添付スクショ自体に `rtk grep 39.1%` `rtk read 22.7%` という低削減コマンドも写っており、**業務内容によってはトータル50%台**になる可能性
  - **設定落とし穴が複数**: PATH、permissions、PreToolUseフック配列の順序、subagent環境への伝播。**入れたつもりで効いてない事故**が報告されている
  - **データを"間引く"以上、AI判断ミスのリスクがゼロではない**: ノイズと判断して捨てた行に重要情報が紛れていたら、エージェントが誤った推論をする可能性。本番デバッグ作業では `rtk` 経由を切る判断が必要
  - **プロンプトキャッシュとの相性問題**: RTK出力が変動すると Anthropic の自動キャッシュが効かなくなり、**思ったほど料金が下がらない**ケースあり（Headroom併用で緩和できる）
  - **長期的には Anthropic 公式が同等機能を取り込む可能性**：Claude Code側にネイティブ実装されたら依存度を下げる方向の判断もある
- **中立的に見るときの補助線**:
  - **「とりあえず1週間入れて `rtk gain` で測る」が一番安全な評価方法**。実数字を見てから常用判断
  - **`grep` `read` 多用な業務（ログ解析・大規模リポ探索）では効果が薄い**ことを理解した上で、`gh pr diff` `curl` `lint` 多用な業務に最適と認識する

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] RTK が "間引いた" 行にバグの根本原因が含まれていた事例は出ているか
- [ ] Anthropic公式が Claude Code に同等の出力圧縮機能を組み込む可能性 / タイムライン
- [ ] **MCP版（alexiyous/rtk-mcp-server）と本家RTKの統合プラン**はあるか
- [ ] 日本語ログ（grep結果・スタックトレース）に対する圧縮率が英語と同等か
- [ ] **企業利用時のセキュリティ監査**：RTKの内部処理がどこまで監査ログを残すか / GDPR・SOC2文脈での評価

---

## 📚 参考資料

- [rtk-ai/rtk (GitHub)](https://github.com/rtk-ai/rtk) — 本家リポジトリ。READMEの公称数字と対応CLI一覧, 取得日 2026-04-26
- [rtk-ai 公式サイト](https://www.rtk-ai.app/) — 設計思想とインストール手順, 取得日 2026-04-26
- [Hacker News: Show HN: RTK](https://news.ycombinator.com/item?id=46974740) — コミュニティの実測報告と反応, 取得日 2026-04-26
- [Andrew Patterson - Token Compression for Claude Code with RTK + Headroom](https://andrewpatterson.dev/posts/token-savings-rtk-headroom/) — 1ヶ月実測ベースの $3,800 コスト削減事例と設定の落とし穴, 取得日 2026-04-26
- [Ginbok - RTK on Windows + Cursor 解説](https://ginbok.com/blog/rtk-the-token-killer-that-sits-between-your-ai-and-the-terminal) — 4つの圧縮戦略の詳細, 取得日 2026-04-26
- [MadPlay - I Only Compressed CLI Output, Yet Tokens Dropped by 80%?](https://madplay.github.io/en/post/rtk-reduce-ai-coding-agent-token-usage) — 圧縮メカニズムのレビュー, 取得日 2026-04-26
- [alexiyous/rtk-mcp-server](https://github.com/alexiyous/rtk-mcp-server) — Claude Desktop向けMCPサーバー化フォーク, 取得日 2026-04-26
- [DEV - RTK, Model Routing, and Community Tools That Actually Work With Claude Code](https://dev.to/harivenkatakrishnakotha/rtk-model-routing-and-the-community-tools-that-actually-work-with-claude-code-3pmh) — Claude Code エコシステムの中での位置づけ, 取得日 2026-04-26
- [@nicos_ai 元投稿](https://x.com/nicos_ai/status/2048112597795308032) — クリッピング: [[Clippings/Post by @nicos_ai on X.md]], 取得日 2026-04-26

---

## 🗒 メモ

- **個人運用のCost Savings観点**: Claude Codeを vault 内で日常使いしてる自分のユースケースだと、**Claude Code 経由で `gh pr diff` `curl` `grep` 系を回す頻度がそこまで高くない**かもしれない。導入前に `ccusage` みたいな計測ツールで「自分は本当に削減対象コマンドを多用してるか」を1週間測ってからの方が無難
- **note記事化の角度**: 「Claude Code が90%安くなる」よりも、**「Claude Codeの"コンテキスト枯渇"を遅らせる」**フックの方が記事として刺さりそう。料金は Pro plan を契約してると体感しにくいが、**「同じセッションで2倍長く作業できる」は誰にでも刺さる**。型③常識を覆す
- **X単発投稿の角度**: スクショの `rtk gain` 表が**画として強い**。引用RTで「90%の内訳：grepは39%、readは23%でしたよ」という**現実値の補足**を出すと、Erickの煽りツイートに対するクオリティ反応として伸びる可能性
- **既存vault内の文脈**: Claude Code関連の調査ノート [[調査/2026-04-24-claude-code-plugin-marketplace.md]] [[調査/2026-04-23-claude-obsidian-llm-wiki.md]] と並べて、「Claude Code 周辺ツールの俯瞰マップ」を作ると価値が出る
- **人格データ整合**: [[_ kiwami/my-clone/brain/プロフィール.md]] の「実績なし・駆け出し2ヶ月目」スタンスで書くなら、**「自分はまだ試してない、まずは `rtk gain` で1週間測って実績共有予定」** という宣言型の出し方がフィット。`rtk` 試行ログを SNS に積み上げると後で記事化素材になる
