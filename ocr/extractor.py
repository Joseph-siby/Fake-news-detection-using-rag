import easyocr
import numpy as np
import cv2
import pytesseract

reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_np: np.ndarray) -> str:
    texts = []

    # ---------- PASS 1 (normal) ----------
    result1 = reader.readtext(image_np, paragraph=True)
    texts += [r[1] for r in result1 if r[2] > 0.4]

    # ---------- PASS 2 (high contrast) ----------
    high_contrast = cv2.convertScaleAbs(image_np, alpha=2, beta=0)
    result2 = reader.readtext(high_contrast, paragraph=True)
    texts += [r[1] for r in result2 if r[2] > 0.3]

    # ---------- PASS 3 (threshold image) ----------
    if len(image_np.shape) == 2:
         gray = image_np
    else:
        gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        result3 = reader.readtext(thresh, paragraph=True)
        texts += [r[1] for r in result3 if r[2] > 0.3]

    # ---------- PASS 4 (Tesseract fallback) ----------
    try:
        tesseract_text = pytesseract.image_to_string(image_np)
        if tesseract_text.strip():
            texts.append(tesseract_text)
    except:
        pass

    # ---------- MERGE ----------
    final_text = " ".join(texts)
    final_text = " ".join(final_text.split())

    return final_text