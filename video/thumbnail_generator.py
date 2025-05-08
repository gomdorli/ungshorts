import os
from PIL import Image, ImageDraw, ImageFont
from shared.config import THUMBNAIL_OUTPUT_PATH

def create_thumbnail(text, filename_prefix=None):
    # 1) THUMBNAIL_OUTPUT_PATH 기본값 보장
    base = THUMBNAIL_OUTPUT_PATH or os.path.join(os.getcwd(), "thumbnails")
    os.makedirs(base, exist_ok=True)

    # 2) 파일명에 한글 공백 섞이지 않게
    prefix = filename_prefix or text
    safe_prefix = "".join(c if c.isalnum() else "_" for c in prefix)

    path = os.path.join(base, f"{safe_prefix}.jpg")

    img = Image.new('RGB', (1280, 720), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    draw.text((50, 300), text, font=font, fill=(0, 0, 0))

    # 3) 절대 경로로 세이브 & 반환
    img.save(path)
    return os.path.abspath(path)
