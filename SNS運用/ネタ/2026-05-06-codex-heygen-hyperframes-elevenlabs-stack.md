---
created: 2026-05-06
tags:
  - 調査
  - AI動画
  - HeyGen
  - HyperFrames
  - ElevenLabs
  - Codex
  - Video-as-Code
  - ワークフロー
source: https://x.com/panchaaan_2/status/2051538076825194967
action: 運用参考, 投稿ネタ
---

# ぱんちゃん氏の「Codex × HeyGen × HyperFrames × ElevenLabs」YouTube動画スタックを解剖する

> [!summary] TL;DR
> - Pineal 広報 ぱんちゃん🥐 氏（AI Agent 書籍著者・5社 AI advisor）が **コーディングエージェント Codex で操作 / HeyGen でアバター / ElevenLabs で声 / HyperFrames で編集** という **4ツール「Video as Code」スタック** で 16秒の解説動画を作って共有
> - **核心は HyperFrames**（HeyGen が 2026-04-17 にリリースした OSS、Apache 2.0）。**HTML/CSS/JS で動画を書く = LLM が読み書きできる動画フォーマット**で、Codex / Claude Code / Gemini CLI が "動画編集者" として作業できる
> - 「無料で組める」わけではなく **HeyGen + ElevenLabs + Codex で月 $50〜$150** が現実値。とはいえ研修動画・YouTube 量産用途で **人月単価ベースのプロ動画編集を圧縮できる**インパクトは本物

---

## 📌 元テキスト（抜粋）

> Codex × HeyGen × HyperFrames × ElevenLabsでYouTube解説動画を作った！
>
> 研修動画とかにもめちゃくちゃ使えそう🙏
>
> 操作：Codex
> アバター：HeyGen
> 声：ElevenLabs
> 編集：HyperFrames

