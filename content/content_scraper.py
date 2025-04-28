# content/content_scraper.py

import requests
import os

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def scrape_content_for_keywords(keyword):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": 3}
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    
    images = []
    if response.status_code == 200:
        data = response.json()
        for photo in data['photos']:
            images.append(photo['src']['original'])

    summary = f"{keyword} is trending now! Here's a quick overview."
    return {"images": images, "summary": summary}
