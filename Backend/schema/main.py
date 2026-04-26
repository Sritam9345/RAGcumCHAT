from pydantic import BaseModel,Field
from enum import Enum

class Role(str,Enum):
    
    user = "user"
    ai = "ai"

class userModel:
    
    name: str
    email: str
    password: str
    
    
class chatModel:
    userId: str
    message: list[str]
    role: Role
    threadId: str
    