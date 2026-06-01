import requests
from datetime import datetime

API_KEY = "db768e5fb622495a84e24c72776028c3"
URL = "https://newsapi.org/v2/everything"

page = 1
oldest_date = None
oldest_article = None

while True:
    params = {
        "q": "news",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 100,
        "page": page,
        "apiKey": API_KEY
    }

    response = requests.get(URL, params=params)
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        break

    for article in articles:
        published = article.get("publishedAt")
        if published:
            dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if oldest_date is None or dt < oldest_date:
                oldest_date = dt
                oldest_article = article

    print(f"Checked page {page}")
    page += 1

print("\n✅ OLDEST CURRENTLY AVAILABLE ARTICLE:")
print("Date:", oldest_date)
print("Title:", oldest_article["title"])
print("Source:", oldest_article["source"]["name"])
