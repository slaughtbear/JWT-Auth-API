from sqlalchemy.ext.asyncio import AsyncSession
from app.users.schemas import UserDB
from app.users.models import User


async def create_user(user_data: dict, db: AsyncSession) -> UserDB:
    user_model = User(**user_data)
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return user_model