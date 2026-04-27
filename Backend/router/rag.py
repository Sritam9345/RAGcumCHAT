from fastapi import FastAPI, APIRouter, Request,File,UploadFile
from service.rag import file_upload
import io
import pdfplumber
from service.rag import search

ragRouter = APIRouter()


@ragRouter.post('/ingest')
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
     text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    file_upload(text)

@ragRouter.get('/search')
async def getChunks(request: Request):
    
    body = await request.json()
    
    print(body)
    try:
       response = search(query=body['query'],collectionName=body['collectionName'])
       return response
    except:
        raise BaseException('hi there')
    


