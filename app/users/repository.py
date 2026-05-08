from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models import User


async def search_user_by_id(id: int, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == id))
    user = result.scalars().first()
    return user


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


async def update_user(user_data: dict, db_user: User, db: AsyncSession) -> User:
    for key, value in user_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user