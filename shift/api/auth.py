from datetime import datetime, timedelta
from uuid import UUID

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from shift.settings import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_token(token: str = Depends(oauth2_scheme)) -> str:
    if token is None:
        return None
    return token


def generate_access_token(user_id: UUID) -> str:
    delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_date = datetime.utcnow() + delta
    payload = {"user_id": str(user_id), "exp": expires_date}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    user_id = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return token


def decode_access_token(token: str = Depends(get_token)) -> dict:
    user_id = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return user_id


def validate_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
