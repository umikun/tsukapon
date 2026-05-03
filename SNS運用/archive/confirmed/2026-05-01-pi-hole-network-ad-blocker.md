---
created: 2026-05-01
tags: [調査, pi-hole, dns, network, privacy, homelab]
source: "[[Clippings/pi-holepi-hole A black hole for Internet advertisements.md]]"
---

# Pi-hole は「DNSシンクホール型のネットワーク広告ブロッカー」——v6で別物になり、AdGuard Homeとの差は"運用思想"に集約された

> **TL;DR**
> Pi-holeはDNS問い合わせを横取りして広告ドメインを"ブラックホール送り"にする、Linux/Raspberry Pi向けのネットワーク広告ブロッカー。**v6（2025-02）でlighttpd+PHPを捨てFTL内蔵Webサーバ＋REST APIに刷新**され、設定はTOML一本化、HTTPS管理画面ネイティブ対応に。最新は**FTL v6.6.1 / Core v6.4.2（2026-04-24）**。競合のAdGuard Homeは「DoH/DoT/DoQ標準装備＋サービス単位ブロック」で初期セットアップが楽。Pi-holeは「グループ管理・コミュニティ資産・カスタマイズ性」で勝つ。**YouTube動画内広告は両者ともDNS層では原理的に無理**。

## 📌 元テキスト（抜粋）

