# 
import time
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter

# App modules
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevent_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY


# ------------------------
# Page setup
# ------------------------
st.set_page_config(
    page_title=" - Document Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# st.markdown(
#     """
#     <style>
#         /* Whole App Background */
#         .stApp {
#             background-color: #000000 !important;
#             color: #e0e0e0 !important;
#         }

#         /* Sidebar background - force pure black */
#         section[data-testid="stSidebar"], .css-1d391kg, .css-1v0mbdj, .css-12oz5g7 {
#             background-color: #000000 !important;
#             color: #e0e0e0 !important;
#         }

#         /* Neon LED Headings */
#         h2,h3{
#             font-weight: bold;
#             color: #00bfff;
#             text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff, 0 0 20px #00bfff;
#         }

#         /* Sidebar headings & text */
#         section[data-testid="stSidebar"] h1,
#         section[data-testid="stSidebar"] h2,
#         section[data-testid="stSidebar"] h3,
#         section[data-testid="stSidebar"] p {
#             color: #00bfff !important;
#             font-weight: bold;
#             text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff;
#         }

#         /* File uploader box */
#         [data-testid="stFileUploader"] {
#             background-color: #111111;
#             border: 2px dashed #00bfff;
#             border-radius: 10px;
#             padding: 1rem;
#             color: #00bfff;
#         }

#         /* Buttons */
#         .stButton>button {
#             background-color: #00bfff;
#             color: black;
#             font-weight: bold;
#             border-radius: 8px;
#         }

#         .stButton>button:hover {
#             background-color: #0288d1;
#             color: white;
#         }

#         /* Success messages in neon blue */
#         .stAlert {
#             font-weight: bold;
#             color: #00bfff !important;
#             text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff, 0 0 20px #00bfff;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
st.markdown(
    """
    <style>
        /* Whole App Background */
        .stApp {
            background-color: #000000 !important;
            color: #e0e0e0 !important;
        }

        /* Sidebar background - force pure black */
        section[data-testid="stSidebar"], .css-1d391kg, .css-1v0mbdj, .css-12oz5g7 {
            background-color: #000000 !important;
            color: #e0e0e0 !important;
        }

        /* Neon LED Headings */
        h2,h3{
            font-weight: bold;
            color: #00bfff;
            text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff, 0 0 20px #00bfff;
        }

        /* Sidebar headings & text */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p {
            color: #00bfff !important;
            font-weight: bold;
            text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff;
        }

        /* Make "Document Upload" bigger */
        section[data-testid="stSidebar"] h3 {
            font-size: 1.6rem !important;
        }

        /* File uploader box */
        [data-testid="stFileUploader"] {
            background-color: #111111;
            border: 2px dashed #00bfff;
            border-radius: 10px;
            padding: 1rem;
            color: #00bfff;
        }

        /* Buttons */
        .stButton>button {
            background-color: #00bfff;
            color: black;
            font-weight: bold;
            border-radius: 8px;
        }

        .stButton>button:hover {
            background-color: #0288d1;
            color: white;
        }

        /* Success messages in neon blue */
        .stAlert {
            font-weight: bold;
            color: #00bfff !important;
            text-shadow: 0 0 5px #00bfff, 0 0 10px #00bfff, 0 0 20px #00bfff;
        }

        /* Chat input box styling */
        div[data-testid="stChatInput"] {
            background-color: #000000 !important;
            border: 2px solid #ffffff !important;
            border-radius: 25px !important;
            padding: 5px !important;
            color: #ffffff !important;
        }

        /* Placeholder text inside input */
        div[data-testid="stChatInput"] input {
            color: #ffffff !important;
        }

        /* White send arrow */
        div[data-testid="stChatInput"] button {
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



# ------------------------
# Session State Initialization
# ------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_model" not in st.session_state:
    st.session_state.chat_model = None


# ------------------------
# Sidebar: Document Upload
# ------------------------
with st.sidebar:
    st.markdown("###  **Document Upload**")
    st.markdown("Upload your documents to start chatting")

    uploaded_files = pdf_uploader()

    if uploaded_files:
        st.success(f"{len(uploaded_files)} document(s) uploaded")

        if st.button("⚡ **Process Documents**", type="primary"):
            with st.spinner("Processing your medical documents..."):
                all_texts = [extract_text_from_pdf(file) for file in uploaded_files]

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )

                # Split into chunks
                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                # Create Vectorstore
                vectorstore = create_faiss_index(chunks)
                st.session_state.vectorstore = vectorstore

                # Load Chat Model
                chat_model = get_chat_model(EURI_API_KEY)
                st.session_state.chat_model = chat_model

                st.success("Documents processed successfully!")
                st.balloons()


# ------------------------
# Main Chat Interface
# ------------------------
st.markdown("### 💬 **Chat with your documents**")

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        st.caption(message["timestamp"])

# User input
prompt = st.chat_input("Ask about your documents!")

if prompt:
    timestamp = time.strftime("%H:%M")

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # ------------------------
    # Generate Assistant Response
    # ------------------------
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching your documents..."):
                if prompt.strip() == "":
                    st.warning("⚠️ Please enter a valid query.")
                else:
                    # Retrieve relevant docs
                    relevant_docs = retrieve_relevent_docs(
                        st.session_state.vectorstore, prompt
                    )
                    context = "\n\n".join([doc.page_content for doc in relevant_docs])

                    # System prompt
                    system_prompt = f"""
                    You are MediChat Pro, an intelligent medical document assistant.
                    Based on the following medical documents, provide accurate and helpful answers.
                    If the information is not in the documents, clearly state that.

                    Medical Documents:
                    {context}

                    User Question: {prompt}

                    Answer:
                    """

                    response = ask_chat_model(st.session_state.chat_model, system_prompt)

                # Display assistant response
                st.markdown(response)
                st.caption(timestamp)
