# news_searcher.py

import requests

API_KEY = "db768e5fb622495a84e24c72776028c3"
BASE_URL = "https://newsapi.org/v2/everything"

def search_news(query, limit=5):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("status") != "ok":
        raise Exception(data.get("message", "NewsAPI error"))

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "source": article.get("source", {}).get("name"),
            "url": article.get("url")
        })

    return articles
