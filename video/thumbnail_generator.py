# video/thumbnail_generator.py

from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(keyword):
    if not os.path.exists('output'):
        os.makedirs('output')
    base = Image.new('RGB', (720, 1280), color=(255, 255, 255))
    draw = ImageDraw.Draw(base)
    
    font = ImageFont.truetype("arial.ttf", 60)
    text = f"{keyword}"
    w, h = draw.textsize(text, font=font)
    draw.text(((720 - w) / 2, (1280 - h) / 2), text, fill="black", font=font)

    thumbnail_path = f"output/{keyword}_thumbnail.jpg"
    base.save(thumbnail_path)
    return thumbnail_path
