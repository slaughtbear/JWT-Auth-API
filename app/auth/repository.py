from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


async def get_user_by_username(username: str, db: AsyncSession) -> User | None:
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalars().first()