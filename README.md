MediChatApp is a Streamlit-based AI assistant that allows users to upload medical PDF documents and ask questions related to them. The app uses LangChain, FAISS, and Euriai API for intelligent document understanding and response generation.

🧠 How It Works
 Upload PDF: User uploads a medical document. 

Extract Text: App parses the PDF into raw text using PyPDF. 

Vectorize: Text is chunked and embedded via Sentence Transformers. 

Store: Embeddings are saved in FAISS for efficient retrieval. 

Ask Questions: User submits questions via chat UI.

Retrieve & Respond: The app fetches the most relevant text chunks and uses the LLM (via Euriai) to generate a response. 

