from uuid import UUID, uuid4

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import UTC_NOW_SQL, Base, str_255, timestamp_tz


class PhotoOrm(Base):
    __tablename__ = "photos"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str_255 | None]
    created_at: Mapped[timestamp_tz]
    updated_at: Mapped[timestamp_tz] = mapped_column(onupdate=UTC_NOW_SQL)
