---
created: 2026-04-24
tags: [調査, ClaudeCode, プラグイン, マーケットプレイス, MCP, Skills]
source: "[[Clippings/Post by @HowToAI_ on X.md]]"
---

# Claude Code "アプリストア"──正体は2候補。Anthropic公式の`/plugin`仕組み×コミュニティマーケットが急成長、ただし"任意コード実行"の自己責任ゾーン

> **TL;DR**
> 元ツイートが名指ししていないが、**「1000超のagent/skill/command/MCP/hook を1コマンドで入れられる無料Claude Codeカタログ」** の正体として最有力なのは2つ：**①jeremylongshore/claude-code-plugins-plus-skills**（423 plugins・2,849 skills・177 agents／CLI `ccpi`／ブラウズ先 tonsofskills.com）と、**②claudemarketplaces.com**（4,200+ skills・770+ MCP・2,500+ marketplacesを束ねるディレクトリ）。どちらもMIT・無料・独立運営で**Anthropic公式ではない**。裏側の仕組みはAnthropicが提供する `/plugin marketplace add owner/repo` → `/plugin install name@marketplace` という公式プロトコル。ただし **Anthropic自身が「プラグインはあなたの権限で任意コードを実行する」と警告**しており、"無料・便利"の影に**サプライチェーン汚染の入り口**があることは絶対忘れてはいけない。

## 📌 元テキスト（抜粋）

> 誰かがClaude Code用のアプリストアを構築しました。
> 1000以上のすぐに使えるエージェント、スキル、コマンド、MCP、フックからなる無料ライブラリで、1つのコマンドでインストールできます。
> しかも、100%無料で利用可能です。

