import uvicorn
from api.auth import auth_router
from api.views import user_router
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

from shift.db.models import User
from shift.db.session import count_users, get_db

app = FastAPI(title="shift")

app.mount(
    "/static",
    StaticFiles(directory="/Users/nikitakolesnik/shift/static"),
    name="static",
)


@app.on_event("startup")
async def populate_admin():
    async for db in get_db():
        async with db.begin():
            user_count = await count_users()

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


main_api_router = APIRouter()
main_api_router.include_router(auth_router, tags=["auth"])
main_api_router.include_router(user_router, tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
