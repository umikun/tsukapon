---
created: 2026-05-07
tags:
  - 調査
  - AI
  - TTS
  - 音声合成
  - ローカルAI
  - Irodori-TTS
source: https://x.com/gigazine/status/2051297127989383651?s=20
action: 投稿ネタ
---

# Irodori-TTS — 絵文字で感情を操る、日本語特化のローカルTTS。MITライセンスで「無制限・無料」の本気度

> **🔗 関連コンテンツ**
> - 🎙 同テーマ（オンデバイス音声クローン）: [[SNS運用/ネタ/2026-04-29-neutts-air-on-device-voice-cloning.md]]
> - 🎙 音声クローンの実用性検証: [[SNS運用/ネタ/2026-05-03-voice-pro-cloning-tool-reality.md]]
> - 🧰 OSS/無料代替ツール系の関連ネタ: [[SNS運用/ネタ/2026-05-06-dont-pay-ai-tool-alternatives.md]]
> - 🎬 商用音声スタックとの対比: [[SNS運用/ネタ/2026-05-06-codex-heygen-hyperframes-elevenlabs-stack.md]]
> - 📝 同日のネタ（兄弟ファイル）: [[SNS運用/ネタ/2026-05-07-frappe-insights-oss-bi.md]]

> **TL;DR**
> Irodori-TTS は個人開発者 Aratako 氏による **日本語特化のローカルTTS**。MITライセンス（コード）＋ 公開モデルウェイトで、**ゼロショット音声クローン** と **40種以上の絵文字による感情・スタイル制御**（👂囁き／😭泣き／😠怒り／⏩早口／📞電話音…）が最大の差別化ポイント。RTX 5070 Ti なら5秒の音声が約3秒で生成、CPU でも約90秒で動く。GitHub スター611（2026-05時点）と新興だが、**ElevenLabs / Style-Bert-VITS2 / VOICEVOX の隙間** に綺麗に刺さる位置取り。商用利用OKだが「他人の声を本人同意なしに模倣禁止」の倫理規定だけは要遵守。

---

## 🗒 メモ

> ⚠️ このセクションは **冒頭に配置**（2026-05-06 ルール変更）。**「この調査をどう使うか」のアクション仮説**を最初に書くことで、次のアクションが見えやすくなる。

### 投稿ネタとしての切り口

- **フックは「絵文字で感情を操る」一点突破**。「ローカルで動く日本語TTS」だけだと Style-Bert-VITS2 と差別化が弱いので、**絵文字インターフェースの体験デモ** を中心に据える
- **構成案**:
  1. 「テキストに👂って絵文字入れたら囁き声になりました」みたいな具体例で引き込む
  2. ゼロショットクローン（参照音声D&D）の手軽さ
  3. MITライセンス＋HF配布で導入5分の話
  4. **倫理オチ**「ただし他人の声を本人同意なく真似るのはNG。そこは普通にAGPLよりタチ悪い面もある」で締める
- 同日ネタの [[SNS運用/ネタ/2026-05-07-frappe-insights-oss-bi.md]] と並べて **「OSSの落とし穴シリーズ」** にもできる（Insights=ライセンス罠、Irodori-TTS=倫理罠）

### このネタの使い道

- **SNS投稿**: Xスレッド（4〜5投稿）or note短記事1本
- **戦略接続**: W18戦略メモの「OSS紹介枠」とリンク、Insightsと連投シリーズ化
- **書くなら**: Xスレッドなら4投稿（フック→機能→絵文字デモ→倫理オチ）、noteなら1500〜2000字

### 派生ネタ候補

- 「日本語ローカルTTSの2026年最新地図」: VOICEVOX / Style-Bert-VITS2 / Irodori-TTS / NeuTTS-air を一枚絵で比較
- 「絵文字プロンプティング」を音声以外（画像生成プロンプト等）に応用するアイデア記事
- 自分のクローン声を作って X の固定動画に使う実験ログ

### 自分用の検証タスク

- [ ] M3 Mac で実際に動かす（MPS動作確認）
- [ ] 自分の声サンプル30秒で VoiceDesign してみる
- [ ] 長文ナレーション（note記事1本分）の自然さテスト

---

## 📌 元テキスト（抜粋）

> 好きな声で好きなセリフを喋らせられるローカルAI「Irodori-TTS」の使い方、日本語特化でローカル動作するので無制限に生成し放題

