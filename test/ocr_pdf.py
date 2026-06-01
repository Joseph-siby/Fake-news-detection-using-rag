# ocr_pdf.py
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
from PIL import Image
import re

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """
    Convert PIL Image to OpenCV, apply grayscale, thresholding, and return cleaned PIL Image
    """
    img_cv = np.array(image)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    denoised = cv2.medianBlur(thresh, 3)
    return Image.fromarray(denoised)

def clean_text(text: str) -> str:
    """
    Clean OCR extracted text
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def read_pdf_with_ocr(pdf_path: str, query: str = None) -> list:
    """
    Extract text from scanned PDF using OCR.
    If query is provided, return only chunks containing the keyword/topic.
    """
    text_chunks = []
    pages = convert_from_path(pdf_path)
    
    for i, page in enumerate(pages):
        clean_page = preprocess_image_for_ocr(page)
        text = pytesseract.image_to_string(clean_page, lang='eng', config='--psm 6')
        text = clean_text(text)
        if text:
            text_chunks.append(text)
    
    # If query is provided, filter chunks
    if query:
        query_lower = query.lower()
        results = [chunk for chunk in text_chunks if query_lower in chunk.lower()]
        return results if results else ["Not found"]
    
    return text_chunks


