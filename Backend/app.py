from router.user import userRouter
from router.rag import ragRouter
from fastapi import FastAPI


app = FastAPI()


@app.get('/')
def home():
    return {"message":"Hi there"}



app.include_router(userRouter,prefix='/user')
app.include_router(ragRouter,prefix='/rag')