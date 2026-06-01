import base64


def understand_image(file, client):
    """
    General image understanding (NOT OCR)

    Returns:
        keywords / meaningful entities from the image
    """

    try:
        # Step 1: Read file safely
        file.file.seek(0)
        image_bytes = file.file.read()

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # Step 2: Strong GENERAL prompt (works for ANY image)
        prompt = """
Analyze this image and extract key information.

Return ONLY concise keywords (no sentences).

Include if present:
- objects (e.g., person, bird, car)
- brands or logos
- text (only if clearly readable)
- scene type (sports, nature, city, etc.)

Rules:
- No explanations
- No full sentences
- No guessing unclear text
- Output 3–10 keywords max
"""

        # Step 3: Call Vision Model
        response = client.chat.completions.create(
            model="openai/gpt-4.1",
            temperature=0,          # 🔥 important for stability
            max_tokens=200,
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

        # Step 4: Extract result
        result = response.choices[0].message.content or ""

        # Step 5: Clean output (simple)
        cleaned = "\n".join(
            [line.strip() for line in result.split("\n") if line.strip()]
        )

        # Step 6: Debug (VERY IMPORTANT)
        print("\n===== UNDERSTANDING OUTPUT =====\n")
        print(cleaned)
        print("\n================================\n")

        return cleaned

    except Exception as e:
        print("❌ Understanding Error:", str(e))
        return ""