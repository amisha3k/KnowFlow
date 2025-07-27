from langchain_community.vectorstores import FAISS
#from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from typing import List




#This model will be used to convert each input string into a high-dimensional vector (embedding).
#Embeds each text using the Hugging Face model,Stores the vectors in a FAISS index for fast similarity search.
def create_faiss_index(texts: List[str]):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2") 
    return FAISS.from_texts(texts,embeddings) 



#function to perform semantic search,vectorstore: the FAISS object (built above),
#query: the user's input (what you want to search for),
#k: the number of top results to return (default is 3).
def retrieve_relevent_docs(vectorstore, query: str , k: int = 3):
    docs=vectorstore.similarity_search(query, k=k)
    return docs


#Performs a similarity search against the FAISS index using the given query.
#Returns the top k documents most similar to the query (based on cosine similarity or L2 norm depending on config).