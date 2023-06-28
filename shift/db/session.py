from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from shift.settings import REAL_DATABASE_URL
from shift.db.models import User

engine = create_async_engine(REAL_DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def count_users(db):
    count = await db.scalar(select(func.count(User.user_id)))
    return count
