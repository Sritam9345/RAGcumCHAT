from vectordb.db import client
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document


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
    include=[collectionName, "distances"]
)
    print(results[collectionName][0])
    return results[collectionName][0]


search('''The village of Aster Hollow sat at the edge of a forest so old that no one could agree where it ended.
Some said the trees reached into neighboring kingdoms.''','documents')