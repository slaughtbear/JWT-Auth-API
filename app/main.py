from fastapi import FastAPI

from app.users.router import router as users_router


app = FastAPI(
    title="JWT Auth API",
    version="1.0"
)


app.include_router(
    router = users_router,
    prefix = "/api/v1/admin/users",
    tags = ["Users"]
)