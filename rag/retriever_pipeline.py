# rag/retriever_pipeline.py

from rag.preprocess import clean_text
from rag.embedder import get_embedding
from rag.vector_store import VectorStore


def chunk_text(text, chunk_size=500, overlap=100):
    """
    Split text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks


def retrieve_from_text(query, documents, top_k=5):
    """
    RAG pipeline using raw scraped article text.

    Args:
        query (str): User claim
        documents (list[str]): List of full article texts
        top_k (int): Number of relevant chunks to return

    Returns:
        list[str]: Top-k relevant chunks
    """

    store = VectorStore()

    # Step 1: Chunk + clean + embed documents
    for doc in documents:
        chunks = chunk_text(doc)

        for chunk in chunks:
            cleaned = clean_text(chunk)

            if not cleaned.strip():
                continue

            emb = get_embedding(cleaned)
            store.add(cleaned, emb)

    # Step 2: Embed query
    query_embedding = get_embedding(query)

    # Step 3: Retrieve top-k similar chunks
    top_chunks = store.search(query_embedding, top_k=top_k)

    return top_chunks

