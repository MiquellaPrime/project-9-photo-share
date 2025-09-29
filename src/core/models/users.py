from sqlalchemy.orm import Mapped, mapped_column

from src.schemas import UserRoles

from .base import Base, bool_f, bool_t, int_pk, str_150
from .mixins import TimestampMixin


class UserOrm(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int_pk]
    email: Mapped[str_150] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[str] = mapped_column(default=UserRoles.USER)
    is_active: Mapped[bool_t]
    is_verified: Mapped[bool_f]
