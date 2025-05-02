from pytrends.request import TrendReq

# 트렌딩 키워드 가져오기
def fetch_trending_keywords(limit=5):
    pytrends = TrendReq(hl='ko', tz=540)
    # 지역 기반 인기 검색어 (South Korea)
    trending_df = pytrends.trending_searches(pn='south_korea')
    keywords = trending_df[0].tolist()[:limit]
    return keywords