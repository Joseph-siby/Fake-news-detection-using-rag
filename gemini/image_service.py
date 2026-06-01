from transformers import pipeline
from PIL import Image
import io

# Load once (will download model on first run)
captioner = pipeline(
    "image-to-text",
    model="Salesforce/blip-image-captioning-base"
)

def describe_image_file(upload_file):
    try:
        upload_file.file.seek(0)
        image = Image.open(upload_file.file).convert("RGB")

        # Resize for speed
        image.thumbnail((512, 512))

        result = captioner(image)

        caption = result[0]["generated_text"]

        return f"Description: {caption}\nUsefulness: yes"

    except Exception as e:
        return f"Error processing image: {str(e)}"