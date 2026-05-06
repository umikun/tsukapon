---
created: 2026-05-06
tags:
  - 調査
  - Microsoft
  - Copilot
  - AI-agent
  - Anthropic
  - Claude
source: https://x.com/satyanadella/status/2051712533174931707
action: 採用なし
---

# Satya Nadella の "Copilot Cowork モバイル/Skills/Plugins" 発表を読み解く

> [!summary] TL;DR
> - Microsoft が **Copilot Cowork** を iOS/Android に解放し、再利用可能な「Skills」と業務システム連携の「Plugins/Connectors」を追加（2026-05-05 発表）。要は **「複数アプリをまたぐ長時間タスクをスマホから委任 → デスクで結果を回収」** が現実になった
> - **中身は Anthropic Claude 製**。OpenAI 一本足だった Copilot は "model diversity" 路線に切り替わり、2025-11 の **Azure × Anthropic 300億ドル契約** がこれを支えるインフラだった
> - ただし現時点は **Frontier プログラム（実験ティア）限定**＋**E7 バンドル $99/user/month**、ローカルファイル不可・200MB上限・幻覚リスク等の運用制約あり。GA は **2026-07 Microsoft Inspire** 狙い

---

## 📌 元テキスト（抜粋）

> New in Copilot Cowork: mobile, skills, and plugins. Now available on iOS and Android, so you can delegate work from your phone, pick it back up on your desktop, and keep tasks moving without breaking flow. And with new connectors, Cowork can operate across business systems and data.

