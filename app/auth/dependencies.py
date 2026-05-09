from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer

from app.auth.schemas import TokenData
from app.core.database import get_session
from app.core.configuration import settings
from app.auth.repository import get_user_by_username
from app.users.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)

    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user = await get_user_by_username(db=db, username=token_data.username)

    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_admin(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You don't have enough permissions."
        )
    
    return user