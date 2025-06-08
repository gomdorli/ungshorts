import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_naver():
    try:
        url = "https://datalab.naver.com/keyword/realtimeList.naver"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        ul = soup.select_one("div.ranking_box > ul")
        if not ul:
            print("[keyword_fetcher] Naver 페이지 구조 파싱 실패")
            return []

        keywords = [li.select_one(".title").get_text(strip=True)
                    for li in ul.select("li") if li.select_one(".title")]

        print(f"[keyword_fetcher] Naver Trends 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Naver Trends 실패: {e}")
        return []
