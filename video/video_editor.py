import os
from shared.config import VIDEO_OUTPUT_PATH
try:
    # 정상적인 경우, editor.py가 있으면 이 구문이 동작합니다.
    from moviepy.editor import ImageClip, AudioFileClip
except ImportError:
    # editor.py가 없을 때는 각 모듈에서 직접 import
    from moviepy.video.VideoClip import ImageClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip

# 영상 생성 (썸네일 + 오디오)
def create_video_from_content(text, audio_path, thumbnail_path, filename_prefix="video"):  
    os.makedirs(VIDEO_OUTPUT_PATH, exist_ok=True)
    audio = AudioFileClip(audio_path)
    clip = ImageClip(thumbnail_path, duration=audio.duration)
    clip.audio = audio
    video_path = os.path.join(VIDEO_OUTPUT_PATH, f"{filename_prefix}.mp4")
    clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
    return video_path