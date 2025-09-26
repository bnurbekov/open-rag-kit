# src/loaders.py

import fitz  # PyMuPDF
import csv
from langchain.schema import Document

def load_pdf(file, filename: str):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    texts = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text("text")
        texts.append(Document(page_content=text, metadata={"source": filename, "page": page_num}))
    return texts

def load_txt(file, filename: str):
    text = file.read().decode("utf-8", errors="ignore")
    return [Document(page_content=text, metadata={"source": filename})]

def load_md(file, filename: str):
    return load_txt(file, filename)

def load_csv(file, filename: str):
    reader = csv.reader(file.read().decode("utf-8").splitlines())
    rows = [" | ".join(row) for row in reader]
    text = "\n".join(rows)
    return [Document(page_content=text, metadata={"source": filename})]