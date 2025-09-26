import os
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from ingestion import PDFIngestor, ImageIngestor, AudioIngestor

class MultiModalRetriever:
    def __init__(self, vectorstore_path="vectorstore/faiss_index"):
        self.embeddings = None  # Initialize lazily
        self.vectorstore_path = vectorstore_path
        self.vstore = None

        # Ingestors
        self.pdf_ingestor = PDFIngestor()
        self.image_ingestor = ImageIngestor()
        self.audio_ingestor = AudioIngestor()
        
        # Load existing vectorstore if it exists
        self._load_existing_vectorstore()

    def _get_embeddings(self):
        """Lazy initialization of embeddings"""
        if self.embeddings is None:
            self.embeddings = OpenAIEmbeddings()
        return self.embeddings

    def _load_existing_vectorstore(self):
        """Load existing vectorstore if it exists"""
        if os.path.exists(self.vectorstore_path):
            try:
                self.vstore = FAISS.load_local(
                    self.vectorstore_path, 
                    self._get_embeddings(), 
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"Warning: Could not load existing vectorstore: {e}")
                self.vstore = None

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
            self.vstore = FAISS.from_texts(texts, self._get_embeddings(), metadatas=metadatas)
        else:
            self.vstore.add_texts(texts, metadatas=metadatas)

        # Save vectorstore after adding
        self.vstore.save_local(self.vectorstore_path)

    def retrieve(self, query: str, k=3):
        if not self.vstore:
            raise RuntimeError("Vectorstore is empty. Add files first.")
        return self.vstore.similarity_search(query, k=k)