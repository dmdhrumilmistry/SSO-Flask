from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    id: str = Field(default_factory=str(uuid4()))
    username: str
    age: str
    created_at:str = Field(default_factory=str(datetime.now()))