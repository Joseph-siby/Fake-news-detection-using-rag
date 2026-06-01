# news/explain_controller.py

import requests
from bs4 import BeautifulSoup

from rag.retriever_pipeline import retrieve_from_text
from llm.llm_service import ask_llm


def extract_text(url):
    """
    Scrape visible text from a news article.
    """
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        # remove scripts and styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator="\n")

    except Exception as e:
        print("Error scraping:", e)
        return ""


def explain_from_sources(query, sources):
    documents = []

    for source in sources[:3]:
        text = extract_text(source["url"])
        if text:
            documents.append(text)

    if not documents:
        return "No valid source content found."

    top_chunks = retrieve_from_text(query, documents, top_k=5)

    combined = "\n\n".join(top_chunks)

    prompt = f"""
Claim: {query}

Using ONLY the retrieved evidence below,
generate a structured explanation.

Evidence:
{combined}
"""

    return ask_llm(prompt)
