---
created: 2026-04-30
tags: [調査, OpenVPN, VPN, ネットワーク, セキュリティ]
source: 直接貼付（キーワード「OpenVPN」のみ）
---

# OpenVPN — オープンソースVPNの "古株" は2026年もまだ現役か

> **TL;DR**
> OpenVPN は James Yonan が2001年に書き始めた GPLv2 のVPNソフトで、TLS/OpenSSL ベースのカスタム暗号化プロトコルを使う。
> 長年「設定が複雑・遅い」が定番の弱点だったが、2025年に **DCO（Data Channel Offload）が Linux 6.16 のメインラインへ取り込まれ**、UDP使用時はWireGuardに肉薄する性能を出せるようになった。
> 一方で**速度勝負ではWireGuardが2〜4倍**、シンプルさでも負けるため、2026年現在の使い分けは「**TCP 443 で検閲・厳しいFW越え**が要るならOpenVPN／**自宅・社内の素直なネットワーク**ならWireGuard」が定石。

## 📌 元テキスト（抜粋）

> OpenVPN

出典: 直接貼付（キーワードのみ。網羅的な俯瞰調査として依頼）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| OpenVPN | TLS/OpenSSLベースのオープンソースVPN実装。カスタムプロトコル | OpenVPN 2.6 / Community Edition |
| Community Edition | OpenVPN 本体。GPLv2 で誰でもサーバ/クライアントを立てられる | `openvpn` パッケージ |
| Access Server | OpenVPN 公式の商用版。Web UI・LDAP・サポート同梱（2接続まで無料） | OpenVPN AS |
| CloudConnexa | OpenVPN 社のクラウド型 ZTNA / SASE サービス（旧 OpenVPN Cloud） | CloudConnexa SASE |
| DCO | Data Channel Offload。データ平面をカーネルに落として高速化 | ovpn-dco / Linux 6.16 |
| TUN / TAP | OS の仮想NIC。TUN=L3、TAP=L2。OpenVPN は両対応 | tun.ko / tap.ko |
| TLS-Crypt v2 | コントロールチャネルを事前共有鍵で覆う追加レイヤ | `--tls-crypt-v2` |
| OpenSSL | OpenVPN が依存する暗号ライブラリ（mbedTLS版もあり） | OpenSSL 3.x |
| WireGuard | 競合の最小実装VPN。Linux カーネルに2020年取り込み済 | wg-quick / NoiseIK |
| SASE | クラウド型「ネットワーク+セキュリティ」統合の概念。OpenVPN社も寄せている | Gartner SASE |

---

## 🧭 背景 / なぜ今これが話題なのか

