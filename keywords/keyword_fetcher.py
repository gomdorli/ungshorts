from pytrends.request import TrendReq
from pytrends.exceptions import ResponseError

# 트렌딩 키워드 가져오기
def fetch_trending_keywords(limit=5):
    pytrends = TrendReq()
    try:
        # south_korea가 동작하지 않으면 예외 발생
        df = pytrends.trending_searches(pn='south_korea')
    except ResponseError as e:
        print(f"[keyword_fetcher] south_korea fetch failed: {e}", flush=True)
        try:
            # fallback: 미국 트렌딩으로 시도
            df = pytrends.trending_searches(pn='united_states')
            print("[keyword_fetcher] Fallback to united_states", flush=True)
        except Exception as e2:
            print(f"[keyword_fetcher] Fallback also failed: {e2}", flush=True)
            return []  # 최악의 경우 빈 리스트 반환

    # 첫 5개 키워드만 리턴
    return df[0].tolist()[:5]