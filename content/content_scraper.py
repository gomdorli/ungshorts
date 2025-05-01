# content/content_scraper.py

import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_API_KEY:
    raise RuntimeError("PEXELS_API_KEY 환경 변수가 설정되지 않았습니다!")

def scrape_content_for_keywords(keyword):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": 3}
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)

    # 디버깅용 로그
    print(f"[content_scraper] Pexels status: {response.status_code}", flush=True)
    print(f"[content_scraper] Response body: {response.text[:200]}", flush=True)

    images = []
    if response.status_code == 200:
        data = response.json()
        for photo in data.get('photos', []):
            images.append(photo['src']['original'])

    summary = f"{keyword} is trending now! Here's a quick overview."
    return {"images": images, "summary": summary}
