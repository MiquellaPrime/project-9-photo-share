from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import photos_tags
from .base import Base
from .mixins import TimestampMixin


class PhotoOrm(TimestampMixin, Base):
    __tablename__ = "photos"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    tags = relationship(
        "TagOrm", secondary=photos_tags, back_populates="photos", lazy="selectin"
    )
