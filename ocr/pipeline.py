import numpy as np
from PIL import Image

from .preprocess import preprocess_image
from .extractor import extract_text
from .cleaner import clean_text
from vision.vision_extractor import extract_with_vision


def process_image(file) -> str:
    """
    Full OCR pipeline:
    Image → Preprocess → OCR → Clean → (Fallback Vision) → Output
    """

    try:
        # Step 1: Reset file pointer
        file.file.seek(0)

        # Step 2: Load image
        image = Image.open(file.file).convert("RGB")
        image_np = np.array(image)

        # Step 3: Preprocess
        processed_image = preprocess_image(image_np)

        # Step 4: OCR
        raw_text = extract_text(processed_image)
        print("RAW OCR TEXT:", raw_text)

        # Step 5: Clean
        cleaned_text = clean_text(raw_text)
        print("CLEANED OCR TEXT:", cleaned_text)

        # 🔥 STEP 6: SMART CHECK
        if not cleaned_text or len(cleaned_text) < 10:
            print("⚠️ OCR weak → switching to Vision AI")

            # VERY IMPORTANT → reset file again
            file.file.seek(0)

            vision_text = extract_with_vision(file)
            print("VISION OUTPUT:", vision_text)

            return vision_text

        # ✅ Normal case
        return cleaned_text

    except Exception as e:
        print("OCR PIPELINE ERROR:", str(e))

        # 🔥 FALLBACK EVEN ON ERROR
        try:
            file.file.seek(0)
            print("⚠️ OCR crashed → using Vision AI")

            vision_text = extract_with_vision(file)
            return vision_text

        except Exception as e2:
            print("VISION ALSO FAILED:", str(e2))
            return ""