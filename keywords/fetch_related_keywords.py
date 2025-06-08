from pytrends.request import TrendReq

def fetch_related_keywords(base_keywords=None):
    try:
        if not base_keywords:
            base_keywords = ["유튜브", "뉴스", "날씨"]

        pytrends = TrendReq(hl='ko', tz=540)
        pytrends.build_payload(kw_list=base_keywords)
        related = pytrends.related_queries()

        keywords = []
        for kw in base_keywords:
            top_df = related.get(kw, {}).get("top")
            if top_df is not None and not top_df.empty:
                keywords.extend(top_df["query"].tolist())

        keywords = list(dict.fromkeys(keywords))
        print(f"[keyword_fetcher] Google Related Queries 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Google Related Queries 실패: {e}")
        return []
