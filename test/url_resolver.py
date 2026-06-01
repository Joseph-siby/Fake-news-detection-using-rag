# url_resolver.py

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RAGBot/1.0)"
}


def resolve_final_url(google_news_url, timeout=10):
    """
    Resolve Google News RSS article link to the original publisher URL
    using canonical link extraction.
    """
    response = requests.get(
        google_news_url,
        headers=HEADERS,
        timeout=timeout
    )

    soup = BeautifulSoup(response.text, "html.parser")

    canonical = soup.find("link", rel="canonical")

    if canonical and canonical.get("href"):
        return canonical["href"]

    # fallback: return original URL if not found
    return google_news_url


if __name__ == "__main__":
    test_url = (
        "https://news.google.com/rss/articles/"
        "CBMiWkFVX3lxTFB6M3NrTlNJTXdUVzk4d05hQWxQR0xfbHdUaF9hZENCdXQydkFl"
        "N3BWb283czFRalI2aHc2djZhakVxZEVxZnpfQ3lQRWxHMWl1cF9sN0hubzRIUdIB"
        "X0FVX3lxTFBOaWlJQThRUFp4d1RZc1pEclFiSjNtNVFSeXVoUFlmYWVsalBwY2Vn"
        "UGNKaWo1T0lYcVNwNE5MOG5YaEpyWDdINkpDeXZfQ2l0enFPMTZZQUU1R3NlOGVN"
        "?oc=5"
    )

    print(resolve_final_url(test_url))


