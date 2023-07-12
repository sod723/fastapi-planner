from beanie import init_beanie, PydanticObjectId
from pydantic import BaseSettings, BaseModel
from typing import List, Optional, Any
from motor.motor_asyncio import AsyncIOMotorClient
from models.events import Event
from models.users import User

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DATABASE_NAME: Optional[str] = "mydb"
    SECRET_KEY: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 6  # 6 hour
    ALGORITHM = "HS256"

    async def init_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client[self.DATABASE_NAME], document_models=[Event, User])

    class Config:
        env_file = ".env"

class Database:
    def __init__(self, model: BaseModel):
        self.model = model

    # 생성처리(레코드 하나[문서의 인스턴스]를 데이터베이스 컬렉션에 추가한다
    async def save(self, document) -> None:
        await document.create()
        return

    # 조회 처리(get_all은 인수가 없고 컬렉션의모든 레코드를 불러온다)
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    # 변경 처리
    '''
    update() 메서드는 하나의 ID와 pydantic 스키마(모델)을 인수로 받는다. 스키마에는 클라이언트가 보낸 PUT 요청에 
    의해 변경된 필드가 저장된다. 변경된 요청 바디는 딕셔너리에 저장된 다음 None 값을 제외하도록 필터링된다.
    이 작업이 완료되면 변경 쿼리에 저장되고 beanie 의 update() 메서드를 통해 실행된다.
    '''

    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dict()

        des_body = {k: v for k, v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

        # 삭제처리(이 메서드는 해당 레코드가 있는지 확인하고 있으면 삭제한다)

    async def delete(self, id: PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True