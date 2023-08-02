from typing import List, Optional

from beanie import Document
from pydantic import BaseModel


class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    creator: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "fast api book launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "we will be discussing the contents of the fast api ...",
                "tags": ["python", "fastapi", "book", "..."],
                "location": "location description",
            }
        }

    class Settings:
        name = "events"


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "fast api book launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "we will be discussing the contents of the fast api ...",
                "tags": ["python", "fastapi", "book", "..."],
                "location": "location description",
            }
        }
