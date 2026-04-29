---
created: 2026-04-29
tags: [調査, birdclaw, x-archive, sqlite, fts5, content-recycle]
source: https://x.com/L_go_mrk/status/2048711308246385014
---

# Birdclaw：自分のXアーカイブをSQLiteに突っ込んで全文検索する OSS──"OpenClaw作者の次の一手"

> **TL;DR**
> - Birdclaw（[steipete/birdclaw](https://github.com/steipete/birdclaw)）は **MIT・436★** のローカル完結 Twitter ワークスペース。Xからエクスポートしたアーカイブを SQLite + FTS5 に取り込み、Web UI + CLI で**ツイート・DM・いいね・ブックマーク**を全文検索＋AI採点インボックスで管理。v0.2.1（2026-04-27リリース）でまだ WIP だが実用可能
> - **作者は Peter Steinberger（steipete）= OpenClaw作者**。Anthropicに潰された経歴がある人物。今回はAPI叩きじゃなく**自分のアーカイブを自分のローカルで処理する**設計で、ToS摩擦は基本ない。代わりにX側の「アーカイブ申請が24-48時間 + 7日で失効」という構造的不便がついて回る
> - X運用者の側面では**過去の自分の発言を発掘して再利用するための"second-brain for X"**として強い。批評型ポジションの一貫性チェック、Day Oneプロモみたいな再販タイミング判断、過去に書いた一文を引用RTの種にするなど、コンテンツリサイクル運用と相性◎

## 📌 元テキスト（抜粋）

> これX運用で使ってるんだけどマジで便利すぎる。
>
> Bird-Claw：自分のXアーカイブを丸ごと取り込んで全文検索できるOSS。
>
> Xから自分のアーカイブを書き出す → birdclawに食わせる → Web UIで「いいね」「メンション」「DM」をタブ別に閲覧 → 全文検索で過去の自分の発言を一瞬で引っ張る
>
> https://github.com/steipete/birdclaw…

出典: [[Clippings/Post by @L_go_mrk on X 5]] / [@L_go_mrkの元投稿](https://x.com/L_go_mrk/status/2048711308246385014)

> 📝 元ツイートは「Bird-Claw」と表記、リポジトリ名は **birdclaw**（ハイフンなし）が正。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Birdclaw | Xアーカイブを取り込んで全文検索する OSS（[steipete/birdclaw](https://github.com/steipete/birdclaw)） | `birdclaw twitter archive` |
| Twitter/Xアーカイブ | XのSettingsから申請できる「自分の全データ」のZIPダウンロード。準備に24-48時間 | `twitter archive download` |
| FTS5 | SQLiteの全文検索エンジン。日本語含む高速インデックス検索が可能 | `sqlite FTS5` |
| AIスコアインボックス | OpenAI APIで重要度を採点して、メンション/DMをトリアージする機能 | `birdclaw inbox AI score` |
| xurl / bird CLI | Twitter APIを叩くためのCLI。Birdclaw の live sync で内部利用 | `xurl twitter cli` |
| Peter Steinberger / steipete | iOS / Mac開発界隈の有名OSS作者。OpenClaw（Anthropic banされたハーネス）の作者 | `peter steinberger openclaw` |
| local-first | データもUIもローカルで完結する設計思想。クラウド依存ゼロ | `local-first software` |
| launchd | macOSの常駐サービス管理。Birdclawの定期同期に使われる | `launchd schedule macos` |
| ライブ同期 | アーカイブ申請を待たずに、API経由で最新ツイート/いいね/ブックマークを差分取り込みする機能 | `birdclaw live sync xurl` |

---

## 🧭 背景 / なぜ今これが話題なのか

**「自分のXデータ、いつ消えるかわからん問題」**が2024年〜2025年にかけて X コミュニティで膨らみ続けて、2026年Q2に local-first ツールとして実装が成熟してきた、というのが文脈の核。

時系列で押さえる:

- **2022年10月**: Twitter買収後、API有料化＋無断凍結が頻発。「自分のツイート資産が一晩で消える」恐怖が常態化
- **2023〜2024年**: コミュニティが Twitter Archive ZIPを保存する文化を確立。だが「保存しても見れない・検索できない」が課題
- **2024年**: tweet-archive ビューアが乱立。ただし**ローカル検索＋AI採点インボックス**まで踏み込んだものは少ない
- **2025年**: Peter Steinberger が **OpenClaw**（Claude Pro/Max OAuthで Claude Code互換のCLIを提供）でAI界隈に名を売る → 後にAnthropicに正式BANされる（[[2026-04-29-jcode-agent-harness-claims]] 参照）
- **2026年4月初旬**: Anthropicが OpenClaw 系を完全遮断（4-04全面執行）。steipete は X 関連の local-first ツールに方向転換
- **2026-04-27**: Birdclaw v0.2.1 リリース。元ツイートはこの直後の紹介投稿

つまり Birdclaw は **「OpenClaw作者の next move」** として、AI連携の中心軸を「Claudeを叩く」から「自分のSNSデータを叩く」に移した結果として出てきた。コミュニティの一部から「steipeteの新作はとりあえず触る」という関心が集まっている文脈もある。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 自分のXアーカイブを丸ごと取り込める | ✅ Twitter ZIPアーカイブのインポートをサポート、画像・アバターのキャッシュも込み | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ✅ 一致 |
| 全文検索できる | ✅ SQLite FTS5 でツイート・DM全文を高速検索 | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ✅ 一致 |
| Web UIでいいね/メンション/DMをタブ別に閲覧 | ✅ Home timeline、Mentions、DMs、Inbox、Blocks のタブ構成あり | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ✅ 一致 |
| OSS（Open Source Software） | ✅ MITライセンス | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ✅ 一致 |
| 「マジで便利すぎる」 | ⚠️ v0.2.1 でWIPステータス。「Real and usable. Not done.」公式表記。実用は可能だが本番運用には注意が必要 | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ⚠️ ほぼ一致（条件付き） |
| 表記「Bird-Claw」 | ❌ 正式名は **birdclaw**（ハイフンなし） | [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw) | ❌ 要注意（タイポ） |

---

## 🌐 最新動向（2026-04-29時点）

- **Birdclaw v0.2.1 リリース（2026-04-27）** — ライブ同期（xurl/bird CLI経由）、ローカル検索フィルタ強化、Likes/Bookmarks 専用ビュー追加 — [GitHub Release](https://github.com/steipete/birdclaw/releases/), 2026-04
- **launchdベースの定期ブックマーク同期**: macOSのlaunchdに常駐ジョブをinstallして自動取り込み。JSONLログ + Git自動バックアップ付き — [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw), 2026-04
- **Git-friendly な年次シャード**: SQLiteの中身をJSONLで年別にエクスポート。複数Mac間でマージ可能 — [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw), 2026-04
- **AIスコアインボックスはOpenAI API任意**: OpenAI APIキー設定すると、メンション/DMの重要度を採点。設定しなくても動作する — [GitHub steipete/birdclaw](https://github.com/steipete/birdclaw), 2026-04
- **作者steipete はOpenClaw完全停止後の転換期にいる**: 2026-04-04のAnthropic OAuth全面執行で OpenClaw が機能停止。Birdclaw は Anthropic ToS摩擦のないローカル完結設計で再起動 — [VentureBeat OpenClaw記事](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and), 2026-04

---

## 🧩 関連概念・隣接分野

- **Twitter/X アーカイブの仕様**: Settings > Your Account > Download an Archive of Your Data から申請。準備に24-48時間、ダウンロードリンクは7日で失効、再申請は24時間に1回。Birdclaw を運用するならこの再申請サイクルに合わせて月1回更新する形になる — [Twitter Archive Guide 2026](https://www.tweetarchivist.com/how-to-download-twitter-archive)
- **OpenClaw（廃絶）**: Birdclaw 作者の前作。Anthropic OAuth経由でClaude Pro/Maxを叩いていた。2026-04-04にAnthropicから正式BAN。Birdclawはその経験を踏まえて**ローカル完結設計**に振り切っている経緯あり
- **既存vault SNS運用との比較**: ユーザーは [[SNS運用]] 配下に384ファイル分のX投稿実体・連投ドラフト・有料記事戦略を Markdown でローカル保存している。これは「自分が書いた予定原稿」のアーカイブ。Birdclawは「**実際に投下されてエンゲージされた結果**」のアーカイブ。両者は補完関係
- **Karpathy LLM Wiki / Graphify パターン**: 個人データをローカルで構造化してAIに食わせる流れ。Birdclawはこの系譜の「X版」と位置付けられる — [[2026-04-29-graphify-knowledge-graph-skill]] 参照
- **content recycling の戦略**: 2025年以降のSNS運用論で常識化した「過去ツイートの再利用は新規よりROI高い」という実務知見。Birdclawの全文検索はその実装基盤になる

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - **ローカル完結＝プライバシー◎、ToS摩擦ゼロ**。OpenClaw教訓を組み込んだ設計
  - SQLite + FTS5 + JSONL 出力 = データポータビリティ最強。10年後も動くアーキテクチャ
  - X運用者にとって「過去の自分の発言を瞬時に引ける」は実務価値が高い。引用RT素材の発掘、批評型ポジションの一貫性チェック、Day Oneプロモみたいな再販記事の発掘
  - 作者がiOS界の有名人で、開発体力が継続的に投下される期待

- **否定 / 慎重派の主張**:
  - **WIP（v0.2.1）**: 公式に「Not done」と書いてある。本番運用前提のツールではない
  - **アーカイブ申請の不便**: 24-48時間待ち + 7日で失効 + 再申請24時間ルール = 月1回更新が現実的なリズム。リアルタイム性は期待できない
  - **ライブ同期は xurl/bird CLI 依存**: X API のレート制限・認証要件にぶつかる可能性。アーカイブ申請より速いが完璧ではない
  - **OpenAI APIキーの管理**: AIインボックス機能を使うなら APIキー漏洩リスクの管理が増える
  - **作者の前科**: OpenClaw が ToS 違反で潰れた経歴。Birdclaw自体はクリーンだが、**今後の機能拡張で同じ罠を踏む可能性**は注視
  - **WebUIに認証なし**: 個人運用前提なのでローカル限定で動かす必要。`localhost:3000` を不用意に外に出すと過去DMが漏れる

- **中立的に見るときの補助線**:
  - **使い方を限定すれば強い**: 月1のアーカイブ更新リズム、ローカル限定、引用RT素材発掘 / 批評型ポジション一貫性確認の用途に特化なら超有用
  - **「リアルタイム X 管理ツール」として期待しない**: それは公式X / TweetDeck の領域
  - **作者の前作で自分の Claude Pro が止まった人にとっては感情的に受け入れにくい**かもしれないが、設計思想は明確に異なる

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] 自分のXアーカイブを実際に申請 → Birdclaw に食わせた時の所要時間（インポート時間）と、384件以上のSNS運用ファイルとの照合運用が成立するか
- [ ] Birdclaw のFTS5検索が**日本語の形態素解析にどの程度対応しているか**（FTS5 unicode61 トークナイザのデフォルト動作で日本語ヒットするか）
- [ ] vault側の SNS運用/post/day*.md / threads/Threads-day*.md と Birdclaw のSQLiteを **n8n で突き合わせる**運用シナリオ。「予定通り投稿された vs 実際にバズった」のギャップ可視化
- [ ] AIインボックス機能でメンションの重要度を採点 → ルーチンB（[[SNS運用/analytics/フォロワー改善.md]]）の優先度判断に組み込めるか
- [ ] Birdclaw のJSONL出力をObsidian vaultに同期する設計。`SNS運用/archive/x-history/YYYY-MM/*.jsonl` のような形で「自分の過去の発言」をvaultに統合する価値
- [ ] steipete の今後のロードマップ（OpenClawから方針転換した先で何を作るのか）

---

## 📚 参考資料

- [GitHub - steipete/birdclaw](https://github.com/steipete/birdclaw) — 一次情報（README、機能、ライセンス、Star、リリース履歴）, 取得日 2026-04-29
- [GitHub Releases - birdclaw](https://github.com/steipete/birdclaw/releases/) — v0.2.1リリースノート, 取得日 2026-04-29
- [Tweet Archivist - How to Download Twitter Archive 2026](https://www.tweetarchivist.com/how-to-download-twitter-archive) — Xアーカイブ申請の最新仕様, 取得日 2026-04-29
- [GitHubTree - steipete/birdclaw structure](https://githubtree.mgks.dev/repo/steipete/birdclaw/main/) — リポジトリ構造の参考, 取得日 2026-04-29
- [Grok on X - Birdclaw紹介](https://x.com/grok/status/2030779263994019899) — 第三者によるBirdclaw解説（Steinbergerと OpenClaw の関係性に言及）, 取得日 2026-04-29
- [VentureBeat - Anthropic cuts off OpenClaw](https://venturebeat.com/technology/anthropic-cuts-off-the-ability-to-use-claude-subscriptions-with-openclaw-and) — OpenClaw廃絶の経緯（Birdclaw作者の前史）, 取得日 2026-04-29
- [Tweet Archivist - Complete Guide to Analyzing Twitter Data](https://www.tweetarchivist.com/download-twitter-archive-complete-guide) — アーカイブ分析手法の一般論, 取得日 2026-04-29

---

## 🗒 メモ

- **note記事化候補（実装記録型）**: 「自分のXアーカイブを Birdclaw に食わせて、批評型ポジションの一貫性をデータで確認した話」型。元ツイートの「マジで便利すぎる」温度感を、**実装した側の具体性**に持ち上げる差別化
- **連投シリーズ素材としての位置**: コンテンツリサイクル系。「過去のバズった発言を再利用するためのlocal-first toolchain」という切り口で、煽り解剖型からは外れた **実装紹介型** の連投。連投シリーズ⑤〜⑥候補
### 🔬 vault統合シナリオの再評価（2026-04-29 検討）

3つのシナリオを冷静に検証した結果、**「価値は3本の調査ノート中最高だが、緊急度は低い」**が結論。

#### シナリオ①: vault統合（月1 SQLite→jsonl→n8n照合）

- 元案: Birdclaw SQLiteから月1でJSONL出力 → n8nで過去同テーマツイートとの照合・リミックス自動提案
- 評価: 🟡 **手動運用「FTS5検索→手で抽出」で90%の価値が出る**。n8n自動化は過剰設計の可能性
- 注目点: Twitter Archive には**imp/like/RT数も含まれる**。「伸びた過去ツイート」の客観的判定が可能
- 「重複投稿回避」より「過去のヒット作の意図的リミックス」の方が運用上のリターンが高い

#### シナリオ②: Day Oneプロモ連動

- 元案: 過去のDay One関連発言を全文検索で発掘して、自分語りツイートのストーリー連続性を強化
- 評価: ❌ **今回プロモには間に合わない**。Day Oneプロモは4/26〜5/3、今申請→5/1到着→残り2日で準備時間ゼロ
- 次回プロモの準備として温めるなら有用

#### シナリオ③: 批評型ポジション自己審査

- 元案: 過去6ヶ月の引用RT履歴を Birdclaw FTS5 で検索して一貫性チェック
- 評価: ❌ **規模感30〜50件で目視で十分**。Birdclaw はオーバースペック
- 「四半期に1回、過去ツイートを目視で読み返す習慣」を作る方が筋。ツールより運用

#### 慎重ポイントの追加情報

- **アーカイブZIPは数GB〜10GB超**: 12年運用歴 + メディア込みなら 5〜15GB の見込み。ダウンロード/展開時間も加味
- **ポート3000衝突リスク**: Vite/Next.js等とデフォルト3000がぶつかる。並行作業時の運用設計が必要
- **macOSスリープ中は launchd 同期も止まる**: [[2026-04-29-sns-automation-implementation-plan]] の caffeinate 議論と同じ問題

#### 修正された総評

価値は **jcode（[[2026-04-29-jcode-agent-harness-claims]]）と違ってBANリスクなし、Graphify（[[2026-04-29-graphify-knowledge-graph-skill]]）と違って明確な実用シナリオあり**で、今日の3本中最高。**ただし緊急度は低い**:

- WIP（v0.2.1）リスク: 1ヶ月で機能が変わる可能性あり
- 既存n8n運用との競合: Phase 1（Bluesky自動投稿）が安定してから次の追加が望ましい
- GW中の作業余力枯渇: 今日3本の調査+Phase 1の60%実装+Day Oneプロモ並走で疲労蓄積
- Day Oneプロモへの応用: 今回間に合わない

#### 推奨される段階導入ロードマップ

| Phase | 時期 | 作業 | 所要 | 状態 |
|---|---|---|---|---|
| **A** | **今すぐ（GW中）** | アーカイブ申請だけ済ませる（X Settings → Download an Archive of Your Data）。実装は寝かせる | 5分 | ✅ **完了 2026-04-29** |
| **B** | **アーカイブ到着後（5/1〜5/2想定、5/8〜9失効）** | Birdclaw を Homebrew インストール、アーカイブ取り込み、**手動運用で1ヶ月試す**。FTS5検索を週1で過去ヒット作発掘に使う。n8n統合は**まだしない** | 30分〜数時間（初回） | ⬜ |
| **C** | **6月（評価後）** | 1ヶ月手動運用の感触を踏まえて、n8n×Birdclaw月次パイプライン構築 or 撤退判断。価値確信なら [[2026-04-29-sns-automation-implementation-plan]] のPhase 6として追記 | TBD | ⬜ |

#### 📅 Phase A 完了記録（2026-04-29）

- ✅ Xアーカイブ申請: 2026-04-29 リクエスト済み
- ⏰ 到着予想: 2026-05-01〜05-02（24〜48時間後にメール通知）
- ⏰ ダウンロード期限: 2026-05-08〜05-09（リンク失効）
- 📥 受領後の保管先候補: `~/Downloads/x-archive-202604/twitter-YYYY-MM-DD-xxxxxxx.zip`
- 🚪 Phase B トリガー: アーカイブ到着メール受信 → ZIP ダウンロード → ファイルサイズ確認

→ **次のアクション**: アーカイブ到着メールを待つ。届いたらPhase Bを開始できる状態にする。
