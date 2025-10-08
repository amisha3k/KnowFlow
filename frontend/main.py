# import time
# import os
# import sys
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning)
# warnings.filterwarnings("ignore", category=DeprecationWarning)


# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# # Use /tmp/.streamlit instead of /app/.streamlit
# os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp/.streamlit"
# os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"

# # Create directory in /tmp (writable in 
#  Face)
# os.makedirs(os.environ["STREAMLIT_CONFIG_DIR"], exist_ok=True)

# import streamlit as st
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.memory import ConversationBufferWindowMemory  # or ConversationBufferWindowMemory


# # App modules
# from app.ui import pdf_uploader
# from app.pdf_utils import extract_text_from_pdf
# from app.vectorstore_utils import create_faiss_index, retrieve_relevent_docs
# from app.chat_utils import get_chat_model, ask_chat_model
# from app.config import EURI_API_KEY


# # Page setup
# st.set_page_config(
#     page_title=" KnowFlow - Document Assistant",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.markdown(
#     """
#     <style>
#         /* Whole App Background */
#         .stApp {
#             background-color: #2c2c2c !important; /* Dark grey */
#             color: #d3d3d3 !important; /* Light grey text */
#         }
        
#         header[data-testid="stHeader"] {
#             background-color: #2c2c2c !important;
#             color: #d3d3d3 !important;
#         }

#         header[data-testid="stHeader"] .stAppHeader {
#             background-color: #2c2c2c !important;
#             color: #d3d3d3 !important;
#         }
        
#         /* Sidebar background */
#         section[data-testid="stSidebar"] {
#             background-color: #3a3a3a !important; /* Slightly lighter grey */
#             color: #d3d3d3 !important;
#         }

#         /* Headings */
#         h1, h2, h3 {
#             font-weight: bold;
#             color: #f0f0f0 !important; /* Very light grey */
#             text-shadow: none !important;
#         }

#         /* Sidebar text */
#         section[data-testid="stSidebar"] h1,
#         section[data-testid="stSidebar"] h2,
#         section[data-testid="stSidebar"] h3,
#         section[data-testid="stSidebar"] p {
#             color: #d3d3d3 !important;
#             font-weight: normal !important;
#             text-shadow: none !important;
#         }

#         /* File uploader box */
#         [data-testid="stFileUploader"] {
#             background-color: #444444; /* Medium grey */
#             border: 0.5px dashed #d3d3d3;
#             border-radius: 5px;
#             padding: 1rem;
#             color: #d3d3d3;
#         }

#         /* Buttons */
#         .stButton>button {
#             background-color: #d3d3d3;
#             color: #2c2c2c;
#             font-weight: bold;
#             border-radius: 5px;
#         }

#         .stButton>button:hover {
#             background-color: #b0b0b0;
#             color: #2c2c2c;
#         }

#         /* Alerts */
#         .stAlert {
#             font-weight: normal;
#             color: #f0f0f0 !important;
#             text-shadow: none !important;
#         }

#         /* Chat input box */
#         div[data-testid="stChatInput"] {
#             background-color: #e0e0e0 !important; /* Light grey input */
#             border: 1px solid #c0c0c0 !important;
#             border-radius: 2px !important;
#             padding: 2px !important;
#             color: #000000 !important;
#         }

#         /* Placeholder text inside input */
#         div[data-testid="stChatInput"] input {
#             color: #000000 !important;
#         }

#         /* Send button */
#         div[data-testid="stChatInput"] button {
#             color: #000000 !important;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )



# # Session State Initialization

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "vectorstore" not in st.session_state:
#     st.session_state.vectorstore = None

# if "chat_model" not in st.session_state:
#     st.session_state.chat_model = None

