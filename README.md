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

## Usage

- Open the Streamlit app in your browser: http://localhost:8501
- Upload PDFs or documents to the app.
- Enter medical queries in the chat interface.
- The AI agent will retrieve relevant information and provide responses.

---

## Installation

> Make sure you have Python 3.10+ installed.

1. Clone the repository:

```bash
git clone https://github.com/your-username/medical_bot.git
cd medical_bot
```
2. Upgrade pip:
```bash
pip install --upgrade pip
```
3. Install Dependencies:
```bash
pip install streamlit faiss-cpu langchain langchain_community fpdf pypdf sentence-transformers fastapi pydantic uvicorn euriapi
```
4. Running the Backend (FastAPI):
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```
5. Running the Frontend (Streamlit):
```bash
cd frontend
streamlit run main.py
```
6. Using Docker (Optional):
```bash
docker build -t medical_bot:latest .
docker run -p 8501:8501 -p 8000:8000 medical_bot:latest
```

---

## Architecture Flow Diagram

```mermaid
flowchart TD
    A[Hugging Face Space Hosting] --> B[Docker Containerized Environment]
    B --> C1[Streamlit Frontend: PDF Upload UI]
    B --> C2[FastAPI Backend: PDF Processing API]
    C1 --> C2
    C2 --> D[PDF Document Upload & Text Extraction / Embeddings]


