from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        salary: float,
        salary_increase_date: str,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            salary=salary,
            salary_increase_date=salary_increase_date,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def create_admin(
        self,
        name: str,
        surname: str,
        email: str,
        password: str,
        salary: float,
        salary_increase_date: str,
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            password=password,
            salary=salary,
            salary_increase_date=salary_increase_date,
            is_admin=True,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def get_user_by_id(self, user_uuid) -> User:
        user = await self.db_session.get(User, user_uuid)
        return user

    async def get_user_by_email(self, email) -> User:
        user = await self.db_session.get(User, email)
        print(user)
        return user
