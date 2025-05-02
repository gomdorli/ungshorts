import os
from PIL import Image, ImageDraw, ImageFont
from shared.config import THUMBNAIL_OUTPUT_PATH

# 썸네일 생성

def create_thumbnail(text, filename_prefix="thumb"):  
    os.makedirs(THUMBNAIL_OUTPUT_PATH, exist_ok=True)
    img = Image.new('RGB', (1280, 720), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    draw.text((50, 300), text, font=font, fill=(0, 0, 0))
    path = os.path.join(THUMBNAIL_OUTPUT_PATH, f"{filename_prefix}.jpg")
    img.save(path)
    return path