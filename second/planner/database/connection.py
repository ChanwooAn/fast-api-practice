from pathlib import Path
from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic import BaseSettings

from planner.models.events import Event
from planner.models.users import User


from dotenv import load_dotenv
from pathlib import Path

# .env 파일의 경로 설정 (planner/database/ 디렉토리에서 상위 디렉토리로 이동)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    DATABASE_NAME: str = "planner-database"
    SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client[self.DATABASE_NAME], document_models=[Event, User]
        )
        # database client를 설정한다. sql model에서 생성한 몽고 엔진 버전과 문서 모델을 인수로 설정한다.

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return

    async def get(self, userid: PydanticObjectId) -> Any:
        doc = await self.model.get(userid)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs

    # 스키마 모델을 인수로 받는다. 클라이언트가 보낸 put 요청에 의해 변경된 필드가 저장된다.
    async def update(self, userid: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = userid
        des_body = body.dict()
        des_body = {k: v for k, v in des_body.items() if v is not None}
        # key와 value이며 des_body.items를 순회하며 None이 아닐 경우에만 des_body에 추가한다는 뜻이다.
        update_query = {"$set": {field: value for field, value in des_body.items()}}

        doc = await self.get(doc_id)
        if not doc:
            return False

        await doc.update(update_query)
        return doc

    async def delete(self, userid: PydanticObjectId) -> bool:
        doc = await self.get(userid)
        if not doc:
            return False
        await doc.delete()
        return True
