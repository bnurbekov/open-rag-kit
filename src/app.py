
import streamlit as st
from langchain.schema import Document

from loaders import load_pdf, load_txt, load_md, load_csv
from chains.rag_chain import build_rag_chain
from embeddings.retriever import build_vectorstore
from evaluation import evaluate_retrieval
from agent import build_agent


st.set_page_config(page_title="📚 Advanced RAG App", layout="wide")
st.title("📚 Advanced RAG with Citations & Evaluation")

st.sidebar.header("Configuration")
model_name = st.sidebar.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
top_k = st.sidebar.slider("Top-k retrieval", 1, 10, 3)

uploaded_files = st.file_uploader("Upload documents", type=["pdf", "txt", "md", "csv"], accept_multiple_files=True)

st.sidebar.header("Mode")
mode = st.sidebar.radio("Choose interaction mode:", ["RAG Chain", "RAG Agent"])

docs = []
if uploaded_files:
    for file in uploaded_files:
        if file.name.endswith(".pdf"):
            docs.extend(load_pdf(file, file.name))
        elif file.name.endswith(".txt"):
            docs.extend(load_txt(file, file.name))
        elif file.name.endswith(".md"):
            docs.extend(load_md(file, file.name))
        elif file.name.endswith(".csv"):
            docs.extend(load_csv(file, file.name))

if docs:
    st.success(f"Loaded {len(docs)} docs. Index cached in `vectorstores/`.")

# Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_question = st.text_input("Ask a question:")

if st.button("Ask") and user_question and docs:
    if mode == "RAG Chain":
        rag_runner = build_rag_chain(docs, model_name=model_name, k=top_k)
        answer = rag_runner(user_question)
    else:  # Agent
        agent = build_agent(docs, model_name=model_name, k=top_k)
        answer = agent.run(user_question)

    st.session_state.chat_history.append(("You", user_question))
    st.session_state.chat_history.append(("Assistant", answer))

if st.session_state.chat_history:
    st.markdown("### Chat History")
    for speaker, text in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {text}")

# Evaluation section
st.sidebar.header("Evaluation")
query = st.sidebar.text_input("Test query")
ground_truth = st.sidebar.text_input("Expected answer keyword")
if st.sidebar.button("Evaluate") and query and ground_truth and docs:
    from embeddings.retriever import get_retriever
    retriever = get_retriever(docs, "rag_index", k=top_k)
    results = retriever.get_relevant_documents(query)
    metrics = evaluate_retrieval(query, results, ground_truth)
    st.sidebar.json(metrics)