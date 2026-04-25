import urllib.parse
import json
import urllib.request
import sys

def synthesize_voice(text, speaker_id=11, output_path="audio.wav"):
    # 1. Create audio query
    query_url = f"http://127.0.0.1:50021/audio_query?text={urllib.parse.quote(text)}&speaker={speaker_id}"
    req = urllib.request.Request(query_url, method="POST")
    with urllib.request.urlopen(req) as res:
        audio_query = res.read()
    
    # 2. Add some post-processing to the query if needed (e.g. speed_scale)
    query_dict = json.loads(audio_query)
    query_dict['speedScale'] = 1.2 # slightly faster for short video
    audio_query = json.dumps(query_dict).encode('utf-8')
    
    # 3. Synthesize voice
    synth_url = f"http://127.0.0.1:50021/synthesis?speaker={speaker_id}"
    req = urllib.request.Request(synth_url, data=audio_query, headers={'Content-Type': 'application/json'}, method="POST")
    with urllib.request.urlopen(req) as res:
        audio_data = res.read()
        
    with open(output_path, "wb") as f:
        f.write(audio_data)

if __name__ == "__main__":
    text = """今日から使えるエーアイ時短術。
角がたたないメールの返信、考えるのめんどくさい。
そんなときは、このプロンプトをエーアイにコピペするだけ！

以下の内容で、取引先への丁寧な返信メールを作成して。
第一に、相手の提案は一部受け入れるが、予算の都合でB案で進めたい。
文脈は、相手からのメールをコピペ。

これだけで、3秒で完璧なビジネスメールが完成します。
考える時間をエーアイに外注して、さっさと帰りましょう！
もっと詳しく知りたい方は、ノートで深掘りした有料記事をご覧ください。"""
    synthesize_voice(text)
    print("Audio generated successfully.")
