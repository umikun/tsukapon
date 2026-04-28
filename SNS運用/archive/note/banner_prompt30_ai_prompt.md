# 「神プロンプト30選」バナー画像 生成AIプロンプト

> **🔗 関連コンテンツ（過去アーカイブ）**
> - 📂 現行note一覧: [[SNS運用/note/note-20260424|最新のnote]]
> - 📝 note運用戦略: [[SNS運用/noteの今後と収益化戦略]]
> - 🎨 サムネ仕様: [[note記事用サムネイルのデザインシステム仕様書]]

## 共通の注意点
- 日本語テキストはAI画像生成では崩れやすいので、**背景イラストのみ生成→Canva等でテキストを後載せ**が推奨
- アスペクト比は **16:9**（noteカバー画像向け）

---

## Midjourney用

### メインプロンプト

```
A modern minimalist office scene at sunset, view through a large window showing a beautiful orange-pink sunset over a city skyline. A wall clock showing exactly 5:00 PM. On the desk, neatly stacked PDF documents and a laptop. The atmosphere is warm, hopeful, and liberating — representing freedom from overtime work. Clean flat illustration style, soft gradients, muted warm tones with red accents. Corporate but friendly. Left side has open space for text overlay. --ar 16:9 --v 7 --s 200
```

### バリエーション（よりフラットなデザイン）

```
Flat vector illustration, split composition. Left side: clean white space for text. Right side: cozy office interior at golden hour, large window with sunset cityscape silhouette, analog clock showing 5PM, desk with organized documents marked PDF in red. Color palette: warm whites, soft oranges, deep navy, accent red #e63946. Minimal, editorial, Japanese design aesthetic. --ar 16:9 --v 7 --s 150
```

### バリエーション（概念的・インパクト重視）

```
Conceptual illustration: a person walking out of an office building at sunset, carrying a briefcase, looking relieved and happy. Behind them, a giant clock shows 5:00 PM. Scattered paper documents transform into birds flying away. Warm sunset colors, flat modern illustration style, clean lines, inspirational mood. Space on left for text overlay. --ar 16:9 --v 7 --s 200
```

---

## DALL-E (ChatGPT) 用

### メインプロンプト

```
Create a wide banner illustration (16:9 ratio) for a Japanese blog article cover. The scene shows a modern office at sunset through a large window. A wall clock displays exactly 5:00 PM. On the desk are neatly stacked documents with red "PDF" labels. The left 55% of the image should be lighter/simpler to allow text overlay. Style: clean flat illustration with soft gradients. Color scheme: warm whites and creams on the left, transitioning to deep navy and sunset oranges on the right. Red (#e63946) as an accent color. The mood should feel hopeful and liberating — the feeling of finally leaving work on time.
```

### バリエーション

```
Wide banner illustration (16:9). Split layout: left side is a clean off-white background with subtle geometric patterns, right side shows a stylized Japanese office scene at 5PM — a clock on the wall, sunset through the window with city buildings silhouetted, and a small stack of PDF documents on a tidy desk. Flat modern vector style, warm color palette with red accents. Professional but approachable. The left side must remain mostly empty for text placement.
```

---

## Stable Diffusion / ComfyUI 用

### プロンプト

```
(flat illustration:1.3), modern office interior, sunset view through large window, city skyline silhouette, wall clock showing 5 PM, organized desk with PDF documents, warm lighting, (orange sunset:1.2), clean minimal design, soft gradients, corporate illustration style, (text space on left:1.2), wide composition, professional, hopeful atmosphere
```

### ネガティブプロンプト

```
photorealistic, 3d render, dark, cluttered, messy, text, letters, words, watermark, signature, blurry, low quality, anime, manga style, people faces, hands
```

### 推奨設定
- 解像度: 1280x720 または 1920x1080
- CFG Scale: 7-8
- Steps: 30-40
- Sampler: DPM++ 2M Karras

---

## Canvaでのテキスト後載せガイド

AI生成した背景画像の上に、以下のテキストを配置する。

### レイヤー構成（上から順に）

**1. タグ（左上）**
- テキスト: 「PDF特典付｜完全保存版」
- フォント: Noto Sans JP Bold
- サイズ: 15px相当
- 背景: 赤（#e63946）角丸ボックス
- 文字色: 白

**2. メインタイトル（左中央）**
- 1行目: 「定時退社を叶える」
- 2行目: 「「神プロンプト 30選」」
- フォント: Noto Sans JP Black
- サイズ: 46px相当（「30」は58px、赤色）
- 文字色: ほぼ黒（#1a1a1a）、「神プロンプト」と「30」は赤（#e63946）

**3. サブコピー（メインの下）**
- 「残業月80時間からゼロへ。」← 黄色マーカー風ハイライト
- 「AIを"最強の時短ツール"に変える、」
- 「コピペOKなプロンプトの全て。」
- フォント: Noto Sans JP Bold
- サイズ: 18px相当
- 文字色: ダークグレー（#333）

**4. ボトムライン（左下）**
- 𝕏アイコン + 「で大反響」（黒丸バッジ内、白文字）
- 「30日間シリーズの集大成」（グレーテキスト）
