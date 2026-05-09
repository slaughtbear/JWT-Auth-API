from datetime import datetime, timedelta, timezone

import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.configuration import settings
from app.core.security import verify_password, DUMMY_HASH
from app.auth.repository import get_user_by_username
from app.users.models import User


async def authenticate_user(username: str, password: str, db: AsyncSession) -> User | bool:
    user = await get_user_by_username(username, db)

    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt