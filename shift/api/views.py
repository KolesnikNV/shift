import logging
import uuid

from api.models import ShowUser, UserCreate
from db.crud import check_is_admin, get_user_id
from db.models import User
from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shift.api.auth import (
    decode_access_token,
    generate_access_token,
    get_token,
)
from shift.api.models import UserToken, UserUpdate


logger = logging.getLogger(__name__)
logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
user_router = APIRouter()
templates = Jinja2Templates(directory="/Users/nikitakolesnik/shift/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


@user_router.post("/login/", response_model=UserToken)
async def login(
    user_id: str, password: str, db: AsyncSession = Depends(get_db)
):
    user = await get_user_id(user_id, db)

    if user and user.password == password:
        token = generate_access_token(user.user_id)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ошибка аутентификации",
        )


@user_router.post("/user/create/", response_model=ShowUser)
async def create_user(
    body: UserCreate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
) -> ShowUser:
    decoded_token = decode_access_token(token=token)
    user_id = decoded_token.get("user_id")
    user = await check_is_admin(user_id, db)
    if not user:
        raise HTTPException(
            status_code=403, detail="Only admins can create users"
        )

    async with db.begin():
        user = User(
            name=body.name,
            surname=body.surname,
            email=body.email,
            password=body.password,
            salary=body.salary,
            salary_increase_date=body.salary_increase_date,
        )
        try:
            db.add(user)
            await db.flush()
        except IntegrityError as err:
            logger.error(err)
            raise HTTPException(
                status_code=500, detail=f"Database error: {err}"
            )
        user_id = user.user_id
        show_user = ShowUser(
            user_id=user_id,
            name=user.name,
            surname=user.surname,
            email=user.email,
            salary=user.salary,
            salary_increase_date=user.salary_increase_date,
        )
        return show_user


@user_router.get("/user/{user_id}/", response_model=ShowUser)
async def get_user_by_id(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> ShowUser:
    async with db.begin():
        user = await db.get(User, user_id)
        return user


@user_router.patch("/user/{user_id}/", response_model=ShowUser)
async def patch_user(
    user_id: uuid.UUID,
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
) -> ShowUser:
    decoded_token = decode_access_token(token=token)
    admin_id = decoded_token.get("user_id")
    admin = await check_is_admin(admin_id, db)
    if not admin:
        raise HTTPException(
            status_code=403, detail="Only admins can patch users"
        )

    user = await get_user_id(user_id, db)

    if body.name is not None:
        user.name = body.name
    if body.surname is not None:
        user.surname = body.surname
    if body.email is not None:
        user.email = body.email
    if body.password is not None:
        user.password = body.password
    if body.salary is not None:
        user.salary = body.salary
    if body.salary_increase_date is not None:
        user.salary_increase_date = body.salary_increase_date
    if body.is_admin is not None:
        user.is_admin = body.is_admin

    try:
        await db.refresh(user)
        await db.flush()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

    show_user = ShowUser(
        user_id=user.user_id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
        salary=user.salary,
        salary_increase_date=user.salary_increase_date,
        is_admin=user.is_admin,
    )
    return show_user


@user_router.delete("/user/{user_id}/")
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
) -> None:
    user = await get_user_id(user_id, db)
    decoded_token = decode_access_token(token=token)
    admin_id = decoded_token.get("user_id")
    admin = await check_is_admin(admin_id, db)
    if not admin:
        raise HTTPException(
            status_code=403, detail="Only admins can create users"
        )
    await db.delete(user)
    await db.commit()
    message = "User has been successfully deleted"
    return message
