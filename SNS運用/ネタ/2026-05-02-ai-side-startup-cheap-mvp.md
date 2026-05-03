---
created: 2026-05-02
tags: [調査, AI駆動開発, 新規事業, MVP, ClaudeCode, リーンスタートアップ]
source: "[[Clippings/AIで金をかけずにサクッと新規事業を作る方法。.md]]"
---

# AIで金をかけずに新規事業を立ち上げる5ステップ論を裏取りする

> **🔗 関連コンテンツ**
> - 📋 元記事: [[Clippings/AIで金をかけずにサクッと新規事業を作る方法。.md]]
> - 📋 vault全体ルール: [[CLAUDE.md]]
> - 🧠 my-cloneブレイン: [[_ kiwami/my-clone/brain/専門知識.md]]

> **TL;DR**
> Claude Code / Codex を中心に「市場リサーチ→MVP定義→LP→マーケ→営業」を一気通貫で回すという主張。骨格は2026年現在のAI駆動開発のメインストリームと一致しており、`ai-website-cloner-template` (12.6k★) や `Higgsfield MCP`（2026-04-30公開）など実装ツール側の整備も急速に進んでいる。一方で「LPデザインを"ぬるっとパクる"」「問い合わせフォーム営業」といった筆者の表現は法務・倫理の地雷を踏みやすく、ここをそのまま真似ると確実に事故る。月額4,980円のメンバーシップ価格はnote相場（500〜1,500円）の上振れ帯で、コンサル特典なしには維持しづらい水準。

## 📌 元テキスト（抜粋）

> 「今のAI情勢で金をかけずにサクッと新規事業を作るならAI駆動塾はこうします。」という記事です。走り書きなので雑な文章なのをお許しください。使うメインのAIはClaudeCodeかCodex。この2つを触っておけばとりあえずOK。…①市場リサーチ → ②商材づくり（受注後でいい） → ③LPと資料作り（競合をぬるっとパクる） → ④マーケ（広告/X/動画/SEO） → ⑤営業（テレアポ/フォーム営業/交流会）。10〜20回やって1つ当たるかどうか。

