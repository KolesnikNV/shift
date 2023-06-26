from typing import Generator

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import shift.settings as settings
from shift.db.models import User

engine = create_async_engine(
    settings.REAL_DATABASE_URL, future=True, echo=True
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db() -> Generator:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def count_users():
    async for db in get_db():
        async with db.begin():
            count = await db.scalar(func.count(User.user_id))
            return count
