from fastapi import FastAPI, APIRouter, Request,HTTPException
from pydantic import BaseModel,Field
from db.main import collection_user
from service.user import createUser




userRouter = APIRouter()



@userRouter.post("/login")
async def user_handler(request: Request):
    body = await request.json()
    try:
        createUser(user=body)
    except Exception as e:
        raise e
    

@userRouter.post("/signup")
async def user_handler(request: Request):
    body = await request.json()
    
    try:
        response = collection_user.insert_one({
            
            
        })
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@userRouter.get("/chat")
async def user_handler():
    return {"message": "This is a dummy user endpoint"}