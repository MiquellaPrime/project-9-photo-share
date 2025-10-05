<<<<<<< Updated upstream
=======
from typing import TYPE_CHECKING

>>>>>>> Stashed changes
from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.schemas import UserRoles

from .base import Base, bool_f, bool_t, int_pk
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .photos import PhotoOrm


class UserOrm(TimestampMixin, Base):
    __tablename__ = "users"

<<<<<<< Updated upstream
    id: Mapped[int] = mapped_column(primary_key=True)
=======
    id: Mapped[int_pk]
>>>>>>> Stashed changes
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    role: Mapped[str] = mapped_column(default=UserRoles.USER)
    is_active: Mapped[bool_t]
    is_verified: Mapped[bool_f]

    photos: Mapped[list["PhotoOrm"]] = relationship(back_populates="user")
