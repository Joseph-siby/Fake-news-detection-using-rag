import re


def clean_text(text: str) -> str:
    """
    Clean and normalize OCR text.

    Steps:
    1. Lowercase
    2. Remove special characters
    3. Remove extra spaces
    4. Fix common OCR issues
    """

    if not text:
        return ""

    # Step 1: Lowercase
    text = text.lower()

    # Step 2: Replace common OCR mistakes
    text = text.replace("0", "o")
    text = text.replace("1", "l")
    text = text.replace("|", "l")

    # Step 3: Remove unwanted characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Step 4: Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text