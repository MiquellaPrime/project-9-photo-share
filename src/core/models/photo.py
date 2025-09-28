import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

Timestamp = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    ),
]


class Photo(Base):
    __tablename__ = "photos"

    uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    cloudinary_url: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Timestamp
    updated_at: Timestamp
