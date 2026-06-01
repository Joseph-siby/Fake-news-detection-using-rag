# article_fetcher.py

from newspaper import Article


def fetch_article_text(url, max_chars=3000):
    """
    Fetch ONE news article and return clean main text.
    The text is limited to avoid token overflow.
    """
    article = Article(url)

    article.download()
    article.parse()

    text = article.text.strip()

    # Safety: limit text size
    if len(text) > max_chars:
        text = text[:max_chars]

    return text


# Simple test
if __name__ == "__main__":
    test_url = "https://www.bbc.com/news/world-asia-india-12345678"  # replace with real URL
    article_text = fetch_article_text(test_url)

    print("\n--- ARTICLE TEXT ---\n")
    print(article_text)
