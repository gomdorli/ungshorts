from pytrends.request import TrendReq

def fetch_related_keywords(base_keywords=["유튜브", "뉴스", "날씨"]):
    try:
        pytrends = TrendReq(hl='ko', tz=540)
        pytrends.build_payload(kw_list=base_keywords)
        related = pytrends.related_queries()

        keywords = []
        for kw in base_keywords:
            if related.get(kw) and related[kw].get("top") is not None:
                keywords.extend(related[kw]["top"]["query"].tolist())

        keywords = list(dict.fromkeys(keywords))  # 중복 제거
        print(f"[keyword_fetcher] Google Related Queries 성공 - {len(keywords)}개")
        return keywords
    except Exception as e:
        print(f"[keyword_fetcher] Google Related Queries 실패: {e}")
        return []
