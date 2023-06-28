import uuid

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shift.db.models import User
from shift.db.session import get_db


async def get_user_id(user_id: uuid.UUID, db: AsyncSession) -> User:
    async with db.begin():
        stmt = select(User).where(User.user_id == user_id)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


async def check_is_admin(user_id, db: AsyncSession = Depends(get_db)) -> User:
    async with db:
        user = await db.get(User, user_id)
        if user:
            return user
        else:
            return None


async def get_user_by_email(email, db: AsyncSession = Depends(get_db)) -> User:
    async with db.begin():
        user = await db.get(User, email=email)
        return user


async def get_user_by_id(user_id, db: AsyncSession = Depends(get_db)) -> User:
    async with db.begin():
        user = await db.get(User, user_id)
        return user
