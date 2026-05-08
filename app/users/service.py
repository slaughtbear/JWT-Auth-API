from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash

from app.users import repository
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


async def create_user(user_data: UserCreate, db: AsyncSession) -> User:
    user_data.password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump(by_alias=True)
    user_model = User(**user_dict)
    new_user = await repository.create_user(user_model, db)
    return new_user


async def update_user_by_id(id: int, user_data: UserUpdate, db: AsyncSession) -> User:
    db_user = await repository.search_user_by_id(id, db)

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    updated_user = await repository.update_user(update_data, db_user, db)
    return updated_user


async def delete_user_by_id(id: int, db: AsyncSession) -> bool:
    db_user = await repository.search_user_by_id(id, db)

    if not db_user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found."
        )
    
    return await repository.delete_user(db_user, db)