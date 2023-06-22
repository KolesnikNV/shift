import uvicorn
from api.handlers import user_router
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="shift")
app.mount(
    "/static",
    StaticFiles(directory="/Users/nikitakolesnik/shift/static"),
    name="static",
)

main_api_router = APIRouter()

main_api_router.include_router(user_router, tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
