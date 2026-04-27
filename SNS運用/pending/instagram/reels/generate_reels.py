#!/usr/bin/env python3
"""
Threads記事(day01-day10)からInstagramリール用縦型ショート動画を生成するスクリプト
"""

import os
import re
import subprocess
import tempfile
import textwrap
from PIL import Image, ImageDraw, ImageFont

# 絵文字をテキスト記号に置換するマッピング
EMOJI_REPLACEMENTS = {
    "👇": " ▼",
    "💻": "",
    "✨": " *",
    "📩": "",
    "🏃‍♂️💨": "",
    "🏃‍♂️": "",
    "💨": "",
    "🤫": "",
    "😇": "",
    "📚": "",
    "🧠": "",
    "💡": " ★",
    "☕️": "",
    "☕": "",
    "🥲": "",
    "😉": "",
    "📋": "■",
    "1️⃣": "①",
    "2️⃣": "②",
    "3️⃣": "③",
    "4️⃣": "④",
    "5️⃣": "⑤",
}


def strip_emojis(text):
    """絵文字を置換・除去する"""
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        text = text.replace(emoji, replacement)
    # 残りの絵文字を正規表現で除去
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U0000FE00-\U0000FE0F"  # variation selectors
        "\U0000200D"             # zero width joiner
        "\U00002600-\U000026FF"  # misc symbols
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U0001FA00-\U0001FA6F"  # chess symbols
        "\U0001FA70-\U0001FAFF"  # symbols extended-A
        "\U00002702-\U000027B0"  # dingbats
        "\U0000FE0F"             # variation selector-16
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    # 連続スペースの整理
    text = re.sub(r"  +", " ", text)
    return text.strip()

# 設定
WIDTH, HEIGHT = 1080, 1920
BG_COLORS = [
    "#1a1a2e",  # ダークネイビー
    "#16213e",  # ディープブルー
    "#0f3460",  # ミッドナイトブルー
    "#1b1b2f",  # ダークパープル
    "#162447",  # ネイビー
    "#1a1a2e",
    "#0d1b2a",  # ダークティール
    "#1b262c",  # チャコール
    "#0b0c10",  # ほぼ黒
    "#1a1a2e",
]
ACCENT_COLORS = [
    "#e94560",  # レッド
    "#00d2ff",  # シアン
    "#ffd700",  # ゴールド
    "#ff6b6b",  # コーラル
    "#48dbfb",  # ライトブルー
    "#ff9ff3",  # ピンク
    "#54a0ff",  # ブルー
    "#5f27cd",  # パープル
    "#01a3a4",  # ティール
    "#f368e0",  # マゼンタ
]

FONT_DIR = os.path.expanduser("~/Library/Fonts")
FONT_BOLD = f"{FONT_DIR}/A-OTF-ShinGoPro-Heavy.otf"       # 新ゴ Heavy（日本語タイトル太）
FONT_MEDIUM = f"{FONT_DIR}/A-OTF-ShinGoPro-Bold.otf"      # 新ゴ Bold（日本語タイトル中）
FONT_REGULAR = f"{FONT_DIR}/A-OTF-ShinGoPro-Medium.otf"   # 新ゴ Medium（日本語本文）
FONT_EN_BOLD = f"{FONT_DIR}/Futura-ExtBol.otf"            # Futura Extra Bold（英語大見出し）
FONT_EN_HANDLE = f"{FONT_DIR}/D-DIN-Bold.otf"             # D-DIN Bold（ハンドル名）

AVATAR_PATH = "/Volumes/500GB/GoogleDrive/_kiwami/my-clone/avatar.jpg"

