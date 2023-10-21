from typing import Dict, List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    auth_method: str
    class Config:
        orm_mode = True

class UserRegister(BaseModel):
    name: str
    email: str
    auth_method: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    auth_method: Optional[str]

class UserLogin(BaseModel):
    email: str
    auth_method: str