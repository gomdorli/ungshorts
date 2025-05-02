import os
import requests
from googletrans import Translator

# Pexels API 키 확인
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
if not PEXELS_API_KEY:
    raise RuntimeError("PEXELS_API_KEY 환경 변수가 설정되지 않았습니다!")

translator = Translator()

def scrape_content_for_keywords(keyword):
    # 1. 한글 키워드를 영어로 번역
    translated = translator.translate(keyword, src='ko', dest='en').text
    print(f"[content_scraper] Translated '{keyword}' to '{translated}'", flush=True)

    # 2. 번역된 키워드로 Pexels 검색
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": translated, "per_page": 3}
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)

    # 디버깅용 로그
    print(f"[content_scraper] Pexels status: {response.status_code}", flush=True)
    print(f"[content_scraper] Response body: {response.text[:200]}", flush=True)

    images = []
    data = response.json() if response.status_code == 200 else {}
    if response.status_code == 200:
        for photo in data.get('photos', []):
            images.append(photo['src']['original'])

    # 요약: 사진의 alt 텍스트를 사용하거나 기본 메시지 생성
    summary = data.get('photos', [{}])[0].get('alt', translated) if images \
              else f"{keyword} is trending now! Here's a quick overview."

    return {"images": images, "summary": summary}