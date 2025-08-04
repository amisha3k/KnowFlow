MediChatApp is a Streamlit-based AI assistant that allows users to upload medical PDF documents and ask questions related to them. The app uses LangChain, FAISS, and Euriai API for intelligent document understanding and response generation.

🧠 How It Works
 1. Upload PDF: User uploads a medical document. 

2. Extract Text: App parses the PDF into raw text using PyPDF. 

3. Vectorize: Text is chunked and embedded via Sentence Transformers. 

4. Store: Embeddings are saved in FAISS for efficient retrieval. 

5. Ask Questions: User submits questions via chat UI.

6. Retrieve & Respond: The app fetches the most relevant text chunks and uses the LLM (via Euriai) to generate a response. 

🙌 Acknowledgments
1. Inspired by the growing need for AI tools in the healthcare documentation space.

2. Built using open-source tools from Hugging Face, FAISS, and LangChain community.

🔮 Future Improvements
1. Fine-tune on medical-specific documents

2. Add document summarization on upload

3. Support for multiple file uploads

4. Add voice input/output integration

5. Deploy via Docker / Streamlit Cloud / Hugging Face Spaces

