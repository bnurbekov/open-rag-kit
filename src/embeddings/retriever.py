import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

from src.ingestion import PDFIngestor, ImageIngestor, AudioIngestor

class MultiModalRetriever:
    def __init__(self, vectorstore_path="vectorstore/faiss_index"):
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore_path = vectorstore_path

        if os.path.exists(vectorstore_path):
            self.vstore = FAISS.load_local(vectorstore_path, self.embeddings)
        else:
            self.vstore = None

        # Ingestors
        self.pdf_ingestor = PDFIngestor()
        self.image_ingestor = ImageIngestor()
        self.audio_ingestor = AudioIngestor()

    def add_file(self, file_path: str):
        ext = os.path.splitext(file_path)[1].lower()
        docs = []

        if ext in [".pdf"]:
            chunks = self.pdf_ingestor.process(file_path)
            docs = [{"text": c, "metadata": {"source": file_path}} for c in chunks]

        elif ext in [".png", ".jpg", ".jpeg"]:
            caption = self.image_ingestor.process(file_path)
            docs = [{"text": caption, "metadata": {"source": file_path}}]

        elif ext in [".mp3", ".wav", ".m4a"]:
            transcript = self.audio_ingestor.process(file_path)
            docs = [{"text": transcript, "metadata": {"source": file_path}}]

        else:
            raise ValueError(f"Unsupported file type: {ext}")

        texts = [d["text"] for d in docs]
        metadatas = [d["metadata"] for d in docs]

        if self.vstore is None:
            self.vstore = FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)
        else:
            self.vstore.add_texts(texts, metadatas=metadatas)

        # Save vectorstore after adding
        self.vstore.save_local(self.vectorstore_path)

    def retrieve(self, query: str, k=3):
        if not self.vstore:
            raise RuntimeError("Vectorstore is empty. Add files first.")
        return self.vstore.similarity_search(query, k=k)