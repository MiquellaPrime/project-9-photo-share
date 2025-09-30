from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_255, uuid_pk
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .users import UserOrm


class PhotoOrm(TimestampMixin, Base):
    __tablename__ = "photos"

    uuid: Mapped[uuid_pk]
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
    )
    cloudinary_url: Mapped[str] = mapped_column(Text)
    description: Mapped[str_255 | None]

    user: Mapped["UserOrm"] = relationship(back_populates="photos")
