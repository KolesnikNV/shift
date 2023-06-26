import re
from typing import Optional
import uuid

from db.models import User
from fastapi import Depends, HTTPException
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
    salary: int
    salary_increase_date: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    is_admin: bool
    salary: int
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


class UserUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin: Optional[bool]
    salary: Optional[int]
    salary_increase_date: Optional[str]


class UserToken(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    password: str