SRC_DIR = "/Volumes/500GB/GoogleDrive/_kiwami/SNS/threads/_fin"
OUT_DIR = "/Volumes/500GB/GoogleDrive/_kiwami/SNS/instagram/reels"


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def create_circular_avatar(size, border_color=None, border_width=4):
    """アバター画像を丸く切り抜いて返す"""
    avatar = Image.open(AVATAR_PATH).convert("RGBA")
    # 正方形にクロップ（中央）
    w, h = avatar.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    avatar = avatar.crop((left, top, left + s, top + s))
    avatar = avatar.resize((size, size), Image.LANCZOS)

    # 丸マスク作成
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)

    # 透明背景に丸く貼り付け
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(avatar, (0, 0), mask)

    # ボーダー描画
    if border_color:
        border_draw = ImageDraw.Draw(result)
        border_draw.ellipse(
            [border_width // 2, border_width // 2,
             size - border_width // 2, size - border_width // 2],
            outline=border_color, width=border_width
        )

    return result


def paste_avatar(img, avatar, x, y):
    """RGBA画像をRGB画像に合成"""
    img.paste(avatar, (x, y), avatar)


def parse_article(filepath):
    """記事を解析してタイトル、本文段落に分割"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.strip().split("\n")
    title = ""
    body_lines = []

    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("#") and not line.startswith("# "):
            # ハッシュタグ行はスキップ
            if not line.startswith("##"):
                continue
        else:
            body_lines.append(line)

    # 本文を段落に分割（空行で区切る）
    paragraphs = []
    current = []
    for line in body_lines:
        if line.strip() == "" or line.strip() == "---":
            if current:
                text = "\n".join(current).strip()
                if text:
                    paragraphs.append(text)
                current = []
        else:
            # ハッシュタグ行を除外
            if line.strip().startswith("#") and " " not in line.strip()[:5]:
                continue
            current.append(line)
    if current:
        text = "\n".join(current).strip()
        if text:
            paragraphs.append(text)

    # ハッシュタグ行を最後の段落から除外
    cleaned = []
    for p in paragraphs:
        # ハッシュタグのみの行を除外
        p_lines = p.split("\n")
        non_hashtag = [l for l in p_lines if not re.match(r'^#\S', l)]
        text = "\n".join(non_hashtag).strip()
        if text:
            cleaned.append(text)

    title = strip_emojis(title)
    cleaned = [strip_emojis(p) for p in cleaned]
    # strip_emojis後に空になった段落を除去
    cleaned = [p for p in cleaned if p.strip()]

    return title, cleaned


def wrap_text(text, font, max_width, draw):
    """テキストを指定幅で折り返す"""
    lines = []
    for paragraph_line in text.split("\n"):
        if not paragraph_line.strip():
            lines.append("")
            continue

        current_line = ""
        for char in paragraph_line:
            test_line = current_line + char
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] > max_width:
                if current_line:
                    lines.append(current_line)
                current_line = char
            else:
                current_line = test_line
        if current_line:
            lines.append(current_line)
    return lines


def create_title_slide(day_num, title, bg_color, accent_color):
    """タイトルスライドを作成（全要素を画面中央に集約）"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(img)

    ac = hex_to_rgb(accent_color)
    center_y = HEIGHT // 2

    # 上下アクセントライン
    draw.rectangle([0, 0, WIDTH, 8], fill=ac)
    draw.rectangle([0, HEIGHT - 8, WIDTH, HEIGHT], fill=ac)

    # アバター（中央から上に配置）
    avatar_size = 160
    avatar = create_circular_avatar(avatar_size, border_color=ac, border_width=6)
    avatar_y = center_y - 370
    paste_avatar(img, avatar, (WIDTH - avatar_size) // 2, avatar_y)

    # アカウント名
    font_account = ImageFont.truetype(FONT_EN_HANDLE, 38)
    acct = "@chackwill"
    bbox = draw.textbbox((0, 0), acct, font=font_account)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, avatar_y + avatar_size + 20), acct, fill="#cccccc", font=font_account)

    # シリーズ名
    font_series = ImageFont.truetype(FONT_REGULAR, 44)
    series_text = "今日から使えるAI時短術"
    bbox = draw.textbbox((0, 0), series_text, font=font_series)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, center_y - 150), series_text, fill=ac, font=font_series)

    # Day番号（Futura Extra Bold で大きく中央）
    font_day = ImageFont.truetype(FONT_EN_BOLD, 220)
    day_text = f"DAY {day_num:02d}"
    bbox = draw.textbbox((0, 0), day_text, font=font_day)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, center_y - 80), day_text, fill="#ffffff", font=font_day)

    # アクセントライン
    line_y = center_y + 170
    draw.rectangle([(WIDTH - 140) // 2, line_y, (WIDTH + 140) // 2, line_y + 6], fill=ac)

    # タイトル（新ゴ Heavy）
    font_title = ImageFont.truetype(FONT_BOLD, 62)
    title_lines = wrap_text(title, font_title, WIDTH - 160, draw)
    y = center_y + 220
    for line in title_lines:
        bbox = draw.textbbox((0, 0), line, font=font_title)
        draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, y), line, fill="#ffffff", font=font_title)
        y += 85

    return img


