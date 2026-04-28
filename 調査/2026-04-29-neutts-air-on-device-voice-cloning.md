---
created: 2026-04-29
tags: [調査, neutts-air, 音声クローン, on-device-AI, TTS]
source: https://x.com/L_go_mrk/status/2049086222803620328
---

# neutts-air：3秒で声をクローンする"ローカル完結"TTS、動画マーケで本当に使えるか

> **TL;DR**
> Neuphonic社が2025年10月にApache-2.0で公開したオンデバイスTTS。Qwen2 0.5B＋NeuCodecの構成で**748Mパラメータ／RAM 400〜800MB**、3〜15秒の参照音声で即時クローン可能。ツイートの「ローカル完結＝機密OK」は概ね正しいが、出力には**Perth Watermarkが必ず埋め込まれる**＋言語サポートが英語中心。日本語社内研修ナレーションに即投入するには、**①日本語性能を実機で必ず検証、②"他人の声"を学習させる場合の同意取得・契約整備、③Perth透かしを残せる用途かの確認**の3点を握っておく必要がある。

## 📌 元テキスト（抜粋）

> これは動画マーケやるなら試した方がいいやつだ。。。
> neutts-air：3秒の音声サンプルから自分の声をクローンできる超リアルなTTSモデル。
> ローカルで完結するので、機密性の高い社内研修動画などのナレーションも安心して任せられる。

