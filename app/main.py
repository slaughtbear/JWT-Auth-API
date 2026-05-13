from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.users.router import router as users_router

from app.core.configuration import settings


app = FastAPI(
    title="JWT Auth API",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins = [settings.frontend_url],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(
    router = auth_router,
    prefix = "/api/v1/auth",
    tags = ["Authentication"]
)


app.include_router(
    router = users_router,
    prefix = "/api/v1/admin/users",
    tags = ["Users"]
)