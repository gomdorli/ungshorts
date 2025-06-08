from pytrends.request import TrendReq

def fetch_related_keywords(base_keywords=None):
    try:
        if not base_keywords:
            base_keywords = ["news", "weather", "tesla", "rivian"]

        pytrends = TrendReq(hl='en', tz=540)
        keywords = []

        for kw in base_keywords:
            print(f"[DEBUG] 관련 쿼리 요청 중: {kw}")
            pytrends.build_payload(kw_list=[kw])
            related = pytrends.related_queries()

            if not related or kw not in related or related[kw].get("top") is None:
                print(f"[keyword_fetcher] '{kw}' 관련 쿼리 없음 → 건너뜀")
                continue

            top_df = related[kw]["top"]
            if not top_df.empty and "query" in top_df.columns:
                keywords.extend(top_df["query"].tolist())

        keywords = list(dict.fromkeys(keywords))
        print(f"[keyword_fetcher] Google Related Queries 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Google Related Queries 실패: {e}")
        return []
