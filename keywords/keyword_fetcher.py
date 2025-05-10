# keywords/keyword_fetcher.py

import requests
import xml.etree.ElementTree as ET
from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError

def fallback_trending_keywords(n=10):
    """
    Google Trends Daily RSS에서 직접 상위 n개 키워드를 파싱합니다.
    """
    rss_url = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=KR"
    resp = requests.get(rss_url, timeout=10)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    items = root.findall('.//item')
    return [item.find("title").text for item in items[:n]]

def fetch_trending_keywords(n=10):
    """
    PyTrends 를 사용해 South Korea 일일 트렌딩 검색어를 가져옵니다.
    실패 시 RSS 폴백으로 대체합니다.
    """
    try:
        pt = TrendReq(hl="ko", tz=540)
        # pn='KR' 로 geo=KR 엔드포인트 호출
        df = pt.trending_searches(pn="KR")
        keywords = df[0].tolist()[:n]
        print(f"[keyword_fetcher] primary fetch succeeded: {keywords}", flush=True)
        return keywords
    except Exception as e1:
        print(f"[keyword_fetcher] primary fetch failed: {e1}", flush=True)
        try:
            keywords = fallback_trending_keywords(n)
            print(f"[keyword_fetcher] RSS fallback succeeded: {keywords}", flush=True)
            return keywords
        except Exception as e2:
            print(f"[keyword_fetcher] fallback also failed: {e2}", flush=True)
            return []
