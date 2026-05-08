from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User


async def create_user(user_data: dict, db: AsyncSession) -> User:
    user_model = User(**user_data)
    db.add(user_model)
    await db.commit()
    await db.refresh(user_model)
    return user_model


async def read_users(db: AsyncSession) -> list[User]:
    statement = select(User)
    result = await db.execute(statement)
    users = result.scalars().all()
    return users