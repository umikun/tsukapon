---
created: 2026-05-03
tags: [調査, syswatch, rust, tui, system-monitor, mac-utility, sre]
source: "[[Clippings/Post by @QingQ77 on X.md]]"
---

# Rust製TUI システム診断ツール syswatch — 中身は本物、ただし "代替" 戦線は思ったより混雑している

> **TL;DR**
> 紹介された `matthart1983/syswatch` は **実在し、説明は概ね正確**。Rust製・cross-platform sysinfo ベース・12タブ（CPU/メモリ/ディスク/GPU/電源/サービス/ネットワーク等）・**Insights** で異常を平易な英語で説明・**Timeline** でセッション中の任意時点へ巻き戻し・**読み取り専用**（プロセス kill や設定変更しない）・更新時CPU 0.5%以下、すべて公式 README とコードで確認できる。開発者 Matt Hartley は Sydney 在住の SRE系エンジニア（Westpac勤務、低レイテンシトレーディング系の経歴、姉妹ツール netwatch / essh あり）。**ただし元ポストの "もう htop / iostat / nettop を山ほど開く必要なし" は誇張**: btop / bottom / glances / zenith / xtop / mactop / NeoHtop / **Below**（Meta 製・time-travel機能あり）等の競合がすでに群雄割拠で、syswatch は **新規参入の有力候補1つ** が正確な位置づけ。差別化の本命は ① Insights の **平易な英語での異常説明**、② Timeline の **scrubber UX**、③ macOS と Linux で同じ12タブ全部レンダリングする統一体験 の3点。Mac で1個 TUI モニタを試すなら btop / bottom / mactop で十分実用、syswatch は **"異常検知＋時系列再生" を求める SRE / 開発者向けの新世代** として評価する位置づけが妥当。

## 📌 元テキスト（抜粋）

> ターミナル一つで単機診断を完結。もう htop、iostat、nettop を山ほど開く必要なし。
> https://github.com/matthart1983/syswatch
> Rust で書かれたシステム診断 TUI。12個のタブページで CPU、メモリ、ディスク、GPU、電源、サービス、ネットワークなどをカバー。macOS と Linux の両方で動作。Insights ページは異常（スワップの揺らぎ、ゾンビプロセス、ディスク満杯など）を自動検知して、わかりやすい言葉で問題を教えてくれる。Timeline ページではタイムラインをドラッグして、セッション全体の任意の時点の状態を振り返れる。読み取り専用で、プロセスを殺したり設定を変更したりしない。更新時の CPU 使用率は 0.5% 以下に抑えられている。

