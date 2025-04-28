# video/video_editor.py

import os
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from moviepy.config import change_settings

# 1. bin/ffmpeg 경로를 moviepy에 등록
ffmpeg_path = os.path.join(os.getcwd(), 'bin', 'ffmpeg')
change_settings({"FFMPEG_BINARY": ffmpeg_path})

def create_video_from_content(image_urls, audio_path, keyword):
    clips = []
    duration_per_image = 2  # 각 이미지당 2초씩 보여주기

    for url in image_urls:
        img_clip = ImageClip(url).set_duration(duration_per_image).resize(height=1280).set_position("center")
        clips.append(img_clip)

    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    final_video = video.set_audio(audio)

    output_path = f"output/{keyword}_shorts.mp4"

    # 2. moviepy가 내부적으로 bin/ffmpeg를 사용해서 렌더링
    final_video.write_videofile(output_path, fps=24)

    return output_path
