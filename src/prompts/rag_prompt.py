from langchain.prompts import PromptTemplate

# Base RAG template: system message + instructions + context injection
RAG_PROMPT_TEMPLATE = """
You are a helpful assistant that answers questions using the provided context.

Use the following rules:
- ONLY use the context to answer the question.
- If the answer is not in the context, say "I don’t know based on the available information."
- Be concise and factual. Do not hallucinate.
- Always cite the source if available.

Context:
{context}

Question:
{question}

Answer:
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=RAG_PROMPT_TEMPLATE,
)