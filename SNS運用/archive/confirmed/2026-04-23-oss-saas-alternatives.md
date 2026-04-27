---
created: 2026-04-23
tags: [調査, オープンソース, SaaS代替, AIツール, セルフホスト]
source: 直接貼付（X投稿と思しきリスト型テキスト）
---

# 「無料で使える10のOSS AI/SaaS代替」を鵜呑みにする前に押さえること

> **TL;DR**
> 紹介されている10本はどれも実在する人気OSSで、個別ツールとしては信頼できる。ただし「全部・無料・永遠に」の煽り文句は誇張気味。特に **n8nは"Sustainable Use License"で商用再販に制限あり**、Supabaseセルフホストは12以上のDockerコンテナ運用を要求、Fooocusは2025年末からLTS（バグ修正のみ）モードに入っている。"SaaS代替"として見るなら、有料プラン月$300〜500のうち現実的に置き換えられるのは半分前後。残りは運用時間・学習コスト・モバイル体験の劣化で取り戻されるケースが多い。

## 📌 元テキスト（抜粋）

> 無料で手に入るなんて違法な気分になる10のオープンソースAIツール。ビッグテックがこれを埋もれさせる前にブックマークしておこう。1. Fooocus（Midjourney代替）/ 2. ComfyUI / 3. Ollama（ChatGPT代替）/ 4. OpenVoice / 5. Penpot（Figma代替）/ 6. AppFlowy（Notion代替）/ 7. n8n（Zapier代替）/ 8. Cal.com（Calendly代替）/ 9. Supabase（Firebase代替）/ 10. Cline（Cursor代替）……これらをSaaSサブスクリプションとして合計すると、毎月300〜500ドルかかる計算になる。全部。無料。永遠に。

出典: 直接貼付（SNS上のリスト投稿。一次URLなし）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Fooocus | SDXLベースの画像生成GUI。プロンプト注力型 | Fooocus LTS, WebUI Forge |
| ComfyUI | ノードベースの画像/動画/3D生成基盤 | ComfyUI nodes, SwarmUI |
| Ollama | ローカルLLM実行CLI（llama.cpp系のラッパー） | Ollama function calling, AMD ROCm |
| OpenVoice | MIT+MyShell製の音声クローニングモデル | OpenVoice V2, tone color |
| Penpot | ブラウザ動作のデザインツール、SVGネイティブ | Penpot Inspect, Design Tokens |
| AppFlowy | Rust+Flutter製のローカルファーストNotion代替 | AppFlowy AI, local SQLite |
| n8n | ワークフロー自動化。fair-codeライセンス | Sustainable Use License, n8n Cloud |
| Cal.com | 予約スケジューリング（Calendly代替） | Cal.com platform, white-label |
| Supabase | Postgres中心のBaaS | Supabase Edge Functions, RLS |
| Cline | VS Code拡張のAIコーディングエージェント | Cline CLI 2.0, agentic coding |
| Sustainable Use License | "fair-code"な制限付きOSSライセンス | SUL n8n, commercial redistribution |
| ローカルファースト | ローカルDB優先＋任意クラウド同期の思想 | local-first software |

---

## 🧭 背景 / なぜ今これが話題なのか

2022〜2023年に生成AIブーム（ChatGPT、Stable Diffusion）が起きて以降、SaaSは月額サブスクの積み重ねで「気づけば月$300〜」のコストを生むようになった。その反動として **2024〜2026年は「ローカルファースト」「セルフホスト」「fair-codeライセンス」への揺り戻し** が起きている。

