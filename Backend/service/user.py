from schema.main import userModel , updateModel
from db.main import collection_user
from fastapi import HTTPException,status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import jwt
import os
from bson import ObjectId

load_dotenv()

key = os.getenv('JWT_SECRET')

def createUser(user: userModel):
    try:
       response = collection_user.find_one(
    {
        "name": user['name'],
        
    }
)       
       
       if response == None:
           response = collection_user.insert_one({
               "name": user['name'],
               "password": user['password']
           })
           
           user_id = str(response)
           token = jwt.encode({"user_id": user_id}, key, algorithm="HS256")
           
           return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "user created successfully",'token':token}
    )
       else:
           return JSONResponse(
    status_code=status.HTTP_409_CONFLICT,
    content={"message": "User already exists"}
)
           
    except Exception as e:
        raise  e


def loginUser(user: userModel):
    try:
       response = collection_user.find_one(
    {
        "name": user['name'],
        "password": user['password']
        
    }
)              
       if response == None:
           return JSONResponse(
    status_code=status.HTTP_409_CONFLICT,
    content={"message": "User doesnt exists"}
)
       else:
           user_id = str(response['_id'])
           token = jwt.encode({"user_id": user_id,'name':response['name']}, key, algorithm="HS256")
           return JSONResponse(
    status_code=status.HTTP_200_OK,
    content={"message": "Login Sucessful!","token":token}
)
           
    except Exception as e:
        raise  e


def updateUser(user_id,user: updateModel):
    update_data = {}

    if user.name is not None:
        update_data["name"] = user.name

    if user.password is not None:
        update_data["password"] = user.password
    
    if user.socketID is not None:
        update_data['socketID'] = user.socketID

    if not update_data:
        return {"message": "Nothing to update"}

    response = collection_user.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": update_data}
    )