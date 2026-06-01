def score_text_output(text: str) -> int:
    """
    Score OCR / Vision OCR output
    (based on amount of meaningful words)
    """
    if not text:
        return 0

    words = text.split()

    # basic score = number of words
    score = len(words)

    # penalty for weird characters
    weird_chars = sum(1 for c in text if not c.isalnum() and c not in " \n")
    if len(text) > 0:
        weird_ratio = weird_chars / len(text)
        if weird_ratio > 0.3:
            score -= 5

    # penalty if too short
    if len(words) < 2:
        score -= 5

    return max(score, 0)


def score_understanding_output(text: str) -> int:
    """
    Score general understanding output
    (we trust it more when it has enough keywords)
    """
    if not text:
        return 0

    words = text.split()

    score = 0

    # reward meaningful keyword count
    if len(words) >= 3:
        score += 20
    if len(words) >= 5:
        score += 20

    # bonus if looks clean (no weird chars)
    if all(w.isalpha() for w in words):
        score += 10

    return score


def is_weak_text(text: str) -> bool:
    """
    Decide if text is unusable
    """
    if not text:
        return True

    text = text.strip()

    # too short
    if len(text) < 10:
        return True

    words = text.split()

    # too few words
    if len(words) < 2:
        return True

    # too many weird characters
    weird_chars = sum(1 for c in text if not c.isalnum() and c not in " \n")
    if len(text) > 0:
        weird_ratio = weird_chars / len(text)
        if weird_ratio > 0.4:
            return True

    return False