def create_content_slide(text, bg_color, accent_color, slide_num, total_slides):
    """本文スライドを作成 - アバター付きカード風（吹き出し三角なし）"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(img)

    ac = hex_to_rgb(accent_color)
    ac_hex = "#{:02x}{:02x}{:02x}".format(*ac) if isinstance(ac, tuple) else ac
    center_y = HEIGHT // 2

    # 上下アクセントライン
    draw.rectangle([0, 0, WIDTH, 6], fill=ac)
    draw.rectangle([0, HEIGHT - 6, WIDTH, HEIGHT], fill=ac)

    # 上部：アバター + アカウント名（中央揃え横並び）
    avatar_size = 70
    avatar = create_circular_avatar(avatar_size, border_color=ac, border_width=3)

    font_name = ImageFont.truetype(FONT_MEDIUM, 30)
    font_handle = ImageFont.truetype(FONT_EN_HANDLE, 24)
    name_text = "AI時短の人"
    handle_text = "@chackwill"
    name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    handle_bbox = draw.textbbox((0, 0), handle_text, font=font_handle)
    name_w = name_bbox[2] - name_bbox[0]
    total_header_w = avatar_size + 16 + max(name_w, handle_bbox[2] - handle_bbox[0])
    header_x = (WIDTH - total_header_w) // 2
    header_y = 60
    paste_avatar(img, avatar, header_x, header_y)
    draw.text((header_x + avatar_size + 16, header_y + 8), name_text, fill="#ffffff", font=font_name)
    draw.text((header_x + avatar_size + 16, header_y + 44), handle_text, fill="#888888", font=font_handle)

    # テキスト描画（カード風）
    is_prompt = text.strip().startswith("以下") or text.strip().startswith("「") or text.strip().startswith("あなたは【")

    card_margin = 50
    card_left = card_margin
    card_right = WIDTH - card_margin

    if is_prompt or ("コピペ" in text and len(text) < 200):
        # プロンプト/コード風カード
        font_text = ImageFont.truetype(FONT_REGULAR, 40)
        text_lines = wrap_text(text, font_text, card_right - card_left - 80, draw)
        card_height = len(text_lines) * 60 + 120
        card_top = center_y - card_height // 2
        card_bottom = center_y + card_height // 2

        # カード背景（角丸、アクセントの左ボーダー付き）
        draw.rounded_rectangle(
            [card_left, card_top, card_right, card_bottom],
            radius=24, fill="#0d1117", outline=ac, width=2
        )
        # 左側にアクセントバー
        draw.rounded_rectangle(
            [card_left, card_top, card_left + 6, card_bottom],
            radius=3, fill=ac
        )

        # プロンプトラベル
        font_label = ImageFont.truetype(FONT_MEDIUM, 28)
        draw.text((card_left + 40, card_top + 30), "PROMPT", fill=ac, font=font_label)

        y = card_top + 80
        for line in text_lines:
            draw.text((card_left + 40, y), line, fill="#e6e6e6", font=font_text)
            y += 60
    else:
        # 通常テキスト（カード風）
        font_text = ImageFont.truetype(FONT_REGULAR, 44)
        text_lines = wrap_text(text, font_text, card_right - card_left - 80, draw)

        card_height = len(text_lines) * 68 + 60
        card_top = center_y - card_height // 2
        card_bottom = center_y + card_height // 2

        # カード背景
        bg_rgb = hex_to_rgb(bg_color)
        card_bg = tuple(min(255, c + 20) for c in bg_rgb)
        draw.rounded_rectangle(
            [card_left, card_top, card_right, card_bottom],
            radius=24, fill=card_bg, outline=(*ac, 80), width=2
        )
        # 左側にアクセントバー
        draw.rounded_rectangle(
            [card_left, card_top, card_left + 6, card_bottom],
            radius=3, fill=ac
        )

        y = card_top + 30
        for line in text_lines:
            color = "#ffffff"
            if re.match(r'^[①②③④⑤⑥⑦⑧⑨⑩1-9]', line.strip()):
                color = ac_hex
            draw.text((card_left + 40, y), line, fill=color, font=font_text)
            y += 68

    # ページインジケーター（下部中央）
    indicator_y = HEIGHT - 80
    dot_spacing = 30
    total_width = (total_slides - 1) * dot_spacing
    start_x = (WIDTH - total_width) // 2
    for i in range(total_slides):
        x = start_x + i * dot_spacing
        if i == slide_num:
            draw.ellipse([x - 8, indicator_y - 8, x + 8, indicator_y + 8], fill=ac)
        else:
            draw.ellipse([x - 5, indicator_y - 5, x + 5, indicator_y + 5], fill="#444444")

    return img


def create_cta_slide(bg_color, accent_color, day_num):
    """CTA（コールトゥアクション）スライドを作成（全要素を画面中央に集約）"""
    img = Image.new("RGB", (WIDTH, HEIGHT), hex_to_rgb(bg_color))
    draw = ImageDraw.Draw(img)

    ac = hex_to_rgb(accent_color)
    center_y = HEIGHT // 2

    # 上下アクセントライン
    draw.rectangle([0, 0, WIDTH, 8], fill=ac)
    draw.rectangle([0, HEIGHT - 8, WIDTH, HEIGHT], fill=ac)

    # アバター（中央基準で配置）
    avatar_size = 220
    avatar = create_circular_avatar(avatar_size, border_color=ac, border_width=6)
    avatar_y = center_y - 280
    paste_avatar(img, avatar, (WIDTH - avatar_size) // 2, avatar_y)

    # アカウント名（D-DIN Bold）
    font_account = ImageFont.truetype(FONT_EN_HANDLE, 48)
    acct = "@chackwill"
    bbox = draw.textbbox((0, 0), acct, font=font_account)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, avatar_y + avatar_size + 30), acct, fill="#ffffff", font=font_account)

    # サブメッセージ
    font_sub = ImageFont.truetype(FONT_REGULAR, 38)
    sub = "毎日AI時短術を発信中"
    bbox = draw.textbbox((0, 0), sub, font=font_sub)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, center_y + 50), sub, fill="#aaaaaa", font=font_sub)

    # メインメッセージ（新ゴ Heavy）
    font_main = ImageFont.truetype(FONT_BOLD, 62)
    msg1 = "役に立ったら"
    msg2 = "保存 & フォロー！"

    bbox1 = draw.textbbox((0, 0), msg1, font=font_main)
    bbox2 = draw.textbbox((0, 0), msg2, font=font_main)

    draw.text(((WIDTH - (bbox1[2] - bbox1[0])) // 2, center_y + 140), msg1, fill="#ffffff", font=font_main)
    draw.text(((WIDTH - (bbox2[2] - bbox2[0])) // 2, center_y + 230), msg2, fill=ac, font=font_main)

    return img


def slides_to_video(slides, output_path, duration_per_slide=4):
    """スライド画像リストから動画を生成"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # スライド画像を保存
        for i, slide in enumerate(slides):
            slide.save(os.path.join(tmpdir, f"slide_{i:03d}.png"))

        # concat用のファイルリスト作成
        concat_file = os.path.join(tmpdir, "concat.txt")
        with open(concat_file, "w") as f:
            for i in range(len(slides)):
                f.write(f"file 'slide_{i:03d}.png'\n")
                f.write(f"duration {duration_per_slide}\n")
            # 最後のスライドを繰り返し（ffmpegの仕様）
            f.write(f"file 'slide_{len(slides)-1:03d}.png'\n")

        # ffmpegで動画生成（フェードトランジション付き）
        # まず各スライドを個別動画にしてからconcatする
        segment_files = []
        for i in range(len(slides)):
            seg_path = os.path.join(tmpdir, f"seg_{i:03d}.mp4")
            segment_files.append(seg_path)

            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", os.path.join(tmpdir, f"slide_{i:03d}.png"),
                "-t", str(duration_per_slide),
                "-vf", f"fade=t=in:st=0:d=0.5,fade=t=out:st={duration_per_slide - 0.5}:d=0.5",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                seg_path
            ]
            subprocess.run(cmd, capture_output=True, check=True)

        # セグメントを結合
        seg_list = os.path.join(tmpdir, "segments.txt")
        with open(seg_list, "w") as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", seg_list,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            output_path
        ]
        subprocess.run(cmd, capture_output=True, check=True)


