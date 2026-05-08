from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.users.schemas import UserCreate
from app.users import repository


router = APIRouter()


@router.post("/")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await repository.create_user(user.model_dump(by_alias=True), db)