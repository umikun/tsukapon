#!/usr/bin/env python3
"""
day11.md からナレーション＋BGM付きInstagramリール動画を生成
generate_reels.py の関数を再利用
"""

import os
import re
import subprocess
import sys
import tempfile
import json
import urllib.request
import urllib.parse

# 同ディレクトリの generate_reels.py から関数をインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_reels import (
    parse_article,
    create_title_slide,
    create_content_slide,
    create_cta_slide,
    strip_emojis,
    SRC_DIR,
    OUT_DIR,
)

DAY = 11
BG_COLOR = "#1a1a2e"
ACCENT_COLOR = "#ffa502"  # オレンジ（11日目用の新色）

# VOICEVOX 設定
VOICEVOX_URL = "http://localhost:50021"
VOICEVOX_SPEAKER = 11  # 玄野武宏（ノーマル）


def normalize_for_tts(text):
    """ナレーション用にテキストを整形
    - 絵文字除去
    - 「AI」→「エーアイ」
    - 記号除去
    """
    text = strip_emojis(text)
    text = re.sub(r"[「」『』【】]", "", text)
    # アスタリスク（強調記号）を削除
    text = text.replace("*", "")
    # AIを単独単語または英大文字境界でエーアイに置換
    # 「AI時短術」「AIに」「AIは」「ChatGPT」などに対応
    # 英大文字AIをエーアイに置換（前後がアルファベットでない場合）
    text = re.sub(r"(?<![A-Za-z])AI(?![A-Za-z])", "エーアイ", text)
    text = re.sub(r"\n+", "。", text)
    text = re.sub(r"。+", "。", text)
    return text.strip()


def generate_tts_audio(text, output_path):
    """VOICEVOX API でTTS音声を生成"""
    narration = normalize_for_tts(text)

    # 1. audio_query
    query_url = f"{VOICEVOX_URL}/audio_query?text={urllib.parse.quote(narration)}&speaker={VOICEVOX_SPEAKER}"
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req) as resp:
        query = json.loads(resp.read().decode("utf-8"))

    # 2. synthesis
    synth_url = f"{VOICEVOX_URL}/synthesis?speaker={VOICEVOX_SPEAKER}"
    req = urllib.request.Request(
        synth_url,
        data=json.dumps(query).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    raw_wav = output_path.replace(".wav", "_raw.wav")
    with urllib.request.urlopen(req) as resp:
        with open(raw_wav, "wb") as f:
            f.write(resp.read())

    # 44100Hz ステレオに統一
    subprocess.run(
        ["ffmpeg", "-y", "-i", raw_wav, "-ar", "44100", "-ac", "2", output_path],
        capture_output=True, check=True,
    )
    os.remove(raw_wav)
    return output_path


def get_audio_duration(path):
    """音声ファイルの長さを取得"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def generate_bgm(duration, output_path):
    """汎用的なBGMを生成（柔らかいシンセパッド風）
    sine波を複数重ねてフェードイン/アウトを付けた汎用BGM
    """
    # 3つの周波数（C4, E4, G4 = Cメジャーコード）を低音量で重ねる
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"sine=frequency=261.63:duration={duration}",
        "-f", "lavfi", "-i", f"sine=frequency=329.63:duration={duration}",
        "-f", "lavfi", "-i", f"sine=frequency=392.00:duration={duration}",
        "-filter_complex",
        f"[0]volume=0.08[a];[1]volume=0.06[b];[2]volume=0.05[c];"
        f"[a][b][c]amix=inputs=3:duration=longest,"
        f"afade=t=in:st=0:d=2,afade=t=out:st={duration-2}:d=2,"
        f"lowpass=f=800,aresample=44100",
        "-ac", "2",
        output_path,
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_path


def slides_to_video_with_audio(slides, narrations, output_path):
    """スライド画像 + ナレーション + BGM で動画を生成

    各スライドの長さ = ナレーション長 + 0.7秒の余白
    （min 3秒、max 8秒）
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        segment_files = []
        durations = []

        for i, (slide, narration_text) in enumerate(zip(slides, narrations)):
            slide_png = os.path.join(tmpdir, f"slide_{i:03d}.png")
            slide.save(slide_png)

            # TTS生成
            tts_wav = os.path.join(tmpdir, f"tts_{i:03d}.wav")
            generate_tts_audio(narration_text, tts_wav)
            tts_dur = get_audio_duration(tts_wav)

            # スライド長（ナレーション + 0.8秒余白、最低3秒、最大10秒）
            seg_dur = max(3.0, min(10.0, tts_dur + 0.8))
            durations.append(seg_dur)

            # ナレーション音声を seg_dur 秒に合わせて無音パディング
            padded_tts = os.path.join(tmpdir, f"tts_pad_{i:03d}.wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tts_wav,
                 "-af", f"adelay=200|200,apad=whole_dur={seg_dur}",
                 "-t", str(seg_dur),
                 padded_tts],
                capture_output=True, check=True,
            )

            # スライド動画 + ナレーション
            seg_path = os.path.join(tmpdir, f"seg_{i:03d}.mp4")
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1", "-i", slide_png,
                "-i", padded_tts,
                "-t", str(seg_dur),
                "-vf", f"fade=t=in:st=0:d=0.4,fade=t=out:st={seg_dur - 0.4}:d=0.4",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "128k",
                "-shortest",
                seg_path,
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            segment_files.append(seg_path)

        # セグメントを連結
        concat_file = os.path.join(tmpdir, "concat.txt")
        with open(concat_file, "w") as f:
            for seg in segment_files:
                f.write(f"file '{seg}'\n")

        merged_path = os.path.join(tmpdir, "merged.mp4")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
             "-c", "copy", merged_path],
            capture_output=True, check=True,
        )

        total_duration = sum(durations)

        # BGM生成
        bgm_path = os.path.join(tmpdir, "bgm.wav")
        generate_bgm(total_duration, bgm_path)

        # 動画 + BGM をミックス（ナレーションは100%、BGMは40%）
        cmd = [
            "ffmpeg", "-y",
            "-i", merged_path,
            "-i", bgm_path,
            "-filter_complex",
            "[0:a]volume=1.0[narration];"
            "[1:a]volume=0.35[bgm];"
            "[narration][bgm]amix=inputs=2:duration=first:dropout_transition=0[aout]",
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            output_path,
        ]
        subprocess.run(cmd, capture_output=True, check=True)


