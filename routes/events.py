from typing import List
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, HTTPException, status, Depends
from database.connection import Database
from models.events import Event, EventUpdate
from auth.authenticate import authenticate

event_router = APIRouter(
    tags=["Events"]
)
# 작성된 모든 이벤트들을 임시 저장하기 위한 리스트(DB사용시 불필요)

event_database = Database(Event)

# 전체 이벤트 조회
@event_router.get("/", response_model=List[Event])
async def get_all_events() -> List[Event]:
    events = await event_database.get_all()
    return events


# 특정 id event 조회
@event_router.get("/{event_id}", response_model=Event)
async def get_event(event_id: int) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 ID 입니다"
        )
    return event

# 이벤트 생성
@event_router.post("/new")
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.save(body)
    return {"message": "event created"}

# 이벤트 전체 삭제
@event_router.delete("/")
async def delete_all_events() -> dict:
    event = await event_database.delete_all()
    return {"message": "all events deleted"}

# 특정 id 이벤트 삭제
@event_router.delete("/{event_id}")
async def delete_event(id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="잘못된 ID 를 입력했습니다"
        )
    return {
        "message": "해당 이벤트는 삭제되었습니다"
    }

# 이벤트 수정
@event_router.put("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)) -> Event:
    event = await event_database.get(id)
    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Operation not allowed"
        )
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event

