---
created: 2026-05-06
tags:
  - 調査
  - Clypra
  - CapCut
  - OSS
  - 動画編集
  - Tauri
source: https://x.com/ericksky/status/2051706069890605431
action: 採用なし
---

# 「CapCutの代わりにClypra（OSS）を使え」を裏取りしてみる

> **🔗 関連コンテンツ**
> - 🆓 同日のSaaS代替リスト調査（Descript→CapCutの上書き対象）: [[2026-05-06-dont-pay-ai-tool-alternatives]]
> - 🤖 Codex × iOS開発（同じ「20分で〇〇」系フォーマット）: [[2026-05-06-codex-gpt55-ios-20min-workflow]]
> - 🐦 関連ネタ（Vault×AIエージェント）: [[Clippings/Post by @obsidianstudio9 on X.md]]

> **TL;DR**
> @ErickSky のスペイン語投稿「CapCutに金を払うな、Clypraを使え」。**Clypraは実在する**（GitHub: AIEraDev/Clypra、Tauri+React+TypeScript+Rust+FFmpeg、MITライセンス）が、**★75と非常に小規模**で**README自身が「プレミアム機能の無料実装に注力」（=網羅ではない）と明記**。同カテゴリには**OpenCut（★48.7k）という圧倒的本命OSS**が存在し、「CapCut OSS代替」を真面目に検討するならOpenCut/Kdenlive/Shotcutが筋。Clypraは**現時点では"将来性ある試み"**であり、「CapCutを今日捨てて移行」と煽るのは過剰。

## 📌 元テキスト（抜粋）

> Olvídate de pagar por CapCut.
>
> Acabo de encontrar Clypra, el editor de video 100% open source que te da todas las funciones premium de CapCut… gratis, sin marcas de agua y con rendimiento nativo.
>
> Construido con Tauri + React + TypeScript + FFmpeg, es rápido como un rayo y se siente como una app de escritorio real (macOS, Windows y Linux).

（日本語訳）
> CapCutに金を払うのは忘れろ。
> Clypraを見つけた。**CapCutの全プレミアム機能を無料で**提供する100%オープンソースの動画エディタだ。ウォーターマークなし、ネイティブパフォーマンス。
> Tauri + React + TypeScript + FFmpeg で構築、超高速で本物のデスクトップアプリの感覚（macOS / Windows / Linux）。

