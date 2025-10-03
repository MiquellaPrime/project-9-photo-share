from uuid import UUID, uuid4

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, str_255
from .mixins import TimestampMixin


class PhotoOrm(TimestampMixin, Base):
    __tablename__ = "photos"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    cloudinary_id: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    description: Mapped[str_255 | None]
