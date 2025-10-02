from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .associations import photos_tags
from .base import Base
from .mixins import TimestampMixin


class TagOrm(TimestampMixin, Base):
    __tablename__ = "tags"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    photos = relationship(
        "PhotoOrm", secondary=photos_tags, back_populates="tags", lazy="selectin"
    )
