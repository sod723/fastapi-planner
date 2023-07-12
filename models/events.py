from pydantic import BaseModel
from typing import Optional, List
from beanie import Document


# 도큐먼트 입력을 위한 모델
class Event(Document):
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "제목",
                "image": "http://test.pri/image.png",
                "description": "설명",
                "tags": ["python", "fastapi", "web"],
                "location": "Google Meet"
            }
        }

    class Settings:
        name = "events" #컬렉션이름


# 업데이트처리를 위한 pydantic 모델(업데이트 문제 있다면 "= None" 추가)
class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "제목",
                "image": "http://test.pri/image.png",
                "description": "설명",
                "tags": ["python", "fastapi", "web"],
                "location": "Google Meet"
            }
        }

