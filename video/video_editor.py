import os
from shared.config import VIDEO_OUTPUT_PATH
from moviepy.editor import ImageClip, AudioFileClip

# 영상 생성 (썸네일 + 오디오)
def create_video_from_content(text, audio_path, thumbnail_path, filename_prefix="video"):  
    os.makedirs(VIDEO_OUTPUT_PATH, exist_ok=True)
    audio = AudioFileClip(audio_path)
    clip = ImageClip(thumbnail_path).set_duration(audio.duration)
    clip = clip.set_audio(audio)
    video_path = os.path.join(VIDEO_OUTPUT_PATH, f"{filename_prefix}.mp4")
    clip.write_videofile(video_path, fps=24, codec='libx264', audio_codec='aac')
    return video_path