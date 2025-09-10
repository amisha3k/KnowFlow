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

## Installation

> Make sure you have Python 3.10+ installed.

1. Clone the repository:

```bash
git clone https://github.com/your-username/medical_bot.git
cd medical_bot
