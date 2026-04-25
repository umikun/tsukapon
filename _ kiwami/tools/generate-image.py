#!/usr/bin/env python3
"""
Gemini / Imagen 画像生成ツール (Nano Banana 2)

使い方:
  python3 tools/generate-image.py "プロンプト" [--output 出力先パス] [--model imagen]

例:
  python3 tools/generate-image.py "夕焼けの富士山、水彩画風"
  python3 tools/generate-image.py "ロゴデザイン、ミニマル" --output logo.png
  python3 tools/generate-image.py "猫のイラスト" --model imagen
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types

API_KEY = "AIzaSyA64lzpANG9ylDAPac60FJu444FQybLhzQ"

MODELS = {
    "gemini": "gemini-2.5-flash-image",
    "imagen": "imagen-4.0-generate-001",
    "imagen-ultra": "imagen-4.0-ultra-generate-001",
    "imagen-fast": "imagen-4.0-fast-generate-001",
}


def generate_with_gemini(client, prompt: str) -> tuple[bytes, str]:
    """Gemini 2.5 Flash Imageで画像生成"""
    response = client.models.generate_content(
        model=MODELS["gemini"],
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        ),
    )
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return part.inline_data.data, part.inline_data.mime_type
    raise RuntimeError("画像が生成されませんでした")


def generate_with_imagen(client, prompt: str, model_key: str = "imagen") -> tuple[bytes, str]:
    """Imagen 4.0で画像生成"""
    response = client.models.generate_images(
        model=MODELS[model_key],
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        ),
    )
    if response.generated_images:
        img = response.generated_images[0]
        return img.image.image_bytes, "image/png"
    raise RuntimeError("画像が生成されませんでした")


def save_image(image_data: bytes, mime_type: str, output_path: str | None) -> str:
    ext = ".png"
    if "jpeg" in mime_type or "jpg" in mime_type:
        ext = ".jpg"
    elif "webp" in mime_type:
        ext = ".webp"

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"generated_{timestamp}{ext}"

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image_data)
    print(f"画像を保存しました: {out}")
    return str(out)


def main():
    parser = argparse.ArgumentParser(description="Gemini/Imagen 画像生成ツール")
    parser.add_argument("prompt", help="画像生成プロンプト")
    parser.add_argument("--output", "-o", help="出力ファイルパス")
    parser.add_argument(
        "--model", "-m",
        choices=["gemini", "imagen", "imagen-ultra", "imagen-fast"],
        default="gemini",
        help="使用モデル (デフォルト: gemini)",
    )
    args = parser.parse_args()

    client = genai.Client(api_key=API_KEY)

    if args.model == "gemini":
        image_data, mime_type = generate_with_gemini(client, args.prompt)
    else:
        image_data, mime_type = generate_with_imagen(client, args.prompt, args.model)

    save_image(image_data, mime_type, args.output)


if __name__ == "__main__":
    main()
