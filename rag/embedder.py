# retriever/embedder.py

import numpy as np

def get_embedding(text, dim=768):
    """
    Mock embedding function: returns a random vector for testing.

    Args:
        text (str): Input text
        dim (int): Dimension of embedding vector (default 768)

    Returns:
        np.array: Mock embedding vector
    """
    np.random.seed(hash(text) % (2**32))  # deterministic for same text
    return np.random.rand(dim)

# ==========================
# Example usage
# ==========================
if __name__ == "__main__":
    text = "NASA discovers water on the Moon"
    embedding = get_embedding(text)
    print("Embedding shape:", embedding.shape)
    print("First 5 values:", embedding[:5])
