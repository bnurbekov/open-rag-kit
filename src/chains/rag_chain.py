from typing import List
from langchain_openai import ChatOpenAI
from langchain.schema import Document

from prompts.rag_prompt import rag_prompt
from embeddings.retriever import MultiModalRetriever


def build_rag_chain(retriever: MultiModalRetriever, model_name: str = "gpt-4o-mini", k: int = 3):
    llm = ChatOpenAI(model=model_name, temperature=0)

    # Use modern LangChain syntax: prompt | llm
    rag_chain = rag_prompt | llm

    def run(question: str) -> str:
        results = retriever.retrieve(question, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        
        # Use invoke instead of run for modern LangChain
        answer = rag_chain.invoke({"context": context, "question": question})

        # Append citations
        sources = ", ".join([f"{doc.metadata.get('source')} (p.{doc.metadata.get('page','?')})" for doc in results])
        return f"{answer}\n\n**Sources:** {sources}"

    return run