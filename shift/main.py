import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
import logging
from shift.api.auth import auth_router
from shift.api.views import user_router
from shift.db.models import User
from shift.db.session import count_users, get_db

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
app = FastAPI(title="shift")


@app.on_event("startup")
async def populate_admin():
    async for db in get_db():
        async with db.begin():
            user_count = await count_users(db)

            if user_count == 0:
                admin = User(
                    name="Admin",
                    surname="Admin",
                    email="admin@mail.ru",
                    password="totally_secret_password",
                    is_admin=True,
                    salary=0,
                    salary_increase_date="",
                )
                db.add(admin)
                await db.commit()
                print(
                    f"Admin's user_id and password is: {admin.user_id, admin.password}"
                )
                return admin.user_id, admin.password
            else:
                admin_dict = await get_admin_user()
                admin = admin_dict["User"]
                print(
                    f"Admin's user_id and password is: {admin.user_id, admin.password}"
                )
                return admin.user_id, admin.password


async def get_admin_user():
    async for session in get_db():
        query = select(User).where(User.is_admin == True)
        result = await session.execute(query)
        admin_row = result.fetchone()
        admin_dict = dict(admin_row._asdict()) if admin_row else None
        return admin_dict


main_api_router = APIRouter()
main_api_router.include_router(auth_router, tags=["auth"])
main_api_router.include_router(user_router, tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
