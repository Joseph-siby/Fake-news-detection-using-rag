import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")
URL = os.getenv("TAVILY_URL")


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


