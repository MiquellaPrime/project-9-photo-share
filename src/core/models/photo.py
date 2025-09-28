from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid as uuid_pkg

from .base import Base


class Photo(Base):
    __tablename__ = "photos"
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4
    )

    cloudinary_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
