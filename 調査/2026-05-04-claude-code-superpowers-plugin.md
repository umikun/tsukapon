---
created: 2026-05-04
tags:
  - 調査
  - Claude-Code
  - superpowers
  - プラグイン
  - 自動化
  - AIコーディング
source: https://x.com/ComagerTon79278/status/2050864764541427772
embed: 要検討
---

> **🔗 関連コンテンツ**
> - 📎 元クリッピング: [[Clippings/Post by @ComagerTon79278 on X]]
> - 🛠 関連ツール: [[_ kiwami/tools/daily-log/analytics.py]] — 同じくClaude Codeから呼ぶ自動化ツール（参考）

# superpowers プラグイン：Claude Code を規律ある開発マシンに変える OSS フレームワーク

> **TL;DR**
> `superpowers` は Claude Code にインストールする無料 OSS プラグイン。コマンド 1 本で 14 種類の「スキル」が注入され、AI が「とりあえずコード書く」から「設計→計画→実装→レビュー→検証」の 7 段階を踏むよう強制される。2026 年 1 月に Anthropic 公式マーケットプレイスに採択済み。YouTubeやCrowdWorksの自動化スクリプト開発のような「複雑な自動化タスク」で特に効果を発揮する。インストールはたしかに 50 秒以内。

## 📌 元テキスト（抜粋）

> 50秒でClaude Codeの性能をパワーアップする方法↓
> superpowersというプラグインをインストールする、だけ。
> YouT〇ubeやクラウドワークスを自動化してるけど、これが無かったら無理だったかも。

