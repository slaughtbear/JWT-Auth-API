from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import check_admin

from app.core.database import get_session

from app.users import repository
from app.users.schemas import UserCreate, UserUpdate, UserResponse
from app.users import service


router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_session), admin = Depends(check_admin)):
    return await service.create_user(user_data, db)


@router.get("/", response_model=list[UserResponse])
async def read_users(db: AsyncSession = Depends(get_session), admin = Depends(check_admin)):
    return await repository.read_users(db)


@router.patch("/{id}", response_model=UserResponse)
async def update_user(id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_session), admin = Depends(check_admin)):
    return await service.update_user_by_id(id, user_data, db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: AsyncSession = Depends(get_session), admin = Depends(check_admin)) -> None:
    await service.delete_user_by_id(id, db)