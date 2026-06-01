# retriever/google_retriever.py

import requests

# TODO: Replace with your own API key and Search Engine ID
API_KEY = "YOUR_GOOGLE_API_KEY"
SEARCH_ENGINE_ID = "YOUR_SEARCH_ENGINE_ID"

def fetch_articles(claim, num_results=5):
    """
    Fetch top articles from Google Custom Search API for a given claim/headline.

    Args:
        claim (str): The claim or headline to search for.
        num_results (int): Number of top results to fetch.

    Returns:
        list of dict: Each dict contains 'title', 'snippet', 'link'.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": claim,
        "num": num_results
    }

    response = requests.get(url, params=params)
    results = []

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        for item in items:
            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })
    else:
        print(f"Error fetching articles: {response.status_code}")
    
    return results

# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    claim = "NASA discovers water on the Moon"
    articles = fetch_articles(claim)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['title']}")
        print(f"   {article['snippet']}")
        print(f"   {article['link']}\n")
