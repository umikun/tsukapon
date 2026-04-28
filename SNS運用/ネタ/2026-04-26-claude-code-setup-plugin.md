---
created: 2026-04-26
tags: [調査, ClaudeCode, Plugin, AgentSkills, MCP]
source: Clippings/Post by @hasantoxr on X.md
---

# Anthropic公式 `claude-code-setup` プラグインを冷静に評価する

> **TL;DR**
> @hasantoxr の「これなしでClaude Code使うな」ツイートはガチ煽りだけど、**プラグイン自体はAnthropic Verifiedで実在**（インストール数 89,470 / 2026-04-26時点）。コードベースをread-onlyでスキャンして **MCP / Skills / Hooks / Subagents / Slash commands の5カテゴリ**から「上位1-2個」を提案してくれる **セットアップ用メタプラグイン**。
> 「シニアエンジニアがレポをレビューするように」は誇張で、実態は **package.json + ディレクトリ構造から技術スタックを推定 → カタログから提案** するシンプルなレコメンダー。例: Reactプロジェクト→Playwright MCP / 認証コード検出→security-reviewer subagent。
> 既存の `.claude/` を整備済みなら導入価値は限定的だが、**新規プロジェクトの初期化や、自分が見落としてる候補を拾う用途**には素直に強い。`/plugin install claude-code-setup@claude-plugins-official` 1コマンドで入る。

## 📌 元テキスト（抜粋）

> このプラグインなしでClaude Codeを使うのをやめてください。
> Anthropicの公式プラグイン「claude-code-setup」というものがあります。
> あなたのプロジェクト全体をスキャンして、正確に何をアクティブにするべきかを教えてくれます。
> → どのフックを設定するか / どのスキルをインストールするか / あなたのスタックに合うどのMCPサーバーか / どのサブエージェントを起動するか / それぞれのステップバイステップ設定
> /plugin install claude-code-setup@claude-plugins-official

