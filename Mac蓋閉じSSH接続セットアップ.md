# Mac蓋閉じSSH接続セットアップ

> **🔗 関連コンテンツ**
> - ⚙️ 関連設定ファイル: [[_ kiwami/tools/daily-log/activity-config.json]]
> - 🛠 daily-log ツール群: [[_ kiwami/tools/daily-log/README]]

> [!info] 調査日
> 2026-05-02

## 課題

MacBook Pro（M3-Pro）の蓋を閉じると外部からの SSH 接続ができなくなる。

## 原因

macOS のデフォルトでは、蓋を閉じると **クラムシェルスリープ** に入り、システム全体が sleep する。`pmset -g` の `sleep 0` 設定（アイドルスリープ無効）は **アイドル sleep 専用** で、蓋閉じ sleep は別系統で制御されているため効かない。

## 解決策の選択肢

| 方法 | 概要 | 向き不向き |
|---|---|---|
| **A. `pmset disablesleep 1`** | 全ての sleep を完全無効化 | 一番素直。サーバー用途に最適 |
| **B. クラムシェルモード（公式）** | 外部ディスプレイ + 外部キーボード/マウス + AC で蓋閉じ稼働 | 外部ディスプレイがある人向け |
| **C. `caffeinate`** | バックグラウンドで起こしっぱなしにする | 一時的な作業向け |

## 採用した方法: A（`pmset disablesleep 1`）

### 実行コマンド

ターミナル（zsh）で実行:

```bash
sudo pmset -a disablesleep 1
```

### 動作確認の注意

`pmset -g` の出力に `DisableSleep` ラインが表示されない macOS の表示仕様（バグ気味）があるため、**plist を直接確認するのが確実**:

```bash
sudo defaults read /Library/Preferences/com.apple.PowerManagement.plist | grep SleepDisabled
```

`SleepDisabled = 1;` が `SystemPowerSettings` セクション内に出れば成功。

### 戻す

```bash
sudo pmset -a disablesleep 0
```

## 推奨運用（たまに外部から SSH する場合）

常時 ON は過剰。**外出前に ON / 帰宅後に OFF** に切り替える運用が良い。

### Step 1: パスワードなしで pmset を切り替え可能にする

```bash
sudo visudo -f /etc/sudoers.d/pmset-nopasswd
```

エディタが開いたら以下を貼り付け（`fukuokase` はユーザー名に合わせる）:

```
fukuokase ALL=(ALL) NOPASSWD: /usr/bin/pmset
```

保存して終了（vi なら `:wq`、nano なら `Ctrl+O` → Enter → `Ctrl+X`）。

`/usr/bin/pmset` 限定なので**他コマンドのパスワード要求は維持**される（最小権限）。

### Step 2: シェルエイリアスを登録

`~/.zshrc` の末尾に追加:

```bash
alias awake-on='sudo pmset -a disablesleep 1 && echo "✅ Sleep disabled (lid-close OK)"'
alias awake-off='sudo pmset -a disablesleep 0 && echo "💤 Sleep restored"'
```

反映:

```bash
source ~/.zshrc
```

### Step 3: 使い方

```bash
# 外出前
awake-on

# 帰宅後
awake-off
```

それぞれパスワード不要・1秒で切り替わる。

## バッテリーへの影響について

### 「最大容量 85%」は充電上限ではなく劣化指標

設定 > バッテリーで表示される「最大容量 85%」は **新品時に対するバッテリー劣化度** であって、充電の上限ではない。バッテリーは0〜100%まで普通に充電される（その100%が新品時の85%相当、というだけ）。

### 「バッテリー充電の最適化」ON のままで OK

リチウムイオンは **100%キープ状態が最も劣化を早める**。AC 常時接続でずっと100%に張り付くと半年で容量が大きく落ちる可能性がある。最適化ONなら使用パターンを学習して 80%前後で待機 → 使用直前に100%補充電してくれる。

### 蓋閉じ運用の物理的注意

- 通気を確保する（毛布の上などはNG。本体が熱を持つ）
- AC 接続必須（バッテリー駆動で `disablesleep 1` だと電池が一晩で消える）

## 副次発見: activity-tracker サイレント死

調査中、`/Users/fukuokase/bin/daily-log/activity-tracker.py` が **2026-05-01 07:49 から exit 1 を吐き続けてサイレントに死んでいた** ことが判明。

### 原因

`_ kiwami/tools/daily-log/activity-config.json` 内に JSON 標準では無効な `// "Day One",` というコメント行が混入していた。tracker は標準の `json.loads` でパースするためエラーで停止していた。

### 修正

- 該当のコメント行を削除
- 同時に `focus.apps` に `"Code"` `"Visual Studio Code"` を追加（VS Code を「集中時間」枠でカウントするため）
- 手動で tracker 実行 → 今日の `activity/2026-05-02.jsonl` への書き込み再開を確認

### 教訓

- launchd の `LastExitStatus` を定期的に監視する仕組みがあると早期発見できる
- JSON コメントが必要な設定ファイルは JSON5 等への切り替えを検討
- エラーログ `/tmp/activity-tracker-error.log` を Daily Log dashboard 等で可視化したい

## 参考

- `pmset` 設定永続化先: `/Library/Preferences/com.apple.PowerManagement.plist`
- `pmset -a` = all power sources（Battery / AC 両方に適用）
- `pmset -b` = Battery only / `pmset -c` = AC (Charger) only
- `disablesleep` の状態確認は `pmset -g` ではなく plist 直読みが信頼できる
