---
created: 2026-04-28
tags: [調査, claude-code, agent-skills, awesome-list, github]
source: "[[Clippings/Post by @chackwill on X.md]]"
---

# Claude Codeリポ「100選」を漁らずに集約リスト4本でカバーできるのか検証

> **TL;DR**
> @chackwill のポスト「集約リスト4本で9割カバー」はスター数の事実関係としてはほぼ正確（実測値と数日分の差で一致）。ただし内訳を見ると **純粋な curated awesome list は 2本だけ**（`hesreallyhim/awesome-claude-code` と `VoltAgent/awesome-agent-skills`）で、残り2本は性質が違う：`anthropics/skills` は公式サンプル集、`affaan-m/everything-claude-code` は自家製スキル統合パック。さらに **`sickn33/antigravity-awesome-skills`（★35,421／1,400+スキル）** が抜けており、Antigravity/Codex/Gemini など他ハーネスもカバーしたい人には必須の5本目。
> 実用上は「awesome-claude-code＋awesome-agent-skills＋antigravity-awesome-skills の3本＋anthropics/skills（教科書として）」の4本構成のほうが過不足が少ない。

## 📌 元テキスト（抜粋）

> "Claude Codeリポ100選を全部見ろ、95%の人より先行できる"系のポスト
> 実は、元から有名な集約リスト4本見れば9割カバーできるって調べてて気づいた😎
> 100個自分で漁る必要、たぶん無いです
> 公式・準公式の集約はもう存在してて：
> 🌟 anthropics/skills … ★124,056（公式）
> 🌟 affaan-m/everything-claude-code … ★167,261
> 🌟 hesreallyhim/awesome-claude-code … ★41,151
> 🌟 VoltAgent/awesome-agent-skills … ★18,877
> この4本ブクマしておけば事足りる気がする

出典: [[Clippings/Post by @chackwill on X.md]]（原ポスト: https://x.com/chackwill/status/2048971688365498547 ）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Agent Skills | Claudeが動的に読み込む「フォルダ単位の指示書」。`SKILL.md` ＋スクリプトで構成 | agentskills.io / SKILL.md spec |
| awesome-* リポジトリ | あるテーマのリンク集に特化したGitHubの定型 | sindresorhus/awesome |
| ハーネス（agent harness） | Claude Code / Codex / Cursor / Gemini CLI など、エージェントを動かす"枠" | Claude Code, Codex CLI, Cursor, Gemini CLI |
| MCP (Model Context Protocol) | エージェントに外部ツール接続させる標準プロトコル | github-mcp-server |
| プラグインマーケットプレイス | `/plugin marketplace add` でリポジトリをマーケットとして登録できるClaude Code機能 | `/plugin install` |
| サブエージェント | メインエージェントから呼び出される専門タスク用エージェント | claude-code-subagents |
| フック (Hook) | セッションイベント時に走る自動化スクリプト | SessionStart, Stop, ECC_HOOK_PROFILE |
| スラッシュコマンド | `/foo` で呼ぶ自作コマンド | `.claude/commands/` |

---

## 🧭 背景 / なぜ今これが話題なのか

2025年10月のClaude Code「Skills」一般公開と、続くプラグインマーケットプレイス機能の追加で、**「自分用の `.skill` / `.command` / `.agent` を共有する」というGitHub文化**が一気に立ち上がった。2026年1〜3月にはAffaan Mustafa の `everything-claude-code` が AnthropicのHackathon賞を受賞して話題になり（v1.10.0は2026年4月リリース、156 skills / 38 agents / 72 legacy commands）、curated listの数も爆発的に増えた。

この爆発を受けて出た反応が大きく2系統ある：

1. **「とにかく100リポ見ろ」系**（Twitter/X、Medium等）— 数で煽る記事・ポストが量産。読者は溺れる。
2. **「awesome-* 系3〜4本に集約されてるから安心せよ」系** — 今回の @chackwill ポストが代表例。

実際、GitHubで `awesome claude code` を検索すると `awesome-claude-code` `awesome-agent-skills` `awesome-claude-skills` `awesome-claude-code-toolkit` `awesome-claude-plugins` `awesome-claude-agents` …と類似名のリポジトリが乱立しており、**「リスト・オブ・リスト問題」が発生中**。

---

## 🔬 主張のファクトチェック

GitHub REST API で 2026-04-28 時点の値を実測。スター数は**ほぼ全て主張通り**で、ポスト後の数日分だけ増えている。