出典: [[Clippings/Post by @ComagerTon79278 on X]] / [原ポスト](https://x.com/ComagerTon79278/status/2050864764541427772)（2026-05-03）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| superpowers | Claude Code 向け OSS スキルフレームワーク。作者: Jesse Vincent (obra) | `obra/superpowers GitHub` |
| スキル (Skill) | Markdown で書かれた「行動指示書」。AIに特定の手順を強制するプロンプト集 | `superpowers skills list` |
| サブエージェント | 各タスクを独立して実行する子 Claude プロセス。並列化・レビューに活用 | `subagent-driven development` |
| TDD 強制 | Red→Green→Refactor サイクルをスキルで義務化。テストなしの実装を禁止 | `superpowers TDD` |
| brainstorming スキル | コード生成前に要件深掘りする対話フロー。「何を作るか」をまず整理する | `superpowers brainstorming` |
| 1% ルール | スキルの適用可能性が 1% でもあれば必ず呼び出す義務ルール | `superpowers dispatcher` |
| クラウドワークス | 日本最大手フリーランスマッチングサービス。API・スクレイピングで自動化可能 | `Crowdworks API automation` |

---

## 🧭 背景 / なぜ今これが話題なのか

### superpowers の誕生（2024〜2025）

Claude Code や Cursor が普及するにつれ、「AI がコードを書くのは速いが、すぐ詰まる・テストを書かない・要件を誤解したまま爆走する」という問題が現場で顕在化した。作者の Jesse Vincent（obra）は 2024 年からこの問題に取り組み、AIコーディングエージェントに「シニアエンジニア的な規律」を強制するスキルフレームワークとして `superpowers` を公開。

### 公式マーケットプレイス採択（2026 年 1 月）

2026 年 1 月 15 日、Anthropic の公式 Claude Code プラグインマーケットプレイスに採択された。これにより `/plugin install superpowers@claude-plugins-official` という 1 コマンドで誰でも導入できるようになり、普及が一気に加速。GitHub スター 92K 超、インストール数 47 万件以上（2026 年 5 月時点）。

### 「50秒インストール」の実態

ツイートの「50秒」は誇張ではなく実態に近い。コマンド 1 本を貼り付けて Claude Code を再起動するだけで完了するため、設定ファイルの編集や依存パッケージのインストールは一切不要。MITライセンス・無料。

### 日本での広がり

2025 年秋〜2026 年春にかけて、Qiita・Developers.IO・SIOS Tech Lab 等で日本語解説記事が増加。フリーランス開発者がクラウドソーシングの自動化スクリプト開発に活用するケースが報告されている。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「50秒でインストールできる」 | `/plugin install superpowers@claude-plugins-official` 1コマンドで完了。再起動込みで 1 分以内は現実的 | [Claude Plugin Hub](https://www.claudepluginhub.com/plugins/obra-superpowers-2) | ✅ 一致 |
| 「superpowersというプラグインをインストールする、だけ」 | 実際は設定変更不要・1コマンド完結。「だけ」は正確 | [GitHub obra/superpowers](https://github.com/obra/superpowers) | ✅ 一致 |
| 「YouTubeやCrowdWorks自動化に必須だった」 | superpowers はコーディング方法論プラグインで「自動化機能」を直接提供するわけではない。ただし複雑な自動化スクリプトを TDD・計画ベースで構築する際に有効なのは事実 | [Superpowers公式](https://claude.com/plugins/superpowers) | ⚠️ ほぼ一致（誤解を招く表現だが嘘ではない） |
| 暗黙：Claude Code 自体の性能がパワーアップする | 正確には「Claude Code の動作規律がパワーアップする」。モデル自体が賢くなるわけではなく、プロンプト注入でワークフローが構造化される | [SIOS Tech Lab](https://tech-lab.sios.jp/archives/52268) | ⚠️ 表現の誤解あり |

---

## 🌐 最新動向（2026-05-04 時点）

- **公式マーケットプレイス採択**（2026 年 1 月 15 日）で一気に普及加速。47 万インストール超 — [Claude Plugins by Anthropic](https://claude.com/plugins/superpowers), 2026-01
- **MCP サーバー版が登場**（`erophames/superpowers-mcp`）。Cursor・Windsurf・Gemini など MCP 対応ツールでも同じスキルが使えるようになった — [GitHub erophames/superpowers-mcp](https://github.com/erophames/superpowers-mcp), 2026-03
- **superpowers-chrome** が公開。Chrome DevTools Protocol 直接制御プラグイン。ブラウザ自動化を Claude Code から直接行えるようになり、YouTube・フリーランスサイト操作との相性が特に高い — [GitHub obra/superpowers-chrome](https://github.com/obra/superpowers-chrome), 2026-02
- **Cursor・Gemini CLI・OpenCode 対応**。Claude Code 独占だったスキルが主要 AI コーディングツール全般で使えるようになった — [GitHub obra/superpowers](https://github.com/obra/superpowers), 2026-04
- **日本語 fork（ishimori/superpowers-ja）** が登場。スキルの日本語化対応版 — [GitHub ishimori/superpowers-ja](https://github.com/ishimori/superpowers-ja), 2026-02

---

## 🧩 関連概念・隣接分野

- **superpowers-chrome**: obra による姉妹プラグイン。YouTube の動画管理・クラウドワークスの案件チェック等をブラウザ操作で自動化する際はこちらを追加インストールするとより強力になる。ゼロ依存で CDP（Chrome DevTools Protocol）に直接繋ぐ軽量設計
- **MCP (Model Context Protocol)**: Claude Code がツール・外部サービスを呼び出す仕組み。superpowers のスキルが「どう振る舞うか」を定義するのに対し、MCP は「何にアクセスできるか」を定義する。2つを組み合わせると本格的なエージェントになる
- **TDD（テスト駆動開発）**: superpowers の根幹。「テストを先に書く」習慣をAIに強制する。自動化スクリプトにも応用でき、「期待する出力のテストを書いてから実装させる」ことで壊れにくい自動化が作れる
- **Git Worktree**: 複数タスクを並列処理する際に使う Git の機能。superpowers がこれを自動活用することで、メインブランチを汚さずに実験的コードを書ける
- **エージェント型開発**: 人間がレビューポイントだけ担い、それ以外はAIが自律実行するスタイル。superpowers はその自律部分の「迷走防止レール」として機能する

---

## 🪞 反対意見 / 別角度からの視点

**肯定側（ツイート主・多数派ユーザー）の主張**
- 「コードを書く前に考える」という当たり前のことをAIに強制できる唯一のフレームワーク
- 複雑な自動化や長時間エージェントセッションで特に効果が出やすい
- ゼロコスト・1コマンド導入というハードルの低さ

**否定・慎重派の主張**
- 「簡易バグ修正・1時間以内の探索的プロトタイプ」には過剰。余計なフェーズが増えてむしろ遅くなる
- スキルが自動発火するため、意図しない計画フェーズに引き込まれることがある（1% ルールの副作用）
- 本質的には「詳細な CLAUDE.md + プロンプト集」であり、慣れたユーザーは手動でも同じことができる

**中立的に見るときの補助線**
- ツイートの「YouTube・クラウドワークス自動化に必須」は、superpowers で構築した**自動化スクリプトの開発プロセス**が改善されたということ。superpowers 自体に自動化機能はない。`superpowers-chrome` との組み合わせで初めて「ブラウザ操作の自動化」に近づく
- 「50秒」はインストール時間の話。学習・実際の効果が出るまでは数日〜1週間かかるというレポートが多い

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] `superpowers-chrome` を追加インストールすると、実際にどこまでブラウザ自動化ができるのか（CDP 直接制御の範囲）
- [ ] クラウドワークスの API を使った自動化と、ブラウザ操作による自動化、どちらがより安定しているか
- [ ] 日本語 fork（`ishimori/superpowers-ja`）はオリジナルと機能差はあるか・メンテ状況は？
- [ ] `superpowers-mcp` を使えば Claude Code 以外（例: Cursor + Obsidian Claudian）でも同じスキルを使えるか

---

## 📚 参考資料

- [GitHub - obra/superpowers](https://github.com/obra/superpowers) — リポジトリ本体・スキル一覧確認、取得日 2026-05-04
- [Superpowers – Claude Plugin | Anthropic](https://claude.com/plugins/superpowers) — 公式マーケットプレイス・インストール数確認、取得日 2026-05-04
- [AIコーディングエージェントの弱点を補う「obra/superpowers」 | SIOS Tech Lab](https://tech-lab.sios.jp/archives/52268) — スキル体系・14スキル詳細、取得日 2026-05-04
- [「Superpowers」完全ガイド | AimanaVo](https://aimanavo.com/c/morphox_ai/a/lnp6WWF1-pnjvw) — 7段階ワークフロー・向き/不向き整理、取得日 2026-05-04
- [GitHub - obra/superpowers-chrome](https://github.com/obra/superpowers-chrome) — Chrome DevTools Protocol 連携プラグイン、取得日 2026-05-04
- [GitHub - erophames/superpowers-mcp](https://github.com/erophames/superpowers-mcp) — MCP サーバー版の詳細、取得日 2026-05-04
- [Claude Code の概要 - Claude Code Docs](https://code.claude.com/docs/ja/overview) — Claude Code 本体の仕組み確認、取得日 2026-05-04

---

## 🗒 メモ

**SNS活用・記事化のヒント**

このプラグイン、Claude Code ユーザーにとって「知ってる人には常識・知らない人にはびっくり」系の情報。Xで「Claude Codeのこれ知ってる？」系フックで投稿すると刺さりやすいかも。

**自分の使い道として検討したいこと**

- Claudian（このvault自体の管理）は Claude Code が動かしているが、superpowers を使うと「スキル」をベースに動くという設計思想が共鳴する。CLAUDE.md のルール体系と組み合わせる可能性がある
- `superpowers-chrome` + Xの投稿操作・analytics取得の自動化ができるなら SNS 運用フローを一部置き換えられるかもしれない → 要調査

**注意: ツイートの誤解しやすい部分**

「Claude Code の性能をパワーアップ」という表現は正確ではなく、「Claude Code の*使い方*をパワーアップ」が正しい。モデル自体が賢くなるわけではなく、複雑な指示体系（スキル群）をプロンプトとして注入することで、AIの行動パターンが変わる。
