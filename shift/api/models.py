import re
import uuid

from db.models import User
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    salary: float
    salary_increase_date: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    salary: float
    salary_increase_date: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
