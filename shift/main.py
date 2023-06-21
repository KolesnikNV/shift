import uvicorn
from api.hadlers import user_router
from fastapi import FastAPI
from fastapi.routing import APIRouter

app = FastAPI(title="shift")


main_api_router = APIRouter()

main_api_router.include_router(user_router, tags=["user"])
app.include_router(main_api_router)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
