import streamlit as st
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevent_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time

# Page setup
st.set_page_config(
    page_title="MediChat - Medical Document Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(
    """
    <style>
        .stApp {
            background-color: #f0f2f6;
        }
        h1 {
            color: #0c5f8a;
        }
        .css-18e3th9 {
            padding: 2rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

# Sidebar upload section
with st.sidebar:
    st.markdown("### Document Upload")
    st.markdown("Upload your medical documents to start chatting")

    uploaded_files = pdf_uploader()

    if uploaded_files:
        st.success(f"{len(uploaded_files)} document(s) uploaded")

        if st.button("Process Documents", type="primary"):
            with st.spinner("Processing your medical documents..."):
                all_texts = []
                for file in uploaded_files:
                    text = extract_text_from_pdf(file)
                    all_texts.append(text)

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )

                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore

                chat_model = get_chat_model(EURI_API_KEY)
                st.session_state.chat_model = chat_model

                st.success("Documents processed successfully")
                st.balloons()

# Chat interface
st.markdown("### Chat with your medical documents")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# User input
prompt = st.chat_input("Ask about your medical documents!")
if prompt:
    timestamp = time.strftime("%H:%M")
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # Generate response
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("Searching your documents..."):
                if prompt.strip() == "":
                    st.warning("Please enter a valid query.")
                else:
                    relevant_docs = retrieve_relevent_docs(st.session_state.vectorstore, prompt)
                    context = "\n\n".join([doc.page_content for doc in relevant_docs])

                    system_prompt = f"""You are MediChat Pro, an intelligent medical document assistant.
Based on the following medical documents, provide accurate and helpful answers.
If the information is not in the documents, clearly state that.

Medical Documents:
{context}

User Question: {prompt}

Answer:"""

                    response = ask_chat_model(st.session_state.chat_model, system_prompt)

                st.markdown(response)
                st.caption(timestamp)
