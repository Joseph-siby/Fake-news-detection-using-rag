def build_news_query(caption: str) -> str:
    caption = caption.lower()

    if "crowd" in caption or "people" in caption:
        context = "public gathering or protest"
    elif "fire" in caption or "smoke" in caption:
        context = "accident or disaster"
    elif "police" in caption:
        context = "law enforcement incident"
    elif "animal" in caption or "snake" in caption:
        context = "viral animal claim"
    else:
        context = "general event"

    return f"""
    Image description: {caption}
    Possible context: {context}

    Verify:
    - Is this real or fake?
    - Is this misleading?
    - Find related news reports.
    """