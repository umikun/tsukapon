# X/Twitter プラットフォームアルゴリズム調査

> 調査日：2026-04-06
> データ有効期限：2023年の初回オープンソース公開から2026年1月の第二次オープンソース公開までの全変遷を網羅
> 情報信頼性：🟢 公式発表／オープンソースコードで確認可能 | 🟡 権威あるメディア報道／データ分析 | 🔴 コミュニティテスト・推測

---

## 一、レコメンドアルゴリズムアーキテクチャの変遷

### 1.1 三段階パイプライン（Pipeline）

🟢 **出典：GitHub オープンソースコード**

Xのレコメンドシステムは三段階パイプラインアーキテクチャを採用しており、2023年の初回オープンソース公開（`twitter/the-algorithm`）から2026年のGrokバージョン（`xai-org/x-algorithm`）まで一貫した設計思想を持つ：

| 段階 | 機能 | 技術実装 |
|------|------|----------|
| **候補取得（Candidate Sourcing）** | 数億件の投稿から約1,500件の候補を絞り込む | in-network（フォロー中のコンテンツ）+ out-of-network（ML検索） |
| **ランキング（Ranking）** | 候補コンテンツのエンゲージメント確率を予測してスコアリング | Phoenix（Grok transformerモデル） |
| **フィルタリングとブレンディング（Filtering & Blending）** | 重複排除・多様性確保・広告挿入 | Home Mixerオーケストレーション層 |

