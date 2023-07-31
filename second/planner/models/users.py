from pydantic import BaseModel, EmailStr
from typing import Optional, List
from planner.models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None

    class Config:
        json_schema_extra = {
            "example": "fastapi@naver.com",
            "password": "strong!!",
            "events": [],
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "email": "fastapi@naver.com",
            "password": "strong!!",
            "events": [],
        }
