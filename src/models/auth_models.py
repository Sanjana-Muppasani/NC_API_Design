from pydantic import BaseModel
from datetime import datetime

class RegisterRequest(BaseModel): 
    name : str
    email : str
    password : str

class RegisterRequestResponseBody(BaseModel): 
    id : int
    name : str
    email : str
    created_at : datetime

class RegisterRequestResponse(BaseModel):
    user: RegisterRequestResponseBody


class LoginRequest(BaseModel): 
    email: str 
    password : str
