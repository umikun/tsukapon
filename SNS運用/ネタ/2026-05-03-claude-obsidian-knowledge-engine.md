---
created: 2026-05-03
tags: [調査, claude-code, obsidian, knowledge-management, second-brain, 批評型, vault運用]
source: "[[Clippings/Post by @this_is_tasnim on X.md]]"
---

# 「Notion AIを削除する claude-obsidian」の正体 — Karpathy LLM Wiki パターン実装と、Tsukapon運用との適合性

> **TL;DR**
> 元ポストが指している `claude-obsidian` は **AgriciDaniel/claude-obsidian** という Claude Code プラグイン（スキル）。Andrej Karpathy が提唱した "LLM Wiki" パターンの Obsidian 実装で、`/wiki` `/save` `/autoresearch` の3コマンドで「ソース取り込み → エンティティ/コンセプト抽出 → クロスリンク自動生成 → 矛盾検知」を回す。Smart Connections のような "ノートと会話する" 受動型ではなく **"ノートを書き換える能動型"** が差別化の本質。100% OSS は事実だが **Claude Code サブスク前提**（OSS ≠ 無料）。「Notion AI を削除」は煽り表現で、実態は Notion AI と完全に役割が違う（Notion AI=社内ドキュメント生成、claude-obsidian=個人/小規模調査ベース知識ベース構築）。Tsukapon vault には既に obsidian-skills 5本が入っているので、**機能的に重複する部分（vault整理）と棲み分けできる部分（自律調査・矛盾検知・Karpathy パターン）の切り分けが導入判断のキモ**。同種競合（llm-wiki / claude-knowledge-vault / obsidian-second-brain など）が複数あるので "選択肢の1つ" として冷静に評価するのが正解。

## 📌 元テキスト（抜粋）

> このせいで Notion AI を削除します。これを claude-obsidian と呼び、Obsidian を実行中のノートテイカーに変えてくれます。あなたが作業している間、ファイルの整理、相互参照の管理、そして自己維持を行います。
> 他のすべての Obsidian AI プラグインとの違いは、アーキテクチャにあります。Smart Connections はあなたのノートの上にチャットインターフェースを置くだけです。これは、ノートそのものを生成、整理、進化させる知識エンジンです。
> （…）100% オープンソース。

