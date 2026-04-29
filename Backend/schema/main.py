from pydantic import BaseModel,Field
from enum import Enum
from typing import Dict,Optional

class Role(str,Enum):
    
    user = "user"
    ai = "ai"


class userModel:
    
    name: str
    password: str
    socketID: str = ""
    
    
class chatModel:
    userId: str
    message: list[Dict[Role,str]]
    threadId: str

class updateModel(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    socketID: Optional[str] = None