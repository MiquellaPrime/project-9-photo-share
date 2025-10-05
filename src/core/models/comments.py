from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, uuid_pk
from .mixins import TimestampMixin

if TYPE_CHECKING:
    from .users import UserOrm


class CommentOrm(TimestampMixin, Base):
    __tablename__ = "comments"

    uuid: Mapped[uuid_pk]
    photo_uuid: Mapped[UUID] = mapped_column(
        ForeignKey("photos.uuid", ondelete="CASCADE"),
    )
    user_id: Mapped[int] = mapped_column(
<<<<<<< Updated upstream
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
=======
        ForeignKey("users.id", ondelete="RESTRICT"),
>>>>>>> Stashed changes
    )
    text: Mapped[str] = mapped_column(Text)

    user: Mapped["UserOrm"] = relationship()
