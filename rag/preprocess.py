import re


def clean_text(text: str):
    """
    Basic text cleaning.
    Removes extra whitespace and normalizes spacing.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def estimate_tokens(text: str):
    """
    Rough token estimation.
    1 token ≈ 4 characters.
    """
    return len(text) // 4


def chunk_text_dynamic(text, max_tokens=800, overlap_tokens=150):
    """
    Dynamically chunk text based on token estimation.
    """

    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token

    chunks = []
    start = 0

    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk)
        start += max_chars - overlap_chars

    return chunks
