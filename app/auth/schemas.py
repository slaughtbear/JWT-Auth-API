from typing import Annotated

from pydantic import BaseModel, BeforeValidator, EmailStr, Field

from app.core.utils import get_clean_lower_text, get_clean_title_text


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserRegister(BaseModel):
    username: Annotated[str, BeforeValidator(lambda v: v.strip())] = Field(min_length=3, max_length=30)
    email: Annotated[EmailStr, BeforeValidator(get_clean_lower_text)]
    full_name: Annotated[str, BeforeValidator(get_clean_title_text)] = Field(min_length=3, max_length=255)
    password: Annotated[str, BeforeValidator(lambda v: v.strip())] = Field(min_length=12, max_length=255, serialization_alias="hashed_password")