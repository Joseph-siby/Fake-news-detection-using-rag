# retriever/vector_store.py

import numpy as np

class VectorStore:
    def __init__(self):
        """
        Initialize an empty vector store.
        """
        self.texts = []
        self.embeddings = []

    def add(self, text, embedding):
        """
        Add text and its embedding to the store.

        Args:
            text (str): The text snippet
            embedding (np.array): Corresponding embedding vector
        """
        self.texts.append(text)
        self.embeddings.append(embedding)

    def search(self, query_embedding, top_k=5):
        """
        Search for top-k most similar texts using cosine similarity.

        Args:
            query_embedding (np.array): Embedding of the query
            top_k (int): Number of top results to return

        Returns:
            list of str: Top-k most similar texts
        """
        if not self.embeddings:
            return []

        # Convert to NumPy array
        embeddings_matrix = np.array(self.embeddings)
        
        # Normalize embeddings
        embeddings_norm = embeddings_matrix / np.linalg.norm(embeddings_matrix, axis=1, keepdims=True)
        query_norm = query_embedding / np.linalg.norm(query_embedding)

        # Cosine similarity
        similarities = embeddings_norm @ query_norm
        top_indices = similarities.argsort()[::-1][:top_k]

        return [self.texts[i] for i in top_indices]

# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    from rag.embedder import get_embedding

    store = VectorStore()
    texts = ["Article about NASA", "Moon discovery news", "Mars exploration", "Water on the Moon", "SpaceX launch"]
    
    for t in texts:
        store.add(t, get_embedding(t))
    
    query = "NASA finds water on the Moon"
    query_emb = get_embedding(query)
    top_texts = store.search(query_emb, top_k=3)
    
    print("Top 3 relevant texts:")
    for t in top_texts:
        print("-", t)