出典: [Post by @ErickSky on X (2026-05-05)](https://x.com/ericksky/status/2051706069890605431) ／ Likes 1,220 / RT 187（2026-05-06時点）／ 添付動画 68秒

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Clypra** | AIEraDev製のOSS動画エディタ。Tauri+React+TypeScript+Rust+FFmpeg | `Clypra AIEraDev video editor` |
| **CapCut Desktop** | ByteDance製の無料動画エディタ。デスクトップ版あり | `CapCut Desktop ByteDance` |
| **Tauri** | Rust + Web技術でデスクトップアプリを作るフレームワーク。Electronより軽量 | `Tauri Rust desktop framework` |
| **OpenCut** | OSS動画エディタの本命。★48.7k、Next.js + Rust構成 | `OpenCut video editor open source` |
| **Kdenlive** | KDE製の老舗OSS動画エディタ。プロ級機能で完全無料 | `Kdenlive open source video editor` |
| **Shotcut** | クロスプラットフォームOSS動画エディタ。GPUアクセラ・多形式対応 | `Shotcut video editor` |
| **frame-accurate編集** | 1フレーム単位で正確にカット/トリムできる精度 | `frame accurate video editing` |
| **FFmpeg** | 動画/音声処理の標準OSSライブラリ。多くの動画エディタの心臓部 | `FFmpeg library encoding` |
| **MIT License** | 商用利用・改変・再配布OKの寛容なOSSライセンス | `MIT License open source` |
| **マルチトラックタイムライン** | 複数の動画/音声/字幕レイヤーを並行編集できるUI | `multi-track timeline editor` |

---

## 🧭 背景 / なぜ今これが話題なのか

**「CapCut課金疲れ」と中国系SaaSへの警戒（2024〜2026）。** ByteDance製CapCutは無料機能が豊富で世界的に普及したが、2024年以降、**有料機能の拡充・透かし強制・利用規約の追加**などで「実質有料化」が進行。同時に**TikTok / ByteDance系のデータ収集懸念**（米国で議論継続中）もあり、「OSSで代替したい」層が拡大。

**OSS動画エディタの新世代台頭（2024〜2026）。** OpenCut（★48.7k）が**「OSSのCapCut代替」の本命**として成長、KdenliveやShotcutといった老舗に加えて、**Tauri + Web技術でモダンUIに振った新興プロジェクト**が次々登場。Clypraもこの波の一例。awesome-capcut-alternatives のキュレーションリポジトリ（[furudo-erika/awesome-capcut-alternatives](https://github.com/furudo-erika/awesome-capcut-alternatives)）まで登場。

**Tauri + React のデスクトップアプリ流行（2024〜）。** ElectronのRAM喰い問題への反動として、**Tauri（Rust + WebView）** がデスクトップアプリ開発で急伸。React/TypeScriptフロント＋Rustバックエンドで「**Webの開発体験 × ネイティブの性能**」を狙う構成は、2026年も主要トレンド。Clypraの技術スタックはこの典型。

**「Don't pay for X, use Y」型のSNSバズ（2024〜）。** [[2026-05-06-dont-pay-ai-tool-alternatives|別ノートで分析した]] @SocialtyPro の14ペアリストと**同じフォーマット**で、@ErickSky の今回のスペイン語投稿はその単発版。Likes 1,220 / RT 187と**スペイン語圏では強い反応**。新興OSSをスポットライトに乗せる役割を果たす一方、**「鵜呑み危険」問題**は同様。

**スペイン語圏のテック系発信者ネットワーク。** @ErickSky を含むスペイン語インフルエンサーは英語圏のリポジトリを**スペイン語圏に翻訳・紹介**するハブ機能を持ち、英語圏でまだ無名のOSSが**先にラテンアメリカで広まる**現象がある。Clypraも英語圏での認知より先にスペイン語圏でバズった可能性。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| **Clypraは実在するOSSか** | GitHub `AIEraDev/Clypra` 実在、**MITライセンス**、★75・fork 7、84コミット、Open Issues 0 | [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra) | ✅ 一致 |
| **Tauri + React + TypeScript + FFmpeg 構成** | 言語比率は **TypeScript 70.7% / Rust 27.2% / CSS 2.0%**、READMEでTauri+React+TS+FFmpegを明記 | [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra) | ✅ 一致 |
| **macOS / Windows / Linux 対応** | Tauriの標準対応プラットフォーム。READMEで明記 | [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra) | ✅ 一致 |
| **「CapCutの全プレミアム機能を無料提供」** | **READMEには "Focus on building **free capabilities of** premium capcut functionalities"** と書かれており、**「プレミアム機能の無料実装に注力」=全機能網羅ではない**。Roadmapに未実装あり | [GitHub - AIEraDev/Clypra (README)](https://github.com/AIEraDev/Clypra) | ❌ 要注意（ツイートの誇張） |
| **「ウォーターマークなし、無料」** | OSS（MIT）のためツールはどちらも事実 | [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra) | ✅ 一致 |
| **「ネイティブパフォーマンス」「電光石火」** | Tauriは Electron比で**軽量**だが、**完全ネイティブ**（Swift/SwiftUI/Cocoa等）と比べると別レベル。"電光石火"は誇張 | [Tauri vs Electron 一般評価] | ⚠️ ほぼ一致（誇張あり） |
| **暗黙の前提：「Clypraが現実的なCapCut代替」** | ★75・Open Issues 0・Roadmap未完で**プロダクション運用には早い**段階。同カテゴリOSSの本命は **OpenCut（★48.7k）** | [GitHub - OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) / [4 Best Open Source CapCut Alternatives 2026](https://openalternative.co/alternatives/capcut) | ❌ 要注意（候補としては成立、本命はOpenCut） |
| **CapCut Desktopは無料でも使える事実** | CapCut Desktopは**基本無料**で使え、有料は一部のAI機能・透かしなしエクスポート等のプレミアム部分。「全部に課金が必要」ではない | [Best CapCut Alternatives 2026 (Movavi)](https://www.movavi.com/learning-portal/apps-like-capcut.html) | ⚠️ 文脈注意（"課金不要のCapCut"も実は存在） |

🔍 未確認: 0件

---

## 🌐 最新動向（2026-05-06時点）

- **OpenCutが「OSSの本命CapCut代替」として★48.7kに到達** — Next.js + Rust構成、ウェブ/デスクトップ/モバイル対応、ローカル処理プライバシー優先 — [GitHub - OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut), 2026-05
- **awesome-capcut-alternativesリポが登場（furudo-erika）** — OSSキュレーションが体系化される段階。Clypraもここに含まれうる候補群 — [awesome-capcut-alternatives (GitHub)](https://github.com/furudo-erika/awesome-capcut-alternatives), 2026
- **Clypraは★75・MITライセンスで開発初期段階** — 84コミット、Open Issues 0、Roadmap未完。**まだ"将来性ある試み"のフェーズ** — [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra), 2026-05
- **Kdenliveがプロ級機能でCapCut代替の鉄板に** — Linux/Win/Mac/BSD対応、マルチトラック・色補正・キーフレーム・形式対応で**完全無料** — [4 Best Open Source CapCut Alternatives 2026](https://openalternative.co/alternatives/capcut), 2026
- **Tauri + React/TS構成のデスクトップアプリ全般が活況** — Clypra・montage・ffmpeg-gui等、**Webスタックでネイティブ風アプリ**を作る試みが量産 — [GitHub Topics: video-editor (TypeScript)](https://github.com/topics/video-editor?l=typescript&o=asc&s=stars), 2026
- **CapCut有料化への市場反発** — TechSmith・Movavi・Kripesh Adwani等の比較記事が「CapCut代替」を体系的に整備、市場が「ポストCapCut」を真剣に探している段階 — [Top 7 CapCut Alternatives 2026 (TechSmith)](https://www.techsmith.com/blog/capcut-alternative/), 2026

---

## 🧩 関連概念・隣接分野

- **OpenCut**: OSSビデオエディタの本命。Clypraと真正面で競合する立ち位置。Next.js + Rust構成でモバイル対応も進める意欲的プロジェクト。
- **Kdenlive / Shotcut / OpenShot**: 老舗OSS動画エディタ。「実用に耐える」観点ではClypraより遥かに成熟。プロは依然これらを推奨。
- **LosslessCut**: 再エンコードなしでカット/トリムだけ高速処理。CapCutの「カット中心」ニーズには十分対応する別系統OSS。
- **DaVinci Resolve**: 商用クローズドソースだが**無料版が機能豊富**。プロ志向の代替として外せない。
- **Tauri**: Clypraの土台フレームワーク。Electron代替として注目され、2025〜26年に動画編集・IDE等の大型アプリでも採用例が増加。
- **FFmpeg**: 多くのOSS動画エディタの裏で動くライブラリ。「FFmpegを直接GUIで叩く」だけのアプローチ（ffmpeg-gui等）も別系統で存在。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（投稿者の立場）**:
  - **OSSでCapCutから自由になれる**こと自体に価値がある（プライバシー・透かし問題・ByteDance依存リスク）
  - Tauri + React/TSは**モダンな技術スタック**で、コミュニティ貢献しやすい
  - スペイン語圏の発信者が早期にClypraを紹介することで、**新興OSSの初期採用層**として機能できる
- **否定 / 慎重派の主張**:
  - **「CapCut全機能の代替」は誇張**: README自身が「プレミアム機能の無料実装に注力」と明記し、現時点では限定機能。CapCut Desktopの全機能（AIエフェクト・自動字幕・テンプレ等）には全く届かない
  - **★75は実用判断には早すぎる**: 同カテゴリの**OpenCut（★48.7k）**と比較して**約650倍の差**。コミュニティサポート・バグ修正速度・継続性の観点でClypraを本番採用は時期尚早
  - **そもそもCapCut Desktopは無料で使える**: 「金を払うな」と煽るが、**CapCut Desktopは基本機能無料**。有料はAI機能等の一部のみ。"使うな"と"金を払うな"を混同している
  - **「鵜呑み危険」のSNSバズ問題**: [[2026-05-06-dont-pay-ai-tool-alternatives|同日調査の14ペアリスト]] と同じ構造で、**新興OSSを実用レベルと誤認させる**コンテンツになりうる
  - **OpenCut/Kdenliveの方が筋が良い**: 真に「OSSでCapCut代替」を狙うなら**まずOpenCutかKdenlive**から検討すべき。Clypraは"見て応援するOSS"段階
- **中立的に見るときの補助線**:
  - **3層で評価する**:
    1. **「面白いOSSプロジェクトとして応援」** → Clypraを試す価値あり
    2. **「実用ツールとして移行」** → OpenCut / Kdenlive / Shotcut が現実解
    3. **「プロ向け代替」** → DaVinci Resolve無料版が依然強い
  - **CapCut課金疲れの本質はAI機能**: AI字幕・AI抽出・AIテンプレ生成のような「**AI機能の有料化**」が課金疲れの主因。OSSでこの部分を埋められるかは**まだ別問題**で、Clypra/OpenCutも追従中
  - **Tauri製アプリの将来性は高い**: Electron比でメモリ・起動速度に優れ、**5〜10年後に主流**になる可能性。Clypraの技術選定は2026年の流れに乗っている

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Clypra と OpenCut の **機能カバレッジ比較表**（実際にCapCutの何機能を再現できているか）
- [ ] Tauri製動画編集アプリの**メモリ・起動時間ベンチマーク**（vs Electron / vs ネイティブ）
- [ ] スペイン語圏インフルエンサー発のOSS紹介が**英語圏に逆輸入されるパスウェイ**の事例研究
- [ ] CapCut Desktopの**有料機能リスト**を整理し、OSSで代替不可能な部分を洗い出す
- [ ] 「OSS動画エディタ × AIエージェント（Claude Code / Codex）」での**自動編集ワークフロー**の可能性
- [ ] awesome-capcut-alternativesリポの**選定基準とメンテナンス頻度**

---

## 📚 参考資料

- [GitHub - AIEraDev/Clypra](https://github.com/AIEraDev/Clypra) — Clypra本体、★75・MITライセンス・Tauri構成の一次情報, 取得日 2026-05-06
- [GitHub - OpenCut-app/OpenCut](https://github.com/OpenCut-app/OpenCut) — OSS本命の★48.7kリポジトリ, 取得日 2026-05-06
- [4 Best Open Source CapCut Alternatives in 2026 (OpenAlternative)](https://openalternative.co/alternatives/capcut) — OSS体系比較, 取得日 2026-05-06
- [Top 7 CapCut Alternatives for Creators in 2026 (TechSmith)](https://www.techsmith.com/blog/capcut-alternative/) — CapCut有料化への市場反応, 取得日 2026-05-06
- [Best Apps Like CapCut in 2026 (Movavi)](https://www.movavi.com/learning-portal/apps-like-capcut.html) — 商用代替を含む15選, 取得日 2026-05-06
- [Best CapCut Alternatives 2026 (Miracamp)](https://www.miracamp.com/learn/capcut/best-alternatives) — 移行ガイド全般, 取得日 2026-05-06
- [GitHub - furudo-erika/awesome-capcut-alternatives](https://github.com/furudo-erika/awesome-capcut-alternatives) — OSSキュレーションリポ, 取得日 2026-05-06
- [GitHub Topics: video-editor (TypeScript)](https://github.com/topics/video-editor?l=typescript&o=asc&s=stars) — Tauri/React系動画エディタの群像, 取得日 2026-05-06
- [GitHub - puzzithinker/ffmpeg-gui](https://github.com/puzzithinker/ffmpeg-gui) — FFmpeg-GUI型の競合プロジェクト, 取得日 2026-05-06

---

## 🗒 メモ

- ツイートの**Likes 1,220 / RT 187**（スペイン語圏で）はバズの定量シグナル。**「英語圏で無名 → スペイン語圏で先行バズ」**は再現可能性のある現象で、自分も**スペイン語圏フォロワー獲得**を考えるなら参考になる構造。
- 投稿構成案（自分の対抗版・日本語）:
  - **「CapCutに金を払うな」じゃなく「CapCutに依存するな」が正解** — Clypra・OpenCut・Kdenliveの3択で**スコープ別の選び分け**を提示
  - 表形式で「★スター数・成熟度・カバー機能・プロ向け or 入門向け」を比較
  - **過剰なバズ煽りに対する"冷静なカウンター"** という建付けで差別化
- vault運用メモ：
  - 自分が動画編集に使うなら**OpenCut**を試す → vault内に記録
  - **awesome-capcut-alternatives** をブックマークして半年ごとにスター数推移を追う運用が取れる
  - `[[調査/2026-05-06-dont-pay-ai-tool-alternatives.md]]` で扱った「Descript→CapCut Desktop」とは**逆ベクトル**の代替提案。両者を組み合わせると「商用→CapCut→OSSへの2段移行」というストーリーが描ける
- スペイン語ポストを日本語化する際は、**「課金しないでOSSに乗り換えよう」を煽り過ぎない**ように注意。自分の信用残高を守るため**「現状の成熟度」をフェアに伝える**スタンスを取りたい。