> The Pi-hole® is a [DNS sinkhole](https://en.wikipedia.org/wiki/DNS_Sinkhole) that protects your devices from unwanted content without installing any client-side software. ……Easy-to-install / Resolute / Responsive / Lightweight / Robust / Insightful / Versatile / Scalable / Modern / Free. ……One-Step Automated Install: `curl -sSL https://install.pi-hole.net | bash`

出典: [[Clippings/pi-holepi-hole A black hole for Internet advertisements.md]]（GitHub `pi-hole/pi-hole` README）

---

## 🔑 キーワード早見表

| 用語 | ざっくり意味 | もっと知りたい時のキーワード |
|---|---|---|
| DNS sinkhole | 広告/マルウェア配信ドメインへの問い合わせを偽の応答で潰す技術 | `Response Policy Zone`, `RPZ`, `null route` |
| Pi-hole | DNSシンクホール型のOSS広告ブロッカー。ネットワーク全体に効く | `pihole/pihole`, `pi-hole.net` |
| FTL / FTLDNS | Pi-holeの中核デーモン。dnsmasq fork。v6からWebサーバ＋REST APIも内包 | `pi-hole/FTL`, `pihole-FTL` |
| Antigravity（v6新機能） | ブロックリストの逆。**購読型のallowlist**。同僚や有志が共有可 | `subscribed allowlists`, `Pi-hole v6` |
| Gravity | Pi-holeのブロックリスト集約・更新コマンド/プロセス名 | `pihole -g`, `gravity database` |
| AdGuard Home | Goで書かれた競合OSS。DoH/DoT/DoQネイティブ＋サービスブロックUI | `AdguardTeam/AdGuardHome` |
| Unbound | 自前で再帰DNS解決する権威リゾルバ。Pi-holeの上流にして暗号化＋プライバシー強化 | `unbound recursive`, `127.0.0.1#5335` |
| cloudflared | CloudflareのDoHプロキシ。Pi-holeの上流にしてDNS-over-HTTPS化 | `cloudflared proxy-dns`, `127.0.0.1#5053` |
| DoH / DoT / DoQ | DNS over HTTPS / TLS / QUIC。経路上の盗聴・改竄を防ぐ暗号化DNS | `RFC 8484`, `RFC 7858`, `RFC 9250` |
| pihole API | `pihole api stats/summary` 等。v6で公式REST APIに統一 | `pi.hole/api/docs` |

---

## 🧭 背景 / なぜ今これが話題なのか

Pi-holeは**2015年に「Raspberry Piで家全体の広告を止める」OSS**として登場。原理は単純で、家庭内ルーターのDNSをPi-holeに向けると、Pi-holeが広告サーバへの名前解決をすべて`0.0.0.0`等に書き換える。**クライアント側にアプリ不要**で、スマートTV・ゲーム機・IoT機器まで一斉に広告がブロックできるのが破壊力だった。

長らくv5系で安定運用されてきたが、**2025-02-18にv6が一般リリース**。これは見た目以上に大きな転換で、内部的には「**lighttpd + PHP管理画面という10年来の構成を捨て、FTL（C実装）の中にWebサーバ＋REST APIを取り込んだ**」モノリス再編。設定ファイルもバラバラだったものが`pihole.toml`一本に集約された（[Pi-hole公式 v6紹介](https://pi-hole.net/blog/2025/02/18/introducing-pi-hole-v6/)）。

その後も継続的にメンテされており、執筆時点（2026-05-01）の最新版系列はおおよそ：

- v6.0.x（2025-02〜03）→ v6.2（2025-05）→ v6.3（2025-10）→ v6.4（2025-11）→ v6.5（2026-02）→ **v6.6 / v6.6.1（2026-04）**
- v6.6.1（2026-04-24）はセキュリティ修正と「**gravity更新中はrestartを待つ**」改善、`resolver.macNames`オプション追加が目玉

並行して競合の**AdGuard Home**（2018〜）が「Goバイナリ1個で動く」「DoH/DoT/DoQ標準装備」「サービス単位ブロック（YouTube/TikTok/Discordをトグル一発）」で勢力を伸ばし、homelab/r/selfhosted界隈では**「初心者ならAdGuard Home、こだわるならPi-hole」**という住み分けがほぼ定着している。

---

## 🔬 主張のファクトチェック

| 元テキストの主張 | 裏取り結果 | ソース | 判定 |
|---|---|---|---|
| Pi-holeはDNSシンクホール | DNS問い合わせを横取りして広告ドメインを潰す方式で公式・第三者ともに一致 | [Wikipedia: DNS sinkhole](https://en.wikipedia.org/wiki/DNS_Sinkhole), [Pi-hole docs](https://docs.pi-hole.net/) | ✅ 一致 |
| クライアント側ソフト不要 | DNS設定変更だけで効くため正しい。ただし**HTTPS化された広告**やアプリ内ハードコード接続には限界 | [Pi-hole docs / FAQ](https://docs.pi-hole.net/) | ⚠️ ほぼ一致（限界あり） |
| 10分以内でインストール完了 | `curl ... | bash`で対話式インストール、Raspberry Pi等で実測5〜10分は妥当 | [Pi-hole prerequisites](https://docs.pi-hole.net/main/prerequisites/) | ✅ 一致 |
| サーバ級HWで数億クエリ捌ける | 公式ブログ「How much traffic can Pi-hole handle?」（2017）で実測あり。古いがアーキ的に否定理由なし | [pi-hole.net 2017](https://pi-hole.net/2017/05/24/how-much-traffic-can-pi-hole-handle/) | ⚠️ ほぼ一致（出典が2017） |
| DHCPサーバとしても使える | 公式discourse FAQで現役機能 | [Discourse: built-in DHCP](https://discourse.pi-hole.net/t/how-do-i-use-pi-holes-built-in-dhcp-server-and-why-would-i-want-to/3026) | ✅ 一致 |
| IPv4 / IPv6両方ブロック | v6でDHCP API側もIPv6完全対応強化（v6.3 Oct 2025） | [v6.3 release notes](https://pi-hole.net/blog/2025/10/25/pi-hole-ftl-v6-3-web-v6-3-and-core-v6-2-released/) | ✅ 一致 |
| `pihole api`コマンドが使える | v6でREST API公式統一。`http://pi.hole/api/docs`でSwagger UI、CLIから`pihole api ...` | [Pi-hole v6 release](https://pi-hole.net/blog/2025/02/18/introducing-pi-hole-v6/) | ✅ 一致 |
| `curl | bash`は議論の余地あり | 元READMEも自認。代替（git clone / wget→sudo bash）を提示している | README本体・コミュニティ議論で広く既知 | ✅ 一致 |
| FTLDNSは軽量で高速 | C実装でメモリフットプリント小、AdGuard Home（Go）よりわずかに軽い、というのが第三者比較の通説 | [WunderTech比較](https://www.wundertech.net/adguard-home-vs-pi-hole-best-ad-blocker/), [getblockify 2026](https://getblockify.com/blog/adguard-home-vs-pi-hole/) | ✅ 一致 |
| READMEに記載のWeb UI構成（lighttpd前提の説明） | **v6で陳腐化**。lighttpd / PHPは廃止済。READMEの一部記述は古い可能性あり（Clippings時点で要確認） | [v6 introduction](https://pi-hole.net/blog/2025/02/18/introducing-pi-hole-v6/) | ❌ 要注意（README更新ラグ） |

---

## 🌐 最新動向（2026-05-01時点）

- **FTL v6.6.1 / Core v6.4.2 リリース（2026-04-24）**: gravity更新中はrestart待機、`resolver.macNames`オプション、セキュリティ修正 — [Pi-hole blog](https://pi-hole.net/blog/2026/04/24/pi-hole-ftl-v6-6-1-and-core-v6-4-2-released/), 2026-04
- **MAC ベースのアクセス制御強化**: v6.6でMACコントロール追加（複雑なネットワークでホスト名解決を制御） — [AlternativeTo news](https://alternativeto.net/news/2026/4/pi-hole-releases-ftl-v6-6-web-v6-5-and-core-v6-4-1-with-security-fixes-adds-mac-control/), 2026-04
- **v6.5（2026-02）の起動時間短縮**: 履歴クエリのDB読み込みを非同期化し、起動直後からDNS解決可能に — [Pi-hole blog](https://pi-hole.net/blog/2026/02/17/pi-hole-ftl-v6-5-web-v6-4-1-and-core-v6-4-released/), 2026-02
- **`.internal` TLDブロック対応**（v6.3, 2025-10）: RFC draft-davies-internal-tld-03に従い、内部用TLDが上流に漏れないように — [Pi-hole blog](https://pi-hole.net/blog/2025/10/25/pi-hole-ftl-v6-3-web-v6-3-and-core-v6-2-released/), 2025-10
- **AdGuard Home比較で「Pi-holeはモジュラー、AdGuardはオールインワン」が2026版の定番結論** — [Blockify比較 2026](https://getblockify.com/blog/adguard-home-vs-pi-hole/), 2026
- **YouTube広告ブロックは依然として原理的に困難**: 動画と広告が同じドメインから配信されるため、DNS層では分離不能。コミュニティのregex対応はpreroll止まりで動画本編が再生されない副作用報告多数 — [Pi-hole Discourse](https://discourse.pi-hole.net/t/youtube-ads-getting-through-pihole-any-advances-in-100-blocking-without-also-blocking-youtube-videos/60951), 2024〜2026継続

---

## 🧩 関連概念・隣接分野

- **Unbound（再帰DNSリゾルバ）**: Pi-holeの上流に立てて、ルートサーバから自前でDNS解決する構成が定番。プライバシー的にCloudflareやGoogleに問い合わせを送らずに済む。`127.0.0.1#5335`で連携 — [Pi-hole公式: unbound](https://docs.pi-hole.net/guides/dns/unbound/)
- **cloudflared / DoHプロキシ**: Pi-hole単体はDoH非対応なので、cloudflaredをローカルプロキシとして挟み`127.0.0.1#5053`を上流にする方式が広く使われる — [Fullmetalbrackets Pi-hole v6 DoH](https://fullmetalbrackets.com/blog/using-dns-over-https-with-pihole/)
- **AdGuard Home**: 競合OSS。**DoH/DoT/DoQ標準装備、サービス別ブロックUI**が強み。逆にグループ管理（端末ごとのブロックリスト切替）はPi-holeの方が緻密
- **Technitium DNS Server**: Windows/Linuxで動くフル機能DNSサーバ。広告ブロックは"おまけ"だが権威DNSも兼任できる第三の選択肢
- **NextDNS**: クラウド型のDNSフィルタ。自宅ハードを持たずに同等の効果。出張先でも効くがプライバシー観点は提供元への信頼次第
- **DNSSEC**: Pi-hole + Unboundで有効化推奨。DNS応答の改竄を検出。広告ブロックとは独立だが「DNS層を整える」という同じ文脈

---

## 🪞 反対意見 / 別角度からの視点

- **肯定側の主張**: 「**1台立てれば家中のスマートTV/ゲーム機/IoTまで広告とトラッカーが消える**」のは、ブラウザ拡張ではどう頑張っても届かない領域。プライバシー意識の高い人にとってPi-hole導入はROIが極めて高い。OSSで運用が透明、コミュニティが厚い。
- **否定 / 慎重派の主張**:
  - **DNS層の限界**: HTTPSコンテンツに混ざった広告（YouTube・Instagram・X等の同一ドメイン配信）は原理的に止まらない。ESNI/ECH時代になるとSNIベース対策も難化。期待値を上げすぎると「Pi-hole入れたのにYouTube広告出るぞ」と落胆する典型パターンに陥る — [Pi-hole Discourse: YouTube問題](https://discourse.pi-hole.net/t/so-youtube-ads-cant-really-be-blocked-properly-with-pi-hole/34986)
  - **単一障害点になり得る**: Pi-holeが落ちると家中のDNSが死ぬ。冗長化（2台運用 or セカンダリDNS指定）を考慮しないと家族の信頼を失う。
  - **`curl | bash`懸念**: README自身が「controversial」と認める通り、サプライチェーン攻撃の標的になりやすい。git cloneかDocker推奨。
  - **AdGuard Home登場以降のコモディティ化**: 「最初の1台」としてAdGuard Homeを選ぶ初心者が増え、Pi-holeの優位性は"運用に手を入れる楽しさ"に寄ってきている。Goバイナリ1個＋GUIでDoH内蔵のAdGuardは初期セットアップで明確に楽 — [XDA Developers: 乗り換え記事](https://www.xda-developers.com/pi-hole-changed-my-network-but-adguard-made-me-forget-pi-hole-existed/)
- **中立的に見るときの補助線**:
  - **DNS層 ≠ コンテンツフィルタ**。広告ブロックは「DNS層（Pi-hole/AdGuard）」「TLS/SNI層（特殊なプロキシ）」「アプリ層（uBlock Origin/SponsorBlock）」の**3層構造**で考えるべき。Pi-holeはDNS層しか担えないと割り切ると期待値がずれない。
  - 暗号化DNSを入れる動機は「**ISPからのDNSログ収集を断つ**」ためであり、広告ブロック性能は変わらない。混同しがち。
  - 家庭ネットワーク全体の品質に効くので、**子持ち家庭の不適切コンテンツブロック**にも転用可。教育用途のブロックリスト購読がコミュニティに豊富。

---

## ❓ まだ残る疑問 / 次に調べると面白いこと

- [ ] Pi-hole v6のREST APIをObsidian Dataviewやhomelab dashboardから叩いて、家庭内DNSログを可視化できるか（[[_ kiwami/tools/daily-log/]] と統合の余地）
- [ ] AdGuard Homeへの完全移行コスト（ブロックリスト・グループ設定・ホストレコード）と、両者を**並列運用**して比較する実験
- [ ] Pi-hole + Unboundスタックを Docker Compose で1ファイル化してGitHubにテンプレ公開する価値（X/note記事ネタ）
- [ ] 「Antigravity（購読型allowlist）」を活用した、業務系SaaS（Slack/Zoom/Notion）誤爆対策のベストプラクティス
- [ ] ECH（Encrypted Client Hello）が普及した時のPi-hole依存度低下シナリオ
- [ ] iCloud Private Relay / NextDNSなどのクラウド型DNSフィルタとの併用時の挙動（DNSが横取りされる順序）

---

## 📚 参考資料

- [Pi-hole 公式GitHub README](https://github.com/pi-hole/pi-hole) — 元テキストそのもの, 取得日 2026-05-01
- [Introducing Pi-hole v6](https://pi-hole.net/blog/2025/02/18/introducing-pi-hole-v6/) — v6でlighttpd/PHP廃止＋FTL内蔵Webサーバ＋REST API＋Antigravity, 取得日 2026-05-01
- [Pi-hole FTL v6.6.1 and Core v6.4.2 Released](https://pi-hole.net/blog/2026/04/24/pi-hole-ftl-v6-6-1-and-core-v6-4-2-released/) — 最新版（2026-04-24）, 取得日 2026-05-01
- [Pi-hole FTL v6.5 release notes](https://pi-hole.net/blog/2026/02/17/pi-hole-ftl-v6-5-web-v6-4-1-and-core-v6-4-released/) — 起動時間改善, 取得日 2026-05-01
- [Pi-hole FTL v6.3 release notes](https://pi-hole.net/blog/2025/10/25/pi-hole-ftl-v6-3-web-v6-3-and-core-v6-2-released/) — `.internal` TLDブロック・Smart Interface Detection, 取得日 2026-05-01
- [AlternativeTo: v6.6 with security fixes](https://alternativeto.net/news/2026/4/pi-hole-releases-ftl-v6-6-web-v6-5-and-core-v6-4-1-with-security-fixes-adds-mac-control/) — MAC制御追加の第三者報, 取得日 2026-05-01
- [Pi-hole Unbound公式ガイド](https://docs.pi-hole.net/guides/dns/unbound/) — 上流再帰DNS構築, 取得日 2026-05-01
- [Fullmetalbrackets: Pi-hole v6 + Cloudflared DoH](https://fullmetalbrackets.com/blog/using-dns-over-https-with-pihole/) — v6対応のDoH手順, 取得日 2026-05-01
- [Blockify: AdGuard Home vs Pi-hole 2026](https://getblockify.com/blog/adguard-home-vs-pi-hole/) — 2026版の比較結論（モジュラー vs オールインワン）, 取得日 2026-05-01
- [WunderTech: AdGuard Home vs Pi-hole](https://www.wundertech.net/adguard-home-vs-pi-hole-best-ad-blocker/) — メモリフットプリント・サービスブロック比較, 取得日 2026-05-01
- [XDA: Pi-hole→AdGuardに乗り換え記事](https://www.xda-developers.com/pi-hole-changed-my-network-but-adguard-made-me-forget-pi-hole-existed/) — 反対視点ソース, 取得日 2026-05-01
- [Pi-hole Discourse: YouTube広告問題](https://discourse.pi-hole.net/t/so-youtube-ads-cant-really-be-blocked-properly-with-pi-hole/34986) — DNS層の原理的限界, 取得日 2026-05-01
- [Pi-hole Discourse: YouTube ads getting through (2024〜)](https://discourse.pi-hole.net/t/youtube-ads-getting-through-pihole-any-advances-in-100-blocking-without-also-blocking-youtube-videos/60951) — 継続的な議論スレ, 取得日 2026-05-01

---

## 🗒 メモ

このClippingsを残した時点では、おそらく**[[2026-04-30-openvpn-overview]]** や **[[2026-04-26-open-seo-self-hosted-stack]]** と同じ「自宅サーバ／プライバシー強化」系の関心の流れにある。Pi-holeはhomelab入門の鉄板で、本vaultの **[[Macで定期的に同期.md]]** 的な"自宅常駐サービス"カテゴリに自然に並ぶ。

使い道:

1. **note記事化**: 「Pi-hole v6 で何が変わったか / AdGuard Homeとどう違うか 2026年版」。表で比較すると検索流入が見込める（「pi-hole adguard 比較」は常時SEO需要あり）
2. **X投稿ネタ**: 「Pi-hole READMEの`curl | bash`は便利だけどgit cloneで読んでから入れる派です」系の啓発投稿。3〜4ポストのスレッドに収まる
3. **自宅運用への取り込み検討**: Mac mini常時稼働ならDocker版Pi-holeを立て、`pihole api stats/summary`を Daily Log dashboard（[[_ kiwami/tools/daily-log/]]）の1カードに混ぜ込むと面白い。**自分のDNSクエリ件数 = 集中度の代理指標**として使えるかも

⚠️ 元README自体に「lighttpd前提」っぽい古い記述が混じっている可能性がある（v6で実態は変わった）。Clippings保存時点のスナップショットとして扱い、**運用に取り入れる時は必ず公式docs最新版を見る**のが安全。
