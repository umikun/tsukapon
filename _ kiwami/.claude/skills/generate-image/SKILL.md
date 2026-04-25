---
name: generate-image
description: Nano Banana 2 APIで画像を生成する。「画像を生成して」「〜の画像を作って」「イラストを生成」などの指示で起動。
---

# Generate Image（Nano Banana 2）

## Overview

Google AI の Gemini / Imagen API を使い、プロンプトから画像を生成する。

## Trigger条件

以下のいずれかに該当する場合、このスキルを適用する：
- 「画像を生成して」「画像を作って」「イラストを生成」などの指示
- SNS投稿やブログ用のアイキャッチ・バナー画像の作成依頼
- `/generate-image` コマンドの実行

## Workflow

### 1. プロンプトの確認

ユーザーの指示から以下を判断する：
- **何を生成するか**（内容・テーマ）
- **出力先**（指定がなければ自動命名）
- **モデル**（指定がなければ `gemini`（デフォルト））

### 2. モデル選択ガイド

| ユーザーの意図 | 推奨モデル | オプション値 |
|---|---|---|
| 通常の画像生成 / 写真風 / イラスト（デフォルト） | Gemini 2.5 Flash Image | `gemini` |
| Imagen指定時 | Imagen 4 Standard | `imagen` |
| 最高品質（バナー・広告） | Imagen 4 Ultra | `imagen-ultra` |
| 速度優先・大量生成 | Imagen 4 Fast | `imagen-fast` |

### 3. 画像生成の実行

以下のコマンドで画像を生成する：

```bash
python3 /Volumes/500GB/GoogleDrive/_kiwami/tools/generate-image.py "プロンプト" --output 出力先パス --model モデル
```

- プロンプトは英語の方が精度が高い。ユーザーが日本語で指示した場合、英語に翻訳してプロンプトに渡す
- `--output` 省略時は `/Volumes/500GB/GoogleDrive/_kiwami/_tmp/generated_YYYYMMDD_HHMMSS.png` に保存する
- SNS用途の場合は `SNS/` 配下の適切なディレクトリに保存する

### 4. 生成結果の確認

生成後、Read ツールで画像を表示してユーザーに確認する。  
修正が必要な場合はプロンプトを調整して再生成する。

## Operating Rules

- プロンプトが曖昧な場合は、生成前にユーザーに確認する
- 1回の指示で複数画像が必要な場合は、順番に生成する
- エラーが出た場合はモデルを変えて再試行する（例: gemini → imagen-fast）
- 料金目安: Gemini 1024px=約10円/枚、Imagen Fast=約3円/枚
