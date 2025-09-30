from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.enums import UserRole

from .base import UTC_NOW_SQL, Base, bool_f, bool_t, timestamp_tz


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(default=UserRole.user)
    is_active: Mapped[bool_t]
    is_verified: Mapped[bool_f]
    created_at: Mapped[timestamp_tz]
    updated_at: Mapped[timestamp_tz] = mapped_column(onupdate=UTC_NOW_SQL)
