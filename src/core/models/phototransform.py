from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.models.photo import PhotoORM


class PhotoTransformORM(Base):
    """
    SQLAlchemy model representing a transformation applied to a photo.
    This model stores a unique link to a transformed version of the original photo,
    along with details about the transformation (e.g., resize, filter).
    """

    __tablename__ = "photo_transforms"

    # Primary key ID for the transformation record.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="CASCADE"), nullable=False
    )
    transformation_type: Mapped[str] = mapped_column(String, nullable=False)
    transformation_value: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    photo: Mapped["PhotoORM"] = relationship(
        "PhotoORM", back_populates="transformations"
    )
