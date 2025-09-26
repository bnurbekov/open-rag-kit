from typing import List, Dict
from langchain.schema import Document

def evaluate_retrieval(query: str, results: List[Document], ground_truth: str) -> Dict:
    """Very simple eval: checks if ground_truth keywords appear in retrieved docs"""
    hits = sum(1 for doc in results if ground_truth.lower() in doc.page_content.lower())
    recall = hits / len(results) if results else 0
    return {
        "query": query,
        "ground_truth": ground_truth,
        "recall@k": recall,
        "docs_retrieved": len(results)
    }