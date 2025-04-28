# content/tts_generator.py

from gtts import gTTS
import os

def generate_tts_audio(text, keyword):
    if not os.path.exists('output'):
        os.makedirs('output')
    filename = f"output/{keyword}_audio.mp3"
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename
