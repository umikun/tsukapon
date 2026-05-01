---
created: 2026-05-01
tags: [調査, Vaultwarden, Bitwarden, Password Manager, Self-Hosted, Rust, Open Source]
source: "[[Clippings/Post by @ihtesham2005 on X.md]]"
---

# Vaultwarden — 5ドルVPSで動く"無料Bitwardenサーバー"の実像と落とし穴

> **🔗 関連コンテンツ**
> - 📰 元クリップ: [[Clippings/Post by @ihtesham2005 on X.md]]
> - 🛠 開発系メモ: [[_ memory/short-term.md]]
> - 📋 調査ノート姉妹: [[調査/2026-05-01-claude-design-mcp-anti-ai-slop.md]]

> **TL;DR**
> Vaultwarden は Bitwarden のオープンAPI互換サーバーを **Rust で再実装** したサードパーティ製OSS（dani-garcia 氏作）。59.5K stars / 最新 v1.35.8（2026-04-25）。**月3〜5ドルのVPSに1コマンドDocker** で個人〜家族のパスワード基盤になる。ただし元ツイートが伏せている事実が3つある: ① **Bitwarden 自身も無料プランで個人パスワード無制限同期できる**（Vaultwarden が "0ドル vs 月3ドル" と煽るのは比較対象がズレている）、② **2025年と2026年に重大CVE**（RCE / 認証バイパス）が立て続けに発見されており、**運用ミス＝自分の全パスワード漏洩** に直結する責任の重さがある、③ Bitwarden 自身も 2024年10〜11月に **SDKライセンス騒動**（GPL→独自）で炎上後 GPL3に戻した経緯があり、"オープンソース vs 商用" の構図は単純ではない。**技術力に自信があるなら最強。ない人は素直に Bitwarden 無料プラン or 月$1.65 Premium**、が誠実な結論。

## 📌 元テキスト（抜粋）

> 1Passwordはユーザーあたり月額3ドルを請求します。Dashlaneは月額4.99ドルを請求します。LastPassは月額3ドルを請求します。
>
> 誰かがBitwardenサーバー全体をRustで書き直し、0ドルでオープンソース化しました。それはすべてのデバイス上のすべての公式Bitwardenアプリと動作します。
>
> それはVaultwardenと呼ばれます。
>
> Vaultwardenは全く同じAPIを実装します。…… 5ドルのVPS上で起動します。BitwardenアプリをサーバーURLにポイントします。すべてのパスワード、すべてのセキュアノート、すべての2FAコードが、あなたが所有するインフラストラクチャを通じてすべてのデバイス間で同期します。
>
> → 完全なAES-256エンドツーエンド暗号化。有料製品と同じ。
> → すべてのプレミアム機能がアンロック。…… 無料。
> → 256MB RAMで動作。…… 1つのDockerコマンド。…… ゼロサブスクリプション。ゼロシート料金。ゼロ信頼必要。
>
> 59K stars. 100% Opensource

出典: [[Clippings/Post by @ihtesham2005 on X.md]] / 元URL: <https://x.com/ihtesham2005/status/2049942008471736403>

> ⚠️ 翻訳ゆらぎ:「ゼロ信頼必要」は原文 "Zero trust required" の直訳で、ここでは "サードパーティを信用する必要がない" という意味。セキュリティ用語の "Zero Trust Architecture"（ZTA）とは別物。

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| **Vaultwarden** | Bitwarden互換のサードパーティ製サーバー（Rust製・OSS） | `dani-garcia/vaultwarden` GitHub |
| **Bitwarden** | 公式パスワードマネージャー本体（クライアント＋公式サーバー）。会社名でもある | bitwarden.com |
| **bitwarden_rs** | Vaultwarden の旧称（2022年に商標配慮で改名） | "bitwarden-rs rename" |
| **Bitwarden API** | クライアントアプリが使うHTTP API。Bitwarden本体がオープンソースなので仕様が公開されている | OpenAPI / Bitwarden API spec |
| **Self-hosted** | 自分でサーバーを運用する形態。VPS / Raspberry Pi / 自宅NASなど | self-hosting / homelab |
| **AES-256 / E2E暗号化** | Bitwarden系で共通の vault 暗号化方式。サーバー側は暗号文のみ保持 | end-to-end encryption |
| **CVE-2025-24364 / -24365** | 2025年にBI.ZONEが報告したVaultwardenのRCE + 権限昇格脆弱性 | Vaultwarden CVE 2025 |
| **CVE-2026-26012** | 2026年公開の認証バイパス。組織メンバーが他コレクションのcipher閲覧可（v1.35.3未満） | Vaultwarden CVE 2026 |
| **Bitwarden SDK 騒動** | 2024年10月〜11月、`sdk-internal` が独自ライセンスでビルド不能化 → 11月にGPL3へ巻き戻し | Bitwarden GPL SDK |
| **CrowdSec / Fail2ban** | Vaultwardenのブルートフォース対策に必須の侵入検知ツール | reverse proxy + IDS |
| **Tailscale / WireGuard** | 公開せずVPN経由のみで使う安全運用パターンに使うVPN | Tailscale Vaultwarden |

