from fastapi import FastAPI, APIRouter, Request,File,UploadFile
from service.rag import file_upload
import io
import pdfplumber

ragRouter = APIRouter()


@ragRouter.post('/ingest')
async def ingest_file(file: UploadFile = File(...)):
    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
     text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
    file_upload(text)

@ragRouter.get('/search')
def getChunks():
    return 'hi'