- **2001年**、James Yonan が中央アジアを移動中に「自宅の社内ネットに安全に入りたいが既存の商用VPNがどれもイマイチ」という個人的な不便から書き始めたのが起点。**2002年に最初のオープンソース版**を公開、ライセンスは **GPLv2**（[OpenVPN公式: History of OpenVPN](https://openvpn.net/blog/the-history-of-openvpn/)）。
- 当時主流だった IPsec は「カーネル実装 + 鍵交換が複雑（IKEv1）」で運用が辛く、OpenVPN は **ユーザー空間 + TLS/OpenSSL** という割り切りで「証明書ベースで普通に動く」VPN を最初に普及させた存在。
- 2010年代を通して **NAT越え・モバイル切替・ポート443で偽装** といった現場の困りごとに強い実装として、特に**社内VPN・拠点間VPN・市販VPNサービス**の裏側で広く採用された。
- 2020年に **WireGuard** が Linux カーネル本体に取り込まれて以降、「軽量・高速・設定が短い」競合の登場で OpenVPN は速度面で後手に。これに対する OpenVPN 側の答えが **DCO（Data Channel Offload）**（[OpenVPN Blog](https://blog.openvpn.net/openvpn-data-channel-offload-dco-the-definitive-guide-to-the-performance-boost-making-openvpn-the-fastest-vpn-protocol)）。
- **2025年4月、ovpn-dco が Linux カーネルメインラインにマージ → Linux 6.16 から正式同梱**。23年ぶりに「ユーザー空間の遅いVPN」というレッテルを剥がしに来た格好。
- 同2025年には **OpenVPN Inc. が M&A オファーを受けた**（買収されたかは未公表）と報じられ、**ESPRE社との提携**も発表。会社としては SASE / ZTNA の方向（CloudConnexa）にシフト中（[OpenVPN Blog: Announcements](https://blog.openvpn.net/tag/announcements)）。

---

## 🔬 主張のファクトチェック

「OpenVPNといえば」で語られがちなクリシェを2026年時点の事実と突き合わせ。

| よく言われる主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| OpenVPN は James Yonan が **2001年** に開発、GPLv2 | 2001年に開発開始、2002年に最初のリリース。GPLv2 で公開 | [OpenVPN - Wikipedia](https://en.wikipedia.org/wiki/OpenVPN), [OpenVPN Blog: History](https://openvpn.net/blog/the-history-of-openvpn/) | ✅ 一致 |
| OpenVPN は **TCP 443 で動かせる** ので検閲・厳しいFWに強い | 「TCP 443 上で OpenVPN を流すと普通の HTTPS と区別が付きにくく、企業FW・ホテル・中国などで効く」と複数比較記事 | [CyberInsider 2026](https://cyberinsider.com/vpn/wireguard/wireguard-vs-openvpn/), [Calmops 2026](https://calmops.com/network/vpn-protocols-comparison-2026/) | ✅ 一致 |
| WireGuard は OpenVPN より **3倍以上速い** | 1Gbps回線の実測で WireGuard 940〜960Mbps / OpenVPN 約480Mbps（UDP）。**2〜4倍**が一般的レンジ | [CyberInsider](https://cyberinsider.com/vpn/wireguard/wireguard-vs-openvpn/), [Tech-Insider 2026](https://tech-insider.org/wireguard-vs-openvpn-2026/) | ⚠️ ほぼ一致（"3x" は条件次第） |
| OpenVPN DCO で **WireGuard 並みの速度**になる | OpenVPN公式は「同一HWで約2倍、条件次第で3〜10倍」、UDP限定。WireGuard を完全には抜かないが肉薄 | [OpenVPN Blog: DCO](https://blog.openvpn.net/openvpn-data-channel-offload-dco-the-definitive-guide-to-the-performance-boost-making-openvpn-the-fastest-vpn-protocol), [Netgate pfSense Docs](https://docs.netgate.com/pfsense/en/latest/vpn/openvpn/dco.html) | ⚠️ ほぼ一致（"並み" は誇張気味） |
| 2025年に **重大脆弱性** が出ている | 2025年にOpenVPN関連で12件のCVE。Access Server の CVE-2025-2704、サーバ assert の DoS 系などあり。ただし高リスクの常時露出系は出ていない | [OpenVPN Security Advisories](https://openvpn.net/security-advisories/), [Stack.Watch](https://stack.watch/product/openvpn/) | ✅ 一致（重大さは「中」程度） |
| Cure53 が **2023年に独立監査**を実施し問題ナシ | OSTIF 出資で Cure53 が監査、High-risk 脆弱性ゼロ。過去の脆弱性は72時間以内修正の運用 | 検索結果（複数サイト経由） | 🔍 二次情報のみ確認（Cure53レポートPDFは別途要確認） |

---

## 🌐 最新動向（2026-04-30 時点）

- **DCO が Linux 6.16 にメインラインマージ済み（2025-04）** — `ovpn` カーネルモジュール経由でデータ平面をカーネル処理。同一HWで約2倍、UDPのみ — [OpenVPN Blog](https://blog.openvpn.net/openvpn-data-channel-offload-dco-the-definitive-guide-to-the-performance-boost-making-openvpn-the-fastest-vpn-protocol), 2026-0X
- **Windows クライアントは wintun を廃止、win-dco がデフォルトに**（フォールバックは tap-windows6）— [GitHub Releases](https://github.com/OpenVPN/openvpn/releases), 2026
- **2025年内にCVEが12件公開**。中でも CVE-2026-40215（TLSハンドシェイクのレース）/ CVE-2026-35058（不正パケットでサーバAssert）あたりは要パッチ — [Security Advisories](https://openvpn.net/security-advisories/), 2026
- **OpenVPN Inc. は2025年4月にM&Aオファー**を受けたとされる。ESPRE 社との提携も発表 — [OpenVPN Announcements](https://blog.openvpn.net/tag/announcements), 2025
- **CloudConnexa（旧 OpenVPN Cloud）** を SASE/ZTNA 寄りにリブランディング。「自前構築 vs マネージド」の選択肢として推す方向 — [OpenVPN: CE vs Access Server](https://blog.openvpn.net/openvpn-community-edition-vs-access-server/), 2026
- **FreeBSD 15 互換**や **big endian Linux で DCO 対応**など、地味だが運用層でのカバレッジ拡大が継続 — [GitHub Releases](https://github.com/OpenVPN/openvpn/releases), 2026

---

## 🧩 関連概念・隣接分野

- **WireGuard**: Linux 5.6 で本体取り込み済の "ミニマル"VPN。約4,000行のコードで NoiseIK ハンドシェイクを実装。OpenVPN と直接競合し、2026年は性能・シンプルさで多くのケースで第一選択。
- **IPsec / IKEv2**: OS 標準・ハードウェア対応が厚い古参VPN。**iOS/Macの Always On** や **企業の拠点間専用線代替**ではいまだ強い。OpenVPN とは「クライアント証明書運用 vs キャリアグレード」のすみ分け。
- **OpenSSL / mbedTLS**: OpenVPN の暗号は外部ライブラリ依存。OpenSSL 3.x の脆弱性（例 CVE-2025-15467）が直接 OpenVPN にも影響することがある。組み込み用途では mbedTLS ビルドも選べる。
- **TUN/TAP デバイス**: OpenVPN が依存する OS の仮想NIC。WireGuard も同じ TUN を使うが、こちらはユーザー空間設定がほぼ不要。
- **SASE / ZTNA**: 「VPN を解体してアプリ単位アクセスへ」のクラウド型統合。CloudConnexa はここに寄せた商品ライン。Cloudflare Access / Tailscale / Twingate などが直接競合。

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張（OpenVPN を選ぶ理由）**:
  - **TCP 443 で動く**ため、検閲国家・厳しい企業FW・公衆Wi-Fi で WireGuard が刺さらない場面でも繋がる。
  - **証明書ベースの運用が枯れている**（PKI・CRL・OCSP）。エンタープライズの監査要件と相性が良い。
  - **TUN/TAP 両対応**で、L2 ブリッジが必要な特殊用途（古いNetBIOS / レガシーゲーム / VLANまるごと）でもOK。
  - 25年近い運用実績。**ノウハウ・サードパーティ製管理ツール・FAQ がとにかく多い**。

- **否定 / 慎重派の主張（WireGuard 等を選ぶ理由）**:
  - 設定ファイル（`server.conf`）の項目数・暗号スイートの選択肢が多すぎ、**設定ミスで弱くなる事故**が起きがち。
  - 同一HWで **WireGuard の方が2〜4倍速い**ケースが多い（DCO 入れても完全には抜けない）。
  - コードベースが大きく、依存も多い（OpenSSL）。**監査面積**が WireGuard より広い。
  - スマホでの**バッテリー持ち**や**スリープからの即時再接続**は WireGuard の方が体感良好。

- **中立的に見るときの補助線**:
  - **「速度 vs 通せる場所」のトレードオフ**で割り切るのが2026年の定石。SASE/ZTNA に行くなら「OpenVPN か WireGuard か」より「**自前構築 vs マネージド**」の軸の方が判断材料として大きい。
  - 中小企業の日本市場では「**ルーター内蔵VPN（IPsec）**」「**VPNサービス契約（FLESPEEQ等）**」「**OpenVPN自前構築**」「**Tailscale等のZTNA**」の4択が現実。OpenVPN自前は**情シス工数を最も食う**選択肢である点は前提に置きたい — [プラムシステムズ: OpenVPN導入支援](https://www.plum-systems.co.jp/service/koutiku/koutiku_openvpn.html), [浅間商事: 中小企業向けVPN](https://www.asama-shoji.co.jp/blog/column/1740/)。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] **DCO 有効時の実測**: macOS / Windows / Linux で同一HW・同一OpenVPN設定で UDP 比較したら、WireGuard との差は具体的に何%まで縮むのか
- [ ] **TLS-Crypt v2** を有効にしたときの DoS 耐性は2026年時点で十分か（最近のCVEはここに集中している）
- [ ] **OpenVPN Inc. のM&A** は誰が買った／買おうとしたのか。CloudConnexa の今後の料金体系に影響するか
- [ ] **SASE/ZTNA への完全移行**を選んだ場合、OpenVPN（CE）を残す合理的なユースケースは何か（OT/IoT・低帯域拠点など）
- [ ] **mbedTLS ビルド**の OpenVPN は2026年も保守されているのか（組み込み・ルータベンダー向け）

---

## 📚 参考資料

- [OpenVPN — Wikipedia](https://en.wikipedia.org/wiki/OpenVPN) — 歴史・ライセンス・対応プラットフォームの一次的まとめ, 取得日 2026-04-30
- [The History of OpenVPN（OpenVPN公式ブログ）](https://openvpn.net/blog/the-history-of-openvpn/) — James Yonan の動機・年表, 取得日 2026-04-30
- [OpenVPN/openvpn — GitHub Releases](https://github.com/OpenVPN/openvpn/releases) — 最新リリース・wintun廃止・FreeBSD 15対応, 取得日 2026-04-30
- [OpenVPN Data Channel Offload — Definitive Guide](https://blog.openvpn.net/openvpn-data-channel-offload-dco-the-definitive-guide-to-the-performance-boost-making-openvpn-the-fastest-vpn-protocol) — DCO 性能と Linux 6.16 マージの背景, 取得日 2026-04-30
- [OpenVPN DCO — pfSense Documentation](https://docs.netgate.com/pfsense/en/latest/vpn/openvpn/dco.html) — DCO の制約（UDP限定等）, 取得日 2026-04-30
- [OpenVPN Security Advisories（公式）](https://openvpn.net/security-advisories/) — CVE と対応バージョン, 取得日 2026-04-30
- [WireGuard vs OpenVPN: 7 Key Differences in 2026 — CyberInsider](https://cyberinsider.com/vpn/wireguard/wireguard-vs-openvpn/) — 2026年時点の性能・FW通過比較, 取得日 2026-04-30
- [VPN Protocols Complete Guide 2026 — Calmops](https://calmops.com/network/vpn-protocols-comparison-2026/) — WireGuard / OpenVPN / IPSec の使い分け表, 取得日 2026-04-30
- [Empirical Performance Analysis of WireGuard vs OpenVPN — MDPI](https://www.mdpi.com/2073-431X/14/8/326) — 査読付き比較研究（クラウド/仮想化環境）, 取得日 2026-04-30
- [OpenVPN Announcements](https://blog.openvpn.net/tag/announcements) — M&A・ESPRE提携・SASE方針, 取得日 2026-04-30
- [OpenVPN Community Edition vs Access Server](https://blog.openvpn.net/openvpn-community-edition-vs-access-server/) — CE / AS / CloudConnexa の使い分け, 取得日 2026-04-30
- [プラムシステムズ: OpenVPN 導入支援](https://www.plum-systems.co.jp/service/koutiku/koutiku_openvpn.html) — 日本語での法人導入実績の参考, 取得日 2026-04-30

---

## 🗒 メモ

- **使い道アイデア**:
  - X 投稿ネタとして「**WireGuard全盛の2026年に、それでも OpenVPN を選ぶ3つの理由**」が手堅い（TCP 443 / 監査運用 / 既存ノウハウ）。LinuxカーネルにDCOマージの話まで盛れる。
  - note の AIニュース日次系には合わないが、**「在宅・出張先からのリモートワーク基礎」シリーズ**を作るなら OpenVPN vs WireGuard vs Tailscale の比較記事は需要が読める。
  - 自前運用するなら、**Access Server無料2接続枠**＋自宅ルータの構成が一番コスパが良いはず。クライアント証明書運用の体験記まで書ければ実装ノウハウ系の差別化になる。
- **個人の所感**: 2026年でも OpenVPN を「**新規で**」選ぶ理由は**通信を通すこと自体**にあって、速度や設定の楽さでは選ばれない。逆に言えば、**「まず繋がる」**を最優先にする現場（出張先のホテル・厳しい企業ネット・規制下のユーザー）では今後も第一選択であり続ける可能性が高い。
- **派生調査の候補**: WireGuard / Tailscale / Cloudflare Access — 「2026年のリモートアクセス事情」というシリーズ調査として束ねると面白い。