出典: [[Clippings/AIで金をかけずにサクッと新規事業を作る方法。.md]]（原典: [@L_go_mrk on X, 2026-04-30](https://x.com/L_go_mrk/status/2049814773982974118)）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Claude Code | Anthropic製のターミナル型AIコーディングエージェント。2026年4月時点でv2.1.x、Opus 4.7対応 | `Claude Code v2.1` `Skills` `Agent Teams` |
| Codex | OpenAI系のコーディングAI（CLI/IDE）。Claude Codeと並走するメインストリーム | `Codex CLI` `OpenAI agent` |
| MCP (Model Context Protocol) | Anthropic主導のエージェント拡張プロトコル。外部サービス（画像/動画/DB等）への共通インターフェース | `MCP server` `Anthropic protocol` |
| Higgsfield MCP | 画像・動画生成（Veo, Sora 2, Kling, Hailuo等30+モデル）をClaude Codeから叩けるMCPサーバー。2026-04-30公開 | `Higgsfield AI` `UGC pipeline` |
| ai-website-cloner-template | URLを渡すと既存サイトのデザインをNext.js + shadcn/ui で再構築するAIエージェント用テンプレ。GitHub 12.6k★ | `JCodesMore` `clone-website skill` |
| SkillGraphs | l_mrk氏が提唱するObsidian上の「ナレッジを粒度ごとにグラフ化してClaude Codeに参照させる」運用 | `SkillGraphs note` `知識グラフ + AI` |
| Claude Design | 2026-04-17公開のAIデザインツール。LP/モック/スライドをテキストから一気通貫生成 | `Claude Design` `Anthropic Labs` |
| MVP | Minimum Viable Product。最小限の機能で市場検証する製品。リーンスタートアップの中核 | `リーンスタートアップ` `BMLループ` |
| 特定電子メール法 | 日本の迷惑メール規制法。問い合わせフォーム営業は第3条4項の例外で原則合法だが拒否表示時はNG | `特電法 第3条4項` `公表メール例外` |
| Remotion + Whisper | プログラマブル動画生成 + 自動文字起こしで字幕付きショートを量産する定番スタック | `faster-whisper` `WhisperX` |

---

## 🧭 背景 / なぜ今これが話題なのか

筆者 @L_go_mrk（フォロワー1.6万）は「AI駆動塾」というnoteメンバーシップを運営する個人事業者で、本記事は **2026年4月30日** にXで公開された走り書きスレッドのnote転載に近い。同氏のnoteには `世界一やさしいClaudeCodeの教科書`, `SkillGraphsを知っているか。`, `X運用の教科書` などが並び、**「AI駆動 × 1人でスケール」という今期最ホットの読者層**を狙い撃つポジショニング。

この種の「AIだけで個人がフルスタックの新規事業を回す」言説が一気に増えたのには地続きの理由がある：

1. **Claude Code が"v2"フェーズに入った**: 2026年1〜3月の3ヶ月で `Skills` / `Plugins` / `Agent Teams` / `Hooks` / `Voice mode` / `Auto mode` が連続投入され、CLIから事業オペ全部叩けるレベルに達した（[Uravation, 2026-04](https://uravation.com/media/claude-code-v2-1-101-30-releases-5-weeks-guide-2026/)）
2. **Opus 4.6で1Mコンテキスト一般提供（2026-03-13）**: 仕様書・既存コードベース・ナレッジを丸ごと食わせて「コードを書きながら戦略を相談する」エージェントが現実的になった
3. **Claude Design / Higgsfield MCP / Sora 2 / Veo 3.1** などビジュアル系の実装も4月に揃った: 「LPもモックも動画広告も全部AI」が **2026-04の30日間** に同時実装可能になった瞬間
4. **noteメンバーシップ市場の過熱**: 上限が月額5万円に引き上げられ（[note公式](https://note.com/info/n/n1403dd6c1cd9)）、AI実務系の高単価メンバーシップが急増

つまり本記事は、**「2026年4月末時点の道具立ての変化を一気にまとめた業界マッピング」** として読むのが正確。3ヶ月後には半分が上書きされている可能性が高い、揮発性の強いコンテンツ。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| メインAIはClaudeCodeかCodexで足りる | 2026年5月時点でAIコーディング市場の事実上の二強。Cursor/Cline/Aider等は派生または上位レイヤー | [AI総研 2026年版まとめ](https://www.ai-souken.com/article/claude-code-updates-2026) | ✅ 一致 |
| HiggsField MCPでClaude Codeから動画量産可能 | **2026-04-30公開**。Veo 3.1/Sora 2/Kling 3.0/Hailuo 02等30+モデルにアクセス、最大15秒・4K | [Higgsfield公式](https://higgsfield.ai/mcp), [MCP.Directory](https://mcp.directory/blog/higgsfield-mcp-guide) | ✅ 一致（記事公開タイミングとほぼ同日） |
| ai-website-cloner-template でデザインを"パクれる" | URL渡すだけでNext.js 16 + React 19 + shadcn/ui で再構築。**GitHub 12.6k★ / 1.8k fork** | [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | ✅ 一致（実在・人気も本物） |
| Whisperのタイムスタンプ精度が微妙 | small/medium モデルで実用域だが、SRT精度は0.01秒単位の手動調整前提との実装報告が多数。WhisperXで単語単位精度に改善する手段あり | [Qiita WhisperX解説](https://qiita.com/yskazuma/items/4cea16510d95d473c216), [Zenn faster-whisper SRT](https://zenn.dev/mossan_hoshi/articles/20241011_faster_whisper_srt) | ⚠️ ほぼ一致（"微妙"は事実だが対策ツールは既に存在＝Whisper単体の問題） |
| 問い合わせフォーム営業は実質OK | 特定電子メール法 **第3条4項の例外**で、公開された連絡先への営業は原則合法。ただし「営業お断り」の明記がある場合は違反 | [迷惑メール相談センター](https://www.dekyo.or.jp/soudan/contents/taisaku/1-2.html), [SakuSaku Magazine](https://dream-up.co.jp/sakusaku/media/toiawaseformeigyou-ihou/) | ⚠️ ほぼ一致（条件付きで合法、無条件OKではない） |
| 10〜20回やって1つ当たるかどうか | 「シリコンバレーで起業したベンチャーの **0.3%しか生き残らない**」という統計はある。一方"10回に1回"の具体的根拠は出典不明 | [Sun* リーンスタートアップ解説](https://sun-asterisk.com/service/development/topics/mvp/1556/) | 🔍 経験則として妥当だが厳密な統計根拠なし |
| 月額4980円メンバーシップは費用対効果が良い | note相場では500〜1,500円が中心。**3,000円超は"割高"扱い**で、Zoom/Discordコンサル等の手厚い特典が前提 | [note編集部 3000件分析](https://note.com/notemag/n/n65bfc3cf1d88) | ⚠️ 文脈次第（コンサル相当の付帯価値が必要） |
| 受注決まってから商材作ればOK | "プレセール"はリーン手法で有効だが、**特商法上「役務提供できないものを売る」と虚偽表示リスク**。受注確定時に提供可能な状態を作る筆者の補足は重要 | リーンスタートアップ手法（一般論） | ⚠️ ほぼ一致（筆者も同条件を明記） |
| LPは競合をぬるっとパクって自社カラーに | デザインの**著作権侵害・不正競争防止法（商品形態模倣）リスク**あり。GUIの個別表現は判例上保護対象になりうる | （本調査では未深掘り） | ❌ 要注意（"ぬるっと"の表現が法的にグレー〜ブラック） |

---

## 🌐 最新動向（2026-05-02時点）

- **Claude Code v2.1.101** がリリースされ、5週間で30以上の機能追加。`/loop` `Voice mode` `Auto mode` が事業オペレーション層で常用される段階に — [Uravation 2026年4月速報](https://uravation.com/media/claude-code-v2-1-101-30-releases-5-weeks-guide-2026/), 2026-04
- **Higgsfield MCP** が公開、Claude Code経由で `1枚の商品画像 → 50本のInstagram広告` が現実化 — [Phemex News](https://phemex.com/news/article/higgsfield-ai-unveils-mcp-server-for-visual-content-creation-with-claude-77601), 2026-04-30
- **Claude Design** が `claude.ai/design` で公開、スライド/LP/プロトを一気通貫生成。Figma株が発表当日 -7.28% — [Impress Watch](https://www.watch.impress.co.jp/docs/news/2102748.html), 2026-04-17
- **Opus 4.7** 搭載 + 1Mコンテキスト（Opus 4.6時点で一般提供）で、設計資料・既存コード・ナレッジを丸投げできる「規模の壁」が崩壊 — [Saiteki AI](https://saiteki-ai.com/basics/ai-tool/claude-code/claude-code-version/), 2026-04
- **note メンバーシップ上限が月額50,000円に**引き上げ。AI×実務系の高単価サブスクが増加傾向 — [note公式](https://note.com/info/n/n1403dd6c1cd9), 2026年内アップデート

---

## 🧩 関連概念・隣接分野

- **リーンスタートアップ / Build-Measure-Learn ループ**: 本記事の①〜③（リサーチ→MVP→LP）は、Eric Ries の枠組みそのもの。"受注前に作らない"はピボット前提のMVPと同じ思想 — [Sun*解説](https://sun-asterisk.com/service/development/topics/mvp/1556/)
- **AIエージェント協調（Agent Teams / Sub-Agents）**: Claude Code v2 で実装された複数エージェント並列開発。記事の「全工程をAI化」が**Sub-Agent前提だと現実的**になる
- **Vibes Coding / Spec-Driven Development**: 仕様書ベースでAIに丸投げする開発スタイル。1Mコンテキスト + Skills で台頭中
- **特定電子メール法 第3条4項の例外**: 公開連絡先への営業送信を許容する条文。フォーム営業を語る上の必須知識 — [迷惑メール相談センター](https://www.dekyo.or.jp/soudan/contents/taisaku/1-2.html)
- **動画コンテンツの3プラットフォーム展開（YouTube Shorts / TikTok / IG Reels）**: 1本の縦動画素材で3面を取りに行くのは2024年以降の鉄板。Higgsfield MCPで生成自体のコストが消える

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（筆者寄り）**: ツール代がほぼゼロで、1人で全工程回せる。失敗しても残るのは X アカウントとClaudeCodeの操作経験＝資産。10〜20回打席に立てれば確率的に当たる
- **否定 / 慎重派の主張**:
  - **「ぬるっとパクる」は2026年でも訴訟リスク**。デザイン著作権・不正競争防止法・パブリシティ権の観点で、AIで再現したから合法とはならない。実際に米国で著作権訴訟が増えているフェーズ
  - **問い合わせフォーム営業は"法的にOK"であっても"レピュテーションは死ぬ"**。BtoB業界SNSで晒される事例が多発しており、AI駆動で送信効率を上げると被害規模も比例して大きくなる
  - **MVPを受注後に作る→提供失敗リスク**。"作れます"と売って実際に作れず返金・炎上のパターンは個人事業者で頻発。筆者も「受注時に提供できる状態を作る」と但し書きしているが、ここを軽く扱う読者が事故る
  - **note メンバーシップ4,980円**は、コンテンツ単体価値ではなく**「筆者本人へのアクセス権」が本体**。スケール（加入者増）すると個別サポートが破綻し、価値が崩壊する典型構造
  - **"10回に1回当たる"の出典不明**。シリコンバレーの統計は0.3%（300回に1回）。個人副業MVPの当選率はフレームワーク化された数字としては存在せず、励まし用の"気合の数字"の可能性
- **中立的に見るときの補助線**: この記事は **「打席数を確保するための道具立てカタログ」** として読めば100点。一方 **「具体的な事業を立ち上げる手順書」** として読むと、法務・倫理・実装の地雷が抜けている。読者が今どっちの目的で参照しているかで価値が変わる

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] AI生成LPの著作権・不正競争防止法判例（2026年時点で日本国内訴訟は出たか？）
- [ ] Claude Code Sub-Agents で「市場リサーチ→MVP仕様→LP生成→広告クリエイティブ生成」を自動連鎖させた具体的事例
- [ ] Higgsfield MCP + Claude Code での動画量産パイプラインの実コスト（API利用料、1本あたりの生成時間）
- [ ] SkillGraphs の運用効果は本人申告（2時間→15分）以外に検証データがあるか
- [ ] noteメンバーシップ4,980円帯で**1年以上**継続できているクリエイターの解約率と続伸理由
- [ ] 「10〜20回やって1つ当たる」の元データ。個人副業のMVP打席統計は実在するのか
- [ ] 問い合わせフォーム営業の「実質OK」と「業界的レピュテーション」のギャップを定量化した調査

---

## 📚 参考資料

- [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) — テンプレ実体・スター数・対応エージェント確認, 取得日 2026-05-02
- [Higgsfield MCP公式](https://higgsfield.ai/mcp) — MCP仕様・対応モデル一覧, 取得日 2026-05-02
- [Phemex: Higgsfield MCP発表記事](https://phemex.com/news/article/higgsfield-ai-unveils-mcp-server-for-visual-content-creation-with-claude-77601) — 2026-04-30公開日特定, 取得日 2026-05-02
- [Uravation: Claude Code v2.1.101完全ガイド](https://uravation.com/media/claude-code-v2-1-101-30-releases-5-weeks-guide-2026/) — 5週間30機能のCHANGELOG, 取得日 2026-05-02
- [AI総合研究所: Claude Code 2026年最新まとめ](https://www.ai-souken.com/article/claude-code-updates-2026) — Skills/Plugins/Agent Teams動向, 取得日 2026-05-02
- [Impress Watch: Claude Design](https://www.watch.impress.co.jp/docs/news/2102748.html) — 2026-04-17公開、Figma株反応, 取得日 2026-05-02
- [迷惑メール相談センター: 特定電子メール法](https://www.dekyo.or.jp/soudan/contents/taisaku/1-2.html) — 第3条4項の例外条件, 取得日 2026-05-02
- [SakuSaku Magazine: フォーム営業の違法性](https://dream-up.co.jp/sakusaku/media/toiawaseformeigyou-ihou/) — 例外適用条件の実務解説, 取得日 2026-05-02
- [Sun*: リーンスタートアップとMVP](https://sun-asterisk.com/service/development/topics/mvp/1556/) — シリコンバレー0.3%統計の出典確認, 取得日 2026-05-02
- [note編集部: 3000件メンバーシップ分析](https://note.com/notemag/n/n65bfc3cf1d88) — 価格相場・プラン構成, 取得日 2026-05-02
- [note公式: メンバーシップ上限5万円改定](https://note.com/info/n/n1403dd6c1cd9) — 価格上限と特典枠拡張, 取得日 2026-05-02
- [Qiita: WhisperXで字幕タイムスタンプ](https://qiita.com/yskazuma/items/4cea16510d95d473c216) — 単語単位精度の改善手段, 取得日 2026-05-02
- [Zenn: faster-whisperでSRT生成](https://zenn.dev/mossan_hoshi/articles/20241011_faster_whisper_srt) — 字幕実装の現実解, 取得日 2026-05-02
- [元記事原典: @L_go_mrk on X](https://x.com/L_go_mrk/status/2049814773982974118) — 一次情報, 公開 2026-04-30

---

## 🗒 メモ

この記事、**自分のnote記事ネタとして転用するなら以下の切り口が刺さる**：

1. **"2026-04 の30日間で揃った道具立て一覧"記事**: Claude Design / Higgsfield MCP / Opus 4.7 / 1Mコンテキスト / Sora 2 を時系列で並べて「個人がスケールできる閾値が4月末に超えた」と書く。米軍Anthropic切り記事と並ぶ規模感
2. **批評型リプの素材**: 「ぬるっとパクる」「フォーム営業」のような表現に対して、共感ベースの「これわかるなぁ。〜だけど、〜の罠もあると思ってて」テンプレで批評型リプの素材として使える。今日13:00枠の昼リプ候補に直結
3. **W19戦略メモの観点として**: AI駆動塾系コンテンツの**揮発性の高さ**は逆にこちら側にも刺さる。"3ヶ月で半分が上書きされる"領域は、毎日撃ち続ける我々の発信フォーマットと相性◎
4. **Day Oneプロモとの絡み**: 「Day One = 1日1個の意思決定の記録」は、**この記事の"打席10〜20回"思想と完全一致**。Day Oneプロモ最終投稿（5/3 22:00）でこの記事を引用すると説得力が一段上がる

注意点メモ:
- 「ぬるっとパクる」表現を**そのまま自分の発信で使うと事故る**。引用する場合は明確に距離を置いた表現に置換
- 4,980円メンバーシップへの感想は**個別の運営者批判ではなく、構造の指摘**として書く（ポジショントーク回避）
