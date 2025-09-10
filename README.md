# Medical Bot AI Agent (RAG-Based)

Medical Bot AI Agent is a **Retrieval-Augmented Generation (RAG)** project designed to provide intelligent responses and assistance for medical-related queries. It integrates a Streamlit frontend with a FastAPI backend and leverages state-of-the-art AI libraries for embedding, retrieval, and document handling.

---

## Features

- **RAG-Based AI**: Uses semantic search to retrieve relevant medical information from PDFs or documents.  
- **Streamlit Frontend**: Interactive web interface for easy user interaction.  
- **FastAPI Backend**: Serves API endpoints for AI inference and document handling.  
- **Document Handling**: Supports PDF uploads and extraction using `fpdf` and `pypdf`.  
- **Semantic Search**: Powered by `faiss-cpu` and `sentence-transformers` for fast and accurate retrieval.  
- **LangChain Integration**: Manages conversational memory, prompts, and retrieval logic.  

---

## Tech Stack

- **Frontend**: Streamlit  
- **Backend**: FastAPI, Uvicorn  
- **RAG & NLP**: LangChain, LangChain Community, FAISS, Sentence Transformers  
- **Document Processing**: PyPDF, FPDF  
- **Data Validation**: Pydantic  

---

## Dependencies

- streamlit
- faiss-cpu
- langchain
- langchain_community
- fpdf
- pypdf
- sentence-transformers
- fastapi
- pydantic
- uvicorn

---

Step 2: Install Dependencies

Install all required packages in one command:

pip install streamlit faiss-cpu langchain langchain_community fpdf pypdf sentence-transformers fastapi pydantic uvicorn


Note: This installs everything needed for both backend and frontend.

Running the Project
Backend (FastAPI)

Open a terminal in the Medical_bot folder.

Run:

uvicorn backend.main:app --host 0.0.0.0 --port 8000


Backend will be available at: http://localhost:8000

Frontend (Streamlit)

Open another terminal in the Medical_bot/frontend folder.

Run:

streamlit run app.py --server.address=0.0.0.0 --server.port=8501


Frontend will be available at: http://localhost:8501

Optional: Run with Docker

If you want to use Docker, follow these steps:

Make sure Docker and Docker Compose are installed.

Build and run containers:

docker-compose up --build


Backend: http://localhost:8000

Frontend: http://localhost:8501

Project Structure
Medical_bot/
│
├── backend/                 # FastAPI backend code
│   ├── main.py
│   └── ...
│
├── frontend/                # Streamlit frontend code
│   ├── app.py
│   └── ...
│
├── Dockerfile.backend       # Dockerfile for backend (optional)
├── Dockerfile.frontend      # Dockerfile for frontend (optional)
├── docker-compose.yml       # Docker compose file (optional)
└── README.md                # This file







