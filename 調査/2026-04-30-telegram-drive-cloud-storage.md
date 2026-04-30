---
created: 2026-04-30
tags: [調査, telegram, cloud-storage, oss, tauri]
source: "[[Clippings/Post by @L_go_mrk on X 6.md]]"
---

# Telegram-Drive：Telegramを「実質無制限のクラウドドライブ」化するOSSアプリの実態

> **TL;DR**
> `caamer20/Telegram-Drive` は Tauri+Rust+React 製の OSS デスクトップアプリで、自分の Telegram アカウントの「Saved Messages / Channel」をローカル風ファイルエクスプローラから操作できるようにしたもの。**「無制限」は本当だがファイル単位では 2GB（無料）/ 4GB（Premium）の上限**があり、Pavel Durov 逮捕後の 2024-09 以降は **TOS 違反者の電話番号・IP を当局に提供する運用**へ切り替わっているため、「ローカル圧迫を避ける作業ファイル置き場」としては便利でも、**機密データやアーカイブ専用ストレージとしての全幅信頼は危険**。同種プロジェクト（teldrive, Pentaract, drivegram など）が 2023〜2026 にかけて複数登場している成熟ジャンルでもある。

## 📌 元テキスト（抜粋）

> これやばいのでは？？？？？
> telegram-drive：自分の Telegram アカウントを「容量無制限のクラウドドライブ」として使えるデスクトップアプリ。動画素材や音声書き起こしの大量ファイルを、ローカルを圧迫せず置けるようになる。
> repo：https://github.com/caamer20/Telegram-Drive…

