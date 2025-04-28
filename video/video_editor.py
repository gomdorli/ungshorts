# video/video_editor.py

import os
import subprocess

def create_video_from_content(image_urls, audio_path, keyword):
    if not image_urls:
        raise ValueError("No images provided for video creation.")
    
    if not os.path.exists('output'):
        os.makedirs('output')
    
    image_path = download_image(image_urls[0], keyword)

    video_path = f"output/{keyword}_shorts.mp4"

    # ffmpeg 명령어로 이미지+오디오를 하나의 영상으로 합치기
    ffmpeg_binary = os.path.join(os.getcwd(), 'bin', 'ffmpeg')

    command = [
        ffmpeg_binary,
        "-loop", "1",
        "-i", image_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-tune", "stillimage",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        "-y",
        video_path
    ]

    subprocess.run(command, check=True)

    return video_path

def download_image(url, keyword):
    import requests

    img_data = requests.get(url).content
    image_path = f"output/{keyword}_thumbnail.jpg"
    with open(image_path, 'wb') as handler:
        handler.write(img_data)
    return image_path
