import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_naver():
    try:
        url = "https://datalab.naver.com/keyword/realtimeList.naver"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)

        print(f"[DEBUG] NAVER 응답 코드: {res.status_code}")
        if res.status_code != 200:
            print(f"[keyword_fetcher] Naver 요청 실패: {res.status_code}")
            return []

        soup = BeautifulSoup(res.text, "html.parser")
        ranking_box = soup.select_one("div.ranking_box")
        print(f"[DEBUG] ranking_box 존재 여부: {ranking_box is not None}")
        if not ranking_box:
            print("[keyword_fetcher] Naver 페이지 구조 파싱 실패")
            return []

        item_titles = ranking_box.select(".item_title")
        print(f"[DEBUG] item_title 요소 수: {len(item_titles)}")

        keywords = [
            tag.get_text(strip=True)
            for tag in item_titles
            if tag.get_text(strip=True)
        ]

        print(f"[keyword_fetcher] Naver Trends 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Naver Trends 실패: {e}")
        return []
