import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_naver():
    try:
        url = "https://datalab.naver.com/keyword/realtimeList.naver"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        ranking_box = soup.select_one("div.ranking_box")
        if not ranking_box:
            print("[keyword_fetcher] Naver 페이지 구조 파싱 실패")
            return []

        keywords = [
            tag.get_text(strip=True)
            for tag in ranking_box.select(".item_title")
            if tag.get_text(strip=True)
        ]

        print(f"[keyword_fetcher] Naver Trends 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Naver Trends 실패: {e}")
        return []
