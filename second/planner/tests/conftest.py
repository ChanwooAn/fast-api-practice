import asyncio
import httpx
import pytest

from planner.main import app
from planner.database.connection import Settings
from planner.models.events import Event
from planner.models.users import User


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"

    await test_settings.initialize_database()


@pytest.fixture(scope="session")
async def default_client():
    await init_db() #db를 먼저 초기화
    async with httpx.AsyncClient(app=app, base_url="http://app") as client: #application을 asyncclient로 호출. async client는 test session이 끝날 때 까지 유지
        yield client
        await Event.find_all().delete()
        await User.find_all().delete()
