from sqlalchemy import TIMESTAMP, DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.schemas.enums import UserRole


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(default=UserRole.user)
    is_active: Mapped[bool] = mapped_column(server_default=text("TRUE"))
    is_verified: Mapped[bool] = mapped_column(server_default=text("TRUE"))
    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
