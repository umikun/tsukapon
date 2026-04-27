import urllib.parse
import json
import urllib.request
import os
import subprocess

sentences = [
    "【今日から使えるAI時短術 1/30】",
    "「角が立たないメールの返信、考えるの面倒…」",
    "そんな時はこのプロンプト（指示文）をAIにコピペするだけ",
    "以下の内容で、取引先への丁寧な返信メールを作成して。",
    "相手の提案は一部受け入れるが、予算の都合でB案で進めたい。",
    "文脈：相手からのメールをコピペ",
    "これだけで、3秒で完璧なビジネスメールが完成します",
    "「考える時間」をAIに外注して、さっさと帰りましょう！",
    "もっと詳しく知りたい方はこちら、",
    "【note】で深掘りした有料記事\nhttps://note.com/chackwill/n/nd015195d2717"
]

spoken_sentences = [
    "今日から使えるエーアイ時短術、さんじゅうぶんのいち。",
    "かどがたたないメールのへんしん、考えるのめんどくさい。",
    "そんなときは、このプロンプトをエーアイにコピペするだけ！",
    "いかの内容で、取引先への丁寧な返信メールを作成して。",
    "相手の提案は一部受け入れるが、予算の都合でB案で進めたい。",
    "文脈は、相手からのメールをコピペ。",
    "これだけで、3秒で完璧なビジネスメールが完成します。",
    "考える時間をエーアイに外注して、さっさと帰りましょう！",
    "もっと詳しく知りたい方はこちら、",
    "ノートで深掘りした有料記事をご覧ください。"
]

speaker_id = 11
speed_scale = 1.2
current_time = 0.0

srt_content = ""
files_to_concat = []

for i, (display_text, spoken_text) in enumerate(zip(sentences, spoken_sentences)):
    # 1. Create audio query
    query_url = f"http://127.0.0.1:50021/audio_query?text={urllib.parse.quote(spoken_text)}&speaker={speaker_id}"
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req) as res:
        audio_query = json.loads(res.read())
        
    audio_query['speedScale'] = speed_scale
    
    # Calculate duration
    duration = 0.0
    for phrase in audio_query['accent_phrases']:
        for mora in phrase['moras']:
            if mora['consonant_length'] is not None:
                duration += mora['consonant_length']
            if mora['vowel_length'] is not None:
                duration += mora['vowel_length']
        if phrase.get('pause_mora'):
            pause = phrase['pause_mora']
            if pause['consonant_length'] is not None:
                duration += pause['consonant_length']
            if pause['vowel_length'] is not None:
                duration += pause['vowel_length']
                
    duration += audio_query.get('prePhonemeLength', 0.1)
    duration += audio_query.get('postPhonemeLength', 0.1)
    duration /= speed_scale
    
    start_time = current_time
    end_time = current_time + duration
    
    def format_time(t):
        hours = int(t / 3600)
        minutes = int((t % 3600) / 60)
        seconds = int(t % 60)
        millis = int((t - int(t)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"
        
    # fonts.md に基づくフォント指定
    # 1行目（タイトル）は FONT_BOLD、それ以外は FONT_REGULAR を使用
    font_face = "A-OTF-ShinGoPro-Heavy" if i == 0 else "A-OTF-ShinGoPro-Medium"
    
    # note URL部分に英語フォントが含まれる場合などでフォントが混ざる場合は後で調整可能ですが、
    # 一旦全体に指定のフォントを適用します。
    display_text_with_font = f'<font face="{font_face}">{display_text}</font>'
    
    srt_content += f"{i+1}\n{format_time(start_time)} --> {format_time(end_time)}\n{display_text_with_font}\n\n"
    
    current_time = end_time
    
    # Synthesize
    synth_url = f"http://127.0.0.1:50021/synthesis?speaker={speaker_id}"
    req = urllib.request.Request(synth_url, data=json.dumps(audio_query).encode('utf-8'), headers={'Content-Type': 'application/json'}, method="POST")
    with urllib.request.urlopen(req) as res:
        with open(f"temp_audio_{i}.wav", "wb") as f:
            f.write(res.read())
            
    files_to_concat.append(f"file 'temp_audio_{i}.wav'")

with open("subtitles.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

with open("concat.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(files_to_concat))

# Concat audio files using ffmpeg
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", "audio_new.wav"])

# Cleanup temp audio files
for i in range(len(sentences)):
    if os.path.exists(f"temp_audio_{i}.wav"):
        os.remove(f"temp_audio_{i}.wav")
os.remove("concat.txt")

# Build final video using ffmpeg
font_dir = os.path.expanduser("~/Library/Fonts")
video_cmd = [
    "ffmpeg", "-y",
    "-stream_loop", "-1", "-i", "bg_video.mp4",
    "-i", "audio_new.wav",
    "-vf", f"subtitles=subtitles.srt:fontsdir={font_dir}",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-b:a", "192k",
    "-pix_fmt", "yuv420p",
    "-shortest",
    "short_movie_final.mp4"
]
subprocess.run(video_cmd)

print("Generated subtitles.srt, audio_new.wav, and short_movie_final.mp4")
