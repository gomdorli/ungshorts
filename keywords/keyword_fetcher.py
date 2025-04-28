# keywords/keyword_fetcher.py

from pytrends.request import TrendReq

def fetch_trending_keywords(limit=5):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["news"])
    trending_searches = pytrends.trending_searches(pn='united_states')
    keywords = trending_searches.head(limit).tolist()
    return keywords
