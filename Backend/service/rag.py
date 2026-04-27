from vectordb.db import client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
import numpy as np


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def file_upload(docs):
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=100,
        chunk_overlap=20
    )
    
    
    
    doc = [Document(page_content=docs)]
    
    chunks = splitter.split_documents(doc)
    
    embeddings = model.encode([chunk.page_content for chunk in chunks]).tolist()
    
    collection = client.get_or_create_collection(name="documents")

    
    collection.add(
        ids=[str(i) for i in range(len(chunks))],          
        embeddings=embeddings,
        documents=[chunk.page_content for chunk in chunks]   
    )
        

def search(query,collectionName):
    
    collection = client.get_collection(collectionName)
    query_embedding = model.encode(query).tolist()
    
    
    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "distances"]
)

    filtered_results = [
        {
            "document": doc,
            "similarity_score": 1 - distance
        }
        for doc, distance in zip(
            results["documents"][0],
            results["distances"][0]
        )
        if (1 - distance) > 0.5
    ]
    
    if len(filtered_results) > 0:
        print({'query':query,'documents':filtered_results})
        return {'query':query,'documents':filtered_results}
    else:
        return {'query':query,'documents':[]}
        
