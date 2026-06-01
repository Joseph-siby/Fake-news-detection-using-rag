# document_retriever.py

import PyPDF2
from test.ocr_pdf import read_pdf_with_ocr
import docx
import re

def clean_text(text: str) -> str:
    """
    Clean OCR or extracted text: remove extra spaces and special characters.
    """
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces/newlines
    text = text.strip()
    return text

def read_pdf(file_path):
    chunks = []
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                chunks.append(clean_text(text))
    if not chunks:
        print("No text found in PDF, using OCR...")
        chunks = read_pdf_with_ocr(file_path)
        # Clean OCR chunks
        chunks = [clean_text(chunk) for chunk in chunks if chunk.strip()]
    return chunks

def read_docx(file_path):
    chunks = []
    doc = docx.Document(file_path)
    for para in doc.paragraphs:
        text = clean_text(para.text)
        if text:
            chunks.append(text)
    return chunks

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [clean_text(line) for line in f if line.strip()]

def read_file(file_path):
    """
    Detect file type and read content
    """
    if file_path.endswith(".pdf"):
        return read_pdf(file_path)
    elif file_path.endswith(".docx"):
        return read_docx(file_path)
    elif file_path.endswith(".txt"):
        return read_txt(file_path)
    else:
        raise ValueError("Unsupported file format")

# ---------------------------
# Keyword/topic search
# ---------------------------
def search_text_chunks(chunks, query):
    """
    Search for a keyword/topic in chunks. Returns relevant chunks or "Not found".
    """
    query_lower = query.lower()
    results = [chunk for chunk in chunks if query_lower in chunk.lower()]
    if results:
        return results
    else:
        return ["Not found"]

