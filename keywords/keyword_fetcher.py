import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_daum():
    try:
        url = "https://media.daum.net/ranking/popular/"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        print(f"[DEBUG] DAUM 응답 코드: {res.status_code}")
        if res.status_code != 200:
            print(f"[keyword_fetcher] DAUM 요청 실패: {res.status_code}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")
        titles = soup.select("strong.tit_g")
        print(f"[DEBUG] DAUM 기사 제목 수: {len(titles)}")

        keywords = [
            tag.get_text(strip=True)
            for tag in titles
            if tag.get_text(strip=True)
        ]

        print(f"[keyword_fetcher] DAUM Trends 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] DAUM Trends 실패: {e}")
        return []
