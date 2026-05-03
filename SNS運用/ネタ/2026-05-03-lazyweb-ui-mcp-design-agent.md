---
created: 2026-05-03
tags: [調査, lazyweb, MCP, design-research, claude-code, UI, vibe-coding, mobbin]
source: "[[Clippings/Post by @ClaudeCode_love on X 1.md]]"
---

# Lazyweb — MCPでAIエージェントに257k+ UIスクリーンを参照させるデザインリサーチ基盤の実態

> **TL;DR**
> Lazyweb（lazyweb.com）は Ali Abouelatta が2026年3月に公開した、MCPサーバー経由でClaude Code・Codex・CursorなどのAIエージェントに25.7万件以上のリアルアプリUIスクリーンを参照させるデザインリサーチ基盤。実在するサービスで、MCP接続・無料アクセス（V1）は公式確認済み。ただし、元ポスト（@ClaudeCode_love）の「完全無料・OSS」という表現のうち **OSS（オープンソース）は確認できない**。無料で使えるが、コードは非公開の可能性が高い。「入れない理由がない」という断言も、OpenAI API keyの二重コスト・V2以降の有料化リスクを無視しており過言。

## 元テキスト（抜粋）

> 25.7万以上のアプリ/Webスクリーンを収録 / 6つのデザインリサーチスキル搭載 / MCPでClaude CodeやCodexと直接連携 / 完全無料／レート制限なし／サブスク不要 / AI nativeで設計されたリサーチ基盤……