出典: [[Clippings/Post by @L_go_mrk on X 3.md]] / [元投稿（@L_go_mrk, 2026-04-28）](https://x.com/L_go_mrk/status/2049086222803620328)

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| neutts-air | Neuphonic社のオンデバイス音声合成LLM。3秒で声をクローン | NeuTTS Air, Neuphonic, on-device TTS |
| Neuphonic | ロンドン拠点の音声AIスタートアップ。NeuTTS／NeuCodecを開発 | Neuphonic AI, voice agents |
| GGUF | llama.cpp系で使われる量子化済みモデル形式。CPU推論が前提 | llama.cpp, gguf quantization Q4 Q8 |
| NeuCodec | Neuphonic独自のニューラル音声コーデック。0.8 kbps / 24 kHzで高音質を実現 | neural audio codec, single codebook |
| Qwen2 | Alibabaの言語モデル。NeuTTS Airのバックボーン | Qwen2 0.5B, 小型LLM |
| Perth Watermarker | resemble-ai/perth が公開する知覚閾値透かし。生成音声に必ず埋め込まれる | Perth watermark, audio provenance |
| espeak-ng | 古典的なオープンソース音声合成エンジン。NeuTTS Airは前段の音素変換に依存 | eSpeak NG dependency |
| ボイスクローニング | 既存音声からその話者の声色をモデル化して任意の発話を生成する技術 | voice cloning, instant cloning |
| ディープフェイク詐欺 | クローン音声でCEOやコールセンターを騙す金銭被害。2026年に急拡大 | CEO fraud 2.0, vishing |
| Apache-2.0 | 商用利用OK・特許条項ありのOSSライセンス | Apache 2.0 commercial use |

---

## 🧭 背景 / なぜ今これが話題なのか

**2025年10月2日**、Neuphonicが NeuTTS Air を Apache-2.0 で公開しました。「**世界初の超リアルなオンデバイス音声言語モデル**」を看板に掲げ、748Mパラメータ・GGUF量子化済みで **Raspberry Pi上でも動く** ことが衝撃的に受け止められました（[MarkTechPost, 2025-10-02](https://www.marktechpost.com/2025/10/02/neuphonic-open-sources-neutts-air-a-748m-parameter-on-device-speech-language-model-with-instant-voice-cloning/)）。

それまでの音声クローン市場は、**ElevenLabsを頂点とするクラウド従量課金モデル**が支配的でした。XTTS v2のCoqui社は2024年初頭にシャットダウン、コミュニティに残された状態。OpenVoiceやChatterboxといったMITライセンスの選択肢はあるものの、 **「3秒で十分／オンデバイス／商用OK」を3点同時に満たす選択肢は2025年9月時点で実質ゼロ** でした。

そこへ 「**3秒・ローカル・Apache-2.0**」 という3点セットでneutts-airが登場し、 **「クラウドAPI課金が嫌だが品質は妥協したくない」中小企業・個人クリエイター・プライバシー重視業種** が一斉に飛びついた、というのが2026年4月時点の温度感です。

ツイートの「動画マーケやるなら試した方がいい」もこの流れで、**自分の声を一度3秒録ればナレーションを無限に量産できる**＝既存の収録／編集コストが消えるという期待が背景にあります。

ただし背景にはもう1つ、無視できない流れがあります。 **音声クローン詐欺の急拡大** です。FraudのVoice deepfake攻撃は直近3年で **+2,137%**、銀行等の平均被害額は **1件$600,000** （[SQ Magazine, 2026年版](https://sqmagazine.co.uk/ai-voice-cloning-fraud-statistics/)）。ローカルで動く＝ **追跡が効きづらい** とも言える両刃の剣で、各国で規制が動き始めています。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 3秒の音声サンプルからクローンできる | 公式は「as little as 3 seconds」。ただし**推奨は3〜15秒**、モノラル・16〜44 kHz・wav・無雑音・連続発話が条件 | [Hugging Face neuphonic/neutts-air](https://huggingface.co/neuphonic/neutts-air) | ⚠️ ほぼ一致（条件多め） |
| ローカルで完結する | Q4で400〜600MB、Q8で約800MB RAM。GGUF形式でllama.cppベース、CPU推論、Raspberry Pi/スマホでも動作確認済み | [MarkTechPost, 2025-10-02](https://www.marktechpost.com/2025/10/02/neuphonic-open-sources-neutts-air-a-748m-parameter-on-device-speech-language-model-with-instant-voice-cloning/) | ✅ 一致 |
| 超リアル | Kokoro と並び**低レイテンシ枠の双璧**との評。ただしブラインドテストで明確にElevenLabs超えと示すデータはneutts-airには未公開（Chatterboxは63.75%でElevenLabs超えのデータあり） | [BentoML, 2026年版TTSサーベイ](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models) | ⚠️ ほぼ一致（用法注意） |
| 機密性の高い社内研修動画も安心 | データがクラウドに出ない点は事実。ただし**生成音声には Perth Watermarker が必ず埋め込まれる**、社内動画でも透かし入りになる | [Hugging Face モデルカード](https://huggingface.co/neuphonic/neutts-air) | ⚠️ ほぼ一致（透かし条件あり） |
| 自分の声をクローン | 自分の声に限らず、参照wavを与えれば**他人の声でもクローン可能**。同意・契約・各国の右of publicity規制に直撃する用途リスクあり | [Holon Law, 2026 Right of Publicity](https://holonlaw.com/entertainment-law/synthetic-media-voice-cloning-and-the-new-right-of-publicity-risk-map-for-2026/) | ⚠️ ほぼ一致（誤解を招く表現） |
| 動画マーケやるなら試した方がいい | 商用利用は **Apache-2.0で許諾**、ただし**NeuTTS-Nano は別ライセンス（NeuTTS Open License 1.0）** で条件異なる。商用前にどちらを使うか要確認 | [GitHub neuphonic/neutts](https://github.com/neuphonic/neutts) | ⚠️ ほぼ一致（モデル選択注意） |

---

## 🌐 最新動向（2026-04-29時点）

- **NeuTTS-Air が Apache-2.0 でリリース**：2025-10-02、Neuphonic公式が748MパラメータのオンデバイスTTSを公開。Hugging FaceとGitHubに同時公開 — [MarkTechPost](https://www.marktechpost.com/2025/10/02/neuphonic-open-sources-neutts-air-a-748m-parameter-on-device-speech-language-model-with-instant-voice-cloning/), 2025-10
- **ファミリー化**：本家repoが `neutts` に統合され、**NeuTTS-Air（360M active）／NeuTTS-Nano（120M active、より小型でラズパイ向け）** の2モデル展開に。Nanoは別ライセンス — [GitHub neuphonic/neutts](https://github.com/neuphonic/neutts), 2026-0X
- **エコシステム拡大**：SUP3RMASS1VE等のサードパーティWebUI実装、Tavus等のエンタープライズベンダーfork、Spheronなど分散GPUプラットフォームのデプロイガイドが続々登場 — [Spheron Blog](https://www.spheron.network/blog/neutts-air-spheron-voice-ai/), 2025-Q4
- **Voice agent市場の本命候補に**：低レイテンシ＋オンデバイスでKokoroと並ぶ「voice agentの実装基盤」候補と評価。GPU不要のCPU推論が鍵 — [BentoML 2026年TTS総覧](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models), 2026-0X
- **詐欺対策側のニュースとセット読み必須**：voice deepfake攻撃が3年で+2,137%増、CEO Fraud 2.0として企業対策が急務に。NeuTTS Airの登場は「攻撃側コストを劇的に下げた」ともとれる — [SQ Magazine 2026 Fraud Stats](https://sqmagazine.co.uk/ai-voice-cloning-fraud-statistics/), 2026-04
- **規制ギャップ**：米国・EU・日本で voice cloning 規制の方向性が一致せず、「1つの生成音声で複数法域の責任が同時発生する」状況に。Japan/Koreaは特に identity rights / IPの保護に寄る — [Harris Sliwoski, 2026 Global Rules](https://harris-sliwoski.com/blog/deepfakes-voice-cloning-and-ai-impersonation-the-global-rules-are-already-here-and-they-dont-agree/), 2026-0X

---

## 🧩 関連概念・隣接分野

- **NeuCodec**: NeuTTS Airの音質を支えるNeuphonic独自のニューラル音声コーデック。0.8 kbps / 24 kHz・単一コードブックで高音質を実現する独立repoが存在。NeuTTS Airの「軽量なのに音が良い」のキモ
- **Perth Watermarker**: resemble-ai/perthが公開する知覚閾値透かし。NeuTTS Airは生成音声すべてに自動付与しており、 **生成物の出処判定（プロベナンス）** を技術で担保する流れの代表例
- **espeak-ng依存**: NeuTTS Airは前段の音素変換でクラシックなeSpeak-NGを使う。**日本語の音素辞書精度がそのまま日本語ナレーション品質に効いてくる**ため、社内研修ナレーション用途では実機検証必須
- **Kokoro**: Hugging Faceで人気の小型オープンソースTTS。NeuTTS Airとよく比較される。**Kokoroは音声クローン非対応**だが事前学習済みボイスの品質はトップクラス、用途で使い分け
- **CEO Fraud 2.0 / Voice Phishing**: クローン音声を使った経営層なりすまし詐欺の総称。2026年は「3秒で誰でもクローンできる時代」のリスクシナリオの代表格、企業のIT部門が新たな声紋認証・コールバックポリシーを整備する動きあり

vault内の関連ノート（横展開候補）:
- [[2026-04-26-cash-while-you-sleep-10-repos]]
- [[Clippings/Post by @L_go_mrk on X.md]]
- [[Clippings/Post by @L_go_mrk on X 1.md]]
- [[Clippings/Post by @L_go_mrk on X 2.md]]

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 3秒でクローン・ローカル完結・Apache-2.0という3点セットは2026年4月時点でほぼ唯一無二。クラウドAPI課金から逃れたい中小・個人クリエイター・コールセンター・voice agent開発者にとって "実質ベンダーロックイン解除" のインパクトがある。社内データがクラウドに出ないのでGDPR/個人情報保護法/医療系規制との相性も良い

- **否定 / 慎重派の主張**:
    - **言語サポート**: 公式が積極的にうたうのは英語中心。日本語の自然性は実機検証なしに前提できない（espeak-ng の日本語音素辞書品質に左右される）
    - **Perth透かし**: ブランド価値の高いマーケ動画で、誰でも「これAI生成だ」と判定できる音声を出して大丈夫か？YouTube/TikTokの規約変更次第では「AI生成ラベル必須」と組み合わさり訴求力が落ちる可能性
    - **法的リスク**: 「自分の声」と書きつつ実際は他人の声を入れることもできる構造。**クライアントの声・タレントの声・故人の声** をうっかり学習させて公開した瞬間、Right of Publicity / 不正競争防止法 / 名誉毀損で詰むケースが既に発生中
    - **詐欺加担リスク**: 攻撃者が同じツールで「上司の声」「親族の声」を3秒のSNS音声から作れてしまう。出てくるたびに「自分も使うべき」と紹介する側にも、攻撃ハードルを下げているという批判が常にある
    - **オープン重みのトレードオフ**: クラウドAPIなら事業者側でレートリミット・本人確認・悪用検知を入れられるが、ローカル＋オープン重みは事実上「使う人の倫理任せ」

- **中立的に見るときの補助線**:
    - 「自分の声を量産する」用途と「他人の声を再現する」用途は **法的に別物として扱う** （社内ガバナンス上もポリシーで分ける）
    - **動画マーケ用途では `①話者は本人 or 書面同意済み` `②Perth透かしを残す or 別途ラベルを付ける` `③クローン元wavとモデル出力ログを6ヶ月保管` の3点セット** をルール化するだけで、「便利さ」と「責任」のバランスが取れる
    - クラウドAPIと併用が現実解：機密データ＋社内向けは neutts-air ローカル、対外公開のブランドナレーションは ElevenLabs等で本人契約 という運用分離

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] **日本語ナレーションの実機品質**：Macbook M3 / iPhone 15で日本語の参照音声を入れた時、敬体／話し言葉／長音／促音の自然さがElevenLabs日本語ボイスと比較してどれくらい劣るか、ABテストしたい
- [ ] **Perth透かしの実用性**：透かし入り音声をH.264にエンコード→ファイル変換→再エンコードしても透かしは残るのか？マーケ動画のワークフローで実用に耐えるか
- [ ] **NeuTTS-Nano vs Air の選択基準**：Nanoのライセンス（NeuTTS Open License 1.0）の商用条件を読み込み、社内研修動画用途でAirとNanoのどちらを選ぶべきか整理
- [ ] **日本国内の法的整理**：日本において他人の声をクローンして公開する行為は2026年4月時点で何法で問えるか（不正競争防止法／パブリシティ権／名誉毀損／著作隣接権 etc.）
- [ ] **コールセンター voice agent 用途のレイテンシ**：Real-Time Factor（RTF）と First Audio Chunk Time（FAT）が、CPU推論で電話の「自然な間」に間に合うか実測値が欲しい
- [ ] **ファインチューン可能性**：3秒のzero-shot cloningだけでなく、自分の声を10分録ってfine-tuneしたら品質はどこまで伸びるか、neutts-air が後段のfine-tune APIを公式に持っているか

---

## 📚 参考資料

- [GitHub - neuphonic/neutts](https://github.com/neuphonic/neutts) — 公式repo（NeuTTS-Air / Nano両モデルが統合）、ライセンス確認に使用、取得日 2026-04-29
- [Hugging Face - neuphonic/neutts-air](https://huggingface.co/neuphonic/neutts-air) — モデルカード、参照音声要件・Perth透かし・espeak-ng依存の確認、取得日 2026-04-29
- [MarkTechPost - Neuphonic Open-Sources NeuTTS Air](https://www.marktechpost.com/2025/10/02/neuphonic-open-sources-neutts-air-a-748m-parameter-on-device-speech-language-model-with-instant-voice-cloning/) — リリース日2025-10-02・パラメータ数・アーキテクチャ確認、取得日 2026-04-29
- [BentoML - The Best Open-Source TTS Models in 2026](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models) — 同時代の競合（Kokoro/XTTS/OpenVoice/Chatterbox）との位置取り、取得日 2026-04-29
- [Holon Law - Synthetic Media & Voice Cloning Risk Map 2026](https://holonlaw.com/entertainment-law/synthetic-media-voice-cloning-and-the-new-right-of-publicity-risk-map-for-2026/) — Right of Publicity観点の法的リスク確認、取得日 2026-04-29
- [Harris Sliwoski - Deepfakes, Voice Cloning, and AI Impersonation 2026](https://harris-sliwoski.com/blog/deepfakes-voice-cloning-and-ai-impersonation-the-global-rules-are-already-here-and-they-dont-agree/) — 各国規制の不一致状況、取得日 2026-04-29
- [SQ Magazine - AI Voice Cloning Fraud Statistics 2026](https://sqmagazine.co.uk/ai-voice-cloning-fraud-statistics/) — voice deepfake詐欺の被害規模数値、取得日 2026-04-29
- [Spheron Blog - Deploy NeuTTS Air](https://www.spheron.network/blog/neutts-air-spheron-voice-ai/) — エコシステム動向（分散GPU上のデプロイ事例）、取得日 2026-04-29

---

## 🗒 メモ

このネタは **「3秒・ローカル・Apache-2.0」** の3拍子をフックに、ニュースを束ねるよりも批評型でいける素材。手元のW18戦略ともきれいに重なる。

書き方の方向性:
1. **批評型X連投**（4〜5投稿）：「3秒でクローン！動画マーケに革命！」系のポストへの「中身は神ツールだけど、Perth透かし＋言語＋法的リスクの3点を抜くと事故る」型ツッコミ。連投シリーズ⑤候補
2. **note記事の1トピック**：本日(4/29)の note の延長で「GW明けに自社で試す軽量AI候補」の1本として使える。GPU-aaSの記事と接続できる
3. **クライアント提案**：クローン音声を「自分の声で量産」と勧めるより、 **「自分専用の声＋契約済みのタレント声以外は使わない」社内ポリシーをまず作る** をセットで提案するほうが信頼を得やすい

要するに、ツイート主のポジションは **「便利さの上澄みを切り取った推奨」** で、社内研修動画に投入する前に **言語性能・Perth透かし・声の権利・詐欺加担リスク** の4点を握っておかないと、半年後に上司から「あれ大丈夫だったの？」と詰められる側になる。

