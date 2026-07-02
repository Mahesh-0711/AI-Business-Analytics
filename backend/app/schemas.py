from datetime import datetime

from pydantic import BaseModel, EmailStr


# ==========================
# Authentication
# ==========================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# ==========================
# Dataset
# ==========================

class DatasetResponse(BaseModel):
    id: int
    filename: str
    rows: int
    columns: int
    uploaded_at: datetime

    class Config:
        from_attributes = True