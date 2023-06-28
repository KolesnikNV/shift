import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from psycopg2 import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from shift.api.auth import (
    decode_access_token,
    generate_access_token,
    get_token,
)
from shift.api.models import ShowUser, UserCreate, UserToken, UserUpdate
from shift.db.crud import check_is_admin, get_user_by_id, get_user_id
from shift.db.models import User
from shift.db.session import get_db

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
user_router = APIRouter()
templates = Jinja2Templates(directory="/Users/nikitakolesnik/shift/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


@user_router.post("/login/", response_model=UserToken)
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    data = await request.json()
    user_id = data["user_id"]
    password = data["password"]
    user = await get_user_id(user_id, db)
    if user and user.password == password:
        token = generate_access_token(user.user_id)
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error",
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
    if not user.is_admin:
        raise HTTPException(
            status_code=403, detail="Only admins can create users"
        )

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
        await db.commit()
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=403, detail=f"Database error: {err}")
    user_id = user.user_id
    show_user = ShowUser(
        user_id=user_id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
        salary=user.salary,
        salary_increase_date=user.salary_increase_date,
    )
    return show_user


@user_router.get("/user/{user_id}/", response_model=ShowUser)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    token: str = Depends(get_token),
):
    decoded_token = decode_access_token(token=token)
    user_id = decoded_token.get("user_id")
    user = await check_is_admin(user_id, db)
    if user.is_admin:
        user = await get_user_by_id(user_id, db)
    elif user_id == user.user_id:
        user = await get_user_by_id(user_id, db)
    else:
        raise HTTPException(
            status_code=403,
            detail="Only admins or user with this id can get this information ",
        )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can patch users",
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
        await db.commit()
        await db.refresh(user)
    except IntegrityError as err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {err}",
        )

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
