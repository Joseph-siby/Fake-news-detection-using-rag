# test_hindu_article.py

from test.rss_fetcher import fetch_rss_feed
from test.article_fetcher import fetch_article_text

HINDU_RSS_URL = "https://www.thehindu.com/news/national/feeder/default.rss"

# 1. Fetch one RSS item
item = fetch_rss_feed(HINDU_RSS_URL, limit=1)[0]

print("\n--- RSS ITEM ---")
print("Title:", item["title"])
print("Article URL:", item["article_url"])
print("Source:", item["source"])

# 2. Fetch full article text
article_text = fetch_article_text(item["article_url"])

print("\n--- ARTICLE TEXT (first 1200 chars) ---\n")
print(article_text[:1200])
