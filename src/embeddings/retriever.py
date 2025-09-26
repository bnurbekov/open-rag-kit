# src/embeddings/retriever.py

import os
from typing import List
from langchain.schema import Document
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

CACHE_DIR = "vectorstores"

def build_vectorstore(docs: List[Document], index_name: str = "rag_index") -> FAISS:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, index_name)

    if os.path.exists(path):
        return FAISS.load_local(path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(path)
    return vectorstore

def get_retriever(docs: List[Document], index_name: str = "rag_index", k: int = 3):
    vectorstore = build_vectorstore(docs, index_name=index_name)
    return vectorstore.as_retriever(search_kwargs={"k": k})