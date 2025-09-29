from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, str_255
from .mixins import TimeMixin


class PhotoOrm(Base, TimeMixin):
    __tablename__ = "photos"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str_255 | None]