出典: [[Clippings/Post by @HowToAI_ on X.md]] / [@HowToAI_ 2026-04-24](https://x.com/HowToAI_/status/2047346924194607470)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code Plugins | Claude Codeにskill/agent/hook/MCPを束ねて足せる"拡張"規格 | `claude code plugin marketplace` |
| `/plugin marketplace add` | 任意のGitHubリポをマーケットプレイスとして登録する公式コマンド | `claude code marketplace add` |
| claude-plugins-official | Anthropic公式マーケットプレイス（Claude Code起動時に自動有効） | `anthropics/claude-plugins-official` |
| tonsofskills.com / `ccpi` | コミュニティ最大級のカタログ。CLI `ccpi` で個別インストール | `jeremylongshore claude-code-plugins-plus-skills` |
| claudemarketplaces.com | Claude Code拡張のディレクトリ。月110k開発者が訪問と謳う | `claudemarketplaces directory` |
| buildwithclaude.com | 別系統のプラグインマーケット | `buildwithclaude plugin marketplace` |
| MCP (Model Context Protocol) | LLMが外部ツール/データに共通APIで触れる規格（Anthropic発） | `model context protocol` |
| Hook | Claude Codeの実行前後に自動で走るスクリプト | `claude code hooks pre tool use` |
| Skill | Claude Codeの"単一指示セット"（プロンプト＋ツール権限） | `claude code skill definition` |
| Agent | Skillをオーケストレートする自律ワーカー | `claude code sub agent` |

---

## 🧭 背景 / なぜ今これが話題なのか

**Claude Code のプラグインマーケットプレイス機構は、2025年末から2026年前半で一気に立ち上がった**。順に追う。

- **〜2025年中盤**: Claude Code（CLI）は `~/.claude/commands/` に自作スキルを置く運用が中心。共有は "awesome-" 系GitHubリストで口コミ。
- **2025年12月**: Anthropicが `/plugin` と `/plugin marketplace` を本格投入。**「GitHubリポ = マーケットプレイス」** の規約（`.claude-plugin/marketplace.json`）が事実上の標準になる。
- **2026年1月**: 公式マーケットプレイス `claude-plugins-official` がデフォルト有効に。GitHub/GitLab/Atlassian/Figma/Vercel/Firebase/Supabase/Slack/Sentry など**MCP統合パック**が即座に並ぶ。
- **2026年1–3月**: コミュニティが爆発。[Plurality まとめ](https://plurality.network/blogs/best-universal-ai-memory-extensions-2026/) 曰く **「npmが10年かけて350kに到達したスケールを、Claudeスキルは2ヶ月で数千→数万まで走った」**。
- **2026年4月14日**: Anthropicが **Claude Code Desktop再設計＋Routines＋Ultraplan** を投入（マルチセッション／クラウドで走るRoutines／CLI→Webエディタ連携）。拡張を前提にした"作業環境としてのClaude Code"が一段完成。
- **2026年4月23–24日**: この流れに乗って、[@HowToAI_](https://x.com/HowToAI_/status/2047346924194607470) が「1000+拡張を1コマンドで」と投稿。該当するのは **tonsofskills.com（`ccpi` CLI、v4.28.0が 2026-04-23 リリース）** か **claudemarketplaces.com** のどちらか（元ツイート画像で特定可能）。

つまり、**「アプリストア」は新発明ではなくAnthropic公式のプロトコル**で、コミュニティがそれを使って**"巨大カタログ"を立ち上げた**状態。"誰かが建てた"というより、"Anthropicが規格を切ってコミュニティが実装した"のが実態に近い。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Claude Code用の"アプリストア"ができた | Anthropicが `/plugin marketplace` 機構を公式に提供済み。その上に乗る**コミュニティカタログ**が複数存在。"新しく誰かが作った"のはカタログ側 | [Claude Code Docs: Discover plugins](https://code.claude.com/docs/en/discover-plugins) | ✅ 一致（ただし"公式の仕組み+コミュニティカタログ"の二層構造） |
| 1000以上のエージェント/スキル/コマンド/MCP/フック | **tonsofskills.com** が 423 plugins・2,849 skills・177 agents・9-10 MCP を公開（合計3,458以上）。**claudemarketplaces.com** は 4,200+ skills・770+ MCP を束ねる | [jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills), [claudemarketplaces.com](https://claudemarketplaces.com/) | ✅ 一致（どちらも1000を大きく超える） |
| 1つのコマンドでインストールできる | 事実。`/plugin install name@marketplace` または `ccpi install name`。公式規約の中核機能 | [Claude Code Docs: Install plugins](https://code.claude.com/docs/en/discover-plugins) | ✅ 一致 |
| 100%無料で利用可能 | tonsofskills / claudemarketplaces ともに "Completely free and open-source (MIT)" と明記 | [claudemarketplaces FAQ](https://claudemarketplaces.com/), [ccpi README](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) | ✅ 一致 |
| "誰か"が構築した（＝単一の個人/組織製） | tonsofskills.comはjeremylongshore 氏、claudemarketplaces.comは独立コミュニティ、buildwithclaude.comはさらに別。**"誰か"は1つに特定できない** | 各サイト | ⚠️ ほぼ一致（単一ではなく複数存在） |
| 安全に"入れるだけ"で使える | **Anthropic公式ドキュメントが明示的に警告**: "plugins are highly trusted components that can execute arbitrary code on your machine with your user privileges" | [Claude Code Docs: Security](https://code.claude.com/docs/en/discover-plugins) | ❌ 要注意（元ツイートは触れていないが重大な留保） |

---

## 🌐 最新動向（2026-04-24時点）

- **Claude Code Desktopリニューアル＋Routines＋Ultraplan** が 2026-04-14 に投入。マルチセッション／クラウドで走るRoutines／CLI→Webエディタ連携が追加──[Build Fast with AI: Claude Code Desktop Redesign](https://www.buildfastwithai.com/blogs/claude-code-desktop-redesign-2026), 2026-04
- **tonsofskills.com（ccpi v4.28.0）** が 2026-04-23 リリース。GitHub Actionsで日次自動更新、26パッケージがnpm `claude-code-plugins` namespaceに常時公開──[GitHub: claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills), 2026-04
- **claudemarketplaces.com** が "月110k開発者訪問" と自称するディレクトリとして急拡大──[claudemarketplaces.com](https://claudemarketplaces.com/), 2026-04
- **skillsmp.com / lobehub skills / SkillsMP** など、Claude以外にもCodex・ChatGPT対応の **横断スキルマーケット** が同時多発で立ち上がっている──[LobeHub skills](https://lobehub.com/skills), [SkillsMP](https://skillsmp.com/), 2026-04
- **Stanford Law School CodeX** が 2026-04-08 に "When Claude Code Meets Apple's App Store" を掲載。**AppleのApp Store登録プロセス/審査スタンダードとの比較**という法的・ガバナンス論点が学術側でも議題化──[Stanford Law CodeX](https://law.stanford.edu/2026/04/08/when-claude-code-meets-apples-app-store/), 2026-04
- **Anthropic公式は"審査しない"立場**: "Anthropic does not control what MCP servers, files, or other software are included in plugins" と明言、責任はユーザー側──[Claude Code Docs](https://code.claude.com/docs/en/discover-plugins), 2026-04

---

## 🧩 関連概念・隣接分野

- **[[調査/2026-04-24-openchronicle-mac-ai-memory.md]]（OpenChronicle）**: Mac作業文脈をClaude Desktopに渡すMCPサーバ。**プラグインではなく"独立MCPサーバ"**なので、プラグインマーケット経由で入れられる日は近い。
- **[[調査/2026-04-23-claude-obsidian-llm-wiki.md]]（claude-obsidian）**: 似た位置取り。Obsidian vaultをClaude Codeから扱うためのpluginだが、まだ公式マーケットには未登録っぽい。
- **MCPサーバの"公式 vs 野良"の境界**: `claude-plugins-official` に同梱されるMCP（GitHub/Linear/Slack等）はAnthropicが動作保証する一方、サードパーティMCPは完全に自己責任。**同じMCPでも"どのマーケット経由で入れたか"で信頼度が変わる**。
- **ccpi（`@intentsolutionsio/ccpi`）**: Claude Code専用のnpmベースパッケージマネージャ。pnpm/npmと同じ感覚で扱える**"Claude Code界のhomebrew"**的ポジション。
- **Claude Code Routines（2026-04-14発表）**: 拡張を"自分のMacで実行" → "Anthropic側のクラウドで常時実行"へ広げる仕組み。**プラグイン×Routines** で「選挙監視Bot」「毎朝ニュース要約」等を無人運用する未来が視野に。
- **SkillsMP / LobeHub / Skills.sh**: プラットフォーム横断のスキルマーケット。ClaudeだけでなくCodex・Gemini・Cursorでも使えるスキルが増えており、**"LLM中立のエクステンションエコノミー"** が形成中。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（元ツイート＆推進派）**:
  - 1コマンドで3000超の拡張が入る圧倒的な生産性。自作コマンドを書き続けるよりも、**"他人が書いた良い道具を無料で借りる"** のが早い。
  - コミュニティが爆速で増えることで、"AIの使い方"そのものが標準化される（=ベストプラクティスの共有が進む）。
- **否定 / 慎重派の主張**:
  - **任意コード実行のリスク**: Anthropic公式ドキュメントが**"highly trusted components that can execute arbitrary code"**と明記。悪意あるhookが1つ紛れ込むだけで、**`.env`、`~/.ssh/`、キーチェーン、ブラウザcookie**まで送信されうる。
  - **スケール問題**: 2ヶ月でnpmの10年を追い抜く勢いで増えているということは、**npm系のサプライチェーン攻撃（typosquatting / 依存関係ハイジャック / メンテナ乗っ取り）と同じ問題が圧縮された時間軸で発生する**ということ。
  - **"公式っぽい"名前の野良マーケット**: `claude-plugins-official` はAnthropic公式だが、`claudemarketplaces.com` / `buildwithclaude.com` は独立運営。名前の似た偽ディレクトリが出てくるのは時間の問題。
  - **ライセンス・商用利用**: MITだからといって **中身のMCPサーバが別途商用制限を持っている** ケース（例: n8nのSustainable Use License）があり、**プラグイン単位で"本当に商用OKか"を確認する必要**がある → 参考: [[調査/2026-04-23-oss-saas-alternatives.md]]。
- **中立的に見るときの補助線**:
  - **"インストール先スコープ"を使い分ける**のが現実解。Anthropic公式機構は **user / project / local** の3スコープを提供している。**業務リポ＝projectスコープで厳選したものだけ** / 個人検証＝localスコープで野良も試す、と分けるのが安全。
  - **Tsukapon vault の `.claude/commands/` 自作運用** との関係: プラグインマーケットで見つけた良スキルを、**コピーしてvault内に自分の命名で保管**する方が、**外部アップデートで挙動が変わるリスクを回避**できる。拡張エコノミーが膨らむほど、**"手元で凍結する"運用の価値**が上がる。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] 元ツイートの画像で名指しされているのは **tonsofskills.com か claudemarketplaces.com か buildwithclaude.com か**（画像確認で即判明）
- [ ] tonsofskills.com / claudemarketplaces.com の **プラグイン審査プロセス**（人間レビューあり？自動チェックのみ？）
- [ ] `ccpi` と `/plugin` の違い（後者はAnthropic公式プロトコル、前者はnpmラッパ）。**併用時の依存関係衝突**は起きないか
- [ ] **悪意あるプラグインの実例**（github issues / HackerNews / CVE）がすでに報告されているか
- [ ] Claude Code **Routines× プラグインマーケット** の組み合わせで自動化できる業務レシピ
- [ ] **[[Claudian-スキル一覧.md]]** の自作スキル群（re-daily / deep-dive / thread 等）を **"個人マーケットプレイス"** としてGitHubに切り出す価値はあるか（=他人と共有 or 別マシンでの再利用）
- [ ] AnthropicのRoutines公開範囲（個人のMacで動くのか、Anthropicクラウドで動くのか）

---

## 📚 参考資料

- [Claude Code Docs: Discover and install prebuilt plugins through marketplaces](https://code.claude.com/docs/en/discover-plugins) — `/plugin marketplace add`／`/plugin install`／セキュリティ警告の一次情報, 取得日 2026-04-24
- [GitHub: jeremylongshore/claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) — 423 plugins / 2,849 skills / 177 agents・ccpi CLI・tonsofskills.com, 取得日 2026-04-24
- [claudemarketplaces.com](https://claudemarketplaces.com/) — 4,200+ skills・770+ MCP・2,500+ marketplaces を束ねるディレクトリ, 取得日 2026-04-24
- [anthropics/claude-plugins-official (GitHub)](https://github.com/anthropics/claude-plugins-official) — 公式マーケットプレイスのリポ, 取得日 2026-04-24
- [Build Fast with AI: Claude Code Desktop Redesign 2026](https://www.buildfastwithai.com/blogs/claude-code-desktop-redesign-2026) — 2026-04-14 のDesktop刷新・Routines・Ultraplan, 取得日 2026-04-24
- [Stanford Law CodeX: When Claude Code Meets Apple's App Store](https://law.stanford.edu/2026/04/08/when-claude-code-meets-apples-app-store/) — 法学的・ガバナンス論点, 取得日 2026-04-24
- [Medium: Claude Code Has a Skills Marketplace Now](https://medium.com/@markchen69/claude-code-has-a-skills-marketplace-now-a-beginner-friendly-walkthrough-8adeb67cdc89) — 入門解説, 取得日 2026-04-24
- [Plurality: Best AI Memory Extensions of 2026](https://plurality.network/blogs/best-universal-ai-memory-extensions-2026/) — スケール感（npm vs Claude skills）の比較, 取得日 2026-04-24
- [wmedia.es: Plugins in Claude Code](https://wmedia.es/en/tips/claude-code-plugin-marketplace-distribution) — マーケットプレイス配布の実務解説, 取得日 2026-04-24

---

## 🗒 メモ

- **使い道（X投稿・note記事）**: 「**タダより怖いものはない──Claude Codeアプリストアの"1000拡張"で見落とされている1行**」という切り口で1本書ける。**元ツイートが一言も触れていないAnthropic公式の警告文**を冒頭で引用→「任意コード実行ゾーンに入っている自覚ありますか？」のフック。関係性KW: 会社のMac／取引先データ。
- **Tsukapon vault の運用への示唆**:
  - `.claude/commands/` 自作運用 は**マーケットへの依存を避けつつ自分仕様**に作る戦略として、むしろ**貴重な資産**。マーケット拡大期こそ、手元の自作レシピが差別化ポイントになる。
  - 既存の [[Claudian-スキル一覧.md]] を **"個人プライベートマーケットプレイス"** 化（GitHubに `.claude-plugin/marketplace.json` を置く）する実験は価値がある。別マシンや別クライアントに一発セットアップできる。
- **優先度高めの次アクション**: 画像確認（元ツイート添付画像）で"誰かが建てたアプリストア"がtonsofskills か claudemarketplaces か確定 → そのGitHubリポを週末に `/plugin marketplace add` で**個人用サブ環境でだけ**試射する。
- **要注意**: 業務Mac／Tsukapon vault に直接入れるのは推奨しない。Anthropic公式が **"任意コード実行"** と明言している以上、**vaultバックアップ（/Volumes/500GB/GoogleDrive/Tsukapon/）の整合性を保ったままの状態**でクリーンな仮想環境で検証する方針を先に固める。