def main():
    for day in range(1, 11):
        print(f"Generating Day {day:02d}...")
        filepath = os.path.join(SRC_DIR, f"day{day:02d}.md")
        title, paragraphs = parse_article(filepath)

        bg = BG_COLORS[day - 1]
        accent = ACCENT_COLORS[day - 1]

        slides = []

        # タイトルスライド
        slides.append(create_title_slide(day, title, bg, accent))

        # 本文スライド（段落ごと）
        # 長すぎる段落は分割
        content_paragraphs = []
        for p in paragraphs:
            if len(p) > 150:
                # 長い段落は文で分割
                sentences = re.split(r'(?<=[。！？\n])', p)
                chunk = ""
                for s in sentences:
                    if len(chunk + s) > 150 and chunk:
                        content_paragraphs.append(chunk.strip())
                        chunk = s
                    else:
                        chunk += s
                if chunk.strip():
                    content_paragraphs.append(chunk.strip())
            else:
                content_paragraphs.append(p)

        total_slides = len(content_paragraphs) + 2  # title + content + CTA
        for i, para in enumerate(content_paragraphs):
            slides.append(create_content_slide(para, bg, accent, i + 1, total_slides))

        # CTAスライド
        slides.append(create_cta_slide(bg, accent, day))

        # 動画生成
        output_path = os.path.join(OUT_DIR, f"day{day:02d}_reel.mp4")

        # スライドの表示時間（タイトル3秒、本文4秒、CTA3秒）
        # 合計が15-30秒になるよう調整
        total_content = len(content_paragraphs)
        if total_content + 2 > 8:
            content_dur = 3  # 多いスライドは短く
        else:
            content_dur = 4

        slides_to_video(slides, output_path, duration_per_slide=content_dur)

        # プレビュー画像も保存
        slides[0].save(os.path.join(OUT_DIR, f"day{day:02d}_thumbnail.png"))

        print(f"  -> {output_path} ({len(slides)} slides)")

    print("\nDone! All reels generated.")


if __name__ == "__main__":
    main()