出典: [[Clippings/Post by @ClaudeCode_love on X 1.md]] / [元ポスト](https://x.com/ClaudeCode_love/status/2050889362574094501)（@ClaudeCode_love, 2026-04-29）

---

## キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Lazyweb | Ali Abouelattaが作ったUIリサーチ×MCPツール | `lazyweb.com` `abouelatta lazyweb` |
| MCP（Model Context Protocol） | AIエージェントが外部サーバーのデータを取得するための標準規格 | `MCP specification anthropic 2024` |
| Streamable HTTP transport | MCPのHTTP経由の接続方式（WebSocket不要） | `MCP streamable HTTP transport` |
| Mobbin | デザインリサーチの老舗有料ライブラリ（$576/year〜） | `Mobbin pricing 2026` |
| Vibe coding | 仕様より感覚・直感で高速開発するスタイル | `vibe coding AI agent 2026` |
| Bearer token | APIアクセスに使う認証トークン。Lazywebは無課金で発行 | `bearer token no-billing MCP` |
| design research skills | MCPツールとして提供されるUI参照・検索・絞り込み機能群 | `Lazyweb MCP tools list` |

---

## 背景 / なぜ今これが話題なのか

「AIはコードは書けるけどデザインがダサい」という問題は2024〜2025年のvibe coding普及とともに顕在化してきた。Claude CodeやCursorが生成するUIがデフォルトの味気ない見た目になりがちなのは、LLMの学習データに「実在する洗練されたUIスクリーン」が十分に含まれていないためだ。

これに対する先行アプローチとして **Mobbin**（2018年〜）や **Refero** などのデザインリサーチライブラリが存在するが、いずれも人間が見るための有料SaaSで、AIエージェントからの直接参照を想定していなかった。

転機は2024年末〜2025年にかけての **MCP（Model Context Protocol）の普及**。MCPによって「外部データベースをAIエージェントのコンテキストとして直接注入する」仕組みが標準化されたことで、「UIライブラリをMCPサーバーとして公開する」というアーキテクチャが自然に成立するようになった。

2026年3月に公開された **Lazyweb** はまさにこの文脈を捉えた。作者のAli AbouelattaはDuolingoを離れ、"7年分のアイデアのうちやっとひとつが刺さった"（First 1000 Substack）と書いている。日本語圏では2026年4-5月にかけてXで拡散が始まっており、今回のポストもその波乗り。

---

## 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 25.7万以上のUIスクリーン | 公式サイト「257k+ real app screens」と一致 | [lazyweb.com](https://www.lazyweb.com/) | ✅ 一致 |
| MCPでClaude Code/Codexと直接連携 | 公式サイトで確認。サーバーURL `https://www.lazyweb.com/mcp`、Streamable HTTP transport | [lazyweb.com](https://www.lazyweb.com/) | ✅ 一致 |
| 完全無料・レート制限なし | 「Lazyweb is free for humans and agents. No product rate limits for V1」と明記 | [lazyweb.com](https://www.lazyweb.com/) | ✅ 一致（V1限定の注記あり） |
| 6つのデザインリサーチスキル搭載 | 公式は「MCP tools: design research / screenshot search / company context / filters / image-backed examples」と5〜6種列挙しているが「6つ」という数字は明記なし | [lazyweb.com](https://www.lazyweb.com/) | ⚠️ ほぼ一致（数え方次第） |
| OSS（オープンソース） | 公式サイト・GitHub・作者記事のいずれにもOSS記述なし。GitHubのlazywebオーガニゼーションは別人の古いFork群のみ | 複数検索 | ❌ 要注意（無料≠OSS。コードは非公開の可能性大） |
| サブスク不要 | V1時点では不要と確認 | [lazyweb.com](https://www.lazyweb.com/) | ✅ 一致（V1時点） |
| Webアプリ対応も今後予定 | 公式は「257k+ app screens」と書いており、Webスクリーンも含む旨のデータあり。「今後予定」が何を指すか不明確 | [First 1000](https://read.first1000.co/p/lazyweb-is-live-finally) | 🔍 未確認（定義が曖昧） |

---

## 最新動向（2026-05-03時点）

- Lazyweb V1は2026年3月公開。作者Ali AbouelattaはDuolingo離職後に「7年で初めて刺さったアイデア」として立ち上げ — [First 1000](https://read.first1000.co/p/lazyweb-is-live-finally), 2026-03
- MCP設計研究ツールは急増中。Mobbin用の非公式MCPエージェント（ismailsaleekh/mobbin-agent）・Monet MCP・InspoAI等が並行して登場 — [PulseMCP](https://www.pulsemcp.com/servers/real-yash-mobbin-design), 2026-03
- 対比となるMobbin有料版はSMB $576/year、Enterprise $2,220/yearと高騰（前年比+91%/+285%）。フリーツールへの需要が高まる背景 — [Spendhound](https://www.spendhound.com/marketplace/mobbin-pricing), 2026-05
- Figmaも「Claude Code → Figma」のコード→デザイン逆変換を公式機能として2026年に統合 — [Figma Blog](https://www.figma.com/blog/introducing-claude-code-to-figma/), 2026
- Ali Abouelattaは「2022年に1週間かかった作業が数時間に」というAI高速開発体験を記事化しており、Lazywebそのものの開発にもAIを活用 — [First 1000](https://read.first1000.co/p/making-ai-great-at-frontend), 2026-03

---

## 関連概念・隣接分野

- **Mobbin / Refero / InspoAI**: 先行するUIリサーチライブラリ。いずれも有料モデル。LazywebはAIエージェントファーストで設計した点で差別化。
- **MCP（Model Context Protocol）**: Anthropicが提唱したAIエージェント-外部サーバー間の標準規格。2024年末公開、2025〜2026年で爆発的に普及。Lazywebがこれに乗れたタイミングが重要。
- **vibe coding**: 仕様書なし・感覚ドリブンで高速開発するスタイル。「コードは書けるがデザインがダサい」という問題が顕在化する文脈そのもの。
- **Context grounding（コンテキスト接地）**: LLMが「実在するデータ」に根ざした出力をするための手法。Lazywebは257k+のリアルスクリーンでエージェントを接地させる。
- **Figma MCP / shadcn/ui MCP**: 同じ「デザインデータをエージェントに渡す」アーキテクチャの別実装。LazywebはスクリーンショットDB、こちらはコンポーネント定義という違い。

---

## 反対意見 / 別角度からの視点

**肯定側の主張**（元ポストの立場）:
「AIの弱点だったデザイン問題が根本解決される。257k+のリアル画面を参照するから、エージェントの出力がプロ品質になる。無料で入れない理由がない。」

**否定 / 慎重派の主張**:
- 「OSS」は誤り可能性大。今は無料でも、V2以降に有料化するリスクは十分ある（Mobbin自身も急騰した）
- MCPで画像を大量に参照する = **コンテキストウィンドウの消費が増大**。Claudeのトークンコストが上がる可能性
- Claude Code内でCodexも使っている場合、LazywebへのOpenAI API key + Lazyweb MCPのトークンで **コスト二重化**の懸念
- 「スクリーンショットを参照させる → UIが良くなる」という因果は自明ではない。LLMがスクリーン画像を適切に解析・適用できるかは別の問題

**中立的に見るときの補助線**:
競合Mobbinの公式MCP実装がないため、現時点でAIエージェントネイティブなUIリサーチツールとしてはLazywebの先行優位は実在する。ただし「入れない理由がない」は言い過ぎ。**クリティカルなデザイン品質が必要なプロジェクト向けに試す価値はあるが、個人ツール・vault管理には過剰かもしれない**という評価が妥当。

---

## まだ残る疑問 / 次に調べると面白いこと

- [ ] V2以降の価格設定はどうなるか（作者のSubstackを追う価値あり）
- [ ] MCPでスクリーン画像を参照した時の実際のトークン消費量は？（APIログで計測できるか）
- [ ] Mobbin公式がMCPサーバーを出す可能性（現在は非公式実装のみ。出たらLazywebの差別化が薄れる）
- [ ] `codex-plugin-cc` + Lazyweb MCPの組合せ：Claudeがコード書き → Codexがレビュー → Lazywebで見た目補強、の3段階ワークフローは実用になるか

---

## 参考資料

- [Lazyweb MCP — Design Context for AI Agents](https://www.lazyweb.com/) — 公式サイト、機能・MCP設定・スクリーン数確認, 取得日 2026-05-03
- [Lazyweb is live (finally) - Ali Abouelatta](https://read.first1000.co/p/lazyweb-is-live-finally) — 作者ブログ、背景・スクリーン数・コンセプト確認, 取得日 2026-05-03
- [Making AI great at frontend - Ali Abouelatta](https://read.first1000.co/p/making-ai-great-at-frontend) — 作者のAI開発手法記事, 取得日 2026-05-03
- [Mobbin Alternatives 2026 - Product Hunt](https://www.producthunt.com/products/mobbin/alternatives) — 競合比較, 取得日 2026-05-03
- [Mobbin Pricing 2026 - Spendhound](https://www.spendhound.com/marketplace/mobbin-pricing) — Mobbinの価格動向確認, 取得日 2026-05-03

---

## メモ

今回のセッションで調査した8本のClippingsの中では**最もファクトに近い投稿**。ツール自体は本物で、MCP接続・無料・257k+スクリーンはすべて公式確認済み。

ただし `@ClaudeCode_love` 流の「OSS」「入れない理由がない」という断言は過剰表現。**煽り度:低・誇大表現:中 / 本質的な価値:あり** という評価。

SNS転用の観点: "LazywebはMobbinの無料AI版……ただしOSSと言われてるが確認できない" という事実整理ポストは批評型コンテンツとして使える。W20バッファ的なネタとして `SNS運用/ネタ/` に転記してもよい。

Tsukapon vault との接点: `codex-plugin-cc` の導入評価（W20後半）と組合せて「Claude builds → Codex breaks → Lazyweb で見た目補強」の3段階ワークフローを試す価値は検討に値する（Obsidianのスキル開発には関係薄いが、クライアントの実装プロジェクトには使えるかも）。
