# rss_fetcher.py

import feedparser

def fetch_rss_feed(rss_url, limit=5):
    feed = feedparser.parse(rss_url)
    items = []

    for entry in feed.entries[:limit]:
        item = {
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "article_url": entry.get("link", ""),   # ✅ DIRECT ARTICLE URL
            "source": "The Hindu",
            "published": entry.get("published", "")
        }
        items.append(item)

    return items


# Test block
if __name__ == "__main__":
    RSS_URL = "https://www.thehindu.com/news/national/feeder/default.rss"

    items = fetch_rss_feed(RSS_URL, limit=1)

    print("\n--- RSS TEST OUTPUT ---")
    print("Title:", items[0]["title"])
    print("Article URL:", items[0]["article_url"])
    print("Source:", items[0]["source"])



