from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

from planner.models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]] = None

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": "fastapi@naver.com",
            "username": "strong!!",
            "events": [],
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
