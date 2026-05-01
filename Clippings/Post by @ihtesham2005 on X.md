---
title: "Post by @ihtesham2005 on X"
source: "https://x.com/ihtesham2005/status/2049942008471736403"
author:
  - "[[@ihtesham2005]]"
published: 2026-05-01
created: 2026-05-01
description: "1Passwordはユーザーあたり月額3ドルを請求します。 Dashlaneは月額4.99ドルを請求します。 LastPassは月額3ドルを請求します。 誰かがBitwardenサーバー全体をRustで書き直し、0ドルでオープンソース化しました。それはすべてのデバイス上のすべて"
tags:
  - "clippings"
---
1Passwordはユーザーあたり月額3ドルを請求します。

Dashlaneは月額4.99ドルを請求します。

LastPassは月額3ドルを請求します。

誰かがBitwardenサーバー全体をRustで書き直し、0ドルでオープンソース化しました。それはすべてのデバイス上のすべての公式Bitwardenアプリと動作します。

それはVaultwardenと呼ばれます。

これが動作させるトリックです：

すべてのBitwardenクライアント、iOSアプリ、Androidアプリ、Chrome拡張、デスクトップアプリは、オープンAPIを通じてサーバーと通信します。BitwardenはそのAPIを公開しています。なぜなら彼らのコードがオープンソースだからです。

Vaultwardenは全く同じAPIを実装します。すべてのデバイス上のすべてのアプリの視点から、公式Bitwardenサーバーにアクセスすることと自分のVaultwardenインスタンスにアクセスすることの間に違いは一切ありません。

それを5ドルのVPS上で起動します。BitwardenアプリをサーバーURLにポイントします。すべてのパスワード、すべてのセキュアノート、すべての2FAコードが、あなたが所有するインフラストラクチャを通じてすべてのデバイス間で同期します。

→ 完全なAES-256エンドツーエンド暗号化。有料製品と同じ。

→ すべてのプレミアム機能がアンロック。ファイル添付、ボールトヘルスレポート、ハードウェア2FAキー。無料。

→ マルチユーザーサポートが組み込み。家族やチーム全体のために実行。

→ 256MB RAMで動作。5ドルのサーバーが数十人のユーザーを瞬きせずに処理。

→ 1つのDockerコマンド。ボールトが10分以内にライブ。

→ ゼロサブスクリプション。ゼロシート料金。ゼロ信頼必要。

商用パスワードマネージャーのビジネスモデルはシンプルです。オープンソースの暗号化を取る。同期サーバーでラップする。シートあたり永遠に請求する。

Vaultwardenは同期サーバーです。アプリは無料です。暗号化はオープンです。

あなたはそれを動かす場所が必要だっただけです。

59K stars. 100% Opensource

![Vaultwarden, an open-source alternative to Bitwarden, offers self-hosted deployment with various features, including personal vaults and API access.](https://pbs.twimg.com/media/HHLbZKdbsAA9ALG?format=png&name=large)