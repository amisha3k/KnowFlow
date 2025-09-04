from fastapi import FastAPI
from pydantic import BaseModel
from app.vectorstore_utils import create_faiss_index, retrieve_relevent_docs
from app.chat_utils import get_chat_model,ask_chat_model
from app.config import EURI_API_KEY

app=FastAPI()

#/upload_docs/ → FAISS → /chat/ → model → answer

chat_model=get_chat_model(EURI_API_KEY)
vectorstore=None

class Query(BaseModel):
    question: str

@app.post("/upload_docs/")
async def upload_docs(chunks : list[str]):
    vectorstore=create_faiss_index(chunks)
    return { "status": "Document processed successfully"}    

@app.post("/chat")
async def chat(query: Query):
    if not vectorstore:
        return {"error": "no document uploaded"}

    relevent_docs=retrieve_relevent_docs(vectorstore,query.question)
    context="\n\n".join([doc.page_content for doc in relevent_docs])

    system_prompt=f"""
    You are DocuChat Pro, an intelligent document assistant.
    Relevant Documents:
    {context}
    User Question : {query.question}
    Answer:
    """
    response=ask_chat_model(chat_model,system_prompt)
    return {"answer": response}


