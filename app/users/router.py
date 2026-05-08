from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.users.schemas import UserCreate, UserResponse
from app.users import repository


router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    return await repository.create_user(user_data.model_dump(by_alias=True), db)


@router.get("/", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_session)):
    return await repository.read_users(db)