from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    role: Mapped[str] =   mapped_column(String(20), default="user", nullable=False)
    disabled: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(server_default=None, onupdate=func.now())