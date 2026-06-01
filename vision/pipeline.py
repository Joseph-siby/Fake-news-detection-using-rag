from vision.vision_extractor import extract_with_vision
from vision.understander import understand_image
from vision.scorer import (
    score_text_output,
    score_understanding_output,
    is_weak_text
)
from ocr.cleaner import clean_text


def process_with_vision(file, client):
    """
    Vision decision pipeline:
    - Runs Vision OCR
    - Runs Image Understanding
    - Scores both
    - Returns BEST result
    """

    print("\n========== VISION PIPELINE ==========\n")

    # Step 1: Vision OCR
    vision_text = extract_with_vision(file)
    vision_text = clean_text(vision_text)

    print("\n--- Vision OCR Output ---\n", vision_text)

    # Step 2: Understanding
    understanding_text = understand_image(file, client)
    understanding_text = clean_text(understanding_text)

    print("\n--- Understanding Output ---\n", understanding_text)

    # Step 3: Score both
    vision_score = score_text_output(vision_text)
    understanding_score = score_understanding_output(understanding_text)

    print("\n--- Scores ---")
    print("Vision OCR Score:", vision_score)
    print("Understanding Score:", understanding_score)

    # Step 4: Weak checks
    vision_weak = is_weak_text(vision_text)
    understanding_weak = is_weak_text(understanding_text)

    print("\n--- Weak Check ---")
    print("Vision Weak:", vision_weak)
    print("Understanding Weak:", understanding_weak)

    # Step 5: Decision logic (CORE 🔥)

    # Case 1: Both weak → return empty
    if vision_weak and understanding_weak:
        print("\n❌ Both outputs weak → returning empty")
        return ""

    # Case 2: Vision good, understanding weak
    if not vision_weak and understanding_weak:
        print("\n✅ Using Vision OCR")
        return vision_text

    # Case 3: Understanding good, vision weak
    if vision_weak and not understanding_weak:
        print("\n✅ Using Understanding")
        return understanding_text

    # Case 4: Both good → compare scores
    if understanding_score > vision_score:
        print("\n🔥 Using Understanding (higher score)")
        return understanding_text
    else:
        print("\n🔥 Using Vision OCR (higher score)")
        return vision_text