from datetime import datetime, timezone
from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, BeforeValidator
from app.core.utils import get_clean_lower_text, get_clean_title_text


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"


class UserBase(BaseModel):
    username: Annotated[str, BeforeValidator(lambda v: v.strip())] = Field(min_length=3, max_length=30)
    email: str
    full_name: str
    role: Role | None = "user"
    disabled: bool | None = None


class UserCreate(UserBase):
    email: Annotated[EmailStr, BeforeValidator(get_clean_lower_text)]
    full_name: Annotated[str, BeforeValidator(get_clean_title_text)] = Field(min_length=3, max_length=255)
    password: Annotated[str, BeforeValidator(lambda v: v.strip())] = Field(min_length=12, max_length=255)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=8, max_length=16)
    full_name: Annotated[str | None, BeforeValidator(get_clean_title_text)] = Field(default=None, min_length=3, max_length=255)
    role: Role | None = None
    disabled: bool | None = None
    password: str | None = None
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime