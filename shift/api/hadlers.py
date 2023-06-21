from db.dals import UserDAL
from db.session import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ShowUser, UserCreate

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                salary=body.salary,
                salary_increase_date=body.salary_increase_date,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active,
                salary=user.salary,
                salary_increase_date=user.salary_increase_date,
            )


@user_router.post("/user", response_model=ShowUser)
async def create_user(
    body: UserCreate, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    return await _create_new_user(body, db)
