from pydantic import BaseModel
from typing import Optional


class CreateUserBase(BaseModel):
    full_name: str
    email: str
    password: str


class UserBase(BaseModel):
    full_name: str
    email: str
    password: str
    is_active: bool
