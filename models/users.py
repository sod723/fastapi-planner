from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr
from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user1@test.pri",
                "username": "test123",
                "events": [],
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str