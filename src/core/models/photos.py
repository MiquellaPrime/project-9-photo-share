from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, str_255, timestamp_tz, uuid_pk
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
    tags: Mapped[list["TagOrm"]] = relationship(
        back_populates="photos",
        secondary="photo_tags",
        order_by="TagOrm.name",
    )


class TagOrm(Base):
    __tablename__ = "tags"

    uuid: Mapped[uuid_pk]
    name: Mapped[str]
    created_at: Mapped[timestamp_tz]

    photos: Mapped[list["PhotoOrm"]] = relationship(
        back_populates="tags",
        secondary="photo_tags",
    )


class PhotoTagM2M(Base):
    __tablename__ = "photo_tags"

    photo_uuid: Mapped[uuid_pk] = mapped_column(
        ForeignKey("photos.uuid", ondelete="CASCADE"),
    )
    tag_uuid: Mapped[uuid_pk] = mapped_column(
        ForeignKey("tags.uuid", ondelete="CASCADE"),
    )
