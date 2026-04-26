from schema.main import userModel
from db.main import collection_user
from fastapi import HTTPException


def createUser(user: userModel):
    try:
        response = response = collection_user.find_one(
    {
        "name": user['name'],
        "email": user['email'],
        "password": user['password']
    }
)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")

