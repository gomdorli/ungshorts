# keyword_fetcher.py

from pytrends.request import TrendReq
import requests
from bs4 import BeautifulSoup

def fetch_trending_keywords_from_google():
    try:
        pytrends = TrendReq(hl='ko', tz=540)  # 한국어, 서울시간
        df = pytrends.trending_searches(pn='south_korea')
        keywords = df[0].tolist()  # 첫 번째 컬럼에 키워드 리스트
        print("[keyword_fetcher] Google Trends 성공")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Google Trends 실패: {e}")
        return None

def fetch_trending_keywords_from_naver():
    try:
        url = "https://datalab.naver.com/keyword/realtimeList.naver"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        keywords = [span.get_text() for span in soup.select(".item_title")]
        print("[keyword_fetcher] Naver Trends 성공")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Naver Trends 실패: {e}")
        return None

def fetch_trending_keywords():
    keywords = fetch_trending_keywords_from_google()
    if not keywords:
        print("[keyword_fetcher] Google 실패 → Naver로 대체 시도")
        keywords = fetch_trending_keywords_from_naver()
    
    if not keywords:
        print("[keyword_fetcher] 모든 트렌드 키워드 수집 실패")
        return []
    return keywords


# 테스트용
if __name__ == "__main__":
    trending_keywords = fetch_trending_keywords()
    print("🔥 가져온 키워드:")
    for kw in trending_keywords:
        print("-", kw)