| 元テキストの主張 | 裏取り結果（2026-04-28実測） | ソース | 判定 |
|---|---|---|---|
| anthropics/skills ★124,056（公式） | ★124,968／Anthropic公式org／pushed 2026-04-23 | [GitHub API](https://api.github.com/repos/anthropics/skills) | ✅ ほぼ一致＋公式 |
| affaan-m/everything-claude-code ★167,261 | ★168,572／pushed 2026-04-26 | [GitHub API](https://api.github.com/repos/affaan-m/everything-claude-code) | ✅ ほぼ一致 |
| hesreallyhim/awesome-claude-code ★41,151 | ★41,583／pushed 2026-04-27 | [GitHub API](https://api.github.com/repos/hesreallyhim/awesome-claude-code) | ✅ ほぼ一致 |
| VoltAgent/awesome-agent-skills ★18,877 | ★19,147／pushed 2026-04-25 | [GitHub API](https://api.github.com/repos/VoltAgent/awesome-agent-skills) | ✅ ほぼ一致 |
| 「公式・準公式の集約」 | `anthropics/skills` は公式だが**curated awesome listではなくAnthropic自身のskillサンプル集**（document-skills, example-skills 等）。「集約」の語は誤解を招く | [README of anthropics/skills](https://github.com/anthropics/skills) | ⚠️ 文脈要注意 |
| 「この4本ブクマで9割カバー」 | 実測ではこの4本に **`sickn33/antigravity-awesome-skills`（★35,421／1,400+スキル）** が抜けている。Antigravity/Codex/Gemini等の他ハーネスも見るなら筆頭候補 | [GitHub API](https://api.github.com/repos/sickn33/antigravity-awesome-skills) | ❌ 重要な抜けあり |
| `everything-claude-code` を「集約リスト」と分類 | 実体は curated list ではなく**1人作者の統合スキル＆ガイド集**（v1.10.0 = 38 agents / 156 skills / 72 commands）。「集約」というよりは"全部入りパック" | [README of everything-claude-code](https://github.com/affaan-m/everything-claude-code) | ⚠️ ジャンル違い |

---

## 🌐 最新動向（2026-04-28時点）

- **`anthropics/skills` は v1系で `/plugin marketplace add anthropics/skills` 経由のインストールに対応**。`document-skills` / `example-skills` のプラグイン分割が進んでいる — [GitHub README](https://github.com/anthropics/skills), 2026-04
- **`everything-claude-code v1.10.0`** で Tkinterダッシュボード、operator系ワークフロー（brand-voice, social-graph-ranker, customer-billing-ops 等）、ECC 2.0 alpha（Rust製control-plane）が追加 — [README v1.10.0](https://github.com/affaan-m/everything-claude-code), 2026-04
- **`sickn33/antigravity-awesome-skills` は1,400+スキル収録**。Claude Code以外（Cursor / Codex CLI / Gemini CLI / Antigravity）にもインストールできるCLIがついており、マルチハーネス勢の事実上の標準に — [GitHub repo](https://github.com/sickn33/antigravity-awesome-skills), 2026-04
- **`VoltAgent/awesome-agent-skills` は1,000+スキル**を「公式開発チーム＋コミュニティ」両軸で集めるスタンス。Claude Code/Codex/Gemini CLI/Cursor互換を明記 — [GitHub repo](https://github.com/VoltAgent/awesome-agent-skills), 2026-04
- **新顔の伸び**: `awesome-claude-code-toolkit`（rohitg00、★1,460）が「135 agents + 35 skills + 42 commands + 150+ plugins + 19 hooks」で1パッケージ化を狙う。`ComposioHQ/awesome-claude-plugins`（★1,557）はプラグイン特化 — [KDnuggets記事](https://www.kdnuggets.com/10-github-repositories-to-master-claude-code), 2026-04
- **単体スキル＆設定**で人気が爆発: `forrestchang/andrej-karpathy-skills`（★94,700／Karpathy由来のCLAUDE.md）と `JuliusBrussee/caveman`（★48,344／"few token do trick"のトークン削減skill）。リストに含まれていない単発リポでも100kクラスが出ている — [GitHub Search API], 2026-04
- **「awesome-* of awesome-*」状態**で重複が増え、コミュニティでは「実際どれをブクマすべきか」議論が継続中 — [Medium記事](https://medium.com/all-about-claude/i-found-the-best-claude-skills-github-repos-heres-what-s-actually-worth-installing-in-2026-506aacd22ee5), 2026-03

---

## 🧩 関連概念・隣接分野

- **Agent Skills の仕様**: `agentskills.io` で標準化が進行中。`SKILL.md`＋frontmatter（`name`, `description`）が最小要件。ハーネス間の互換性はこの仕様の普及次第
- **プラグインマーケットプレイス**: Claude Codeの `/plugin marketplace add <repo>` でリポジトリをそのままマーケットとして登録できる仕組み。awesome-* に頼らず「気に入ったリポを直接マーケット化」できる
- **MCPサーバー**: スキルとは別レイヤー。skill = 指示書、MCP = 外部ツール接続。`github-mcp-server` のような一次ソース系MCPは awesome-claude-code とは別軸で押さえる必要あり
- **サブエージェント / オーケストレーション**: `vijaythecoder/awesome-claude-agents`（★4,211）や `VoltAgent/awesome-claude-code-subagents`（★18,584）が専門。skillとは粒度が違う
- **トークン最適化系の単体skill**: `caveman`（出力削減）や Karpathy CLAUDE.md系。curated listに載らない「one-skill repo」が独自に伸びる現象

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側（@chackwill ら）の主張**: 「100個漁る前に集約リスト数本ブクマしろ。重複だらけだから時間の無駄」
- **否定 / 慎重派の主張**:
  - awesome-* は**作者のキュレーション基準**でフィルタされている。例えば `hesreallyhim/awesome-claude-code` は "skills, hooks, slash-commands, agent orchestrators, applications, plugins" と幅広いが、**single-skill repoの拾い漏れ**がある（実際 Karpathy系・cavemanは未収録ケース多い）
  - **更新頻度の差**が大きい。awesome系は週単位で動くが、`anthropics/skills` のようなサンプル集は月単位の更新で「最新トレンド」を映さない
  - 4本ともスター数で並べているため、**ジャンル的な重複検知ができない**（curated list / 自家製パック / 公式サンプルが混在）
- **中立的に見るときの補助線**:
  - 目的別に分けて考える: ①「網羅的に新着スキルを追いたい」→ awesome-claude-code＋antigravity-awesome-skills、②「即インストールできる完成パック」→ everything-claude-code or awesome-claude-code-toolkit、③「Anthropic公式の作法を学ぶ教科書」→ anthropics/skills、④「Claude Code以外のハーネスも視野」→ awesome-agent-skills or antigravity-awesome-skills
  - スター数 ≠ 実用性。`caveman` のような「1機能で爆伸び」したskillはリストの俎上に乗っていなくても効く

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] `awesome-claude-code` と `awesome-agent-skills` と `antigravity-awesome-skills` の実エントリ重複率はどれくらいか（自動diffを取る）
- [ ] `everything-claude-code` の156 skillsと、上記awesome系の合計はどの程度被っているか（同名 vs 同機能）
- [ ] Antigravity / Codex / Gemini CLI など他ハーネスでの`SKILL.md`互換性の実態（同じ.skillが本当に動くか）
- [ ] Anthropic公式が今後 `anthropics/skills` を curated index 化する動きはあるか（marketplace側に寄せる流れ？）
- [ ] スター数が3桁なのに本質的に強いskill（lurking gem）の見つけ方 — awesome-* に依存しない発見ルート

---

## 📚 参考資料

- [anthropics/skills (GitHub)](https://github.com/anthropics/skills) — 公式skillサンプル集、★124,968 を実測, 取得日 2026-04-28
- [affaan-m/everything-claude-code (GitHub)](https://github.com/affaan-m/everything-claude-code) — v1.10.0の構成（38 agents / 156 skills / 72 commands）を確認, 取得日 2026-04-28
- [hesreallyhim/awesome-claude-code (GitHub)](https://github.com/hesreallyhim/awesome-claude-code) — ★41,583／pushed 2026-04-27, 取得日 2026-04-28
- [VoltAgent/awesome-agent-skills (GitHub)](https://github.com/VoltAgent/awesome-agent-skills) — ★19,147／1,000+スキル, 取得日 2026-04-28
- [sickn33/antigravity-awesome-skills (GitHub)](https://github.com/sickn33/antigravity-awesome-skills) — ★35,421／1,400+スキル／マルチハーネス対応, 取得日 2026-04-28
- [10 GitHub Repositories To Master Claude Code (KDnuggets)](https://www.kdnuggets.com/10-github-repositories-to-master-claude-code) — 2026年版の主要リポ概観, 取得日 2026-04-28
- [I Found the Best Claude Skills GitHub Repos (Medium / All About Claude)](https://medium.com/all-about-claude/i-found-the-best-claude-skills-github-repos-heres-what-s-actually-worth-installing-in-2026-506aacd22ee5) — 2026-03の選定基準議論, 取得日 2026-04-28
- [Top 50 Claude Skills and Github Repos 2026 (Blockchain Council)](https://www.blockchain-council.org/claude-ai/top-50-claude-skills-and-github-repos/) — リスト of リスト, 取得日 2026-04-28
- [GitHub Search API: awesome+claude+code](https://api.github.com/search/repositories?q=awesome+claude+code&sort=stars&order=desc) — リスト類のスター順実測, 取得日 2026-04-28

---

## 🗒 メモ

- このネタ、X用に**反証カウンターポスト**として使える: 「集約リスト4本で十分は半分本当・半分嘘。実は2本＋別ジャンル2本＋抜け1本（antigravity）」という構成にすると刺さりそう
- vault内の関連リソース: [[2026-04-24-claude-code-plugin-marketplace]] と組み合わせて「マーケットプレイス時代のskill探索戦略」note記事に発展できる
- スレッド化するなら:
  1. ポストの主張紹介
  2. 4本のスター数ファクトチェック（数字はほぼ正しい）
  3. でも内訳を見ると2本だけがawesome list、残りはサンプル集と統合パック
  4. 抜けてる5本目: antigravity-awesome-skills
  5. 目的別の最適4本を再提案（網羅／即パック／教科書／他ハーネス）
- 単発スター爆発系（caveman, karpathy系）の発見ルートはGitHub Trendingか「awesome-* に載らないgem」というpaper.li的サブチャンネルが必要かも → 別ノートで深掘り余地あり
