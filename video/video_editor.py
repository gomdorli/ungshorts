# video/video_editor.py

from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os

def create_video_from_content(image_urls, audio_path, keyword):
    clips = []
    duration_per_image = 2

    for url in image_urls:
        img_clip = ImageClip(url).set_duration(duration_per_image).resize(height=1280).set_position("center")
        clips.append(img_clip)

    video = concatenate_videoclips(clips, method="compose")
    audio = AudioFileClip(audio_path)
    final_video = video.set_audio(audio)

    output_path = f"output/{keyword}_shorts.mp4"
    final_video.write_videofile(output_path, fps=24)
    return output_path
