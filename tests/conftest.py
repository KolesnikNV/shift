import asyncio
import os

import pytest
from shift.settings import TEST_DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
test_async_session = sessionmaker(
    test_engine, expire_on_commit=False, class_=AsyncSession
)
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def run_migrations():
    os.system("alembic init migrations")
    os.system('alembic revision --autogenerate -m "test running migrations"')
    os.system("alembic upgrade heads")
