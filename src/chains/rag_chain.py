from typing import List
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import Document

from prompts.rag_prompt import rag_prompt
from embeddings.retriever import get_retriever


def build_rag_chain(docs: List[Document], model_name: str = "gpt-4o-mini", k: int = 3):
    retriever = get_retriever(docs, index_name="rag_index", k=k)
    llm = ChatOpenAI(model=model_name, temperature=0)

    rag_chain = LLMChain(
        llm=llm,
        prompt=rag_prompt,
        verbose=True
    )

    def run(question: str) -> str:
        results = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in results])
        answer = rag_chain.run({"context": context, "question": question})

        # Append citations
        sources = ", ".join([f"{doc.metadata.get('source')} (p.{doc.metadata.get('page','?')})" for doc in results])
        return f"{answer}\n\n**Sources:** {sources}"

    return run