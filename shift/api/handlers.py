from datetime import datetime, timedelta

import jwt
from db.dals import UserDAL
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ShowUser, UserCreate, UserToken, oauth2_scheme

user_router = APIRouter()
templates = Jinja2Templates(directory="/Users/nikitakolesnik/shift/templates")
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def _create_new_user(
    body: UserCreate, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                password=body.password,
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


@user_router.post("/user/", response_model=ShowUser)
async def create_user(
    body: UserCreate, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    return await _create_new_user(body, db)


@user_router.post("/login/", response_model=UserToken)
async def login(
    user_id: str, password: str, db: AsyncSession = Depends(get_db)
):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_email(user_id)

            if user and user.password == password:
                token = generate_access_token(user.user_id)
                return {"access_token": token, "token_type": "bearer"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Ошибка аутентификации",
                )


def get_token(authorization: str = Depends(oauth2_scheme)) -> str:
    print("authorization =", authorization)
    if authorization is None:
        return None
    return authorization


@user_router.get("/user/{user_id}/")
async def get_user(
    user_id: str,
    token: str = Depends(get_token),
    db: AsyncSession = Depends(get_db),
):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.get_user_by_id(user_id)
            if user:
                validate_token(token)
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Такого пользователя нет",
                )


def generate_access_token(user_id: UUID) -> str:
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_date = datetime.utcnow() + delta
    payload = {"user_id": str(user_id), "exp": expires_date}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_token(authorization: str):
    try:
        jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации",
        )