出典: [GIGAZINE @gigazine on X](https://x.com/gigazine/status/2051297127989383651?s=20)（2026-05-04）／[GIGAZINE 本記事](https://gigazine.net/gsc_news/en/20260504-irodori-tts-text-to-speech-ai/)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| TTS (Text-to-Speech) | テキスト→音声合成。AI界隈の定番タスク | `text to speech AI` |
| ゼロショット音声クローン | 数秒のサンプル音声から話者の声を真似る | `zero-shot voice cloning` |
| Flow Matching | 拡散モデルの後継として注目される生成手法。学習が安定で推論も速い傾向 | `flow matching generative model` |
| RF-DiT | Rectified Flow Diffusion Transformer。Irodori-TTS のコア生成器 | `rectified flow transformer` |
| Semantic-DACVAE | 音声を低次元の潜在表現に圧縮するコーデック。32次元・48kHz対応の日本語版を採用 | `DAC neural audio codec` |
| Echo-TTS | Irodori-TTS の設計の元になった先行OSS | `Echo-TTS` |
| Hugging Face Hub | モデルウェイトの配布インフラ | `huggingface hub` |
| uv | Rust製のPythonパッケージマネージャ。Pipより速い | `astral uv python` |
| VoiceDesign | テキスト記述だけで「こういう声」を作れる派生モデル | `Irodori-TTS VoiceDesign` |

---

## 🧭 背景 / なぜ今これが話題なのか

### 日本語TTSの「商用 vs OSS」二極化

これまで日本語の高品質TTSは以下の構図だった:

- **商用（クラウド）**: ElevenLabs、にじボイス、VOICEPEAK等。品質高いが従量課金、外部送信、規約縛り
- **OSS（ローカル）**: VOICEVOX（ずんだもん等のキャラ固定）、Style-Bert-VITS2（学習が必要）、Coqui XTTS-v2（多言語だが日本語は二番手）

**「ローカルで動いて、好きな声で、感情も操れて、しかも商用OK」** という三拍子が揃ったOSSは長年の空白地帯だった。Irodori-TTS は Aratako 氏（個人開発者）が2026年1〜4月にかけて段階リリースし、**v2 で完成度が一気に上がった** 形。

### 技術的な転機: Flow Matching と Echo-TTS

2025年頃から音声生成は **Diffusion Transformer + Flow Matching** が主流化（XTTS-v3、F5-TTS、CosyVoice2 等）。Irodori-TTS は OSS の **Echo-TTS** をベースに、日本語データで学習し直し、独自の **Semantic-DACVAE-Japanese-32dim** コーデックで48kHz音質を実現したのが特徴。

「**個人が小〜中規模モデル（500M〜2.5B）で商用クラスを出せる時代** になった」象徴的なプロジェクトといえる。

### 絵文字による感情制御という発明

VOICEVOXは事前登録キャラの「ノーマル/喜び/怒り」程度。Style-Bert-VITS2は感情ベクトル指定だが直感的でない。Irodori-TTS は **テキスト中に絵文字を埋めるだけ** で感情・スタイル・効果音まで制御可能。

```
こんにちは👂（小声で）今日は天気がいいね😊⏩（明るく早口で）
```

この「自然言語＋絵文字」インターフェースは、ChatGPT世代のユーザーが直感で触れる形に振り切っており、X で拡散した最大要因と推測される。

### 2026年GW期の盛り上がり

- 2026-04-28 [くろくまそふと記事](https://kurokumasoft.com/2026/04/28/irodori-tts/)
- 2026-04-29 NeuTTS Air 公開（同じ「ローカル音声クローン」枠の競合）→ [[SNS運用/ネタ/2026-04-29-neutts-air-on-device-voice-cloning.md]]
- 2026-05-04 GIGAZINE 紹介で一般層に拡散
- 2026-05-07 GitHub スター611、Hugging Face のダウンロードも増加中

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| ローカルで動く | Python+uv+Git があれば Linux/Win/macOS(MPS) で動作。GPU推奨だがCPU可 | [GitHub: Aratako/Irodori-TTS](https://github.com/Aratako/Irodori-TTS) | ✅ 一致 |
| 日本語特化 | 学習データが日本語中心、コーデックも `Semantic-DACVAE-Japanese-32dim` | [Aratako/Irodori-TTS-500M-v2 (HF)](https://huggingface.co/Aratako/Irodori-TTS-500M-v2) | ✅ 一致 |
| 無制限に生成し放題 | ローカル動作で従量課金なし。実質的に無制限。ただし倫理規約あり | [GIGAZINE 記事](https://gigazine.net/gsc_news/en/20260504-irodori-tts-text-to-speech-ai/) | ⚠️ ほぼ一致（倫理条件付き） |
| 好きな声で喋らせられる | 参照音声をD&Dするゼロショットクローンに対応 | [GitHub README](https://github.com/Aratako/Irodori-TTS) | ✅ 一致 |
| 5秒音声を3秒で生成（GPU） | RTX 5070 Ti + Ryzen 7 9700X 環境での実測値として GIGAZINE が記載 | [GIGAZINE 記事](https://gigazine.net/gsc_news/en/20260504-irodori-tts-text-to-speech-ai/) | ✅ 一致（環境依存） |
| MITライセンスで商用利用OK | コードはMIT。ただし「なりすまし禁止」（声優・著名人・公人を本人同意なく模倣しない）の倫理規定あり | [HF モデルカード](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign) | ⚠️ ほぼ一致（倫理規約は別途遵守） |

---

## 🌐 最新動向（2026-05時点）

- **v2 が主軸リリース。500M（メイン）と2.5B（高品質）の2サイズ展開** — [Aratako/Irodori-TTS-500M-v2 on Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2), 2026-04
- **VoiceDesign 派生モデル登場**: テキストキャプションだけで「20代女性、明るく早口」みたいな声を作れる — [Aratako/Irodori-TTS-500M-v2-VoiceDesign](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign), 2026-04
- **GitHub スター611・コードはMIT**: 2026-05-07時点。新興だが伸び率は高い — [GitHub: Aratako/Irodori-TTS](https://github.com/Aratako/Irodori-TTS), 2026-05
- **GIGAZINE が日本語/英語両記事で大々的に紹介**: 一般層への露出が一気に拡大 — [GIGAZINE en](https://gigazine.net/gsc_news/en/20260504-irodori-tts-text-to-speech-ai/), 2026-05-04
- **Emoji-TTS というフォーク（WebUI改善版）登場**: コミュニティで派生プロジェクトが動き始めている — [iron-mukakin/Emoji-TTS](https://github.com/iron-mukakin/Emoji-TTS), 2026
- **Mac (Apple Silicon) でも動作報告多数**: MPS バックエンド対応で Mac ユーザーも導入可 — [Mac で試した記事 (note)](https://note.com/kazu_t/n/nbdd0ee937600), 2026-04
- **Zenn / note / YouTube でレビュー記事が爆増**: 2026-04-28 のくろくまそふと記事を皮切りに、GW期間中に解説コンテンツが急増 — [zenn scraps](https://zenn.dev/kun432/scraps/87d7776909e4d9), 2026-04

---

## 🧩 関連概念・隣接分野

- **Style-Bert-VITS2**: 日本語TTSの定番OSS。学習工程あり・スタイルベクトル指定。Irodori-TTS は「学習不要で参照音声D&D」が差別化
- **VOICEVOX**: ずんだもん等の固定キャラ向け。MIT的な使いやすさだが声質を増やせない。Irodori-TTS は声質自由
- **NeuTTS-air**: 2026-04登場の競合「オンデバイス音声クローン」。多言語対応 vs 日本語特化の構図 → [[SNS運用/ネタ/2026-04-29-neutts-air-on-device-voice-cloning.md]]
- **CosyVoice2 / F5-TTS / XTTS-v3**: 海外勢の Flow Matching ベースTTS。日本語対応は弱め
- **ElevenLabs**: 商用クラウドの王者。多言語・超高品質だが従量課金。Irodori-TTS は「無料・ローカル・日本語限定」のトレードオフ
- **Semantic codec（DACVAE / Encodec / SoundStream）**: 音声の潜在表現を作るコーデック群。TTSモデルの音質と速度を決める縁の下の力持ち

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - 日本語に最適化された学習データ＋コーデックなので、海外OSSより自然なイントネーション
  - 絵文字インターフェースが直感的で「触ってみたら動いた」体験が強い
  - MIT＋HF配布で導入障壁が低い。`uv sync` で完結
  - VoiceDesign で「素材音声を持ってない人」も声を作れる（音声素材の権利問題回避）

- **否定 / 慎重派の主張**:
  - **倫理リスク**: ゼロショットクローンは「本人同意なし模倣」の入り口にもなる。詐欺電話・なりすまし動画の温床になりかねない（モデル規約は禁止だが技術的には可能）
  - **モデルウェイトのライセンス曖昧さ**: コードはMITだが、モデル本体はHFのモデルカードで個別規約。商用利用時は要確認
  - **学習データの透明性**: 公開データセット名・スピーカー同意プロセスがフルには開示されていない（モデルカードに概要のみ）
  - **個人開発の継続性リスク**: メンテナがAratako氏ほぼ単独。バス係数1問題
  - **多言語対応なし**: 英語混じりや中国語は弱い／不安定。グローバル製品には組み込みづらい
  - **「無制限」≠「自由」**: 商用利用の解釈、声優の声を学習に使うかどうかなど、グレーゾーンを自分で判断する責任が利用者側に残る
  - **生成感・抑揚の不自然さ**: ElevenLabsやVOICEPEAK等の商用品質と比較すると、長文での自然さ・呼吸感はまだ一歩劣るとの評価あり

- **中立的に見るときの補助線**:
  - **「自分の声 or 自作キャラの声を、自分用に動画/ゲーム/読み上げで使う」** なら最強候補
  - **「他人の声を本人同意なく使う」「商用プロダクトに組み込んで顧客提供」** はグレー〜NG。倫理規約の遵守 + 法務確認必須
  - 商用クラウド（ElevenLabs等）と比較する時は **「品質 vs ローカル動作・無料・日本語自然さ」** のトレードオフで判断

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] 学習データの完全な内訳（声優事務所との契約データ？クリエイティブコモンズ音源？）
- [ ] ElevenLabs / VOICEPEAK / Style-Bert-VITS2 と長文ナレーションでの自然さブラインドテスト
- [ ] 2.5B モデルと500M モデルの実用差（VRAM要件・体感品質）
- [ ] 商用プロダクト組み込み事例の実例（誰がどう使っているか）
- [ ] iOS/Android（オンデバイス）対応の見通し ─ NeuTTS-air は対応済
- [ ] ライブストリーミング配信での遅延（リアルタイム読み上げ用途で使えるか）
- [ ] VoiceDesign キャプションのプロンプトエンジニアリングのコツ集

---

## 📚 参考資料

- [GIGAZINE @gigazine on X](https://x.com/gigazine/status/2051297127989383651?s=20) — 元ツイート（2026-05-04）, 取得日 2026-05-07
- [GIGAZINE: How to use Irodori-TTS (英語版記事)](https://gigazine.net/gsc_news/en/20260504-irodori-tts-text-to-speech-ai/) — 機能・性能・導入方法の総合レビュー, 取得日 2026-05-07
- [GitHub: Aratako/Irodori-TTS](https://github.com/Aratako/Irodori-TTS) — 公式リポジトリ・ライセンス・スター数・技術スタック, 取得日 2026-05-07
- [Aratako/Irodori-TTS-500M-v2 on Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2) — モデルウェイト・モデルカード, 取得日 2026-05-07
- [Aratako/Irodori-TTS-500M-v2-VoiceDesign on Hugging Face](https://huggingface.co/Aratako/Irodori-TTS-500M-v2-VoiceDesign) — テキストキャプションで声を作る派生モデル, 取得日 2026-05-07
- [くろくまそふと: Irodori-TTS導入方法・使い方](https://kurokumasoft.com/2026/04/28/irodori-tts/) — GW直前の早期解説記事, 取得日 2026-05-07
- [zenn scraps: 「Irodori-TTS」を試す](https://zenn.dev/kun432/scraps/87d7776909e4d9) — 開発者目線の検証メモ, 取得日 2026-05-07
- [note: テキスト指示だけで声を作れる日本語TTS Irodori-TTS VoiceDesign を Mac で試した](https://note.com/kazu_t/n/nbdd0ee937600) — Apple Silicon (MPS) 動作確認, 取得日 2026-05-07
- [はとはとブログ: Irodori-TTSの考察](https://hatohato.jp/blog/core/single.php?id=1032) — 学習データ・倫理規定・商用利用の整理, 取得日 2026-05-07
- [GitHub: iron-mukakin/Emoji-TTS](https://github.com/iron-mukakin/Emoji-TTS) — Irodori-TTSのフォーク（WebUI改善版）, 取得日 2026-05-07