---

## 🧭 背景 / なぜ今これが話題なのか

### Vaultwarden の出自

Vaultwarden は dani-garcia 氏が **2018年頃** に `bitwarden_rs` として開発を開始したサードパーティ製サーバー。Bitwarden公式サーバーは .NET / MS SQL Server で重く、家庭用Raspberry Piや小型VPSには重すぎた。これを**Rust + SQLite/MySQL/PostgreSQL** で軽量に再実装し、メモリ50MB前後で動かせるようにしたのが原型。

**2022年**、Bitwarden社からの商標配慮要請を受けて `bitwarden_rs` → `vaultwarden` に改名。以降も Bitwarden 公式クライアント（iOS/Android/Chrome拡張/デスクトップ）と100%互換のサーバーを提供し続けている。

### なぜ "今" Xでバズるか

1. **2026年Q1のBitwarden値上げ**: Bitwarden Premium が10年ぶりに $10/年 → **$19.80/年** に値上げ（2026年1月）。1Password / Dashlane も値上げ → "サブスク疲れ" の風潮の中で「自前ホストで0円」が刺さるタイミング
2. **Dashlane 無料プラン廃止**（2025年9月）→ "無料の選択肢" を探すユーザー流入
3. **2024年10月のBitwarden SDK 騒動** で「公式Bitwardenも完全にFOSSなのか？」の不信感が燻ぶり、代替を探す層が形成された
4. **r/selfhosted / Hacker News / X の "1分で解説" ジャンル** がバズ構造になっており、Vaultwardenは典型的な"映える"題材（数字 + 0円 + 1コマンド + Rust）

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| 「1Password $3/月、Dashlane $4.99/月、LastPass $3/月」 | **要注意**: 1Password Individual は $2.99/月（年払）/ $3.99/月（月払）。Dashlane Premium は $4.99/月で一致。LastPass Personal は $7/月（公開情報）が現行値で、$3 は古い情報の可能性 | [Bitwarden Pricing 2026](https://comparetiers.com/tools/bitwarden) / [Best Password Managers 2026](https://costbench.com/best/best-password-managers-2026/) | ⚠️ ほぼ一致（LastPass価格は要再確認） |
| 「Bitwardenサーバー全体をRustで書き直し」 | 正確には **互換実装（クリーンルーム）**。公式Bitwardenソースコードを書き写したのではなく、公開APIに合わせてゼロから実装 | [GitHub dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) | ⚠️ ほぼ一致（"書き直し" より "互換実装" が正確） |
| 「すべての公式Bitwardenアプリと動作」 | iOS / Android / Chrome 拡張 / デスクトップ / Web Vault すべてサーバーURLを向ければ動く。READMEで明記 | [Vaultwarden README](https://github.com/dani-garcia/vaultwarden) | ✅ 一致 |
| 「5ドルのVPSで動く」「256MB RAMで動作」 | アイドル時は約 **50MB RAM**（README記載）。256MBは推奨環境としては妥当 | [Vaultwarden README / OSSAlt 解説](https://ossalt.com/guides/vaultwarden-self-host-bitwarden-2026) | ✅ 一致（より少なくても動く） |
| 「全プレミアム機能がアンロック（ファイル添付・vaultヘルス・ハードウェア2FA）無料」 | Vaultwardenは公式のPremium機能制限を実装しないため事実上アンロック状態。ただし**機能自体はBitwardenが開発したもの**であり、Vaultwarden が独自開発したわけではない | [Self-host Vaultwarden 2026](https://corelab.tech/digital-vault-self-hosting-vaultwarden/) | ✅ 一致（功績は公式Bitwarden側） |
| 「マルチユーザー・組織機能 組み込み」 | organizations / collections / user management / emergency access / sends / TOTP すべて実装済み | [Vaultwarden 機能一覧](https://github.com/dani-garcia/vaultwarden) | ✅ 一致 |
| 「1つのDockerコマンドで10分以内」 | 正式手順では reverse proxy (Caddy/Nginx/Traefik) と HTTPS 設定が必須。**素のDocker一発はWeb Vaultがブラウザ仕様で動かない**（Web Crypto API がHTTPS必須） | [Vaultwarden README "HTTPS Requirement"](https://github.com/dani-garcia/vaultwarden) | ❌ 要注意（"1コマンド" は誇張） |
| 「ゼロ信頼必要」 | "サードパーティを信用しなくて良い" の意味では正しい。ただし**自分のサーバー運用スキル・OS・SSL・VPS事業者を信用する必要が増える**。トラストの所在が移るだけ | [XDA: Self-hosting risks](https://www.xda-developers.com/self-hosted-password-manager-risks-limitations-locked-out/) | ⚠️ ほぼ一致（信頼の移転として再解釈が必要） |
| 「59K stars 100% Opensource」 | 2026-05-01 時点で **59,500 stars**（README確認）。ライセンスは AGPLv3 で完全FOSS | [GitHub dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) | ✅ 一致 |
| 暗黙の主張: 「Vaultwarden = Bitwardenより常に安全」 | **2025年: CVE-2025-24364（RCE）/ -24365（権限昇格）/ 2026年: CVE-2026-26012（認証バイパス、v1.35.3未満）** が報告。運用怠るとむしろ危険 | [SentinelOne CVE-2026-26012](https://www.sentinelone.com/vulnerability-database/cve-2026-26012/) / [BI.ZONE 報告](https://bi.zone/eng/news/my-obnaruzhili-uyazvimosti-vysokogo-urovnya-opasnosti-v-vaultwarden/) | ❌ 要注意（重要な未言及事実） |

---

## 🌐 最新動向（2026-05-01時点）

- **Vaultwarden v1.35.8 リリース**（2026-04-25）。直前の v1.35.3 で CVE-2026-26012 認証バイパスを修正済み。v1.35.x 系列は**必ずアップデート必須** — [Vaultwarden Releases](https://github.com/dani-garcia/vaultwarden/releases), 2026-04
- **GitHub stars 59.5K** に到達。元ツイートの "59K" 数字とほぼ一致（5/1 時点で取得） — [GitHub repo](https://github.com/dani-garcia/vaultwarden), 2026-05
- **Bitwarden Premium が10年ぶり値上げ**（$10/年 → $19.80/年）。これがVaultwarden乗り換え議論を再燃させた直接トリガー — [CompareTiers Bitwarden Pricing 2026](https://comparetiers.com/tools/bitwarden), 2026-01
- **Dashlane 無料プラン廃止**（2025-09）。"無料"ニーズの行き場として Bitwarden 無料プラン / Vaultwarden 自前ホストへ流入 — [Costbench Dashlane Pricing 2026](https://costbench.com/software/password-management/dashlane/), 2025-09
- **Bitwarden SDK 騒動 (2024-10〜11) は GPL3 巻き戻しで決着**したが、コミュニティの "Bitwarden は将来 closed source 化するのでは" 不安は残存。Vaultwarden 議論の心理的背景になっている — [The Register: Bitwarden GPL3](https://www.theregister.com/2024/11/04/bitwarden_gpls_password_manager/), 2024-11
- **CVE-2025-24364 (RCE) / CVE-2025-24365 (権限昇格)** が BI.ZONE により報告。修正済みだが「自前ホストでアップデート遅延 = 自分のVaultが攻撃可能」を再認識させた — [SecurityOnline](https://securityonline.info/password-management-at-risk-vaultwarden-vulnerabilities-expose-millions/), 2025
- **推奨運用パターンの定着**: 公開せず Tailscale / WireGuard 経由のみアクセスする"VPN内専用Vault" 構成が r/selfhosted の主流に — [XDA: Self-hosting password manager isn't dangerous](https://www.xda-developers.com/self-hosting-a-password-manager-isnt-dangerous/), 2026

---

## 🧩 関連概念・隣接分野

- **Bitwarden 公式サーバー**: 公式は .NET / MSSQL ベースで重い（推奨2GB RAM）。エンタープライズ機能（SSO・Directory Connector）は公式のみ提供。**個人用無料プランで vault 同期は無制限** という事実は元ツイートが触れていない最大のミスリード
- **Passbolt**: チーム向けOSSパスワードマネージャー。Bitwarden系とは別系統で、PGP暗号 + 共有特化。Vaultwarden vs Passbolt 比較記事が増加中
- **KeePass / KeePassXC**: ファイルベース（自前同期）の老舗OSS。クラウド同期ではなく Dropbox/iCloud に kdbx ファイルを置く流派
- **Proton Pass**: Proton Mail系の比較的新しい商用パスワードマネージャー。E2E + プライバシー訴求で Bitwarden / 1Password の対抗馬として急成長
- **Self-hosted vs Managed の二項対立**: 自前ホストは「コントロール最大化」、Managed は「運用責任の外注」。**両者のリスク座標が違うだけで、後者が必ず劣るわけではない**

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**:
  - 自分のデータが他社サーバーに置かれない安心感
  - 月数ドル × 家族人数 × 永遠 のサブスク回避
  - すべてのプレミアム機能が無料で使える
  - Rust製で軽量・高速、Docker化で展開楽
  - ライセンス AGPLv3 で完全FOSS（公式の SDK 騒動と無縁）
- **否定 / 慎重派の主張**:
  - **そもそも Bitwarden 無料プランで個人パスワード同期は無制限**。"$3/月かかる" 前提が崩れている
  - 自前ホストの**運用コスト（時間 / アップデート / バックアップ / SSL更新 / インシデント対応）** はサブスク代より遥かに高い
  - **2025-2026年に立て続けに重大CVE**。アップデート遅延で攻撃される事例が現実化
  - サーバーが落ちると**airport で2FAコード見られない**等の致命的UX事故。XDA記事が "Locked out at the airport" として警鐘
  - VPS事業者が破綻 / 故障 / 凍結すると**全パスワード喪失**のリスク（バックアップ運用が必須）
  - "1コマンドで10分" は誇張。HTTPS / リバースプロキシ / 認証強化 / IDS（CrowdSec/Fail2ban）まで含めると**最低半日仕事**
  - "Zero trust" は誤解を招く表現。サードパーティ信用を**自分の運用スキルへの信用に置換**しただけで、信用総量は変わらない
- **中立的に見るときの補助線**:
  - **判断基準の3軸**: ① 技術力（Linux/Docker/Reverse Proxy 自走可能か） / ② 運用継続性（5年後もアップデートし続けられるか） / ③ 重要度（家族の銀行・医療情報を預けて落とした時の影響）
  - **段階的移行**: いきなり全パスワード移すのではなく、まず試験用vaultを Vaultwarden に立てて1ヶ月運用 → 問題なければ本番へ
  - **VPN専用運用**: Tailscale 等で**インターネット非公開**にすれば攻撃面の大半が消える。CVE が出ても認証部分まで到達されにくい
  - **公式Bitwarden無料プラン + Vaultwardenバックアップ**等のハイブリッド構成も選択肢

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Vaultwarden を実プロダクションで使っている企業/家庭の実例レポート（特に5年以上の長期運用ケース）
- [ ] CVE-2026-26012 の影響範囲: 組織機能を使っていない個人ユースで実害はあるのか
- [ ] Bitwarden 公式の無料プランが今後も "無制限同期" を維持するか（値上げ後の経営戦略）
- [ ] Tailscale Funnel 等で公開せず外部からアクセスする運用の最新ベストプラクティス
- [ ] Vaultwarden の AGPLv3 が将来商用クラウド（"Vaultwarden as a Service"）を阻むか
- [ ] Proton Pass / 1Password / KeePassXC との横断比較（特に2FA・Passkey対応の実装差）
- [ ] 日本国内（Sakura VPS / Conoha / さくらのクラウド）で月500円VPS運用した場合の実コスト・性能ベンチ

---

## 📚 参考資料

- [GitHub: dani-garcia/vaultwarden](https://github.com/dani-garcia/vaultwarden) — 公式リポジトリ / README / リリースノート, 取得日 2026-05-01
- [Vaultwarden Releases](https://github.com/dani-garcia/vaultwarden/releases) — v1.35.8 (2026-04-25) 確認, 取得日 2026-05-01
- [SentinelOne: CVE-2026-26012](https://www.sentinelone.com/vulnerability-database/cve-2026-26012/) — 認証バイパス脆弱性詳細, 取得日 2026-05-01
- [BI.ZONE: Vaultwarden 高リスク脆弱性](https://bi.zone/eng/news/my-obnaruzhili-uyazvimosti-vysokogo-urovnya-opasnosti-v-vaultwarden/) — CVE-2025-24364 (RCE) / -24365 (権限昇格), 取得日 2026-05-01
- [SecurityOnline: Password Management at Risk](https://securityonline.info/password-management-at-risk-vaultwarden-vulnerabilities-expose-millions/) — 脆弱性インパクト解説, 取得日 2026-05-01
- [CompareTiers: Bitwarden Pricing 2026](https://comparetiers.com/tools/bitwarden) — Bitwarden 値上げ詳細（$1.65/月）, 取得日 2026-05-01
- [Costbench: Best Password Managers 2026](https://costbench.com/best/best-password-managers-2026/) — 4社価格比較, 取得日 2026-05-01
- [Costbench: Dashlane Pricing 2026](https://costbench.com/software/password-management/dashlane/) — 無料プラン廃止 (2025-09), 取得日 2026-05-01
- [The Register: Bitwarden GPL3 化](https://www.theregister.com/2024/11/04/bitwarden_gpls_password_manager/) — SDK 騒動の決着, 取得日 2026-05-01
- [Bitwarden community forum: Open Source Concerns](https://community.bitwarden.com/t/concerns-over-bitwarden-moving-away-from-open-source-what-does-our-future-hold/74800) — コミュニティ反応の一次資料, 取得日 2026-05-01
- [Vaultwarden discussion #5115: SDKライセンス影響](https://github.com/dani-garcia/vaultwarden/discussions/5115) — Vaultwarden 側の見解, 取得日 2026-05-01
- [XDA: Self-hosting risks (Locked out at airport)](https://www.xda-developers.com/self-hosted-password-manager-risks-limitations-locked-out/) — UX事故の警鐘, 取得日 2026-05-01
- [XDA: Self-hosting a password manager isn't as dangerous as you think](https://www.xda-developers.com/self-hosting-a-password-manager-isnt-dangerous/) — 反論側, 取得日 2026-05-01
- [OSSAlt: Vaultwarden 5分セルフホスト 2026](https://ossalt.com/guides/vaultwarden-self-host-bitwarden-2026) — 最新セットアップ手順, 取得日 2026-05-01
- [OSSAlt: Passbolt vs Vaultwarden vs Bitwarden チーム比較 2026](https://ossalt.com/guides/passbolt-vs-vaultwarden-vs-bitwarden-teams-2026) — チーム用途比較, 取得日 2026-05-01
- [Corelab: Self-Host Vaultwarden Securely 2026 Guide](https://corelab.tech/digital-vault-self-hosting-vaultwarden/) — セキュア運用ガイド, 取得日 2026-05-01
- 元クリップ: [[Clippings/Post by @ihtesham2005 on X.md]] — Xポスト原文（2026-05-01）

---

## 🗒 メモ

- **note記事化候補（強）**: 「Vaultwarden で月3ドル節約は本当に得か？— "0円で同じ" の裏側にある3つの落とし穴」というアングル。元ツイートが触れない **(1) Bitwarden 無料プランで十分な現実 / (2) 2025-2026年の重大CVE / (3) 運用コストの可視化** を3部構成で。逆張りでも煽りでもなく "技術力の自己診断軸" として提示すれば刺さる
- **X連投シリーズ候補**: 元ツイートを引用RTする形で「✅ 言ってることは大筋本当 ⚠️ でも触れてない事実が3つ」の批評型連投4本。ルーチンB（昼の批評型リプ）の弾としても使える
- **個人実用**: Tsukapon 関連の vault は iCloud Keychain でカバー中なので、現状 Vaultwarden 移行の必然性は低い。ただし **試験用に1台立てて Tailscale 越しの運用感を体験** する価値はある（記事化のネタ確保 + 自前ホストの手触り）
- **記事の差別化ポイント**: SNS の"バズリ系" Vaultwarden 紹介は **CVE と運用コストにほぼ触れない**。逆に技術系メディア（XDA, SecurityOnline）は警鐘寄り。**両者を中央でブリッジする日本語記事は手薄** = ニッチが空いている
- **継続ウォッチ**:
  - Bitwarden の次の値上げ・プラン改編
  - Vaultwarden v1.36 系の新機能・破壊的変更
  - Passkey 対応の進捗（Vaultwarden / Bitwarden 両方）
  - 日本国内VPS（Sakura / Conoha）+ Vaultwarden の運用ベンチ
