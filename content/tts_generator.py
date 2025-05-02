import os
from gtts import gTTS
from shared.config import AUDIO_OUTPUT_PATH

# 텍스트를 음성으로 변환

def generate_tts_audio(text, filename_prefix="tts"):  
    os.makedirs(AUDIO_OUTPUT_PATH, exist_ok=True)
    tts = gTTS(text=text, lang='ko')
    audio_path = os.path.join(AUDIO_OUTPUT_PATH, f"{filename_prefix}.mp3")
    tts.save(audio_path)
    return audio_path