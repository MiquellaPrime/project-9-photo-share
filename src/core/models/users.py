from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from src.schemas.enums import UserRoles

from .base import Base, bool_f, bool_t
from .mixins import TimestampMixin


class UserOrm(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(default=UserRoles.USER)
    is_active: Mapped[bool_t]
    is_verified: Mapped[bool_f]