出典: [[Clippings/Post by @this_is_tasnim on X.md]] / [元ポスト](https://x.com/this_is_tasnim/status/2050605306766610810)（@this_is_tasnim, 2026-05-03）

> ⚠️ **作者は @this_is_tasnim ではない**: このプロジェクトの作者は **Daniel Agrici (AgriciDaniel)** で、@this_is_tasnim は紹介者。元ポストには明記がない（紹介者ポジションにありがちな「自分が作った風」のトーン）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| claude-obsidian | AgriciDaniel 作の Claude Code プラグイン。/wiki /save /autoresearch | github agricidaniel claude-obsidian |
| LLM Wiki パターン | Andrej Karpathy が提唱したLLMで知識ベースを構築・維持する設計パターン | karpathy llm wiki pattern |
| Smart Connections | brianpetro 作の老舗 Obsidian AI プラグイン。RAG/意味検索 | obsidian smart connections |
| Obsidian Copilot | RAG ベースで vault 全体に質問できる Obsidian プラグイン | obsidian copilot plugin |
| Obsidian Bases | Obsidian v1.9.10（2025-08）から正式提供のDB的ビュー機能 | obsidian bases |
| エンティティ/コンセプト/ソース | Karpathy パターンで取り込みデータを分類する3カテゴリ | karpathy wiki entities concepts sources |
| Claude Code スキル | `.claude/skills/` 配下に置く拡張定義 | claude code skills |
| MCP (Model Context Protocol) | LLMにツール・データソースを統合する標準仕様 | model context protocol |
| Karpathy LLM Wiki | OpenAI 元創業メンバーの Andrej Karpathy が2024年提唱した個人知識ベースパターン | karpathy compounding knowledge |

---

## 🧭 背景 / なぜ今これが話題なのか

**2024年: Karpathy が "LLM Wiki" パターンを発信**
Andrej Karpathy（OpenAI 共同創業 → Tesla AI ヘッド → Eureka Labs 創業）が、個人の調査・読書を「LLMに維持させる wiki」として積み上げる発想を発信。**ソース取り込み → エンティティ/コンセプト抽出 → クロスリファレンス → 矛盾検知** のループ設計が話題化。

**2025〜2026年: Obsidian + Claude Code の組み合わせが定番化**
2025年8月の Obsidian v1.9.10 で Bases（DB的ビュー）が正式提供。2026年2月時点で Obsidian は **150万ユーザー突破・YoY 22%成長**、ローカルファースト×Markdown×プラグイン拡張性で「AI second brain の基盤」として支持を獲得（[NxCode: Obsidian AI Second Brain Guide 2026](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026)）。Claude Code が CLI から vault を直接操作できる文脈で、"AI が vault を書き換える" 系のプロジェクトが2026年Q1〜Q2に爆発的に増加。

**2026年Q1〜Q2: Karpathy パターン実装の競合乱立**
`AgriciDaniel/claude-obsidian` 以外に、**ekadetov/llm-wiki**、**Psypeal/claude-knowledge-vault**、**rvk7895/llm-knowledge-bases**、**eugeniughelbur/obsidian-second-brain**、**dxxx/claude-obsidian-memory** など、同じ Karpathy パターン由来のプロジェクトが多数。差別化は「ソース取り込み元（Zotero/PubMed等）」「ビジュアル化（Bases/Canvas）」「自律性レベル」など。

**今回の元ポスト（2026-05-03 @this_is_tasnim）の文脈**
@this_is_tasnim はインフルエンサー的アカウントで、AgriciDaniel/claude-obsidian の紹介投稿を行っている。「Notion AI を削除」は典型的な **インフルエンサー煽りフレーズ**。一方で AgriciDaniel 自身の公式ブログ（[claude-obsidian: AI Second Brain](https://agricidaniel.com/blog/claude-obsidian-ai-second-brain)）も同様の論調で発信しており、**プロジェクト本体のポジショニングがそういうトーン**であることは事実。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「これを claude-obsidian と呼び」（自分が作った風） | 作者は **AgriciDaniel (Daniel Agrici)**。@this_is_tasnim はあくまで紹介者 | [GitHub: AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | ❌ 要注意（誤認誘発表現） |
| 「Notion AI を削除します」 | claude-obsidian と Notion AI は **役割が完全に違う**（前者は個人の調査ベースを Karpathy パターンで構築、後者は Notion ドキュメント上の生成・要約）。実用上の代替性は限定的 | （複合判断） | ⚠️ ほぼ一致（誇張。"削除する代替" は言い過ぎ） |
| 「Smart Connections はチャットインターフェースを置くだけ。これは知識エンジン」 | Smart Connections は意味検索 + RAG ベースのチャット。claude-obsidian はノート自体を生成・更新するため **アーキテクチャ的差異は事実**。ただし Smart Connections も "ノートに紐付くリンク提案" 機能を持っており「チャットを置くだけ」は過小評価 | [obsidian-smart-connections GitHub](https://github.com/brianpetro/obsidian-smart-connections) | ⚠️ ほぼ一致（差異は本物だが過小評価あり） |
| 「取り込むすべてをエンティティ・コンセプト・ソースに自動整理」 | これは **Karpathy LLM Wiki パターン** の本質仕様。実装も `wiki/` 配下を青=concepts / 緑=sources / 紫=entities で色分けするのが claude-obsidian の特徴 | [Stefano Salvucci: Claude Obsidian Knowledge Vault](https://www.stefanosalvucci.com/en/blog/github-claude-obsidian-knowledge-companion) | ✅ 一致 |
| 「ボールト全体で矛盾をフラグ付け、コールアウトで指摘」 | claude-obsidian は **8カテゴリの lint**（orphans / dead links / gaps 含む）を持つ。"矛盾検知" は実装されているが、深い意味的矛盾検知ではなく **構造的整合性** が中心 | [agricidaniel.com](https://agricidaniel.com/blog/claude-obsidian-ai-second-brain) | ⚠️ ほぼ一致（"矛盾" の解像度に注意） |
| 「自律的な3ラウンドのウェブリサーチ」 | `/autoresearch` コマンドで多段リサーチを実行。3ラウンドの正確な仕様は README 参照必要 | [GitHub: AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | ⚠️ ほぼ一致（リサーチ深度はWebSearch結果の質に依存） |
| 「クエリは特定のWikiページを引用、曖昧な類似性マッチではない」 | これは Karpathy パターンの設計思想と一致。"ベクトル検索の "それっぽい" 結果" を排除し、明示的なエンティティ参照に倒している | [Karpathy パターンの解説（複数ソース）](https://github.com/ekadetov/llm-wiki) | ✅ 一致 |
| 「ネイティブの Obsidian Bases ダッシュボード + ビジュアルキャンバス」 | Obsidian Bases (v1.9.10+) を活用したダッシュボードと Canvas 連動は実装済みの主要機能 | [Stefano Salvucci](https://www.stefanosalvucci.com/en/blog/github-claude-obsidian-knowledge-companion) | ✅ 一致 |
| 「100% オープンソース」 | リポジトリ自体は OSS で正しい。**ただし Claude Code サブスク前提**（OSS = 無料運用、ではない） | [GitHub: AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | ⚠️ ほぼ一致（重要な前提条件が省略） |

---

## 🌐 最新動向（2026-05-03時点）

- **Karpathy LLM Wiki パターン由来の Claude Code プラグインが乱立**: AgriciDaniel/claude-obsidian / ekadetov/llm-wiki / Psypeal/claude-knowledge-vault / rvk7895/llm-knowledge-bases / dxxx/claude-obsidian-memory 等、同パターンの実装が多数並立 — [GitHub検索: Karpathy LLM Wiki](https://github.com/search?q=karpathy+llm+wiki), 2026
- **eugeniughelbur/obsidian-second-brain は別系統で人気**: 31コマンド・vault-first リサーチ・スケジュール agent 対応で、claude-obsidian と同じく Karpathy パターン後継だが "より能動的" な位置付け — [obsidian-second-brain GitHub](https://github.com/eugeniughelbur/obsidian-second-brain), 2026
- **Obsidian Bases が AI 連携の中核に**: 2025年8月にv1.9.10で正式提供開始の Bases が、Notion DB の代替として AI プラグインから参照される基盤に。Bases を活用するプラグインが2026年Q1〜Q2に増加 — [NxCode: Obsidian AI Second Brain Guide 2026](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026), 2026
- **Obsidian ユーザー数 150万人超え（2026年2月）・YoY 22%成長**: ローカルファースト×Markdown が AI 統合の理想基盤として支持拡大。Claude Code 連動の解説記事が量産化 — [NxCode: Guide 2026](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026), 2026-02
- **Smart Connections は依然 Obsidian No.1 AI プラグイン**: RAG ベースで vault 全体と会話、Claude/Gemini/GPT/ローカルモデル全部対応。"知識エンジン" 系は Smart Connections の代替ではなく **補完** として位置付けるべき — [Smart Connections GitHub](https://github.com/brianpetro/obsidian-smart-connections), 2026
- **コミュニティでは "claude-obsidian は Claude Code 課金前提" の指摘が増加**: 100% OSS と謳うが実運用には API/サブスク費用がかかる前提を明示してない投稿が多い、という冷静な批評がXとRedditで散見 — [XDA Developers: I put Claude Code inside Obsidian](https://www.xda-developers.com/claude-code-inside-obsidian-and-it-was-eye-opening/), 2026

---

## 🧩 関連概念・隣接分野

- **Andrej Karpathy LLM Wiki パターン**: 本プロジェクトの設計思想の源泉。エンティティ/コンセプト/ソースの3層分離 + クロスリファレンス自動生成 + 矛盾検知の組合せが特徴
- **Obsidian Bases**: Notion DB 的な機能を Obsidian 内で実現。claude-obsidian は Bases を主要 UI として使う
- **Obsidian Canvas + JSON Canvas**: ビジュアル知識マップ。claude-obsidian は Canvas をコンパニオンビューとして提供
- **MCP (Model Context Protocol)**: Claude Code から vault へのアクセスはMCP経由が主流。obsidian-cli 系MCPと組み合わせて使うのが典型
- **obsidian-skills (kepano公式)**: ユーザー Tsukapon vault に既に導入済み（`obsidian-markdown` `obsidian-bases` `defuddle` `json-canvas` `obsidian-cli` の5本）。**claude-obsidian と機能領域が一部重複**するため棲み分けが必要

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（=元ポストの立場）**:
  - "ノートを書き換える能動型" は確かに既存 Obsidian AI プラグインと差別化される
  - Karpathy パターンは個人知識ベース構築には理にかなった設計
  - 100% OSS でロックインなし

- **否定 / 慎重派の主張**:
  - **「Notion AI を削除」は誇張**: 役割が違うものを "代替" として煽る典型パターン。Notion AI が必要だった人の用途（チームでのドキュメント共有・ブロックレベル生成）はclaude-obsidianでは置き換わらない
  - **「100% OSS」の罠**: Claude Code サブスク前提＝API課金が積み上がる。本格運用すると月数十〜数百ドル規模になりうる。"OSS=無料" と誤読する人が多いポジショントーク
  - **同種競合が乱立中**: llm-wiki / claude-knowledge-vault / obsidian-second-brain など、同じ Karpathy パターン由来が複数並立。**今 claude-obsidian を選ぶ決定打が "trending" 以外にあるか** は要検討
  - **vault が AI に書き換えられるリスク**: 矛盾検知や lint で勝手にノートが整理されると、"自分の意図的なメモ構造" が壊される可能性あり。**vault のバージョン管理（git）が事実上必須**
  - **作者と紹介者の混同**: 元ポストは作者ではなく紹介者の発信。コミュニティに対してプロジェクトの帰属が曖昧化される副作用がある（OSS文化的にもよろしくない）
  - **Smart Connections への過小評価**: Smart Connections も2026年現在は単なる "チャット" ではなく、ノートグラフ可視化・関連リンク提案・100+モデル対応で進化中。"ただチャットを置くだけ" は事実誤認

- **中立的に見るときの補助線**:
  - **"既存 Obsidian AI プラグインの代替" ではなく "AI による vault 自動メンテ層" として捉える** のが正解。Smart Connections（検索＋会話）と claude-obsidian（自動構築＋整理）は併用も成立
  - **Karpathy パターン実装は5〜6本ある中の1つ** として比較検討すべき。trending = ベスト ではない
  - **本格導入前に小さい vault でPoC**：いきなりメインの vault に入れて vault 全体を AI に書き換えさせると事故る。サブvault で1週間試して挙動を見るのが安全

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] claude-obsidian と obsidian-second-brain (eugeniughelbur) と llm-wiki (ekadetov) の **実機能比較表** はどこかにあるか / 自分で作る価値はあるか
- [ ] Tsukapon vault の **現運用（obsidian-skills 5本 + 自作カスタムスキル群）と claude-obsidian の機能重複マップ**
- [ ] Karpathy LLM Wiki パターンの本家解説（Karpathy のツイートやブログ）の正確な引用元
- [ ] 100% OSS と謳われる類似プロジェクト群の **実運用 API 課金実績**（月平均トークン消費量）
- [ ] 2025年8月リリースの Obsidian Bases に対する claude-obsidian の依存度。Bases 仕様変更時の脆弱性
- [ ] vault 内ノートが AI に勝手に書き換えられた事故事例の有無（Reddit / GitHub Issues 確認価値あり）

---

## 📚 参考資料

- [GitHub: AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — 本体リポジトリ。Karpathy LLM Wiki パターン実装, 取得日 2026-05-03
- [Obsidian AI Second Brain: The Open-Source Plugin That Organizes Itself (作者ブログ)](https://agricidaniel.com/blog/claude-obsidian-ai-second-brain) — 作者 Daniel Agrici 自身による解説, 取得日 2026-05-03
- [Claude Obsidian Knowledge Vault on GitHub (Stefano Salvucci)](https://www.stefanosalvucci.com/en/blog/github-claude-obsidian-knowledge-companion) — 第三者による独立紹介, 取得日 2026-05-03
- [Obsidian AI Second Brain: Complete Guide 2026 (NxCode)](https://www.nxcode.io/resources/news/obsidian-ai-second-brain-complete-guide-2026) — Obsidian + AI second brain の市場概況, 取得日 2026-05-03
- [GitHub: brianpetro/obsidian-smart-connections](https://github.com/brianpetro/obsidian-smart-connections) — 比較対象。Obsidian No.1 AI プラグイン, 取得日 2026-05-03
- [GitHub: eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) — 同種競合。31コマンド・スケジュール agent 対応, 取得日 2026-05-03
- [GitHub: ekadetov/llm-wiki](https://github.com/ekadetov/llm-wiki) — 同パターンの別実装, 取得日 2026-05-03
- [GitHub: Psypeal/claude-knowledge-vault](https://github.com/Psypeal/claude-knowledge-vault) — Zotero/PubMed/arXiv 取り込みに特化, 取得日 2026-05-03
- [GitHub: rvk7895/llm-knowledge-bases](https://github.com/rvk7895/llm-knowledge-bases) — 同パターン別実装, 取得日 2026-05-03
- [GitHub: dxxx/claude-obsidian-memory](https://github.com/dxxx/claude-obsidian-memory) — claude-obsidian派生, 取得日 2026-05-03
- [I put Claude Code inside Obsidian, and it was awesome (XDA Developers)](https://www.xda-developers.com/claude-code-inside-obsidian-and-it-was-eye-opening/) — Claude Code × Obsidian の体験レポート, 取得日 2026-05-03
- [Agentic Note-Taking: Transforming My Obsidian Vault with Claude Code (Stefan Imhoff)](https://www.stefanimhoff.de/agentic-note-taking-obsidian-claude-code/) — 個人開発者の vault 自動化体験, 取得日 2026-05-03

---

## 🗒 メモ

- **Tsukapon vault との適合性検討（重要）**:
  - 既導入: obsidian-skills 5本（kepano公式）+ 自作カスタムスキル多数（[[Claudian-スキル一覧.md]]）
  - claude-obsidian の `/wiki` `/save` `/autoresearch` のうち、**`/autoresearch` は Tsukapon の `/deep-dive` スキルと完全重複**
  - **重複しない領域**: 8カテゴリ lint（orphans / dead links / gaps）と Karpathy 流のエンティティ/コンセプト/ソース3層分離は Tsukapon にはない
  - **本格導入の前に確認**: 現状の `_ memory/` 多階層メモリ・調査ノート群との衝突有無
  - **PoC方針**: メインvaultにいきなり入れず、サブvaultで1週間試行 → 重複機能の整理 → 8カテゴリ lint 等の固有機能だけ抽出して自作スキル化検討
- **W18戦略のネタ**:
  - 「100% OSS という煽りの裏 — Claude Code 課金前提の罠」 → 批評型ロング解説の素材
  - 「Karpathy LLM Wiki パターン実装6本比較」 → ニッチで濃い記事候補（連投シリーズ向き）
  - 「Notion AI を削除という煽りに乗る前にチェックすべき3点」 → 4/26リプ再現型のテンプレ
- **メンバーシップ素材**: [[SNS運用/note/_メンバーシップ準備ロードマップ.md]] のネタプール枠 "実装ツール紹介" に登録価値あり
  - 切り口候補: 「claude-obsidian を Tsukapon vault に試した1週間レポート（重複/補完/事故）」
  - 切り口候補: 「Karpathy LLM Wiki パターン実装6本ガチ比較 — 結論は1本ではない」
- **元ポストの帰属問題**: @this_is_tasnim が作者を明示せず紹介している件は、**OSS文化への配慮欠如** として批評型リプの題材にできる（人格攻撃せず、文化的観点から指摘するトーンがW18勝ち型）
- **Karpathy パターン本体の調査ノート**を別途立てる価値あり: 元理論を理解しないとどの実装も評価できない。基礎ノート1本作っておくと、6本の実装比較も書きやすい