- 出典：[GitHub - xai-org/x-algorithm](https://github.com/xai-org/x-algorithm) | [GitHub - twitter/the-algorithm](https://github.com/twitter/the-algorithm)

### 1.2 Grokによる全面的なレコメンド掌握（2025年10月→2026年1月オープンソース）

🟢 **出典：Elon Muskのツイート + GitHubリリース**

**タイムライン：**
- **2025年9月**：Muskが「The algorithm will be purely AI by November」と宣言し、2週間ごとのオープンソース公開を約束
- **2025年10月**：Grokが従来のヒューリスティクスルール（heuristics）を全面的に置き換え開始
- **2025年11月**：Following feedもGrokによるランキングに変更
- **2026年1月20日**：xAIがGitHubで`xai-org/x-algorithm`を公開、Rust書き換えバージョンが正式オープンソース化

**主な変更点：**
- ScalaからRust（62.9%）**+ Python（37.1%）**の混合アーキテクチャへ刷新
- コアtransformerアーキテクチャはGrok-1由来、レコメンドシーンに適応
- Grokが「すべての投稿を読み、すべての動画を視聴」（日次処理1億件以上のコンテンツ）
- 4週間ごとのコード更新＋開発者向け説明の提供を約束

- 出典：[Elon Muskのツイート](https://x.com/elonmusk/status/1969081066578149547) | [@XEngのツイート](https://x.com/XEng/status/2013471689087086804) | [TechCrunch報道](https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies/) | [Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-switching-to-fully-ai-powered-grok-algorithm/803174/)

### 1.3 四大コアモジュール（2026年オープンソース版）

🟢 **出典：GitHubリポジトリのコードおよびREADME**

| モジュール | 言語 | 機能 |
|------------|------|------|
| **Home Mixer** | Rust | オーケストレーション層。gRPCリクエストを受け取り、Pipeline全体を調整 |
| **Thunder** | Rust | インメモリ投稿ストレージ。Kafkaイベントを消費し、サブミリ秒のin-networkコンテンツクエリを提供 |
| **Phoenix** | Python/JAX | Grok transformerランキングエンジン。エンゲージメント確率を予測 |
| **Candidate Pipeline** | Rust | 再利用可能なフレームワーク：Sources取得→Hydrators拡充→Filters絞り込み→Scorers採点→Selector TopN返却 |

- 出典：[xai-org/x-algorithm README](https://github.com/xai-org/x-algorithm/blob/main/README.md) | [Phoenix README](https://github.com/xai-org/x-algorithm/blob/main/phoenix/README.md) | [DeepWiki分析](https://deepwiki.com/xai-org/x-algorithm)

### 1.4 Promptable Feeds（プロンプト指定可能なFeed）

🟡 **出典：Muskのツイート + メディア報道**

ユーザーが自然言語の指示でFeedを調整できる機能。例：「Show me more tech innovations, less politics」と入力するだけで変更可能。GrokをレコメンドエンジンへダイレクトOGに組み込んだことによる産物。

- 2025年9月にMuskが本機能を発表
- 2026年1月のオープンソース版にpromptable feedsインターフェースが含まれる
- 出典：[WebProNews](https://www.webpronews.com/xs-promptable-algorithm-musks-bid-to-hand-users-the-feed-controls/) | [Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-moving-to-personalized-ai-powered-algorithm/760698/)

---

## 二、エンゲージメント権重公式

### 2.1 正確な重み（オープンソースコードで確認可能）

🟢 **出典：xai-org/x-algorithm オープンソースコード + Social Media Today確認**

Xは主要SNSの中で唯一、レコメンドアルゴリズムを2回オープンソース化したプラットフォームであり、エンゲージメント権重は完全に公開されている：

| エンゲージメント種別 | 重み | 相対倍数（vs Like） | 説明 |
|----------------------|------|---------------------|------|
| **会話返信**（Reply + 投稿者からのエンゲージメント） | +75 | **150x** | 自分の返信が元投稿者から返信またはいいねされた場合 |
| **返信（Reply）** | +13.5 | **27x** | 通常の返信 |
| **プロフィールクリック** | +12.0 | **24x** | ユーザーがプロフィールを訪問していいねまたは返信した場合 |
| **会話の詳細クリック** | +11.0 | **22x** | ユーザーが会話を開いて返信またはいいねした場合 |
| **滞在時間（Dwell > 2min）** | +10.0 | **20x** | ユーザーが会話を開いて2分以上滞在した場合 |
| **リポスト（Retweet）** | +1.0 | **2x** | リポスト |
| **いいね（Like）** | +0.5 | **1x（基準）** | 基準値 |
| **ブックマーク（Bookmark）** | ~+10 | **~20x** | コミュニティ分析による推測、公式の正確値ではない |

**コアの洞察：会話の深さがすべてを凌駕する。** 投稿者からのエンゲージメントを引き出した返信チェーン1件は、いいね150個分の価値を持つ。

⚠️ **バージョン間の重みデータについて**：
- 2023年初回オープンソース版と2026年版では重みが若干異なる
- 初期のコミュニティ分析で引用されていた「Reply 27x, Retweet 40x」などのデータは2023年版の簡略計算に基づくもの
- 2026年版ではRetweet重みが大幅に低下（~20xから~2xへ）し、会話重みがさらに向上
- 本ドキュメントは2026年オープンソース版を基準とする

- 出典：[Social Media Today](https://www.socialmediatoday.com/news/x-formerly-twitter-open-source-algorithm-ranking-factors/759702/) | [posteverywhere.aiソース分析](https://posteverywhere.ai/blog/how-the-x-twitter-algorithm-works) | [Typefully分析](https://typefully.com/blog/x-algorithm-open-source)

### 2.2 ネガティブシグナル（ペナルティ機構）

🟢 **出典：オープンソースコード**

| ネガティブシグナル | ペナルティ重み | 効果 |
|--------------------|----------------|------|
| **報告（Report）** | -369x | ほぼ直接的に配信から除外 |
| **ブロック/ミュート/Show Less** | -74x | 該当ユーザーへのレコメンドを大幅に低下 |

🟡 **出典：メディア分析**

| ネガティブシグナル | ペナルティ効果 |
|--------------------|----------------|
| **外部リンク** | リーチが30〜50%低下。非Premiumアカウントでは2025年3月以降リンク付き投稿の中央値エンゲージメントがゼロ |
| **2つ以上のハッシュタグ** | リーチが約40%低下。スパムシグナルと判定される |
| **重複コンテンツ／リンク** | 段階的に視認性が低下。深刻な場合はシャドウバンを引き起こす |

- 出典：[posteverywhere.ai](https://posteverywhere.ai/blog/how-the-x-twitter-algorithm-works) | [Tweet Archivist](https://www.tweetarchivist.com/how-twitter-algorithm-works-2025)

---

## 三、Premiumサブスクリプションの視認性ブースト

### 3.1 アルゴリズム加算倍数

🟢 **出典：オープンソースコードで確認**

| シーン | Premiumブースト | 説明 |
|--------|-----------------|------|
| **In-network（フォロワーFeed）** | **4x** | フォロワーのFeedに自分の投稿が表示される確率×4 |
| **Out-of-network（非フォロワーFeed）** | **2x** | フォロワー外のFeedに自分の投稿が表示される確率×2 |

### 3.2 実際の効果データ

🟡 **出典：Buffer 1,880万件投稿分析 + メディア報道**

- Premiumアカウントの1投稿あたりリーチ量は通常アカウントの約**10倍**
- Premium+アカウントは2025年以降さらに格差が拡大
- Premiumの返信は人気投稿の議論内でデフォルトで上位表示（Q1 2026データで返信インプレッション30〜40%増）
- 非Premiumアカウントが外部リンク付き投稿を投稿した場合、2026年3月以降は中央値エンゲージメントがゼロ

### 3.3 TweepCredとPremiumの関係

🟡 **出典：Circleboom分析**

Premiumサブスクライバーは即時+100のTweepCred加算が付与されるため、-128スタートが-28スタートへと変わり、アカウントの立ち上げ期間（コールドスタート）を大幅に短縮できる。

- 出典：[Circleboom](https://blog-content.circleboom.com/does-x-premium-boost-algorithm/) | [posteverywhere.ai](https://posteverywhere.ai/blog/how-the-x-twitter-algorithm-works) | [Bufferデータ](https://buffer.com/resources/data-best-content-format-social-media/)

---

## 四、TweepCred アカウント信頼性スコア

🟢 **出典：オープンソースコード内のTweepCredモジュール**

### 4.1 基本機構

- すべてのXアカウントには非公開の信頼性スコア：**TweepCred**が存在する
- 範囲：**-128 〜 +100**
- 新規アカウントの初期値：**-128**
- 通常配信の最低閾値：**+17**（これを下回るとコンテンツがリミット制限される）
- Premiumサブスクライバーは即時**+100加算**を取得

### 4.2 影響要因

🟡 **出典：コミュニティによるリバースエンジニアリング分析**

TweepCredはPageRank型の加重複合スコアであり、以下の要因によって決まる：

| 要因 | 方向性 |
|------|--------|
| フォロー数／フォロワー比率 | フォローがフォロワーを大幅に上回る→ネガティブ |
| エンゲージメント品質 | 高品質な会話→ポジティブ |
| アカウント履歴 | 古いアカウント＋一貫した行動→ポジティブ |
| 投稿言語とBio | 完全なプロフィール→ポジティブ |
| 投稿スタイルの一貫性 | 突然の大幅な変更→ネガティブ |
| **Grokセンチメントスコア（2025年新追加）** | ポジティブ／建設的なコンテンツ→ポジティブ |

⚠️ **2025年の新変化**：Grok AIがすべての投稿の**センチメント（語調）**をスコアリングするようになり、ポジティブで建設的なコンテンツがより多くの配信を獲得できるようになった。

- 出典：[Circleboom TweepCred分析](https://circleboom.com/blog/tweepcred-what-it-is-why-it-matters-and-how-to-increase-your-score-on-x-twitter/) | [Radaar](https://www.radaar.io/resources-121/blog-388/are-you-ready-to-discover-the-hidden-x-algorithm-secrets-behind-tweepcred-shadow-hierarchy-and-dwell-time-in-2025-15361/)

---

## 五、コンテンツタイプ別の扱い

### 5.1 テキスト vs 動画：Xはテキストが動画を凌駕する唯一のプラットフォームか？

🟡 **出典：Buffer 4,500万件以上の投稿分析 + 複数メディア**

**結論：状況は複雑であり、データには矛盾が存在する。**

| データソース | 結論 |
|--------------|------|
| Buffer 2025〜2026データ | テキスト投稿の中央値エンゲージメント率（0.48%）が動画をわずかに上回る |
| 複数のSEO／マーケティング機関 | ネイティブ動画は約10倍のエンゲージメント＋アルゴリズム優遇配信を獲得 |
| 2026年ソーシャルメディア戦略レポート | ショート動画（37%）とテキスト（36%）のユーザー嗜好がほぼ拮抗 |

**より正確な表現**：Xは主要SNSの中で**テキスト投稿のパフォーマンスが動画に最も近く、場合によって上回るプラットフォーム**だが、「テキストが動画を圧倒する」とは一概に言えない。アルゴリズム的にはネイティブ動画が配信上の優遇を受けているが、実際のエンゲージメント率では高品質なテキスト投稿が動画に引けを取らない。

### 5.2 各コンテンツタイプのアルゴリズム的優遇

🟡 **出典：複数の分析を統合**

| コンテンツタイプ | アルゴリズムの扱い |
|------------------|-------------------|
| **純テキスト投稿** | エンゲージメント率が安定して最高。特に会話を誘発するのに適している |
| **ネイティブ動画（<2:20）** | 配信上の優遇あり。完全視聴率が重要なシグナル |
| **画像付き投稿** | 滞在時間（dwell time）を増加させるポジティブシグナル |
| **外部リンク付き投稿** | ⚠️ 深刻なペナルティ：リーチが30〜50%低下、非Premiumではほぼ非表示 |
| **引用リポスト（Quote Tweet）** | 通常のリポストより高い重み |
| **Thread（長文スレッド）** | 複数投稿のエンゲージメントが累積し、全体的な効果が高い |

- 出典：[Buffer](https://buffer.com/resources/data-best-content-format-social-media/) | [Sprout Social](https://sproutsocial.com/insights/twitter-algorithm/) | [SocialBee](https://socialbee.com/blog/twitter-algorithm/)

---

## 六、重要な時間帯

### 6.1 ゴールデン30分とエンゲージメント速度（Engagement Velocity）

🟡 **出典：複数の分析機関のコンセンサス**

- **最初の30分**が決定的なウィンドウ：この時間帯のエンゲージメント速度がアルゴリズムによるより大きなトラフィックプールへの押し上げを決める
- より広義では**最初の2時間**も重要
- **速度 > 総量**：10分以内に100いいね > 3日間かけて累積した500いいね
- アルゴリズムのコアロジック：早期エンゲージメント = 品質認定（quality stamp）

### 6.2 滞在時間（Dwell Time）

🟢 **出典：オープンソースコードの重み定義**

- ユーザーが投稿／会話に2分以上滞在した場合 = +10重み（いいねの約20倍）
- 短い滞在時間は低品質コンテンツと見なされ、アルゴリズムが抑制
- つまり**読み続けたくなる長文**は**さっと流し読みされる短いコンテンツ**よりもアルゴリズムに好まれる

### 6.3 最適な投稿時間

🟡 **出典：Buffer 100万件投稿分析 + Sprout Social + SocialPilot 5万アカウント分析**

| 次元 | 推奨 |
|------|------|
| **最適時間帯** | 平日 9AM〜2PM（現地時間）、次点は12PM〜6PM |
| **最適曜日** | 火曜・水曜・木曜（火曜が最良） |
| **最悪の曜日** | 土曜日 |
| **投稿頻度** | **1日3〜5件**が最適レンジ、2〜3時間間隔 |
| **頻度上限** | 1日5件超は成長がむしろ鈍化 |
| **頻度下限** | 1日1件未満は成長が著しく不足 |

⚠️ 上記はグローバル英語ユーザーのデータ。日本語クリエイターはターゲット読者のタイムゾーンに合わせて調整が必要（例：日本のフォロワーを対象にする場合、日本時間 9AM〜2PM に合わせる）。

- 出典：[Buffer](https://buffer.com/resources/best-time-to-post-on-twitter-x/) | [Sprout Social](https://sproutsocial.com/insights/best-times-to-post-on-twitter/) | [SocialPilot](https://www.socialpilot.co/insights/best-time-to-post-on-twitter) | [Tweet Archivist](https://www.tweetarchivist.com/twitter-posting-frequency-guide-2025)

---

## 七、シャドウバン（Shadow Ban）

### 7.1 四種類のタイプ

🟡 **出典：シャドウバン検出ツール + コミュニティ分析**

| タイプ | 症状 |
|--------|------|
| **Search Suggestion Ban** | ユーザー名が検索候補に表示されない |
| **Search Ban** | 投稿が検索結果に表示されない |
| **Ghost Ban** | 返信が他のユーザーから見えない |
| **Reply Deboosting** | 返信が「Show more replies」内に折りたたまれる |

### 7.2 発動条件

🟡 **出典：Pixelscan + 複数のガイド**

| 行動 | リスクレベル |
|------|-------------|
| 短時間での大量フォロー／フォロー解除 | 🔴 高（大量フォロー解除で3ヶ月シャドウバンが発動する場合あり） |
| 1時間以内に200件以上いいね | 🔴 高（自動化検出） |
| フォローしていない大量のユーザーへの返信 | 🟡 中 |
| 同じリンク／ハッシュタグの繰り返し投稿 | 🟡 中 |
| 不審なサードパーティツールの使用 | 🔴 高 |
| 複数ユーザーから報告されたコンテンツの投稿 | 🔴 高（-369xペナルティ） |

### 7.3 検出方法

- オンラインツール：[shadowban.yuzurisa.com](https://shadowban.yuzurisa.com/) でユーザー名を入力するだけで4種類の制限を検出可能
- 手動確認：自分をフォローしていない人に、自分のユーザー名や返信を検索してもらう

### 7.4 回復方法

🟡 **出典：複数ガイドのコンセンサス**

1. **即座に停止**：発動行動をトリガーする行為をやめる（徐々に減らすのではなく、完全に停止）
2. 重複・低品質・過剰なリンク／ハッシュタグを含む投稿を削除
3. 不審なサードパーティアプリの連携を解除
4. **48〜72時間待機**（自動シャドウバンは通常この期間内に解除）
5. 完全回復サイクル：**2〜14日**
6. 回復期間中は通常の低頻度・高品質の投稿を維持

- 出典：[Pixelscanガイド](https://pixelscan.net/blog/twitter-shadowban-2025-guide/) | [Tweet Archivist](https://www.tweetarchivist.com/twitter-shadowban-complete-guide-2025) | [Multilogin](https://multilogin.com/blog/twitter-shadow-bans/)

---

## 八、広告とオーガニック成長の関係

### 8.1 有料 vs オーガニックのパフォーマンス

🟡 **出典：WebFX + メディア報道**

| 指標 | 有料プロモーション | オーガニック投稿 |
|------|-------------------|-----------------|
| 平均CTR | 1〜3% | 0.5〜1.5% |
| Premiumアカウントのリーチ | — | 通常アカウントの約10倍 |
| 非Premiumのリンク付き投稿エンゲージメント | — | 0（2026年3月以降） |

### 8.2 重要な発見

🟡 **出典：複数の分析**

- 有料とオーガニックのアルゴリズムは**独立して動作**しており、「お金を払うとオーガニックリーチが下がる」というペナルティは存在しない
- ただし構造的なトレンドとして、オーガニックリーチは継続的に低下している（X特有ではなくプラットフォーム全体の現象）
- 広告で獲得した新フォロワーはその後のオーガニック投稿のパフォーマンスに**影響を与える**（フォロワーが増える→in-network配信が増加）
- Premiumサブスクリプションは本質的に**最低コストの「広告出稿」**：4x/2xの視認性ブーストは同等価格の広告効果をはるかに上回る

- 出典：[WebFX](https://www.webfx.com/blog/social-media/x-twitter-marketing-benchmarks/) | [Avenue Z](https://avenuez.com/blog/2025-2026-x-twitter-organic-social-media-guide-for-brands/)

---

## 九、Community Notes の影響

### 9.1 投稿パフォーマンスへの影響

🟢 **出典：ワシントン大学研究（2025年9月）**

| 指標 | Community Note付与後の変化 |
|------|---------------------------|
| リポスト数 | **46%減少** |
| いいね数 | **44%減少** |
| 閲覧数 | 影響は小さい（FeedアルゴリズムはNote付き投稿を積極的に降格しない） |

### 9.2 重要な詳細

- XはアルゴリズムレベルでCommunity Note付き投稿の配信を積極的に下げることは**しない**
- 減少の主因は**ユーザーの行動変化**：Noteを見たユーザーがリポストやいいねを減らすことによる
- Noteの**タイムライン的な有効性**が極めて重要：48時間後に付与されたNoteはほぼ効果なし（コンテンツはすでに拡散済み）
- **改ざんメディア**（フェイク写真／動画）へのNoteが最も大きな効果を発揮

### 9.3 クリエイターへの示唆

🔴 **推測／戦略的提言**

- 物議を醸す可能性がある事実的な主張を投稿する際は出典を確認する
- Community Noteはアルゴリズム的には直接降格させないが、**エンゲージメントを間接的に殺す**（リポスト-46%）
- Noteが付いた投稿は閲覧数は変わらなくても、拡散力が半減する
- 建設的かつ出典のあるコンテンツはNoteを付けられにくい

- 出典：[ワシントン大学研究](https://www.washington.edu/news/2025/09/18/community-notes-x-false-information-viral/) | [Wikipedia - Community Notes](https://en.wikipedia.org/wiki/Community_Notes)

---

## 十、コンテンツクリエイターへのコアな示唆

### 10.1 アルゴリズム最適化の優先度（ROI順）

| 優先度 | 戦略 | 根拠 |
|--------|------|------|
| **P0** | 会話を誘発し、すべてのコメントに返信する | 会話返信150x重み |
| **P0** | Premiumに加入する | 4x/2xの視認性＋TweepCred加算＋リンク投稿の視認性 |
| **P1** | 最初の30分でエンゲージメントを爆発させる | エンゲージメント速度が配信量を決定 |
| **P1** | 人を立ち止まらせて読ませる長文を書く | Dwell Time 20x重み |
| **P2** | 平日9AM〜2PMに投稿する | データで裏付けられた最適時間帯 |
| **P2** | 外部リンクを避ける（またはコメント欄に置く） | 30〜50%のリーチペナルティ |
| **P3** | ポジティブ／建設的な語調を保つ | Grokセンチメントスコアが配信に影響 |
| **P3** | ハッシュタグを2個以下に抑える | 2個超でスパム判定が発動 |

### 10.2 絶対禁止事項

| 行動 | 結果 |
|------|------|
| 短時間での大量フォロー／フォロー解除 | 3ヶ月シャドウバン |
| 自動化ツールでのエンゲージメント操作 | アカウント信頼性の永続的な損傷 |
| 外部リンク付き投稿の頻繁な投稿（非Premium） | 投稿がほぼ非表示 |
| 報告されたコンテンツの投稿 | -369xペナルティ、コンテンツが直接消失 |
| 突然の投稿パターン変更 | TweepCredの低下 |

### 10.3 Xの独自優位性（他プラットフォームとの比較）

- **アルゴリズムを2回オープンソース化した唯一の主要プラットフォーム**：精確な最適化が可能
- **テキストコンテンツに親和的**：他のプラットフォームのように動画制作を強いられない
- **会話駆動型**：表面的なエンゲージメントではなく、深い交流を真に報酬として扱う
- **Promptable Feeds**：ユーザーが推薦をカスタマイズできるため、高品質なニッチコンテンツに長期的な価値がある

---

## 付録：情報源一覧

### 公式／一次情報源
- [xai-org/x-algorithm GitHub](https://github.com/xai-org/x-algorithm) — 2026年1月オープンソース化されたGrokバージョンアルゴリズム
- [twitter/the-algorithm GitHub](https://github.com/twitter/the-algorithm) — 2023年初回オープンソース版
- [Elon Muskのツイート（2025.09）](https://x.com/elonmusk/status/1969081066578149547) — アルゴリズムの純粋AI化を宣言
- [@XEngのツイート（2026.01）](https://x.com/XEng/status/2013471689087086804) — 新アルゴリズムのオープンソース化を発表

### 権威あるメディア報道
- [TechCrunch: X open sources its algorithm](https://techcrunch.com/2026/01/20/x-open-sources-its-algorithm-while-facing-a-transparency-fine-and-grok-controversies/)
- [Social Media Today: Key ranking factors](https://www.socialmediatoday.com/news/x-formerly-twitter-open-source-algorithm-ranking-factors/759702/)
- [Social Media Today: Grok algorithm shift](https://www.socialmediatoday.com/news/x-formerly-twitter-switching-to-fully-ai-powered-grok-algorithm/803174/)

### データ分析
- [Buffer: Best content format 2026（4,500万件以上の投稿分析）](https://buffer.com/resources/data-best-content-format-social-media/)
- [Buffer: Best time to post（100万件の投稿分析）](https://buffer.com/resources/best-time-to-post-on-twitter-x/)
- [Sprout Social: Twitter algorithm 2026](https://sproutsocial.com/insights/twitter-algorithm/)
- [ワシントン大学: Community Notes研究](https://www.washington.edu/news/2025/09/18/community-notes-x-false-information-viral/)

### コミュニティ深度分析
- [posteverywhere.ai: ソースコード解説](https://posteverywhere.ai/blog/how-the-x-twitter-algorithm-works)
- [Typefully: アルゴリズム更新分析](https://typefully.com/blog/x-algorithm-open-source)
- [Circleboom: TweepCred詳細解説](https://circleboom.com/blog/tweepcred-what-it-is-why-it-matters-and-how-to-increase-your-score-on-x-twitter/)
- [nibzard: Rust+Pythonアーキテクチャ分析](https://nibzard.github.io/twitter-algorithm-tufte/)
- [ByteByteGo: アルゴリズムアーキテクチャ図解](https://blog.bytebytego.com/p/the-algorithm-that-powers-your-x)
- [Pixelscan: シャドウバンガイド](https://pixelscan.net/blog/twitter-shadowban-2025-guide/)
- [DeepWiki: x-algorithmリポジトリ分析](https://deepwiki.com/xai-org/x-algorithm)