def main():
    filepath = os.path.join(SRC_DIR, f"day{DAY:02d}.md")
    title, paragraphs = parse_article(filepath)

    # マークダウン強調記号 ** や * をスライド本文からも除去
    title = title.replace("*", "")
    paragraphs = [p.replace("*", "") for p in paragraphs]

    slides = []
    narrations = []

    # タイトルスライド
    slides.append(create_title_slide(DAY, title, BG_COLOR, ACCENT_COLOR))
    narrations.append(f"今日から使えるAI時短術、デイ イレブン。{title}")

    # 本文スライド
    content_paragraphs = []
    for p in paragraphs:
        if len(p) > 150:
            sentences = re.split(r"(?<=[。！？\n])", p)
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

    total_slides = len(content_paragraphs) + 2
    for i, para in enumerate(content_paragraphs):
        slides.append(create_content_slide(para, BG_COLOR, ACCENT_COLOR, i + 1, total_slides))
        narrations.append(para)

    # CTAスライド
    slides.append(create_cta_slide(BG_COLOR, ACCENT_COLOR, DAY))
    narrations.append("役に立ったら保存とフォローお願いします")

    output_path = os.path.join(OUT_DIR, f"day{DAY:02d}_reel.mp4")
    print(f"Generating Day {DAY:02d} with narration + BGM...")
    print(f"  Slides: {len(slides)}")
    slides_to_video_with_audio(slides, narrations, output_path)

    # サムネ
    slides[0].save(os.path.join(OUT_DIR, f"day{DAY:02d}_thumbnail.png"))
    print(f"  -> {output_path}")
    print("Done!")


if __name__ == "__main__":
    main()
