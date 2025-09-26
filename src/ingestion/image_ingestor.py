from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

class ImageIngestor:
    def __init__(self, model="Salesforce/blip-image-captioning-base"):
        self.processor = BlipProcessor.from_pretrained(model)
        self.model = BlipForConditionalGeneration.from_pretrained(model)

    def process(self, image_path: str) -> str:
        """Generate a caption for the given image."""
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(image, return_tensors="pt")
        out = self.model.generate(**inputs, max_length=50)
        caption = self.processor.decode(out[0], skip_special_tokens=True)
        return caption