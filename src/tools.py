from langchain.tools import Tool
from langchain.schema import Document
from embeddings.retriever import get_retriever
from chains.rag_chain import build_rag_chain


def make_rag_tools(docs: list[Document], model_name: str = "gpt-4o-mini", k: int = 3):
    retriever = get_retriever(docs, index_name="rag_index", k=k)

    def search_docs(query: str) -> str:
        results = retriever.get_relevant_documents(query)
        return "\n\n".join([f"{doc.page_content[:500]}... (Source: {doc.metadata.get('source')})" for doc in results])

    def summarize_docs(query: str) -> str:
        results = retriever.get_relevant_documents(query)
        summary = " | ".join([doc.page_content[:200] for doc in results])
        return f"Summary of top docs: {summary}"

    def count_docs(_: str) -> str:
        return f"Number of documents indexed: {len(docs)}"

    # Wrap RAG chain
    rag_runner = build_rag_chain(docs, model_name=model_name, k=k)

    def rag_answer(query: str) -> str:
        return rag_runner(query)

    return [
        Tool(name="SearchDocs", func=search_docs, description="Search uploaded documents for relevant text"),
        Tool(name="SummarizeDocs", func=summarize_docs, description="Summarize top-k retrieved documents"),
        Tool(name="CountDocs", func=count_docs, description="Get number of indexed documents"),
        Tool(name="AskRAG", func=rag_answer, description="Use RAG pipeline to answer complex user questions with citations"),
    ]