出典: [[Clippings/Post by @QingQ77 on X.md]] / [元ポスト](https://x.com/QingQ77/status/2050550873550717420)（@QingQ77, 2026-05-02）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| syswatch | matthart1983 製の Rust TUI 単機診断ツール | github matthart1983 syswatch |
| TUI (Text User Interface) | ターミナル内で動くフルスクリーンUI | tui terminal user interface |
| sysinfo | Rust製のクロスプラットフォーム system info ライブラリ | sysinfo crate rust |
| ratatui | Rust の TUI フレームワーク（旧tui-rs） | ratatui rust |
| htop | 老舗の対話的プロセスモニタ（C製） | htop linux |
| iostat | ディスクI/O統計コマンド | iostat |
| nettop | macOS純正のプロセス別ネットワーク監視 | macos nettop |
| btop | C++ 製のリッチTUI モニタ | btop btop++ |
| bottom (btm) | Rust製 TUI モニタ。クロスプラットフォーム | bottom rust btm |
| glances | Python製のクロスプラットフォーム監視ツール | glances python |
| Below | Meta製の時間軸再生機能を持つLinux監視 | below meta facebook |
| mactop | macOS専用 htop風モニタ | mactop macos |
| Stats | macOSメニューバー常駐のOSS監視 | stats menubar macos |
| anomaly detection | "異常" を自動検知する機能 | anomaly detection sre |

---

## 🧭 背景 / なぜ今これが話題なのか

**2010年代: top → htop → btop の系譜**
top（標準）→ htop（インタラクティブ、2004〜）→ btop / btop++（C++、リッチUI、2020〜）と進化。Linuxでは btop が事実上の準標準。

**2018〜2022年: Rust製TUIモニタの興隆**
**bottom (btm)**（2019〜、Rust）、**ytop**（2019〜、Rustだが現在は archived）、**zenith**（2019〜、Rust、ズーム可能チャート）など、Rust 製の TUI モニタが続々登場。GoやC++ よりメモリ安全＋並行性の素直さでこのジャンルとの相性◎。

**2023年: Meta が `below` を OSS化**
[Meta製 below](https://github.com/facebookincubator/below) が **時間軸の "再生"** という新機軸を提供。"システム状態を継続記録 → 過去任意時点に戻れる" というUXを SRE 業界に普及させた重要なリファレンス。

**2024〜2025年: macOS Apple Silicon 対応の波**
M1/M2/M3 普及で macOS でも CPU/GPU/Power の細かい計測ニーズ増加。**mactop**（Apple Siliconフルサポート）、**NeoHtop**（Tauri+Svelte）、**Stats**（メニューバーOSS）等が登場。`powermetrics` を要 sudo で叩く課題への代替策が複数並行開発。

**2026年: ratatui ベースの新世代TUI モニタが量産期**
ratatui（旧tui-rs）の成熟で個人開発でも本格的なTUI が作れる時代に。`xtop`（btop-inspired）、`syswatch`（本記事対象）等が2026年Q1〜Q2に登場。**個人エンジニアの "自分の業務で必要だったから作った" 系** のツールが急増。

**今回の元ポスト（2026-05-02 @QingQ77）の文脈**
@QingQ77 はターミナル系/Rust 系の中華圏発信アカウント。投稿は **既存ツール（htop/iostat/nettop）を多数開く煩雑さに対する解** として syswatch を紹介する素直なトーン。前項のような "事件" "速報" "史上最高" 系の煽りは無く、**機能説明は概ね事実通り**。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「Rust で書かれたシステム診断 TUI」 | リポは Rust 1.75+ 必須、ratatui + sysinfo ベース。事実 | [GitHub: matthart1983/syswatch](https://github.com/matthart1983/syswatch) / [Cargo.toml](https://github.com/matthart1983/syswatch/blob/main/Cargo.toml) | ✅ 一致 |
| 「12個のタブページで CPU、メモリ、ディスク、GPU、電源、サービス、ネットワークなどをカバー」 | 公式README 確認、12タブ実装済み（CPU/memory/disks/processes/GPU/power/services/network + Timeline scrubber + Insights anomaly engine 等） | [GitHub: syswatch README](https://github.com/matthart1983/syswatch) | ✅ 一致 |
| 「macOS と Linux の両方で動作」 | 全12タブが macOS と Linux で実データレンダリング。Linux は無依存、macOS は system frameworks にリンク | [syswatch README](https://github.com/matthart1983/syswatch) | ✅ 一致 |
| 「Insights ページは異常（スワップの揺らぎ、ゾンビプロセス、ディスク満杯など）を自動検知して、わかりやすい言葉で問題を教えてくれる」 | Insights anomaly engine として実装。"plain English insights" は公式の主要訴求点 | [syswatch README](https://github.com/matthart1983/syswatch) | ✅ 一致 |
| 「Timeline ページではタイムラインをドラッグして、セッション全体の任意の時点の状態を振り返れる」 | "Session scrubber" として実装。Below とコンセプトが近い（ただし Below は永続記録、syswatch は "セッション中" のメモリ保持） | [syswatch README](https://github.com/matthart1983/syswatch) | ✅ 一致 |
| 「読み取り専用で、プロセスを殺したり設定を変更したりしない」 | 公式に "read-only" 設計を明記。htop/btop のような kill 機能は意図的に省略している | [syswatch README](https://github.com/matthart1983/syswatch) | ✅ 一致 |
| 「更新時の CPU 使用率は 0.5% 以下に抑えられている」 | README の主要な性能訴求。実測条件・サンプリング間隔の細かい記載は要確認 | [syswatch README](https://github.com/matthart1983/syswatch) | ⚠️ ほぼ一致（条件次第） |
| 「もう htop、iostat、nettop を山ほど開く必要なし」 | syswatch でこれら3つを統合できるのは事実。ただし **同等以上の統合機能を持つ btop / bottom / glances / Below 等が既に存在** していて "1つで全部" の謳い文句は syswatch 固有ではない | [GitHub: btop](https://github.com/aristocratos/btop) / [GitHub: bottom](https://github.com/ClementTsang/bottom) | ⚠️ ほぼ一致（誇張は穏やかにあり） |

---

## 🌐 最新動向（2026-05-03時点）

- **syswatch v0.x（最新）が2026年Q2リリース**: ratatui + sysinfo ベース、cargo install or build from source で導入。星数・スポンサー数はまだ少ないが活発に開発中 — [syswatch Releases](https://github.com/matthart1983/syswatch/releases), 2026
- **同じ matthart1983 の姉妹ツール群**: `netwatch`（リアルタイムネットワーク診断）、`essh`（拡張SSHクライアント）と連携して "ターミナル中心の SRE ワークフロー" を構築する設計思想 — [matthart1983 GitHub](https://github.com/matthart1983), 2026
- **Below (Meta製) が時間軸再生機能の先行リファレンス**: SRE業界では "below = time-travel" が定着。syswatch の Timeline scrubber は同コンセプトのライト版（セッション内に限定） — [The Tech Basket: Best TUI Apps 2026](https://www.thetechbasket.com/best-tui-apps/), 2026
- **xtop（xscriptor製）が同時期に登場**: btop-inspired、ratatui + sysinfo の同じスタック、cross-platform。syswatch とエコシステム的に直接競合 — [GitHub: xscriptor/xtop](https://github.com/xscriptor/xtop), 2026
- **mactop が macOS Apple Silicon フルサポート**: M1/M2/M3 ネイティブで CPU/メモリ/プロセス監視＋kill 操作可。"macOS で1個" を求めるなら mactop が現状の有力候補 — [AlternativeTo: htop alternatives 2026](https://alternativeto.net/software/htop/), 2026
- **NeoHtop (Rust+Tauri+Svelte) も並走**: TUI ではなく desktop app。Rust製エコシステムの "TUI vs GUI" の選択肢が揃ってきた — [NeoHtop](https://abdenasser.github.io/neohtop/), 2026

---

## 🧩 関連概念・隣接分野

- **htop / btop / bottom / glances / zenith / xtop**: 各々の老舗・準標準。syswatch を採用する前にこれらと比較するのが筋
- **Below (Meta)**: 時間軸再生の先行リファレンス。syswatch Timeline scrubber のコンセプト元と推定
- **mactop / NeoHtop / Stats / iStatistica**: macOS固有の監視ツール群。syswatch と棲み分け
- **netwatch / essh (matthart1983 sibling)**: 同じ作者の姉妹ツール。組み合わせて使う設計思想
- **sysinfo crate / ratatui crate**: Rust エコシステムの共通基盤。syswatch / xtop / bottom 等は同じスタックを使うため、機能差は実装次第
- **OpenTelemetry / Prometheus + Grafana**: 多ホストや本番系の監視はこちら。syswatch は "**単機・対話的・即時診断**" 用途に特化（README の "Single-host" 明記）

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（=元ポストの立場）**:
  - 12タブで Mac/Linux 両対応、Insights と Timeline が魅力的
  - 既存ツールを複数開く煩雑さは確かに実在し、統合UI のメリットは大きい
  - Read-only 設計で "間違って kill" 事故ゼロ、SREの安全運用に合う

- **否定 / 慎重派の主張**:
  - **"htop/iostat/nettop を山ほど開く必要なし" は誇張**: btop / bottom / glances がすでに同等以上の統合UI を提供。syswatch 固有のメリットではない
  - **新規ツールの安定性リスク**: 星数・コントリビュータ数が少なく、半年後・1年後にメンテされ続けるかは不透明。**bottom / btop は数年安定** で長期運用には現状そちらが安全
  - **Read-only は両刃の剣**: kill / nice / renice したい SRE 用途には不足。htop / btop の利便性を犠牲にしている
  - **Timeline は "セッション中" 限定**: Below のように **永続記録 + 任意時刻再生** ではないため、"システム障害の事後解析" には使えない
  - **Insights の "plain English" は LLM ではなくルールベース**: 細かい異常パターンの拡張性は限定的。現状 README に書かれた "swap thrash / zombie processes / disk full" 等の典型ケース中心
  - **macOS で powermetrics や sudo 必要箇所の挙動** が README から読み取りにくい。実機検証必要

- **中立的に見るときの補助線**:
  - **"今すぐ実運用で安定的に使う" なら**: btop（Linux）/ bottom（cross-platform）/ mactop（macOS）が現状最有力
  - **"異常検知＋時系列再生のUX を試したい" なら**: syswatch 試す価値あり、ただし **Below との比較** を必ずする（Below が永続記録で本格、syswatch がセッション内で軽量）
  - **作者・姉妹ツール・設計思想**: matthart1983 は実在の SRE で、netwatch / essh と組み合わせる "ターミナル中心SRE" のビジョンは明確。**長期的には支援する価値ある個人開発**
  - **判定軸の明確化**: 「**統合UI が欲しい**」→ btop / bottom 優先、「**異常検知** 機能が欲しい」→ syswatch / Below、「**過去再生** が欲しい」→ Below 優先、「**macOS 固有最適化**」→ mactop

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] syswatch の Timeline scrubber は **どれくらいの時間範囲** をメモリ保持するか（README に記載があるか要確認）
- [ ] Insights anomaly engine の検知ルールは **拡張可能か**（カスタムルール定義のAPI有無）
- [ ] Below と syswatch を併用する SRE ワークフローの実例（永続記録は Below、リアルタイム対話は syswatch、等）
- [ ] macOS の `powermetrics`（要sudo）相当のデータを syswatch がどう取得しているか（fallback or 制限事項）
- [ ] Apple Silicon の **GPU タブ** の精度（M1/M2/M3 でMetal GPU 使用率を正確に取れているか）
- [ ] xtop / syswatch / bottom / btop の **実消費メモリ・CPU・スタートアップ時間** のベンチマーク

---

## 📚 参考資料

- [GitHub: matthart1983/syswatch](https://github.com/matthart1983/syswatch) — 公式リポジトリ。機能・動作環境の一次情報, 取得日 2026-05-03
- [syswatch Cargo.toml](https://github.com/matthart1983/syswatch/blob/main/Cargo.toml) — Rust 1.75+ 必須・ratatui/sysinfo 依存の確認, 取得日 2026-05-03
- [syswatch Releases](https://github.com/matthart1983/syswatch/releases) — リリース活動状況の確認, 取得日 2026-05-03
- [matthart1983 GitHub プロフィール](https://github.com/matthart1983) — 作者と姉妹ツール（netwatch, essh）の確認, 取得日 2026-05-03
- [GitHub: matthart1983/netwatch](https://github.com/matthart1983/netwatch) — 姉妹ツール、ネットワーク特化, 取得日 2026-05-03
- [GitHub: aristocratos/btop](https://github.com/aristocratos/btop) — 競合: C++製の準標準TUIモニタ, 取得日 2026-05-03
- [GitHub: ClementTsang/bottom](https://github.com/ClementTsang/bottom) — 競合: Rust製クロスプラットフォーム, 取得日 2026-05-03
- [GitHub: facebookincubator/below](https://github.com/facebookincubator/below) — 競合: Meta製、時間軸再生の先行例, 取得日 2026-05-03
- [GitHub: xscriptor/xtop](https://github.com/xscriptor/xtop) — 競合: btop-inspired Rust TUI, 取得日 2026-05-03
- [Comparing Alternatives to top Written in Rust (Wesley Moore)](https://www.wezm.net/v2/posts/2020/rust-top-alternatives/) — Rust製top代替の比較記事（古め）, 取得日 2026-05-03
- [9 System Monitoring Tools for Linux That are Better Than Top (It's FOSS)](https://itsfoss.com/linux-system-monitoring-tools/) — Linuxモニタの全体像, 取得日 2026-05-03
- [The Tech Basket: Best TUI Apps for Linux Developers 2026](https://www.thetechbasket.com/best-tui-apps/) — 2026年TUI概観, 取得日 2026-05-03
- [Mac Performance Monitor Guide (MoniThor)](https://monithor.dev/guides/mac-performance-monitor) — macOSの top/iostat/nettop/powermetrics の解説, 取得日 2026-05-03
- [Stats — Free macOS Menu Bar System Monitor](https://mac-stats.com/) — macOS GUIメニューバー監視ツール, 取得日 2026-05-03
- [NeoHtop](https://abdenasser.github.io/neohtop/) — Rust+Tauri+Svelte のデスクトップ版, 取得日 2026-05-03

---

## 🗒 メモ

- **本日の "煽り解剖" シリーズの中で唯一 "穏当な紹介投稿"**: 本ポストは数字捏造・規約違反・誇張表現がほぼ無く、紹介として真っ当。**「全部嘘ばかりではない」サンプル** として批評型コンテンツの中で対比に使える
- **Tsukapon vault 運用への適合性**: 自分（Mac開発者）が試すなら、まず btop / mactop / bottom と並行で1週間試してから採用判断するのが正解。**vault 内のスキル `daily-summary` 等で `_ kiwami/tools/daily-log/` 監視に組み合わせる発想** もあり
- **批評型ロング解説の素材**: [[SNS運用/note/_メンバーシップ準備ロードマップ.md]] のネタプール枠 "実装ツール紹介" に登録価値あり。切り口候補:
  - 「Mac で TUI システムモニタを1個選ぶならどれか — btop / bottom / mactop / syswatch ガチ比較」
  - 「煽らない紹介投稿の見分け方 — 良い投稿の3つの特徴（数字検証可・代替を否定しない・作者バックグラウンド明示）」
  - 「個人開発OSS の "賞味期限" を見極める3指標 — 星数 / 更新頻度 / 姉妹ツール群」
- **note記事の応用**: 本日の他4本（KDP $214k嘘 / kepano盛り / Voice-Pro盛り / iOS-test盛り / 10リポ盛り）と対比して、**"煽る投稿 vs 穏当な紹介投稿の見分け方"** の note 記事1本書ける。**煽る側ばかり批判すると視野が狭く見える** ので、こういう "良い投稿" を1本混ぜるとバランスが取れる
- **連投シリーズへの転用**: "X で見かけたAIツール紹介の見分け方" 連投の "良い例" として組み込み可能
- **ルーチンB対象**: @QingQ77 は穏当な紹介系インフルエンサーなので **批評対象ではなく、共感・拡散・対話の対象** として観察。批評型リプじゃなく **"いいね＋引用補足"** タイプの軽い反応が向いている
- **本日6本連続調査ノートの締めくくりとして良い位置取り**: "煽り 5本 + 穏当 1本" のバランスで、**自分自身が "ただの煽り批判家" にならない** ためのアンカー
