import uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from enum import Enum

Base = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"
    ROLE_PORTAL_SUPERADMIN = "ROLE_PORTAL_SUPERADMIN"


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
    roles = Column(ARRAY(String), nullable=False)
    salary = Column(Integer, nullable=False, comment="Current salary")
    salary_increase_date = Column(
        String, nullable=False, comment="Expected salary increase date:"
    )

    @property
    def is_superadmin(self) -> bool:
        return PortalRole.ROLE_PORTAL_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return PortalRole.ROLE_PORTAL_ADMIN in self.roles
