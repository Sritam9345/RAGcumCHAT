from fastapi import FastAPI, APIRouter, Request,HTTPException
from pydantic import BaseModel,Field
from db.main import collection_user
from service.user import createUser,loginUser




userRouter = APIRouter()



@userRouter.post("/login")
async def user_handler(request: Request):
    body = await request.json()
    try:
        response = loginUser(user=body)
        return response
    except Exception as e:
        raise e
    

@userRouter.post("/signup")
async def user_handler(request: Request):
    body = await request.json()
    
    try:
       response = createUser(body)
       return response
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@userRouter.get("/chat")
async def user_handler():
    return {"message": "This is a dummy user endpoint"}