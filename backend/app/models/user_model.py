from pydantic import BaseModel, EmailStr
from typing import Literal

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: Literal["owner", "employee"]  # only two roles allowed

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str