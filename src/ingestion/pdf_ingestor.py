import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class PDFIngestor:
    def __init__(self, chunk_size=800, chunk_overlap=100):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def extract_text(self, file_path: str) -> str:
        """Extract text from PDF. Fallback to OCR if necessary."""
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

        if not text and OCR_AVAILABLE:
            # OCR fallback for scanned PDFs
            images = convert_from_path(file_path)
            for img in images:
                text += pytesseract.image_to_string(img)

        return text

    def process(self, file_path: str):
        raw_text = self.extract_text(file_path)
        return self.splitter.split_text(raw_text)