# if "memory" not in st.session_state:
#     st.session_state.memory = ConversationBufferWindowMemory(
#         memory_key="chat_history",  # Key to store chat in session state
#         return_messages=True,       # Keep messages as objects
#         k=5                         # Only remember last 5 messages (prevents long memory buildup)
#     )
# # if "memory" not in st.session_state:
# #     st.session_state.memory = ConversationBufferMemory(
# #         memory_key="chat_history",
# #         return_messages=True
# #     )
#     # Swap with ConversationBufferWindowMemory(k=5, return_messages=True)
#     # if i want it to only remember the last 5 exchanges

# # Sidebar: Document Upload

# with st.sidebar:
#     st.markdown("###  **Document Upload**")
#     st.markdown("Upload your documents to start chatting")

#     try:
#         uploaded_files = pdf_uploader()
#     except Exception as e:
#         print("error while uploading",e)    

#     # uploaded_files = pdf_uploader()

#     if uploaded_files:
#         st.success(f"{len(uploaded_files)} document(s) uploaded")

#         if st.button("⚡ **Process Documents**", type="primary"):
#             with st.spinner("Processing your medical documents..."):
#                 all_texts = [extract_text_from_pdf(file) for file in uploaded_files]

#                 text_splitter = RecursiveCharacterTextSplitter(
#                     chunk_size=1000,
#                     chunk_overlap=200,
#                     length_function=len,
#                 )

#                 # Split into chunks
#                 chunks = []
#                 for text in all_texts:
#                     chunks.extend(text_splitter.split_text(text))

#                 # Create Vectorstore
#                 vectorstore = create_faiss_index(chunks)
#                 st.session_state.vectorstore = vectorstore

#                 # Load Chat Model
#                 chat_model = get_chat_model(EURI_API_KEY)
#                 st.session_state.chat_model = chat_model

#                 st.success("Documents processed successfully!")
#                 st.balloons()


# # Main Chat Interface yeyeee
# st.markdown("### 💬 **Chat with your documents**")

# # Display past messages
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#         st.caption(message["timestamp"])


# # # User input
# prompt = st.chat_input("Ask about your documents!")

# if prompt:
#     timestamp = time.strftime("%H:%M")

#     # Store user message
#     st.session_state.messages.append({
#         "role": "user",
#         "content": prompt,
#         "timestamp": timestamp
#     })

#     # Display user message
#     with st.chat_message("user"):
#         st.markdown(prompt)
#         st.caption(timestamp)

 
#     # Generate Assistant Response with Memory
#     if st.session_state.vectorstore and st.session_state.chat_model:
#         with st.chat_message("assistant"):
#             with st.spinner("🔍 Searching your documents..."):
#                 relevant_docs = retrieve_relevent_docs(
#                     st.session_state.vectorstore, prompt
#                 )
#                 context = "\n\n".join([doc.page_content for doc in relevant_docs])

#                 # Retrieve chat history from memory
#                 history_text = st.session_state.memory.load_memory_variables({})["chat_history"]

#                 # System prompt with history + context
#                 system_prompt = f"""
#                 You are MediChat Pro, an intelligent medical document assistant.

#                 Conversation so far:
#                 {history_text}

#                 Relevant Medical Documents:
#                 {context}

#                 Now, answer the user's latest question clearly and helpfully.

#                 User Question: {prompt}

#                 Answer:
#                 """

#                 response = ask_chat_model(st.session_state.chat_model, system_prompt)

#                 # Save response to messages
#                 st.session_state.messages.append({
#                     "role": "assistant",
#                     "content": response,
#                     "timestamp": timestamp
#                 })

#                 # Save into memory
#                 st.session_state.memory.chat_memory.add_user_message(prompt)
#                 st.session_state.memory.chat_memory.add_ai_message(response)

#                 # Display assistant response
#                 st.markdown(response)
#                 st.caption(timestamp)
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

                # Create Vectorstore
                try:
                    vectorstore = create_faiss_index(chunks)
                    st.session_state.vectorstore = vectorstore
                except Exception as e:
                    st.error(f"error creating vectorstor : {e}")


                # Load Chat Model
                chat_model = get_chat_model(EURI_API_KEY)
                st.session_state.chat_model = chat_model

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