出典: [[Clippings/Post by @L_go_mrk on X 6.md]]（[原ポスト](https://x.com/L_go_mrk/status/2049408596476064235), 2026-04-29）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| Telegram-Drive | 本ポストで紹介された OSS デスクトップアプリ。Saved Messages を仮想ドライブ化 | `caamer20 Telegram-Drive Tauri` |
| Saved Messages | Telegram の自分専用チャット。実質無料の個人クラウドメモ | `Telegram saved messages cloud` |
| Tauri | Rust 製の軽量デスクトップアプリ枠組み（Electron 代替） | `Tauri v2 Rust desktop` |
| MTProto | Telegram の独自プロトコル。クライアント API で大容量転送に使う | `MTProto API file upload` |
| 4GB upload | Telegram Premium 加入で 1 ファイル上限が 2GB→4GB に拡張 | `Telegram Premium 4GB limit` |
| Fair-use throttling | Telegram の事実上のレート制限。大量同期は減速 | `Telegram rate limit upload abuse` |
| Teldrive | divyam234 製の Go ベース類似プロジェクト。rclone 連携あり | `tgdrive teldrive rclone` |
| Pentaract | Rust 製 Telegram バックエンドのファイルストレージ | `Dominux Pentaract` |

---

## 🧭 背景 / なぜ今これが話題なのか

Telegram のクラウドは「**送信したメッセージとファイルがすべてサーバ側に永続保存される**」という設計を 2013 年のローンチ当初から持っており、無料でも実質的に容量無制限という珍しい立て付けだった。一方、ファイルサイズ上限は 2020-07 に 1.5GB→2GB に拡張、2022 年の Telegram Premium 開始で **Premium 限定 4GB アップロード**が追加された（[ghacks 2020](https://www.ghacks.net/2020/07/27/telegram-increases-file-size-limit-to-2gb-adds-support-for-multiple-accounts-on-desktop-profile-videos-on-mobile/) / [Telegram Premium FAQ](https://telegram.org/faq_premium)）。

この「無制限ストレージ＋大ファイル上限」の組み合わせを Google Drive 代替として使い倒そうという発想は前からあり、`rclone` のフォーラムでも 2021 年頃から議論されている（[rclone forum 2021](https://forum.rclone.org/t/telegram-unlimited-cloud-storage-and-rclone/27490)）。実装としては **2022〜2024 年にかけて divyam234/teldrive・AstraNode/Telegram-Drive・mxvsh/drivegram・Dominux/Pentaract・ebinxavier/telegramCloudStorage など同種 OSS が乱立**しており、`caamer20/Telegram-Drive` はその系譜の最新作。

ホットな理由は単純で、**Tauri 製で macOS / Windows / Linux のネイティブバイナリ＋自動アップデートまで揃えた「ふつうの人がそのまま使える完成度」のものは少なかった**から。リポジトリは MIT、最新リリース v1.1.6 が 2026-04-29 とポスト前日付け（[GitHub Releases](https://github.com/caamer20/Telegram-Drive/releases)）。X で「やばいのでは？？？」と話題化したのはこのリリース直後のタイミングだった。

ただし時期的にもう一つ重要なのは、**2024-08 の Pavel Durov 逮捕→ 2024-09 のプライバシーポリシー大改訂**。「テロ容疑のみ」だった当局協力が「TOS 違反全般」へ拡大し、2024 年だけで米国当局へ電話番号・IP が **900 件・2253 ユーザー分提供**された（[TechCrunch 2025-01](https://techcrunch.com/2025/01/07/telegram-reports-spike-in-sharing-user-data-with-law-enforcement/)）。Durov の渡航禁止は 2025-11 に解除された（[Wikipedia](https://en.wikipedia.org/wiki/Arrest_and_indictment_of_Pavel_Durov)）が、ポリシー側は元に戻っていない。「**便利になった**」と「**プライバシー前提が変わった**」が同時に進行している、という二重文脈で読む必要がある。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「容量無制限のクラウドドライブとして使える」 | 総容量はほぼ無制限で公式 FAQ も明言。ただし**ファイル単位は 2GB / Premium 4GB の上限あり**。さらに「fair-use」スロットルがあり大量初期同期は実測で週末単位 | [Telegram Premium FAQ](https://telegram.org/faq_premium) / [Aiia 2026](https://aiia.ro/blog/telegram-drive-unlimited-cloud-storage/) | ⚠️ ほぼ一致（無制限は本当だが「単一巨大ファイル」は分割必須） |
| 「Telegram アカウントを使うデスクトップアプリ」 | 公式 README で Tauri+Rust+React 製、macOS/Windows/Linux ネイティブ、MIT、v1.1.6 (2026-04-29 リリース) を確認 | [GitHub caamer20/Telegram-Drive](https://github.com/caamer20/Telegram-Drive) | ✅ 一致 |
| 「動画素材や音声書き起こしを置けば、ローカルを圧迫せず置けるようになる」 | 4GB 以下の動画クリップ・音声ファイルなら問題なく置ける。媒体ストリーム再生（DLせず再生）にも対応 | [GitHub README](https://github.com/caamer20/Telegram-Drive) | ✅ 一致 |
| 「リポジトリ：github.com/caamer20/Telegram-Drive」 | 実在確認。950★、17リリース、MIT | [GitHub caamer20/Telegram-Drive](https://github.com/caamer20/Telegram-Drive) | ✅ 一致 |
| (暗黙) 「Telegram は安全な保管先」 | **2024-09 以降、TOS 違反者の電話番号と IP が当局へ提供される運用に変更**。「テロ容疑のみ」から「ルール違反全般」へ大幅拡大 | [The Record 2024-09](https://therecord.media/telegram-shares-ip-addresses-enforcement) / [TechCrunch 2025-01](https://techcrunch.com/2025/01/07/telegram-reports-spike-in-sharing-user-data-with-law-enforcement/) | ❌ 要注意（前提が崩れている） |
| (暗黙) 「Telegram のクラウドは E2E 暗号化されている」 | **Saved Messages を含む通常チャットは E2E ではなく Server-Client 暗号化**。E2E は Secret Chat のみ | [Telegram Privacy Policy](https://telegram.org/privacy) | ❌ 要注意（誤解されがち） |

---

## 🌐 最新動向（2026-04-30 時点）

- `caamer20/Telegram-Drive` v1.1.6 が 2026-04-29 リリース、署名済みバイナリで mac (Intel/ARM)・Win・Linux 対応 — [GitHub Releases](https://github.com/caamer20/Telegram-Drive/releases), 2026-04
- 同種プロジェクトの中では **divyam234/teldrive** が Go 実装 + Material You UI + rclone 連携 + Docker デプロイで最も成熟しており、サーバ側ホスト型として根強い人気 — [tgdrive/teldrive](https://github.com/tgdrive/teldrive), 2026-04
- Telegram 側は 2024-09 のポリシー改訂以降も **TOS 違反者の IP・電話番号当局提供を継続**、2024 年通年で米国 900 件・2253 ユーザー分の開示 — [TechCrunch](https://techcrunch.com/2025/01/07/telegram-reports-spike-in-sharing-user-data-with-law-enforcement/), 2025-01
- Pavel Durov の **渡航禁止が 2025-11 に解除**、刑事手続きは継続中 — [Wikipedia](https://en.wikipedia.org/wiki/Arrest_and_indictment_of_Pavel_Durov), 2025-11
- 「サイバー犯罪者が Telegram から離れて Private Cloud に移った」と分析されるレベルで、過剰な hoarding はモニタリング対象になり始めている — [White Blue Ocean 2026](https://www.whiteblueocean.com/newsroom/the-great-cybercriminal-migration-why-stolen-data-went-private-in-2025-and-what-to-expect-in-2026/), 2026-Q1

---

## 🧩 関連概念・隣接分野

- **MTProto API**: Telegram 公式のクライアントプロトコル。Bot API（20MB 制限）ではなくこちらを叩くから 2/4GB アップロードと無制限ストレージが実現できる。Telegram-Drive 系がすべてこの上に乗る根拠。
- **Tauri v2**: Electron に対する Rust 軽量代替。`caamer20/Telegram-Drive` がローカルバイナリでサクサク動く理由。Obsidian プラグインや mac 向け OSS で 2025-2026 にかけて採用が増えた。
- **rclone + teldrive**: コマンドラインで Telegram を S3 / Google Drive と同列に扱いたいなら GUI 型ではなく rclone 経由の方が自動化に強い。バックアップ用途ならこちら。
- **Telegram Premium の経済性**: 月 ~$5 で 4GB 上限・広告非表示・ダウンロード優先が付く。容量目当てで Google One/iCloud ($10〜) と比較するなら、4GB 上限は明確な差分なので「動画素材ストレージ」として比較する意味はある。
- **Self-hosted 代替**: Nextcloud / Seafile / MinIO + Garage など、自前 NAS を Tauri クライアントから叩くやり方も 2026 時点では選択肢。プライバシー観点ではこちらが上。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  「ローカル SSD を圧迫せずに動画素材や書き起こしを退避できるなら最高。Premium $5/月で 4GB 上限になるなら Google One よりコスパが良い。OSS で MIT、ネイティブバイナリだから何も失うものがない」
- **否定 / 慎重派の主張**:
  - **TOS リスク**: Telegram 公式 TOS は「メッセージング」を主目的とした設計で、「自分専用クラウドストレージ的乱用」は明確には禁止していないが、過剰な hoarding は fair-use 違反扱いされ得る（[Aiia](https://aiia.ro/blog/telegram-drive-unlimited-cloud-storage/) も同様の警告）。BAN されると**ファイル全消失**で復旧手段なし。
  - **プライバシー誤解**: Saved Messages は E2E ではない。**サーバ側にプレーンに置かれている前提**で考える必要があり、機密データを置くなら必ずクライアント側暗号化を噛ませる（teldrive 等は対応、caamer20 版は README に "robust encryption" の言及がない＝要注意）。
  - **法執行リスク**: 2024-09 以降の方針で、「TOS 違反通報」起点で電話番号と IP が出る。違法でなくても**規約違反通報されたら身バレ起点になり得る**。
  - **単一プロバイダ依存**: Telegram は商用クラウドストレージとして SLA を提供していない。Drive/iCloud と同じ感覚で使うと「ある朝アクセス不能」のリスクが残る。
- **中立的に見るときの補助線**:
  - 「**作業中の中間ファイル置き場**」と「**唯一のバックアップ**」を分けて考える。前者なら Telegram-Drive は便利。後者には絶対しない。
  - 機密性の高いものは **rclone crypt** や **Cryptomator** で先に暗号化してから上げる。
  - 容量・速度・撤退戦の3点を測る：「200GB 上げきれるか」「DL速度は実用域か」「明日 Telegram が落ちても困らないか」。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] `caamer20/Telegram-Drive` v1.1.6 はクライアント側暗号化に対応しているか（README には明示なし、コード読みが必要）
- [ ] teldrive と caamer20 版の**速度・安定性ベンチマーク**比較（GUI 型 vs server 型）
- [ ] Telegram fair-use throttle の実数値（何 GB/h 以上で減速し始めるか）
- [ ] Premium 4GB 上限を回避する分割アップロード機能の実装状況（caamer20 版にあるか？）
- [ ] 動画素材ワークフローで使うなら **Cryptomator + Telegram-Drive** の二段構えが現実解か検証
- [ ] 自分の運用ケース（SNS用素材＋音声書き起こし）で **iCloud 200GB（既契約）+ Telegram-Drive 補助**が、純粋に iCloud 1TB に切り替えるよりコスト効率が良いか試算

---

## 📚 参考資料

- [GitHub caamer20/Telegram-Drive](https://github.com/caamer20/Telegram-Drive) — README・最新リリース v1.1.6 (2026-04-29)・MIT ライセンス確認, 取得日 2026-04-30
- [GitHub Releases - Telegram-Drive](https://github.com/caamer20/Telegram-Drive/releases) — リリース履歴・対応プラットフォーム確認, 取得日 2026-04-30
- [Telegram Premium FAQ](https://telegram.org/faq_premium) — 無制限ストレージ・4GB 上限の公式記述, 取得日 2026-04-30
- [Telegram Privacy Policy](https://telegram.org/privacy) — Saved Messages の暗号化仕様確認, 取得日 2026-04-30
- [TechCrunch: Telegram reports spike in sharing user data with law enforcement (2025-01)](https://techcrunch.com/2025/01/07/telegram-reports-spike-in-sharing-user-data-with-law-enforcement/) — 2024 年通年 900 件・2253 ユーザー分の開示数値, 取得日 2026-04-30
- [The Record: Telegram shares IP addresses](https://therecord.media/telegram-shares-ip-addresses-enforcement) — 2024-09 ポリシー転換の Durov 公式声明, 取得日 2026-04-30
- [Aiia Blog: Telegram Drive Unlimited Free Cloud Storage](https://aiia.ro/blog/telegram-drive-unlimited-cloud-storage/) — fair-use throttle の実例言及, 取得日 2026-04-30
- [GitHub tgdrive/teldrive](https://github.com/tgdrive/teldrive) — 競合 OSS の機能比較, 取得日 2026-04-30
- [rclone forum: Telegram unlimited cloud storage and rclone](https://forum.rclone.org/t/telegram-unlimited-cloud-storage-and-rclone/27490) — 2021 年からの議論経緯, 取得日 2026-04-30
- [Wikipedia: Arrest and indictment of Pavel Durov](https://en.wikipedia.org/wiki/Arrest_and_indictment_of_Pavel_Durov) — 渡航禁止解除（2025-11）の確認, 取得日 2026-04-30
- [ghacks: Telegram increases file size limit to 2GB (2020-07)](https://www.ghacks.net/2020/07/27/telegram-increases-file-size-limit-to-2gb-adds-support-for-multiple-accounts-on-desktop-profile-videos-on-mobile/) — 上限変更の歴史, 取得日 2026-04-30

---

## 🗒 メモ

- 投稿者の「やばいのでは？？？？？」は素直に共感できる便利さだが、**「無制限」の3文字に惹かれて飛びつく前に "ファイル単位 4GB" と "Saved Messages は平文" の2点だけ押さえれば事故らない**、というのが調査後の結論。
- 自分の運用に直結する観点は2つ：
  1. **SNS素材ワークフロー**用の中間置き場としてはアリ（撮影素材→書き出し→投稿）。原本は外付け SSD + Google Drive バックアップに置いたまま、作業コピーだけ Telegram-Drive、という二段構えがちょうど良い。
  2. **音声書き起こしファイル**を置くなら、文字起こし対象に名前や個人情報が入っていないかだけ確認すれば実用的。
- 派生ネタ候補：
  - 「Tauri 製 OSS が 2026 に増えている件」をまとめると note 1本書ける（Telegram-Drive, Hermes 系, etc）
  - 「Telegram を商用クラウド代替にするときの落とし穴 5選」は X スレッドにしやすい
  - my-clone 人格でやるなら「無制限という言葉に弱い人へ」みたいな切り口で 1 ポストいけそう
