
import streamlit as st
import tempfile
import os
from langchain.schema import Document

from loaders import load_pdf, load_txt, load_md, load_csv
from chains.rag_chain import build_rag_chain
from embeddings.retriever import MultiModalRetriever
from evaluation import evaluate_retrieval
from agent import build_agent


st.set_page_config(page_title="📚 Advanced RAG App", layout="wide")
st.title("📚 Advanced RAG with Citations & Evaluation")

st.sidebar.header("Configuration")
model_name = st.sidebar.selectbox("LLM Model", ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"])
top_k = st.sidebar.slider("Top-k retrieval", 1, 10, 3)

uploaded_files = st.file_uploader("Upload documents", type=["pdf", "txt", "md", "csv", "png", "jpg", "jpeg", "mp3", "wav", "m4a"], accept_multiple_files=True)

st.sidebar.header("Mode")
mode = st.sidebar.radio("Choose interaction mode:", ["RAG Chain", "RAG Agent"])

# Initialize MultiModalRetriever
retriever = MultiModalRetriever(vectorstore_path="vectorstores/rag_index")

if uploaded_files:
    with st.spinner("Processing files..."):
        for file in uploaded_files:
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Add file to retriever
                retriever.add_file(tmp_file_path)
                st.success(f"Processed: {file.name}")
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
            finally:
                # Clean up temporary file
                os.unlink(tmp_file_path)

    st.success(f"Processed {len(uploaded_files)} files. Index cached in `vectorstores/rag_index/`.")

# Chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_question = st.text_input("Ask a question:")

if st.button("Ask") and user_question and uploaded_files:
    try:
        if mode == "RAG Chain":
            rag_runner = build_rag_chain(retriever, model_name=model_name, k=top_k)
            answer = rag_runner(user_question)
        else:  # Agent
            agent = build_agent(retriever, model_name=model_name, k=top_k)
            answer = agent.run(user_question)

        st.session_state.chat_history.append(("You", user_question))
        st.session_state.chat_history.append(("Assistant", answer))
    except Exception as e:
        st.error(f"Error processing question: {str(e)}")

if st.session_state.chat_history:
    st.markdown("### Chat History")
    for speaker, text in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {text}")

# Evaluation section
st.sidebar.header("Evaluation")
query = st.sidebar.text_input("Test query")
ground_truth = st.sidebar.text_input("Expected answer keyword")
if st.sidebar.button("Evaluate") and query and ground_truth and uploaded_files:
    try:
        results = retriever.retrieve(query, k=top_k)
        metrics = evaluate_retrieval(query, results, ground_truth)
        st.sidebar.json(metrics)
    except Exception as e:
        st.sidebar.error(f"Evaluation error: {str(e)}")