from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, str_255, uuid_pk
from .mixins import TimestampMixin


class PhotoOrm(TimestampMixin, Base):
    __tablename__ = "photos"

    uuid: Mapped[uuid_pk]
    cloudinary_url: Mapped[str] = mapped_column(Text)
    description: Mapped[str_255 | None]
