import base64
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


def clean_text(text: str) -> str:
    """Remove noise and normalize text"""
    lines = text.split("\n")
    cleaned = [line.strip() for line in lines if line.strip()]
    return "\n".join(cleaned)


def extract_with_vision(file):
    """Extract text from image using Vision AI"""

    # Step 1: Read file safely
    file.file.seek(0)
    image_bytes = file.file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Step 2: Strong OCR Prompt
    prompt = """
You are an OCR engine.

Extract ALL text from the image exactly as it appears.

Rules:
- Output ONLY raw text
- Keep original structure (line breaks)
- Do NOT explain
- Do NOT summarize
- Do NOT add extra words
- If text is unclear, still output best guess
"""

    # Step 3: Call Vision Model
    response = client.chat.completions.create(
        model="openai/gpt-4.1",
        max_tokens=1500,
        temperature=0,  # 🔥 VERY IMPORTANT (more accurate)
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{base64_image}",
                    },
                ],
            }
        ],
    )

    # Step 4: Extract response
    raw_text = response.choices[0].message.content or ""

    # Step 5: Clean text
    cleaned_text = clean_text(raw_text)

    # Step 6: Debug logs (CRITICAL)
    print("\n===== RAW TEXT =====\n", raw_text)
    print("\n===== CLEANED TEXT =====\n", cleaned_text)

    return cleaned_text