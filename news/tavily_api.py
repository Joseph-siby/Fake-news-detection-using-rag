import requests

API_KEY = "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"
URL = "https://api.tavily.com/search"

def tavily_search(query: str):
    payload = {
        "api_key": API_KEY,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "max_results": 5
    }

    res = requests.post(URL, json=payload)
    res.raise_for_status()
    return res.json()


