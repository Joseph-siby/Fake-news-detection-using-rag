# rag/run_pipeline.py

from rag.retriever_pipeline import retrieve_from_text
from llm.llm_service import ask_llm
import requests
from bs4 import BeautifulSoup


def extract_text(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text(separator="\n")

    except Exception as e:
        print("❌ Failed to fetch:", e)
        return ""


def main():
    query = input("\n🔎 Enter a claim: ").strip()

    if not query:
        print("❌ Query cannot be empty")
        return

    urls_input = input("\n🔗 Enter article URLs separated by commas:\n").strip()

    urls = [u.strip() for u in urls_input.split(",") if u.strip()]

    if not urls:
        print("❌ No URLs provided")
        return

    documents = []

    print("\n📄 Fetching article content...\n")

    for url in urls:
        print("Fetching:", url)
        text = extract_text(url)
        if text:
            documents.append(text)

    if not documents:
        print("❌ No valid documents retrieved.")
        return

    print("\n🧠 Running RAG retrieval...\n")

    top_chunks = retrieve_from_text(query, documents, top_k=5)

    print("\n📌 Top Retrieved Evidence:\n")

    for i, chunk in enumerate(top_chunks, 1):
        print(f"\n--- Evidence {i} ---\n")
        print(chunk[:800])

    combined = "\n\n".join(top_chunks)

    prompt = f"""
Claim: {query}

Using ONLY the retrieved evidence below,
generate a structured explanation.

Evidence:
{combined}
"""

    print("\n🤖 Generating grounded explanation...\n")

    explanation = ask_llm(prompt)

    print("\n📝 Final Explanation:\n")
    print(explanation)


if __name__ == "__main__":
    main()
