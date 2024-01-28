import time
from PIL import Image
from io import BytesIO
from base64 import b64encode
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def generate_caption(image):
    "Generate caption from the image"
    with Image.open(image) as img:
        raw_image = img.convert("RGB")

        inputs = processor(raw_image, return_tensors="pt", max_new_tokens=100)

        start_time = time.time()
        out = model.generate(**inputs, max_new_tokens=10)
        generation_time = time.time() - start_time

        caption = processor.decode(out[0], skip_special_tokens=True)
        return caption, generation_time