出典: [Satya Nadella @satyanadella](https://x.com/satyanadella/status/2051712533174931707) — 2026-05-05 17:16 UTC、272K views / 2.2K likes / 286 RT
添付: 33.8 秒のプロモ動画（1920×1080）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Copilot Cowork** | M365 内で「長時間・複数ステップのタスク」を AI に委任し、人間は途中介入で steer するエージェント機能 | "Copilot Cowork" "Frontier" |
| **Frontier プログラム** | Microsoft 365 の3層リリースモデル（Frontier / Standard / Deferred）の最上流。実験的機能の早期アクセス層 | "Microsoft 365 Frontier" "Wave 3" |
| **Microsoft 365 E7** | E5 + Copilot + Agent 365 を統合した新フラッグシップ SKU。$99/user/month、2026-05-01 GA | "M365 E7" "Frontier Suite" |
| **Skills（Cowork）** | 「やり方の手順書」を再利用可能な命令セットとして保存し Cowork に適用する仕組み | "Cowork Skills" "reusable instructions" |
| **Plugins / Connectors** | Power BI・Dynamics 365・HubSpot・Notion 等、業務システムへ Cowork から到達するための拡張点 | "Cowork connectors" "M365 plugins" |
| **Work IQ** | Outlook/Teams/Excel 等のシグナルを横断する Microsoft 独自のコンテキスト層。Cowork のグラウンディング基盤 | "Work IQ" Microsoft |
| **Agent 365** | エージェントを ID・権限・コンプライアンス境界の中で運用する管理プレーン | "Agent 365" Microsoft |
| **Researcher（M365 Copilot）** | 同 Copilot 内の別エージェント。Claude / OpenAI を使い分ける深掘りリサーチ用 | "Researcher Copilot Anthropic" |

---

## 🧭 背景 / なぜ今これが話題なのか

**1. 流れは「会話する Copilot → 動く Copilot」への移行**
2023〜2025 の Copilot は「サイドバーで Q&A する助手」だった。2026-03-09 の **Wave 3** で Microsoft は方針を切り替え、複数ステップを自走する **Cowork** を発表。3月末に Frontier プログラムで広く試せるようになり、5月にモバイル + Skills + Plugins まで一気に開いた、というのが今回のツイートの流れ。

**2. 中身が Anthropic Claude というのが最大のニュース性**
ローンチ時点から Cowork は **Anthropic の Claude モデル** で動いている。2025-11 に Microsoft は **Azure コンピュートで $30B（約4.5兆円）規模の Anthropic 契約**を結び、Claude を Azure 上でエンタープライズ規模に走らせる土台を作った。Researcher 機能側でも OpenAI と Anthropic を切り替えるマルチモデル化が進んでおり、「OpenAI 一本足」だった Copilot は明確に転換している。

**3. E7 という新 SKU で課金導線が固まった**
2026-05-01 に **Microsoft 365 E7** が GA。E5 に Copilot と Agent 365 を統合し $99/user/month。Cowork は基本この E7（ないし Frontier 参加者）に紐付く。ChatGPT Enterprise や Gemini Enterprise との「人月単価で殴り合う」フェーズに入ったと見ていい。

**4. なぜ "モバイル" がそんなに重要なのか**
Cowork はクラウドで走るので **PC を開きっぱなしにする必要がない**。「通勤電車で iPhone から Q2 営業数字をまとめてリーダーシップに 15時までにメール」と音声で投げ、デスクに着いた頃には PowerPoint と送信済みメールが揃っている、というのが Microsoft の描く絵。**スマホは「指示の入口」、デスクトップは「結果の検収口」**。これが従来の "AI チャットアプリ" と Cowork を決定的に分ける UX 設計。

**5. Skills と Plugins がもたらすロックイン**
Skills は組織ごとの「やり方」を Cowork に貯めていく仕組み。**運用が長引くほど他社製エージェントに乗り換えるコストが累積する** — Microsoft の本丸はここ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| iOS/Android で利用可能になった | Frontier 参加者向けに TestFlight / Google Play Beta で展開、GA は 2026-07 Microsoft Inspire 予定 | [Neowin](https://www.neowin.net/news/microsoft-brings-copilot-cowork-to-ios-and-android-adds-skills-and-plugins/), [Thurrott](https://www.thurrott.com/a-i/335689/microsofts-copilot-cowork-agent-mobile-plugins-support) | ⚠️ ほぼ一致（"今すぐ全員" ではなく Frontier ベータ段階） |
| スマホで委任しデスクで継続 | クラウド実行のため端末をまたいで進捗が保持される、と公式ブログが明言 | [Microsoft 365 Blog 2026-05-05](https://www.microsoft.com/en-us/microsoft-365/blog/2026/05/05/copilot-cowork-from-conversation-to-action-across-skills-integrations-and-devices/) | ✅ 一致 |
| 新コネクタで業務システム横断 | HubSpot / LSEG / Moody's / Notion が公開済み、Miro / monday.com / S&P Global Energy 等が "coming soon" | 同上 + [Windows News](https://windowsnews.ai/article/microsofts-copilot-cowork-expands-to-ios-and-android-with-reusable-skills-and-deep-integrations.416571) | ⚠️ ほぼ一致（一部はまだ "coming soon"） |
| Cowork が「動くエージェント」 | 計画立案 → 確認質問 → 実行までを自動。ただし高インパクトな操作は人間の承認を要求する設計 | [Microsoft Learn — Cowork overview](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/) | ✅ 一致 |
| （ツイートでは触れていないが）Claude 製である | Cowork は Anthropic Claude モデルで動作 | [Fortune](https://fortune.com/2026/03/09/microsoft-copilot-cowork-ai-agents-anthropic-e7-m365-saas/), [Windows Central](https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/this-is-microsoft-new-copilot-cowork-ai) | ✅ 一致（広報的にはあえて目立たせていない） |

---

## 🌐 最新動向（2026-05-06 時点）

- **2026-05-05**: Cowork、iOS / Android に解放（Frontier 限定ベータ）。Skills と Plugins が同時公開 — [Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/05/05/copilot-cowork-from-conversation-to-action-across-skills-integrations-and-devices/), 2026-05
- **2026-05-01**: **Microsoft 365 E7** と **Agent 365** が GA。E5 + Copilot + Agent 365 を $99/user/month に統合 — [Topedia Blog](https://blog-en.topedia.com/2026/04/new-three-tier-release-model-for-microsoft-365-starting-with-copilot/), 2026-04
- **2026-04-21**: Frontier 変革をパートナーエコシステムで加速する公式発表（SI/コンサル経由の導入支援強化）— [Microsoft Blog](https://blogs.microsoft.com/blog/2026/04/21/accelerating-frontier-transformation-with-microsoft-partners/), 2026-04
- **2026-04**: M365 Copilot に **Anthropic Claude Opus 4.7** が利用可能に。Researcher / メインチャットの両方で Claude を選択できる体制が固まった — [Microsoft Tech Community](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/available-today-anthropic-claude-opus-4-7-in-microsoft-365-copilot/4511666), 2026-04
- **2026-03-30**: Cowork が Research Preview から Frontier プログラムに昇格、E5 上のアドオンとして広く試せるように — [Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/30/copilot-cowork-now-available-in-frontier/), 2026-03
- **2026-03-09**: Wave 3 で Cowork 初公開、E7 バンドルを発表 — [Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/09/copilot-cowork-a-new-way-of-getting-work-done/), 2026-03
- **2025-11**: Microsoft × Anthropic が Azure コンピュートで **$30B 契約**。これが現在の Cowork インフラの基礎 — [Fortune](https://fortune.com/2026/03/09/microsoft-copilot-cowork-ai-agents-anthropic-e7-m365-saas/), 2026-03

---

## 🧩 関連概念・隣接分野

- **Anthropic 自身の Claude Cowork**: 同名だが別物。Anthropic 純正は**デスクトップ専用**で、Microsoft 版が iOS/Android/Web を持つ。今回の発表で UX 面では Microsoft が一歩リード
- **OpenAI ChatGPT Agent / GPT-5**: 「データの場所を選ばない（Slack/Dropbox/Notion 横断）」がウリ。M365 ロックインを嫌う組織にとっての対抗馬
- **Google Gemini 3.x Agent Mode**: 100万トークンの長コンテキスト + Workspace 統合。"Workspace 純正で完結する" 案件で強い
- **Microsoft Researcher エージェント**: Cowork と同じ M365 Copilot 内のもう1つのエージェントで、深掘り調査が用途。Cowork が "実行"、Researcher が "調査" という役割分担
- **MCP（Model Context Protocol）**: Plugins/Connectors の隣接概念。「業務システムにエージェントが安全に到達する標準プロトコル」という同じ問題を、Anthropic 側はオープンに解こうとしている
- **Work IQ**: Cowork が Outlook/Teams/Excel をまたいで "今この人の仕事" を理解する基盤層。これが M365 内データを持つ組織だけが Cowork で得られる強み

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - 「人間の `承認 → 実行` を保ったままタスクを並列化できる」「監査ログ・ID・権限が M365 の枠内で機能するので、独立 SaaS の AI エージェントより統制しやすい」
  - エージェントが**間違える複数アプリ**にまたがって正しく動けるのは、データ・ID 基盤を持つ Microsoft の構造的優位

- **否定 / 慎重派の主張**:
  - **ローカルファイル不可・200MB 上限・暗号化ファイル不可** で「OneDrive/SharePoint に乗っている仕事」しか自動化できず、レガシー業務は射程外（[xenoss.io](https://xenoss.io/blog/microsoft-copilot-enterprise-limitations) ほか）
  - Outlook/Teams/Excel をまたいで動くエージェントは **複数アプリで同時に間違える**。承認ワークフロー・ロールバック手順・権限スコープを設計する IT コストが Cowork 導入前に発生する
  - **値段が見えにくい**: 単体価格は非公開で実質 E7 ($99/user/month) を買う絵。E5 から E7 への跳ね上がりを正当化するだけの ROI を測るのは初期段階だと難しい
  - **Skills のロックイン**: 自社の "やり方" を Microsoft 環境に貯めれば貯めるほど他社エージェントへの移行コストが上がる
  - **モデル選択の不透明さ**: Cowork が Claude で動いていることは Microsoft 側ブログでは控えめな扱い。"どのタスクでどのモデルが走ったか" の説明責任は今後の論点

- **中立的に見るときの補助線**:
  - 「Cowork で全部できる」ではなく **「監査要件を満たす範囲で、メール/ドキュメント/会議要約系の定型ワークフローを 5〜10 個 Skill 化する」** あたりが現実解。最初から E7 を全社展開しない
  - スマホ起点 UX は便利だが、**最初の数ヶ月は "送信前必ず確認" で運用**しないと、移動中の音声指示が誤動作する事故が確実に起きる

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Cowork の Skills は **個人単位 / チーム単位 / テナント単位** のどの粒度で共有・再利用されるのか（ガバナンス上の論点）
- [ ] Anthropic Claude を使っている事実が、ユーザー側 UI / 監査ログでどう表示されるのか（モデル選択の透明性）
- [ ] **Agent 365** と Cowork の境界はどこか — Cowork は「Agent 365 上で走る公式エージェントの 1つ」という整理でいいのか
- [ ] Microsoft Inspire 2026-07 で発表されると目される **GA 時点の正式価格**（E7 同梱で押し切るのか、Cowork 単体 SKU が出るのか）
- [ ] 競合の **Anthropic Claude Cowork** がモバイル展開を追従するか、オープン路線（MCP / 任意データソース接続）で差別化するか
- [ ] 国内エンプラ（特に SI 経由導入）で **日本語タスク委任** の実用度がどこまで来ているか — 実運用レポートが出始めるのは 2026-Q3 以降か

---

## 📚 参考資料

- [Copilot Cowork: From conversation to action across skills, integrations, and devices](https://www.microsoft.com/en-us/microsoft-365/blog/2026/05/05/copilot-cowork-from-conversation-to-action-across-skills-integrations-and-devices/) — 2026-05-05 公式発表（Skills/Plugins/モバイルの一次ソース）, 取得日 2026-05-06
- [Microsoft brings Copilot Cowork to iOS and Android, adds Skills and plugins — Neowin](https://www.neowin.net/news/microsoft-brings-copilot-cowork-to-ios-and-android-adds-skills-and-plugins/) — モバイル展開のリリース時期（GA は 2026-07 Microsoft Inspire 狙い）裏取り, 取得日 2026-05-06
- [Microsoft's Copilot Cowork Agent Launches on Mobile and Adds Plugins Support — Thurrott](https://www.thurrott.com/a-i/335689/microsofts-copilot-cowork-agent-mobile-plugins-support) — エンタープライズ視点の解説と利用シナリオ, 取得日 2026-05-06
- [Microsoft debuts Copilot Cowork built with Anthropic's help and E7 software suite — Fortune](https://fortune.com/2026/03/09/microsoft-copilot-cowork-ai-agents-anthropic-e7-m365-saas/) — Anthropic との $30B 契約と Cowork の関係を裏取り, 取得日 2026-05-06
- [This is Microsoft's new "Copilot Cowork" — Windows Central](https://www.windowscentral.com/artificial-intelligence/microsoft-copilot/this-is-microsoft-new-copilot-cowork-ai) — Cowork が Claude モデルで動く点を確認, 取得日 2026-05-06
- [Powering Frontier Transformation with Copilot and agents — Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/03/09/powering-frontier-transformation-with-copilot-and-agents/) — Wave 3 全体像と Frontier プログラムの位置づけ, 取得日 2026-05-06
- [Copilot Cowork overview (Frontier) — Microsoft Learn](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/) — 公式ドキュメント。タスク承認モデル・対応アプリ範囲, 取得日 2026-05-06
- [Microsoft Copilot in enterprise: Limitations and best practices — Xenoss](https://xenoss.io/blog/microsoft-copilot-enterprise-limitations) — ローカルファイル/200MB/暗号化ファイル等の制限を裏取り, 取得日 2026-05-06
- [New three-tier release model for Microsoft 365 — Topedia Blog](https://blog-en.topedia.com/2026/04/new-three-tier-release-model-for-microsoft-365-starting-with-copilot/) — Frontier / Standard / Deferred の三層モデル, 取得日 2026-05-06
- [Available today: Anthropic Claude Opus 4.7 in Microsoft 365 Copilot — Microsoft Tech Community](https://techcommunity.microsoft.com/blog/microsoft365copilotblog/available-today-anthropic-claude-opus-4-7-in-microsoft-365-copilot/4511666) — Claude Opus 4.7 が Copilot で利用可能になった経緯, 取得日 2026-05-06

---

## 🗒 メモ

- 「Copilot は OpenAI で動く」という 2024-25 の常識は、2026 時点で **完全に過去の話**。実態は **マルチモデル化**で、Cowork は Anthropic、Researcher は両刀、メインチャットも切替可。**「Microsoft = OpenAI ラッパー」というフレームで Copilot を語ると間違える**
- 自分のクライアント案件で Cowork を提案するなら、**最初の Skill は「請求書ドラフト確認 → 経理に共有」のような短いループから**。いきなり営業フォローアップを丸投げさせない
- X 投稿の素材としては **「Microsoft 公式が Claude を使い始めた件、ツイートでは目立たせないけど技術ブログを掘ると明白」** が刺さる切り口。AI 業界マップの再描画ネタとして強い
- 自分の vault 運用で言えば、Cowork の "Skills" 概念は Claudian の `.claude/commands/` の発想と同じ。**「組織の作業手順を再利用可能にする」は エンプラ AI の共通本流**になりつつある
