import uuid

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique user identifier",
    )
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(
        String,
        nullable=False,
        unique=True,
    )
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    salary = Column(Integer, nullable=False, comment="Current salary")
    salary_increase_date = Column(
        String, nullable=False, comment="Expected salary increase date:"
    )
