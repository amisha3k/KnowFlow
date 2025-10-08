
import time
import os
import sys
import warnings

# -------------------------
# Suppress warnings
# -------------------------
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# -------------------------
# Path setup
# -------------------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Streamlit config directory
os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp/.streamlit"
os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"
os.makedirs(os.environ["STREAMLIT_CONFIG_DIR"], exist_ok=True)

# -------------------------
# Imports
# -------------------------
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage, AIMessage
from langchain_core.chat_history import BaseChatMessageHistory

# App modules
from app.ui import pdf_uploader
from app.pdf_utils import extract_text_from_pdf
from app.vectorstore_utils import create_faiss_index, retrieve_relevent_docs
from app.chat_utils import get_chat_model, ask_chat_model
from app.config import EURI_API_KEY

# -------------------------
# Custom Memory Class
# -------------------------
class CustomChatMemory(BaseChatMessageHistory):
    """Stores chat messages in memory for LangChain."""

    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(
    page_title="KnowFlow - Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Dark Theme CSS
# -------------------------
st.markdown("""
<style>
.stApp { background-color: #2c2c2c !important; color: #d3d3d3 !important; }
header[data-testid="stHeader"] { background-color: #2c2c2c !important; color: #d3d3d3 !important; }
section[data-testid="stSidebar"] { background-color: #3a3a3a !important; color: #d3d3d3 !important; }
h1,h2,h3 { color: #f0f0f0 !important; font-weight:bold; }
.stButton>button { background-color: #d3d3d3; color: #2c2c2c; font-weight:bold; border-radius:5px;}
.stButton>button:hover { background-color: #b0b0b0; color:#2c2c2c; }
[data-testid="stFileUploader"] { background-color: #444444; border:0.5px dashed #d3d3d3; border-radius:5px; padding:1rem; color:#d3d3d3;}

/* Chat messages text color */
.stChatMessage div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
}

/* Optional: assistant message background */
.stChatMessage[data-testid="stMessage"]:nth-child(2) div[data-testid="stMarkdownContainer"] {
    background-color: #444444 !important;
    border-radius: 5px;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# Session State Initialization
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_model" not in st.session_state:
    st.session_state.chat_model = None

if "memory" not in st.session_state:
    st.session_state.memory = CustomChatMemory()

# -------------------------
# Sidebar: Document Upload
# -------------------------
with st.sidebar:
    st.markdown("###  **Document Upload**")
    st.markdown("Upload your documents to start chatting")

    uploaded_files = pdf_uploader()
    if uploaded_files:
        st.success(f"{len(uploaded_files)} document(s) uploaded")

        if st.button("⚡ **Process Documents**", type="primary"):
            with st.spinner("Processing your documents..."):
                all_texts = [extract_text_from_pdf(file) for file in uploaded_files]

                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )

                chunks = []
                for text in all_texts:
                    chunks.extend(text_splitter.split_text(text))

                st.write("Step 2: Chunks created", len(chunks)) 

                # Create Vectorstore
                try:
                    vectorstore = create_faiss_index(chunks)
                    st.session_state.vectorstore = vectorstore
                    st.write("Step 3: Vectorstore created", st.session_state.vectorstore is not None)
                except Exception as e:
                    st.error(f"error creating vectorstor : {e}")


                # Load Chat Model
                chat_model = get_chat_model(EURI_API_KEY)
                st.session_state.chat_model = chat_model
                st.write("Step 4: Chat model loaded", st.session_state.chat_model is not None)

                st.success("Documents processed successfully!")
                st.balloons()

# -------------------------
# Main Chat Interface
# -------------------------
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

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": timestamp
    })

    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(timestamp)

    # Generate Assistant Response
    if st.session_state.vectorstore and st.session_state.chat_model:
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching your documents..."):
                try:
                   relevant_docs = retrieve_relevent_docs(st.session_state.vectorstore, prompt)
                   context = "\n\n".join([doc.page_content for doc in relevant_docs])
                except Exception as e:
                    st.error(f"Error generating response: {e}")
                    response = "Sorry, something went wrong."   

                # Retrieve conversation history
                history_text = "\n".join([
                    f"{msg.type}: {msg.content}" for msg in st.session_state.memory.get_messages()
                ])

                # System prompt
                system_prompt = f"""
You are KnowFlow, an intelligent document assistant.

Conversation so far:
{history_text}

Relevant Documents:
{context}

User Question: {prompt}

Answer clearly and helpfully:
"""

                # Get response from chat model
                response = ask_chat_model(st.session_state.chat_model, system_prompt)

                # Save messages to memory
                st.session_state.memory.add_message(HumanMessage(content=prompt))
                st.session_state.memory.add_message(AIMessage(content=response))

                # Save assistant message to session
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": timestamp
                })

                # Display assistant response
                st.markdown(response)
                st.caption(timestamp)