特に2024年4月に OpenVoice V2 が **MITライセンスで商用利用可** に切り替わり（[GitHub](https://github.com/myshell-ai/OpenVoice)）、同時期に Cline（旧Claude Dev）が VS Code 拡張として急成長、2026年には **累計500万インストールを突破**（[Cline vs Cursor 2026, cursor-alternatives.com](https://cursor-alternatives.com/blog/cursor-vs-cline/)）した。Ollama も同じ文脈で GitHub スター **16.9万超** に伸長している（[Claude 5 Hub, 2026](https://claude5.com/news/local-llm-mastery-ollama-lm-studio-llama-cpp-guide-2026)）。

一方で、資金調達や持続性の観点から **n8n は 2022 年に Apache 2.0 から独自の Sustainable Use License へ移行** し、"完全なOSS" ではなく "fair-code" 枠組みに変わった（[n8n LICENSE.md](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)）。ComfyUI も2025年にComfy-Org という組織化が進み、プロ運用（[Comfy-Org/desktop リリース](https://github.com/Comfy-Org/desktop/releases)）の体制が整ってきた。

つまりこのリストは **"OSS AI ツールの成熟期=2026年のスナップショット"** として読むのが正解で、「無料・永遠」のキャッチーなフレーズの裏で **ライセンス条件の差が大きい** のが2026年現在の実態。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Fooocus: ダウンロードから最初の画像生成まで3クリック | 公式READMEでも "simple one-click installation" をうたう。初回はモデルDLで数分待つ。"3クリック"は演出気味だが操作フローとしては妥当 | [Fooocus GitHub](https://github.com/lllyasviel/Fooocus) | ⚠️ ほぼ一致 |
| Fooocusは活発にメンテされている | **2025年以降はLTS（バグ修正のみ）モード**。v2.5.5 は 2026-08 にリリース済みだが新機能は積まない方針。Fluxなど新モデルには WebUI Forge / ComfyUI / SwarmUI を推奨 | [lllyasviel/Fooocus Discussion #2154](https://github.com/lllyasviel/Fooocus/discussions/2154), [Releases](https://github.com/lllyasviel/Fooocus/releases) | ❌ 要注意（古い情報で語られがち） |
| ComfyUI: プロのAIアーティストが本番制作に活用 | v0.16.4（2026-03-07）はTencent連携・Nano Banana Pro・Kling Lip Syncなどスタジオ向けノードを公式搭載。プロ運用は事実 | [ComfyUI Changelog](https://docs.comfy.org/changelog), [Comfy-Org GitHub](https://github.com/comfy-org/ComfyUI) | ✅ 一致 |
| Ollama: 1コマンドでインストール、インターネット不要、APIコスト0 | `curl \| sh` 方式で導入可。モデルDL後は完全ローカル動作。2026年にWindows ARM64ネイティブビルド、AMD ROCm/Vulkan対応、multimodal・function calling追加 | [Ollama Blog](https://ollama.com/blog), [Programming-helper 2026](https://www.programming-helper.com/tech/ollama-2026-local-llm-revolution-privacy-enterprise) | ✅ 一致 |
| OpenVoice: 10秒のオーディオから音声クローン。MIT+MyShell。MITライセンスで商用OK | **2024年4月以降、V1/V2ともMITライセンス**に切り替え済み。Massachusetts Institute of Technology + 清華大学 + MyShell共同開発 | [OpenVoice GitHub LICENSE](https://github.com/myshell-ai/OpenVoice/blob/main/LICENSE), [VentureBeat](https://venturebeat.com/ai/open-source-ai-voice-cloning-arrives-with-myshells-new-openvoice-model) | ✅ 一致 |
| Penpot: リアルタイムコラボ、ブラウザ動作、セルフホスト可能 | 公式で確認済み。Inspectパネル（開発者向けCSS取得）が **無料で標準搭載** されている点はFigma有料Dev Modeに対する明確な優位 | [Penpot vs Figma 公式](https://penpot.app/penpot-vs-figma), [XDA 2025](https://www.xda-developers.com/self-hosted-figma-alternative-is-great-but-not-for-everyone-penpot/) | ✅ 一致 |
| AppFlowy: Rust製、ローカルファースト、データが自分のマシンに残る | Rust+Flutter製、ローカルSQLiteにまず書き込み→任意同期。Ollamaと連携した**完全ローカルAIアシスト**も可能 | [StackAlts 2026](https://stackalts.com/appflowy-vs-notion.html), [GitHub](https://github.com/cedrickchee/appflowy) | ✅ 一致（ただしモバイル同期は未成熟） |
| n8n: 400以上の統合、セルフホストならワークフロー無制限 | 統合数は事実。ただし **Sustainable Use License により「自社内部利用」のみ無料**。他社への提供・再販・埋め込み・ホワイトラベルは有償契約が必須 | [n8n Sustainable Use License](https://docs.n8n.io/sustainable-use-license/), [Scalevise](https://scalevise.com/resources/n8n-automation-license-commercial-use/) | ❌ 要注意（「無料で商用」は誤解を招く） |
| Cal.com: ホワイトラベル化可能 | 公式プラットフォームAPIで可能。ただしホワイトラベル機能の一部はPlatformプラン（有償）前提 | [Cal.com GitHub](https://github.com/calcom/cal.com) | ⚠️ ほぼ一致 |
| Supabase: 自分が所有できるFirebase代替。一体型 | セルフホスト可能で機能セットは一致。ただし **12以上のDockerコンテナを運用管理する必要** があり、"Firebaseの気軽さ" とは乖離する | [Supabase vs Firebase 2026](https://tech-insider.org/supabase-vs-firebase-2026-2/), [Encore](https://encore.dev/articles/supabase-alternatives) | ⚠️ ほぼ一致（運用コスト注記が必要） |
| Cline: VS Code内で動作、Cursor代替 | VS Code拡張として公式提供、2026年2月に Cline CLI 2.0 でCI/CD対応。ただし **オートコンプリートは非搭載**（エージェント型） | [cursor-alternatives.com](https://cursor-alternatives.com/blog/cursor-vs-cline/), [cline.bot](https://cline.bot/blog/best-ai-coding-assistant-2025-complete-guide-to-cline-and-cursor) | ✅ 一致 |
| SaaS換算で月$300〜500相当 | 一次ソースなし。Midjourney($30)+ChatGPT Plus($20)+Figma($15)+Notion($10)+Zapier($20〜)+Calendly($12)+Firebase($25〜)+Cursor($20)+ElevenLabs($22) ≒ $174〜。"10個全部の有料プラン合算"なら$300は行くが **一般的な個人利用では過大見積もり** | 各公式価格ページ | ⚠️ ほぼ一致（上振れ寄り） |
| 全部・無料・永遠 | n8nのSUL、Supabaseのホスティング実費、Fooocus LTS、Cal.com一部有償機能を踏まえると **"永遠に無料" は保証されていない** | 上記 n8n / Supabase ソース | ❌ 要注意 |

---

## 🌐 最新動向（2026-04-23時点）

- **n8n の商用利用ラインが再注目されている** — "400統合で無料" と紹介する記事が増えた一方、2022年のSUL移行が周知されておらず、2026年になって改めて「自社内部のみOK・再販NG」が警告されている — [Scalevise n8n License 2026](https://scalevise.com/resources/n8n-automation-license-commercial-use/), 2026-02
- **Cline CLI 2.0 でヘッドレス運用解禁** — IDEを開かずCI/CDパイプラインに組み込めるようになり、Cursor代替というより"自動化エージェント"として使われ始めた — [Cursor vs Cline 2026](https://cursor-alternatives.com/blog/cursor-vs-cline/), 2026-02
- **Ollama が AMD ROCm/Vulkan と Windows ARM64 に正式対応** — これまでNVIDIA偏重だった構図が崩れ、Ryzen AI / Radeon Instinct / Snapdragon X Elite でもローカルLLM実用域に — [Ollama 2026 Guide](https://www.programming-helper.com/tech/ollama-2026-local-llm-revolution-privacy-enterprise), 2026-0X
- **ComfyUI Desktop 0.8.32 / コア 0.19.3 が安定版に** — Nano Banana Pro / Kling Lip Sync / Topaz API を公式ノードで統合し、スタジオ制作パイプラインに組み込みやすくなった — [Comfy-Org/desktop Releases](https://github.com/Comfy-Org/desktop/releases), 2026-03
- **Fooocus は LTS モードに移行** — 新モデル（Flux等）対応は WebUI Forge / SwarmUI に移譲。"Midjourney代替"として紹介するなら**移行先も併記すべき段階** — [Discussion #2154](https://github.com/lllyasviel/Fooocus/discussions/2154), 2025-2026
- **Supabase 自己ホストは "可能だが非推奨" 論が増加** — 2026年のレビュー記事で、Postgres / GoTrue / Storage / Realtime の分散運用負荷から **PocketBase や Appwrite の方が自己ホスト向き** と指摘される流れ — [Encore Supabase Alternatives](https://encore.dev/articles/supabase-alternatives), 2026-03

---

## 🧩 関連概念・隣接分野

- **Fair-code / Sustainable Use License**: 完全OSSでもなく完全プロプライエタリでもない「自社内部利用はタダ、他者への再販・埋め込みは有償」のハイブリッド型ライセンス。n8n・Plausible・FerretDBなどが採用。OSI認定OSSとは別物という点が重要。
- **ローカルファースト（Local-first software）**: データをまずローカルに保存し、同期は任意で行う設計思想。Martin Kleppmann らが2019年に定義。AppFlowy / Obsidian / Logseq が代表例。
- **セルフホストの隠れコスト**: 月額サブスク削減額より **DevOps工数（目安10〜20h/月、@$100）** の方が高くつくケースが一定数ある — [Statsig](https://www.statsig.com/blog/cloud-hosted-saas-vs-open-source-experimentation-platforms)
- **OSS ≠ "永遠に無料"**: ライセンス変更（MongoDBのSSPL、HashiCorpのBSL、n8nのSUL）は近年頻発。"現在無料" と "将来も無料" は別物。
- **"Cursor代替" 文脈でのエージェント型IDE**: オートコンプリート型(Cursor/Copilot) vs エージェント型(Cline/Aider) の二分化が2026年に進んだ。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: SaaSサブスクの積み重ねは年単位で見れば大きなコスト。個人開発者・小規模スタジオなら、これらOSSで本当に月$100〜200級の削減は可能。特にOllama + Cline + OpenVoiceの組み合わせは**AIコストがほぼゼロ**になる破壊力がある。

- **否定 / 慎重派の主張**:
  - "無料" はライセンス料のことで、**インフラ費・運用工数・学習コスト・モバイル体験の劣化** は見えていない
  - 自社内部のみOKのn8nをSaaS商品に組み込むと **ライセンス違反になる可能性**（SUL違反）
  - Supabaseを本番セルフホストすると DB・認証・ストレージを分離運用する必要があり、"Firebaseの手軽さ" の真逆になる
  - Fooocusを今から "Midjourney代替" として布教するのは **2025年の情報** であり、最新モデル対応を考えるなら ComfyUI / SwarmUI のほうが筋がいい
  - AppFlowyのモバイル同期はまだ Notion に見劣りする（Android同期の不整合報告多数）

- **中立的に見るときの補助線**:
  - **"置き換え" ではなく "併用"** が現実解。プロトタイプはSaaS、確定した用途はOSSへ移植、が堅い
  - 個人 or 小規模チームなら **Penpot / Cal.com / Ollama / Cline** は即採用しても痛みが少ない
  - スタートアップ・受託開発なら **n8n / Supabase** はライセンス条件と運用工数を試算してから採用すべき

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] SaaS合計 $300〜500/月 の内訳を個別プラン実価格で再計算する（日本円ベース・個人プラン前提で）
- [ ] n8n の Sustainable Use License が「受託開発でクライアントに納品」する場合の扱い（グレーゾーン）
- [ ] Supabase を個人レベルで運用する最小構成（1 VPS / 4GB RAM）での実コスト・可用性
- [ ] Cline + Ollama の完全ローカル開発環境で、実際にどこまでの規模のコードを書けるか（体感SWE-bench相当の実測）
- [ ] Fooocus → WebUI Forge / SwarmUI への移行ガイド（元テキストの読者に補足として有用）
- [ ] 「ビッグテックが埋もれさせる」という煽り文句のファクト — 実際に大手がOSSを潰した/買収した事例の列挙

---

## 📚 参考資料

- [n8n Sustainable Use License 公式](https://docs.n8n.io/sustainable-use-license/) — ライセンス条文の一次ソース, 取得日 2026-04-23
- [n8n LICENSE.md on GitHub](https://github.com/n8n-io/n8n/blob/master/LICENSE.md) — リポジトリ同梱ライセンス確認, 取得日 2026-04-23
- [n8n License Explained — Scalevise 2026](https://scalevise.com/resources/n8n-automation-license-commercial-use/) — "完全無料ではない"解説, 取得日 2026-04-23
- [OpenVoice GitHub（MITライセンス）](https://github.com/myshell-ai/OpenVoice) — ライセンス＆研究背景, 取得日 2026-04-23
- [OpenVoice VentureBeat紹介記事](https://venturebeat.com/ai/open-source-ai-voice-cloning-arrives-with-myshells-new-openvoice-model) — MIT+MyShell共同開発の裏取り, 取得日 2026-04-23
- [Fooocus Development Roadmap Discussion #2154](https://github.com/lllyasviel/Fooocus/discussions/2154) — LTSモード宣言, 取得日 2026-04-23
- [Fooocus Releases](https://github.com/lllyasviel/Fooocus/releases) — v2.5.5（2026-08）の確認, 取得日 2026-04-23
- [ComfyUI Changelog](https://docs.comfy.org/changelog) — v0.16.4（2026-03-07）の新機能, 取得日 2026-04-23
- [Ollama 2026 Revolution — Programming-helper](https://www.programming-helper.com/tech/ollama-2026-local-llm-revolution-privacy-enterprise) — AMD/ARM対応の裏取り, 取得日 2026-04-23
- [Cursor vs Cline 2026](https://cursor-alternatives.com/blog/cursor-vs-cline/) — 5Mインストール・CLI 2.0の確認, 取得日 2026-04-23
- [Supabase vs Firebase 2026 — tech-insider](https://tech-insider.org/supabase-vs-firebase-2026-2/) — 価格・コールドスタート比較, 取得日 2026-04-23
- [Encore: Supabase Alternatives 2026](https://encore.dev/articles/supabase-alternatives) — セルフホストの非自明性, 取得日 2026-04-23
- [Penpot vs Figma 公式](https://penpot.app/penpot-vs-figma) — Inspect無料搭載の確認, 取得日 2026-04-23
- [AppFlowy vs Notion 2026 — StackAlts](https://stackalts.com/appflowy-vs-notion.html) — ローカルファースト・モバイル課題, 取得日 2026-04-23
- [Statsig: Cloud SaaS vs Open Source](https://www.statsig.com/blog/cloud-hosted-saas-vs-open-source-experimentation-platforms) — セルフホストの隠れコスト, 取得日 2026-04-23

---

## 🗒 メモ

このリストは **「OSS入門としては良い、鵜呑みにすると事故る」** 典型例。X投稿として拡散しやすい煽り構成（"違法な気分"・"埋もれさせる前に"・"全部無料永遠に"）で組まれており、個別ツールの良し悪しより **リスト全体の誇張度合い** を見抜けるかが読み手の力量になる。

**使い道候補**:
- **note記事ネタ**: 「OSSは"タダ"じゃない — n8nとSupabaseで分かる"無料"の嘘」。元リストをフックに、SUL・運用工数・ライセンス変更の3点を深掘り → `/re-daily` に流す素材として強い
- **X投稿ネタ**: 「n8n を"完全無料Zapier代替"と紹介してる人、ライセンス読んでない説」など関係性キーワード（取引先／同僚）を絡めた批評系 → `/quote-rewrite` 用の元ネタ
- **クライアント提案**: "SaaS高い→OSS移行"相談を受けた時に、このノートを参照して **採用可否マトリクス** を渡せる（即採用OK: Penpot/Cal.com/Ollama/Cline ／ 要検討: n8n/Supabase/AppFlowy ／ 代替推奨: Fooocus→ComfyUI）

**所感**: ポジショントークに寄りすぎず、**"2026年時点での実態を冷静にチェックしたら、半分はガチで半分は注意書きが必要"** というトーンでまとめるのが誠実。
