from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import TimestampMixin


class CommentOrm(TimestampMixin, Base):
    __tablename__ = "comments"

    uuid: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    photo_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("photos.uuid", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)