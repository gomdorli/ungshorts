from pytrends.request import TrendReq

def fetch_related_keywords(base_keywords=None):
    try:
        if not base_keywords:
            base_keywords = ["유튜브", "뉴스", "날씨"]

        pytrends = TrendReq(hl='ko', tz=540)
        keywords = []

        for kw in base_keywords:
            print(f"[DEBUG] 관련 쿼리 요청 중: {kw}")
            pytrends.build_payload(kw_list=[kw])  # ✅ 단일 키워드만 사용
            related = pytrends.related_queries()
            top_df = related.get(kw, {}).get("top")
            print(f"[DEBUG] '{kw}' → top_df: {top_df}")

            if top_df is not None and not top_df.empty and "query" in top_df.columns:
                keywords.extend(top_df["query"].tolist())

        keywords = list(dict.fromkeys(keywords))
        print(f"[keyword_fetcher] Google Related Queries 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Google Related Queries 실패: {e}")
        return []