出典: [[Clippings/Post by @hasantoxr on X.md]]（投稿: 2026-04-25, [元ツイート](https://x.com/hasantoxr/status/2048004868292678143)）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Plugin (Claude Code) | `.claude-plugin/plugin.json` を持つパッケージ単位の拡張 | claude code plugin spec |
| Marketplace | プラグインのキュレーション集（公式/コミュニティ/パートナー） | claude-plugins-official |
| `/plugin install` | ターミナル内でmarketplaceから1コマンド導入するCLI | discover-plugins docs |
| MCP server | Model Context Protocol準拠の外部ツール連携サーバ | playwright-mcp, github-mcp |
| Skill (SKILL.md) | YAML+MD で書ける呼び出し可能な手順書 | agent skills |
| Subagent | 親エージェントから呼ぶ専門子エージェント | security-reviewer subagent |
| Hooks | PreToolUse/PostToolUse/Stop等のイベント差し替え機構 | claude code hooks |
| Slash command | `/cmd` 形式のskill呼び出しUI | .claude/commands/ |
| Anthropic Verified | Anthropic公式が品質確認したラベル | claude.com/plugins |
| Read-only scan | 書き込みなしでpackage.json等を読むだけ | safe-by-default tool |

---

## 🧭 背景 / なぜ今これが話題なのか

Claude Code は2025年中盤に **Plugin / Marketplace 機能**を解放してから、`.claude/` 配下に大量のskill・MCP・subagentを詰め込めるようになった。結果として2026年Q1には **「何を入れればいいか分からない」** 問題が発生 — このVaultでも別途調査済み（[[2026-04-26-claude-code-100-best-repos]] / [[2026-04-24-claude-code-plugin-marketplace]]）。

`claude-code-setup` はその「**選択肢過多をAnthropic公式が直接ナビする**」プラグイン。位置づけは**メタプラグイン**で、自分は何もしないが**「あなたのプロジェクトには何を入れるべきか」を提案する**。

公式marketplaceは **2026-04時点で4本**並んでいる：

- `anthropics/claude-plugins-official` ★17,905 — 公式中核
- `anthropics/knowledge-work-plugins` ★11,558 — Cowork（非エンジニア向け）寄り
- `anthropics/financial-services-plugins` ★7,773 — 金融特化
- `anthropics/claude-plugins-community` ★58 — community read-only mirror

`claude-code-setup` は claude-plugins-official 内のフラッグシップ的存在で、インストール数 **89,470**（[claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) 2026-04-26時点）。**Anthropic Verified** ラベル付きで、内部でやってることはとてもシンプル：

1. `package.json`、言語ファイル、ディレクトリ構造を **read-onlyで**スキャン
2. プロジェクトタイプ・スタックを推定（React / Python / Laravel など）
3. **MCP / Skills / Hooks / Subagents / Slash commands** の5カテゴリから **上位1-2個** を提案
4. ユーザが「もっと見たい」と言えば3-5個まで展開

つまり「シニアエンジニアがレビュー」というよりは **賢いレコメンダー** に近い。"なし" でもClaude Codeは動くので、ツイートの「使うのをやめてください」は明確に煽り文句。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Anthropicの公式プラグインである | `anthropics/claude-plugins-official` リポジトリ収録 + Anthropic Verified ラベル付き | [GitHub anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) | ✅ 一致 |
| プロジェクト全体をスキャンする | `package.json`・言語ファイル・ディレクトリ構造を **read-only** でスキャンと公式記載 | [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) | ✅ 一致（read-only限定） |
| フック/スキル/MCP/サブエージェントの5カテゴリで提案 | 公式説明: MCP servers / skills / hooks / subagents / slash commands の5カテゴリ | [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) | ✅ 一致 |
| `/plugin install claude-code-setup@claude-plugins-official` で導入 | 公式CLI構文と一致。marketplace は起動時に自動追加 | [Claude Code Docs: Discover plugins](https://code.claude.com/docs/en/discover-plugins) | ✅ 一致 |
| シニアエンジニアがレポをレビューするように監査 | 実態は **read-only のレコメンダー**。コード品質レビュー機能はない（似た用途は別途 `security-review`等のskill） | [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) | ⚠️ ほぼ一致（メタファー寄り） |
| 「これなしでClaude Codeを使うのをやめてください」 | 公式説明にそんな表現はない。**煽り** | — | ❌ 要注意（レトリック） |
| ステップバイステップ設定を提示 | デフォルトで「上位1-2個」、要望時に「3-5個」を出す。各項目に設定ガイド付き | [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup) | ✅ 一致 |

> 集計: ✅5 / ⚠️1 / ❌1。**ツール自体は本物**、**煽り文言は釣り**、というよくあるパターン。

---

## 🌐 最新動向（2026-04-26時点）

- **claude-plugins-official が★17,905** に到達、main ブランチ 303 commits。Anthropic直管理で活発 — [GitHub anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official), 2026-04
- **claude-code-setup インストール数 89,470** をclaude.com公式ページで表示中。Anthropic Verified ラベル — [claude.com/plugins/claude-code-setup](https://claude.com/plugins/claude-code-setup), 2026-04
- **knowledge-work-plugins**（★11,558）が Claude Cowork 向けの非エンジニア層プラグインを集約 — [GitHub anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins), 2026-04
- **financial-services-plugins**（★7,773）が金融業界向けカテゴリとして独立 — [GitHub anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins), 2026-04
- Marketplace全体のディレクトリ構造が固まり、**`/plugin install <name>@<marketplace>` 形式が標準**化。`claude-plugins-community` が読み取り専用ミラーとして稼働 — [GitHub anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community), 2026-04
- **コミュニティ製の "starter pack" リポ**も依然強い: `garrytan/gstack`（★83,674）、`centminmod/my-claude-code-setup`（★2,231）。手動セットアップ派の選択肢として並走 — [GitHub gstack](https://github.com/garrytan/gstack), 2026-04
- 第三者カタログサイト（claudemarketplaces.com / aitmpl.com / buildwithclaude.com）が乱立し、Web側からのプラグイン発見性が向上 — [Claude Code Marketplace](https://claudemarketplaces.com/), 2026-04

---

## 🧩 関連概念・隣接分野

- **Awesome系キュレーション**: `claude-code-setup` が "公式が選ぶ" 路線なら、`hesreallyhim/awesome-claude-code` ★41k 等は "コミュニティが並べる" 路線（[[2026-04-26-claude-code-100-best-repos]]）
- **Plugin Marketplace 全体構造**: 公式/コミュニティ/特化（金融など）の3層化。詳細は [[2026-04-24-claude-code-plugin-marketplace]]
- **MCP server 経済圏**: claude-code-setup の提案先の半分はMCP。Playwright/GitHub/Postgresなど自分のスタックに合うものを当てに行く設計
- **Subagent オーケストレーション**: security-reviewer / refactor / test-runner 等、専門子エージェントを並べる設計はrohitg00系列ツールキットでも標準化中
- **Vault側の `.claude/` 設計**: 自分のVaultでは `_ memory/` の3層メモリ + `.claude/commands/` のskill群 + CLAUDE.md（[[CLAUDE.md]]）で似たことを手動運用中

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側（@hasantoxr）**: 「公式が直接 "あなたに必要なもの" を提案してくれる以上、選ばない理由がない」
- **否定 / 慎重派**:
  - **既存セットアップ勢には無価値**: `.claude/` を自分で固めてる人にとっては、**提案が現状とぶつかる/上書き提案になりがち**。読まずに従うと運用ルールが崩れる
  - **公式バイアス**: claude-plugins-official 内からしか選ばないので、コミュニティ製の良スキル（VoltAgent 1000+ など）は提案候補に出ない
  - **"Verified" ≠ "あなたに最適"**: インストール数89kはあくまで導入実績。**自分のプロジェクトでハマるかは別問題**
  - **煽りメタファー**: 「シニアエンジニアがレビュー」は明確に誇張。実態はread-onlyレコメンダーなので過剰期待しない
- **中立的に見る補助線**: **新規プロジェクトの初期化** or **半年以上.claude/を見直してない** タイミングで、レコメンドだけ受け取って **採用判断は自分でする** のがちょうどいい付き合い方

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] claude-code-setup が**何件のMCP/skill/subagentをカタログとして持っている**のか（推定母集団のサイズ）
- [ ] 「上位1-2個」の選定アルゴリズム（人気度? 公式タグ?）— Anthropic側で重み付けを公開しているか
- [ ] **Obsidian Vault運用**（このプロジェクト）に当てた場合、何を提案してくるか実走してみる価値あり
- [ ] knowledge-work-plugins / financial-services-plugins と比較して、**業務領域別マーケットプレイスの分割戦略**が今後どう広がるか
- [ ] `claude-code-setup` の提案を採用した後の **6ヶ月後の継続率** （導入と定着は別問題）

---

## 📚 参考資料

- [Claude Code Setup – Anthropic公式ページ](https://claude.com/plugins/claude-code-setup) — 機能・スキャン対象・導入数89,470, 取得日 2026-04-26
- [GitHub anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official) — 公式marketplace本体 ★17,905, 取得日 2026-04-26
- [Claude Code Docs: Discover plugins](https://code.claude.com/docs/en/discover-plugins) — `/plugin install` 構文と marketplace 自動追加, 取得日 2026-04-26
- [GitHub anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community) — community marketplace（read-only mirror）, 取得日 2026-04-26
- [GitHub anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) — Cowork向け公式marketplace ★11,558, 取得日 2026-04-26
- [GitHub anthropics/financial-services-plugins](https://github.com/anthropics/financial-services-plugins) — 金融特化公式marketplace ★7,773, 取得日 2026-04-26
- [Build with Claude (3rd-party catalog)](https://buildwithclaude.com/) — Web側プラグイン検索, 取得日 2026-04-26
- [Claude Code Marketplace catalog](https://claudemarketplaces.com/) — 別系列の3rd partyカタログ, 取得日 2026-04-26
- [元ツイート @hasantoxr](https://x.com/hasantoxr/status/2048004868292678143) — 出典, 取得日 2026-04-26

---

## 🗒 メモ

- **note記事ネタ案**: 「Anthropic公式の`claude-code-setup`に自分のObsidian Vaultをスキャンさせてみた」型の **実走レポ**。普通のWebアプリじゃなくVault相手にやらせるのが差別化ポイント。提案結果と「実際採用したのは何個」を晒すと読まれる
- **X案**: 「`/plugin install claude-code-setup@claude-plugins-official` が公式提供されてること自体を知らない人が多い」を肯定的に紹介する短文。@hasantoxrの煽り文句を **やわらかく言い直す**版（「使うな」→「試したら3個ハマった」）にすれば共感型に変換できる
- **CLAUDE.md側に書くか検討**: vault運用ルール上「公式setup pluginの提案を受け入れるか」の方針を明文化しておくと、未来の自分が迷わない（採用基準: 既存skillと衝突しない / 月1回以上使う想定がある / read-only検証可能 の3条件）
- 煽り構造の学び: **「公式」+「数字（5カテゴリ）」+「1コマンドで完結」+「FOMO（やめてください）」** はリスト系より反応取りやすい。フォロワー改善の素材として参考になる（[[SNS運用/analytics/フォロワー改善.md]]）
