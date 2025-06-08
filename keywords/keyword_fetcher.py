import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_zum():
    try:
        url = "http://zum.com"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        print(f"[DEBUG] ZUM 응답 코드: {res.status_code}")
        if res.status_code != 200:
            print(f"[keyword_fetcher] ZUM 요청 실패: {res.status_code}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select("div.ranking li a")
        print(f"[DEBUG] ZUM .ranking li a 요소 수: {len(items)}")

        keywords = [
            tag.get_text(strip=True)
            for tag in items
            if tag.get_text(strip=True)
        ]

        print(f"[keyword_fetcher] ZUM Trends 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] ZUM Trends 실패: {e}")
        return []
