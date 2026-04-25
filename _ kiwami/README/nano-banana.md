# Nano Banana 2（Gemini / Imagen 画像生成API）

> **🔗 関連コンテンツ（ツール手順書）**
> - 📘 n8n手順: [[_ kiwami/README/n8n.md]]
> - ⚙️ n8n × サイボウズ × Chatwork セットアップ: [[_ kiwami/tools/n8n-cybozu-chatwork-setup.md]]

## 概要

Google AI の画像生成APIを使って、プロンプトから画像を生成するツール。  
Gemini 2.5 Flash Image と Imagen 4.0 シリーズに対応。

## APIキー

- **プロバイダ:** Google AI Studio
- **キー:** `AIzaSyA64lzpANG9ylDAPac60FJu444FQybLhzQ`
- **プラン:** 有料（請求先アカウント設定済み）
- **管理画面:** https://ai.dev/projects

## セットアップ

### 必要なパッケージ

```bash
pip3 install --break-system-packages google-genai
```

### インストール済み環境

- Python 3.13.5（`/usr/local/bin/python3`）
- google-genai 1.72.0

## 使い方

### 基本コマンド

```bash
python3 tools/generate-image.py "プロンプト"
```

### オプション

| オプション | 短縮 | 説明 |
|---|---|---|
| `--output <パス>` | `-o` | 出力ファイルパス（省略時: `generated_YYYYMMDD_HHMMSS.png`） |
| `--model <モデル>` | `-m` | 使用モデルの指定（省略時: `gemini`） |

### 使用例

```bash
# デフォルト（Gemini 2.5 Flash Image）で生成
python3 tools/generate-image.py "夕焼けの富士山、水彩画風"

# 出力先を指定
python3 tools/generate-image.py "ロゴデザイン、ミニマル" --output logo.png

# Imagen 4.0 で生成
python3 tools/generate-image.py "猫のイラスト" --model imagen

# Imagen 4.0 Ultra（高品質）で生成
python3 tools/generate-image.py "風景写真風の海" --model imagen-ultra

# Imagen 4.0 Fast（高速）で生成
python3 tools/generate-image.py "シンプルなアイコン" --model imagen-fast
```

## 対応モデル

| オプション値 | モデルID | 特徴 |
|---|---|---|
| `gemini`（デフォルト） | `gemini-2.5-flash-image` | テキスト+画像生成、汎用的 |
| `imagen` | `imagen-4.0-generate-001` | 画像生成特化、高品質 |
| `imagen-ultra` | `imagen-4.0-ultra-generate-001` | 最高品質、処理時間長め |
| `imagen-fast` | `imagen-4.0-fast-generate-001` | 高速生成、軽量用途向け |

## 料金体系

> 全モデル無料枠なし（有料プラン必須）  
> 料金参照: https://ai.google.dev/gemini-api/docs/pricing

### Gemini 2.5 Flash Image（デフォルトモデル）

| 解像度 | トークン数 | 1画像あたりの料金 |
|---|---|---|
| 512px | 747 | $0.045（約7円） |
| 1024x1024px | 1,120 | $0.067（約10円） |
| 2048x2048px | 1,680 | $0.101（約15円） |
| 4096x4096px | 2,520 | $0.151（約23円） |

- 入力: $0.50 / 100万トークン
- 出力（画像）: $60.00 / 100万トークン
- Batch利用時は出力が半額（$30.00 / 100万トークン）

### Imagen 4.0

| モデル | オプション値 | 1画像あたりの料金 |
|---|---|---|
| Imagen 4 Fast | `imagen-fast` | $0.02（約3円） |
| Imagen 4 Standard | `imagen` | $0.04（約6円） |
| Imagen 4 Ultra | `imagen-ultra` | $0.06（約9円） |

### コスト目安（月間利用例）

| 用途 | 枚数/月 | モデル | 月額目安 |
|---|---|---|---|
| SNS投稿用アイキャッチ | 30枚 | Gemini（1024px） | 約300円 |
| ブログ記事用画像 | 100枚 | Imagen Fast | 約300円 |
| 高品質バナー制作 | 50枚 | Imagen Ultra | 約450円 |

## スキル（generate-image）での使い方

Claude Codeのスキルとして登録済み。自然な日本語で指示するだけで画像を生成できる。

### 基本的な指示例

```
夕焼けの富士山の画像を生成して
```

```
ブログ用のアイキャッチ画像を作って。テーマは「AIと働き方改革」
```

```
猫のフラットデザインイラストを生成して、SNS/post/に保存して
```

### モデルを指定する場合

```
高品質でバナー画像を作って（Imagen Ultraで）
```

```
アイコンを5種類、速度優先で生成して
```

### スキルが自動で行う処理

1. 日本語の指示を画像生成に適した英語プロンプトに翻訳
2. 用途に応じたモデルを自動選択（指定も可能）
3. `tools/generate-image.py` を実行して画像を生成
4. 生成結果を表示し、必要に応じて再生成

### スキルのモデル自動選択ガイド

| ユーザーの指示 | 自動選択されるモデル |
|---|---|
| 特に指定なし / 写真風 / イラスト | Gemini 2.5 Flash Image |
| 「高品質で」「バナー用に」 | Imagen 4 Ultra |
| 「速度優先で」「大量に」 | Imagen 4 Fast |
| 「Imagenで」 | Imagen 4 Standard |

## ファイル構成

```
tools/
  generate-image.py                        # 画像生成ツール本体
.claude/skills/generate-image/SKILL.md     # スキル定義
```

## 注意事項

- Imagen系モデルは有料プラン必須（無料プランではクォータ0）
- 出力フォーマットはPNG（モデルによりJPEG/WebPの場合あり）
- プロンプトは日本語・英語どちらでも可
- 出力先ディレクトリが存在しない場合は自動作成される
