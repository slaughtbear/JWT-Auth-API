from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import repository
from app.users.models import User
from app.users.schemas import UserUpdate


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