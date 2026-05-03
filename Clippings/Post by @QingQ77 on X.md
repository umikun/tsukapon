---
title: "Post by @QingQ77 on X"
source: "https://x.com/QingQ77/status/2050550873550717420"
author:
  - "[[@QingQ77]]"
published: 2026-05-02
created: 2026-05-03
description: "ターミナル一つで単機診断を完結。もう htop、iostat、nettop を山ほど開く必要なし。 https://github.com/matthart1983/syswatch… Rust で書かれたシステム診断 TUI。12個のタブページで CPU、メモリ、ディスク、G"
tags:
  - "clippings"
---
ターミナル一つで単機診断を完結。もう htop、iostat、nettop を山ほど開く必要なし。

https://github.com/matthart1983/syswatch…

Rust で書かれたシステム診断 TUI。12個のタブページで CPU、メモリ、ディスク、GPU、電源、サービス、ネットワークなどをカバー。macOS と Linux の両方で動作。Insights ページは異常（スワップの揺らぎ、ゾンビプロセス、ディスク満杯など）を自動検知して、わかりやすい言葉で問題を教えてくれる。Timeline ページではタイムラインをドラッグして、セッション全体の任意の時点の状態を振り返れる。読み取り専用で、プロセスを殺したり設定を変更したりしない。更新時の CPU 使用率は 0.5% 以下に抑えられている。