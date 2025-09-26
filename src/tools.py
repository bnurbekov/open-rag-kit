from langchain.tools import Tool
from langchain.schema import Document
from embeddings.retriever import MultiModalRetriever
from chains.rag_chain import build_rag_chain


def make_rag_tools(retriever: MultiModalRetriever, model_name: str = "gpt-4o-mini", k: int = 3):
    def search_docs(query: str) -> str:
        results = retriever.retrieve(query, k=k)
        return "\n\n".join([f"{doc.page_content[:500]}... (Source: {doc.metadata.get('source')})" for doc in results])

    def summarize_docs(query: str) -> str:
        results = retriever.retrieve(query, k=k)
        summary = " | ".join([doc.page_content[:200] for doc in results])
        return f"Summary of top docs: {summary}"

    def count_docs(_: str) -> str:
        try:
            # Try to get a count by doing a broad search
            results = retriever.retrieve("", k=1000)  # Get many results to estimate count
            return f"Number of documents indexed: {len(results)}"
        except:
            return "Number of documents indexed: Unknown"

    # Wrap RAG chain
    rag_runner = build_rag_chain(retriever, model_name=model_name, k=k)

    def rag_answer(query: str) -> str:
        return rag_runner(query)

    return [
        Tool(name="SearchDocs", func=search_docs, description="Search uploaded documents for relevant text"),
        Tool(name="SummarizeDocs", func=summarize_docs, description="Summarize top-k retrieved documents"),
        Tool(name="CountDocs", func=count_docs, description="Get number of indexed documents"),
        Tool(name="AskRAG", func=rag_answer, description="Use RAG pipeline to answer complex user questions with citations"),
    ]