出典: [ぱんちゃん🥐 @panchaaan_2](https://x.com/panchaaan_2/status/2051538076825194967) — 2026-05-05 14:42 JST、255 likes / 11 RT / 7 reply、16秒動画（1920×1080）添付

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **HyperFrames** | HeyGen が 2026-04-17 公開した OSS。**HTML/CSS/JS で動画を書き、決定論的に MP4 にレンダリングする**。Apache 2.0 | "HyperFrames" HeyGen open source |
| **Video as Code** | HyperFrames の思想。動画をタイムライン編集ではなく**ソースコードで記述**するパラダイム。Remotion の対抗馬 | "video as code" Remotion HyperFrames |
| **HeyGen Avatar V** | 2026-04 リリース。15秒動画から studio-quality アバター生成、175 言語の音素レベルリップシンク | "HeyGen Avatar V" 2026 |
| **ElevenLabs** | AI 音声合成・声クローン。プロ品質ナレーションの定番 | "ElevenLabs" voice cloning 2026 |
| **Codex** | 文脈上は **OpenAI Codex CLI**（コーディングエージェント）。HyperFrames 用 HTML/CSS を書く役割 | "OpenAI Codex CLI" 2026 |
| **Pineal** | ぱんちゃん氏が広報を務める会社。AI 関連事業 | Pineal 広報 AI |
| **uravation.com** | ぱんちゃん氏が CEO の AI 研究開発会社 | uravation AI |
| **Remotion** | HyperFrames の先行ライブラリ。React で動画を書く既存 OSS | Remotion video React |

---

## 🧭 背景 / なぜ今これが話題なのか

**1. 著者は AI Agent 領域で複数ポジションを持つ広報・研究者**
@panchaaan_2 = ICU 卒、デザイナー（PERSOL Career → LIG）→ Pineal 広報マーケター。さらに **AI 研究開発会社 uravation.com の CEO**、書籍『AI Agent Work Methods』著者、**5社の AI advisor**、早稲田 AI 研究会 founder。**実装現場 + 広報 + 経営**を兼ねるタイプで、ツールスタックの実用性に対する目利きとして信頼性がある（[X プロフィール](https://x.com/panchaaan_2)）。

**2. 核心は "HyperFrames" の登場（2026-04-17）**
HeyGen が 2026-04-17 に OSS として公開（Apache 2.0、[GitHub: heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)）。**HTML/CSS/JS で動画コンポジションを書き、決定論的に MP4 にレンダリングする**フレームワーク。LLM が HTML をスムーズに書けるので、**Claude Code / OpenAI Codex / Gemini CLI が "動画編集者" として直接作業**できるようになった。これが「**Codex で操作 / HyperFrames で編集**」という記法の背景。

**3. Remotion 対抗 + AI agent first 設計**
HyperFrames の直接の比較対象は **Remotion**（React で動画を書く既存 OSS）。差別化は **「AI エージェントを第一級市民に据える」**設計：HTML を読み書きするエージェントが安定して動画を生成できるよう、決定論的レンダリング（同じ入力で同じ出力）と、frame-by-frame の予測可能性を保証している（[AI Engineering Trend](https://ai-engineering-trend.medium.com/heygens-hyperframes-the-open-source-framework-challenging-remotion-in-html-based-video-creation-c10437f0afca)）。

**4. HeyGen Avatar V がアバター品質を一段階引き上げた**
2026-04 リリースの **Avatar V** で **15秒の自撮り動画から studio-quality のデジタルツイン**を生成、**175 言語**の音素レベルリップシンク、長尺・多角度でアイデンティティが崩れない品質に。**研修動画・YouTube 解説動画の "演者コスト"** がほぼゼロになる転換点（[HeyGen Blog](https://www.heygen.com/)）。

**5. ElevenLabs は声側の標準デファクト**
プロ品質の AI 音声合成・声クローンの定番。HeyGen も[公式統合ガイド](https://www.storylane.io/tutorials/how-to-integrate-heygen-with-elevenlabs)を出しており、**「HeyGen のアバター + ElevenLabs の声」**は 2025〜2026 の定番組み合わせ。2026 のスタックで珍しさはないが、**確実に動く一手**として組み込まれている。

**6. Codex の意味の確認**
ツイートでは「操作: Codex」と書かれており、文脈的には **OpenAI Codex CLI（コーディングエージェント）** を指していると判断できる。HyperFrames が HTML/CSS/JS のソースコードを必要とするので、Codex がそのコードを書く・実行する役回り。Claude Code でも代用可能で、**著者がたまたま Codex を選んだ** だけと読める。

**7. なぜ今 4ツールスタックが組めるのか**
- **2026-04-17**: HyperFrames OSS リリース ← 最新ピース
- **2026-04**: HeyGen Avatar V ← アバター品質の質的飛躍
- **2025〜**: ElevenLabs の音声品質が定常化
- **2025-2026**: Codex / Claude Code 等のコーディングエージェントが HTML/CSS を実用レベルで書けるように

つまり **2026-04 月の HyperFrames が「最後のピース」** で、4ツールスタックが組めるようになったのは ここ 1 ヶ月。ぱんちゃん氏のツイートはそのトピックに即反応した試作報告。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| HyperFrames で動画編集ができる | HeyGen が 2026-04-17 に OSS 公開、HTML/CSS/JS で動画記述 → MP4 レンダリング、Apache 2.0 | [GitHub heygen-com/hyperframes](https://github.com/heygen-com/hyperframes), [HeyGen 公式](https://hyperframes.heygen.com/) | ✅ 一致 |
| HeyGen でアバター動画 | Avatar V 2026-04 リリース、15秒映像から studio-quality アバター・175言語対応 | [HeyGen Blog](https://www.heygen.com/blog/best-ai-video-generator-faceless-youtube) | ✅ 一致 |
| ElevenLabs で声 | プロ品質音声合成・声クローン。HeyGen との公式統合あり | [Storylane 統合ガイド](https://www.storylane.io/tutorials/how-to-integrate-heygen-with-elevenlabs) | ✅ 一致 |
| Codex で操作 | OpenAI Codex CLI が HTML を書く・実行できることは確認済み。Claude Code でも代用可 | [MindStudio: Claude Code + HyperFrames](https://www.mindstudio.ai/blog/ai-video-editing-claude-code-hyperframes) | ✅ 一致（具体的に Codex CLI かどうかは要本人確認） |
| 研修動画にも使える | アバター固定・スクリプト変更だけで量産可能なので、社内研修用途には強い適合 | [n8n テンプレ例](https://n8n.io/workflows/11895-generate-ai-avatar-videos-from-scripts-using-elevenlabs-and-heygen/) | ✅ 一致（業界の現実的な使い道として既に検証済み） |
| 「無料で組める」（明示はしてないが暗黙） | HyperFrames は OSS だが HeyGen / ElevenLabs / Codex は有料。月 $50〜$150 が実勢 | [HeyGen 料金](https://www.heygen.com/), [ElevenLabs 料金](https://elevenlabs.io/pricing) | 🔍 未確認（著者は「無料」と明言していないが、フォロワーが誤読する余地あり） |

---

## 🌐 最新動向（2026-05-06 時点）

- **2026-05-05 14:42 JST**: ぱんちゃん氏が4ツールスタックでの試作報告 — [元ツイート](https://x.com/panchaaan_2/status/2051538076825194967), 2026-05
- **2026-04-17**: HyperFrames OSS リリース。Apache 2.0、HTML/CSS/JS で動画、AI agent first 設計 — [HeyGen GitHub](https://github.com/heygen-com/hyperframes), 2026-04
- **2026-04**: HeyGen Avatar V リリース。15秒映像 → studio-quality digital twin、175言語リップシンク — [HeyGen Blog](https://www.heygen.com/blog/best-ai-video-generator-faceless-youtube), 2026-04
- **2026-04**: HyperFrames vs Remotion の比較記事が技術系メディアで多数公開、**Video as Code がトレンド化** — [AI Engineering Trend](https://ai-engineering-trend.medium.com/heygens-hyperframes-the-open-source-framework-challenging-remotion-in-html-based-video-creation-c10437f0afca), 2026-04
- **2026-Q2**: Claude Code / Codex CLI / Gemini CLI を HyperFrames で動画編集する解説記事が増加 — [MindStudio](https://www.mindstudio.ai/blog/ai-video-editing-claude-code-hyperframes), 2026-Q2
- **2026-09 予定**: HeyGen が Video Agent を一般公開予定（プロンプト1つで脚本→映像→声→編集→納品まで自動化）— [storytool.io](https://storytool.io/blogs/best-ai-dubbing-tools-2026), 2026 リリースロードマップ

---

## 🧩 関連概念・隣接分野

- **Remotion**: HyperFrames の直接の競合 OSS。**React で動画を書く** 先行ライブラリ。エコシステム成熟度は Remotion が上、AI agent 親和性は HyperFrames が上
- **Video Agent (HeyGen, 2026-09 予定)**: 1プロンプトで脚本→映像→声→編集→納品を自動化する HeyGen の次のキラー機能。HyperFrames はその基盤の一つ
- **Synthesia**: HeyGen の最大の競合アバター動画 SaaS。研修動画用途では老舗。**「演者付き解説動画」**という同じ市場
- **Codex CLI / Claude Code / Gemini CLI**: HyperFrames を駆動するエージェント側の選択肢。**HTML 出力品質と決定論性**で選ぶ
- **MCP (Model Context Protocol)**: 4ツールを繋ぐ将来の接続規格。今は手動オーケストレーションだが、いずれ MCP で完全自動化されると見られる
- **n8n / Zapier ワークフロー**: 同じ4ツールの **ノーコード版オーケストレーション**。エンジニアでない層はこちらを使う

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - **時代の組み合わせとして完成度が高い**: HyperFrames（2026-04-17）+ Avatar V（2026-04）の合流タイミングを即座に試したセンスは秀逸
  - **研修動画ユースケース**: アバター固定 + 台本差し替えで量産できるので、社内研修・オンボーディング・LMS 教材で**人月コストを圧縮**できる現実解
  - **OSS 中核**: HyperFrames が Apache 2.0 なので、エンタープライズ用途でも採用しやすい

- **否定 / 慎重派の主張**:
  - **「無料で組める」フレームに誤読される危険**: 著者は明言していないが、AI ツール紹介系は **HeyGen $24/月・ElevenLabs $5〜$99/月・ChatGPT Plus $20/月**等のランニング費用が伴う。フォロワーが「無料で全部できる」と勘違いするリスクあり
  - **学習コスト**: HTML/CSS で動画を書く発想は **web 制作者には親和性高いが、動画編集者には逆向き**。「Codex で操作」の前提に **HTML/CSS リテラシー**がある点を見落とすと再現できない
  - **アバター動画の "うっすら違和感"**: Avatar V でも **15秒の解説動画レベルなら違和感ゼロだが、長尺になると微妙**。研修用途の長尺動画への適合は実機検証要
  - **Codex の指定が曖昧**: 「Codex」だけだと OpenAI Codex CLI / Codex GPT-5.5 / 別の何か、を読み手が判断できない。**ツール名の表記揺れ**は教材性を落とす
  - **"Video Agent" 待ち合戦**: HeyGen が 2026-09 に Video Agent（1プロンプトで全自動）を出すと、4ツールを手動で組む価値が一気に減る可能性

- **中立的に見るときの補助線**:
  - 「**今すぐ動かす実装**」と「**4-6 ヶ月後の Video Agent**」のどちらに乗るか、用途次第。**実機で慣れたい人は今組む、量産だけなら待つ**
  - 4ツールを **「組み合わせのスケッチ」**として記憶しておけば、Video Agent 登場後も **個別ピースを差し替えて使える**

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] **「Codex」の指定**: ぱんちゃん氏のリプ欄で OpenAI Codex CLI / Codex GPT のどちらか確認
- [ ] **16秒動画の制作時間**: 4ツールを手動で繋いだ場合、構想→納品までの実時間はどのくらいか（プロンプト試行錯誤を含めて）
- [ ] **研修動画の長尺化**: 5分・10分の長尺で同じ品質が保てるか、Avatar V の identity-consistency 限界の検証
- [ ] **HyperFrames vs Remotion** の実機比較: AI agent 親和性と既存エコシステムのトレードオフを定量化
- [ ] **MCP 経由での全自動化**: 4ツールをすべて MCP server 化して **1 プロンプトで完了** までいけるか（HeyGen Video Agent 待ちか、自前で組むか）
- [ ] **クライアント案件としての提案価値**: 自分の web 制作クライアントで「研修動画を AI で量産したい」ニーズが顕在化した時、このスタックを提案する条件と価格設定
- [ ] **ElevenLabs の日本語品質**: 2026 時点での日本語ナレーション自然性の最新評価。日本語クライアント案件での適合度

---

## 📚 参考資料

- [ぱんちゃん 元ツイート（@panchaaan_2 2026-05-05）](https://x.com/panchaaan_2/status/2051538076825194967) — 投稿の一次情報, 取得日 2026-05-06
- [HeyGen HyperFrames 公式](https://hyperframes.heygen.com/) — 機能・思想の一次ソース, 取得日 2026-05-06
- [GitHub: heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) — OSS リポジトリ・Apache 2.0 ライセンス確認, 取得日 2026-05-06
- [HeyGen's HyperFrames vs Remotion — Medium](https://ai-engineering-trend.medium.com/heygens-hyperframes-the-open-source-framework-challenging-remotion-in-html-based-video-creation-c10437f0afca) — 競合比較とリリース日（2026-04-17）, 取得日 2026-05-06
- [How to Build AI Video Editing Workflow with Claude Code and Hyperframes — MindStudio](https://www.mindstudio.ai/blog/ai-video-editing-claude-code-hyperframes) — エージェント駆動の実装例, 取得日 2026-05-06
- [Best AI Video Tools 2026 — aivideopicks](https://aivideopicks.com/posts/best-ai-video-tools-2026.html) — HeyGen Avatar V の機能評価, 取得日 2026-05-06
- [Best AI Dubbing Tools 2026 — Storytool](https://storytool.io/blogs/best-ai-dubbing-tools-2026) — HeyGen Video Agent の 2026-09 リリース予定, 取得日 2026-05-06
- [How to Integrate HeyGen with ElevenLabs — Storylane](https://www.storylane.io/tutorials/how-to-integrate-heygen-with-elevenlabs) — HeyGen × ElevenLabs 連携手順, 取得日 2026-05-06
- [Generate AI avatar videos using ElevenLabs and HeyGen — n8n](https://n8n.io/workflows/11895-generate-ai-avatar-videos-from-scripts-using-elevenlabs-and-heygen/) — ノーコード版ワークフロー比較, 取得日 2026-05-06
- [ぱんちゃん X プロフィール](https://x.com/panchaaan_2) — 著者ポジション確認, 取得日 2026-05-06

---

## 🗒 メモ

- **このスタックは「組み合わせのスケッチ」として価値が高い**: 個別ピースは知っていても、**HyperFrames（2026-04-17 リリース）が最後のピース**で4 ツールが噛み合う構図を整理しているのが新しい。Tsukapon の `_ kiwami/` 配下にスタックメモとして保存推奨
- **note 記事化案**: 「**HyperFrames で動画を書く時代 — 4ツール × Video as Code の全体像**」型で1本書ける。図解（Mermaid シーケンス図）+ コード例（HyperFrames の HTML サンプル）+ 月額コスト表 まで揃えれば SEO 観点でも強い
- **クライアント提案ストック**: web 制作クライアントが **「研修動画 / オンボーディング動画 / 製品解説動画」**で困っている時の標準提案として登録。**月運用 $50〜$150** で1本量産できる経済性は刺さる
- **my-clone 文体への翻訳**: ぱんちゃん氏の箇条書きは簡潔で良いが、my-clone 流儀に翻訳するなら **「組み立てた感想」「詰まったポイント」「差し替え可能な部分」** を必ず添える。「動いたよ」だけでは情報密度が低い
- **HeyGen Video Agent (2026-09) 待ち戦略**: 4ヶ月後に1プロンプトで全自動化が来るなら、**今は手動で組んで仕組みを理解しておく** のが正解。Video Agent が来たら手動オーケストレーションは廃れるが、**ピースの理解は残る**
- **Tsukapon の SNS運用への適用**: my-clone のアバターを HeyGen Avatar V で作って、**自分の解説動画を量産する**ことは技術的に可能。ただし **本人不在の動画化は my-clone 人格と衝突するか** を要検討（"実測寄りの自分" がアバター動画で語ることの違和感）
- **Codex 表記の曖昧さ問題**: 自分が同種の投稿をする時は **「Codex CLI（OpenAI）」「Claude Code」「Gemini CLI」** のように**ベンダー + 製品名**で書く方が読み手に親切。ツール名の揺れは教材性を落とす、というのは普段から気をつけたい
