from __future__ import annotations

from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.models.photo import PhotoORM, photo_tag


class TagORM(Base):
    """
    SQLAlchemy model representing a tag in the database.
    Tags are unique and can be associated with multiple photos.
    """

    __tablename__ = "tags"

    # Primary key ID
    id: Mapped[int] = mapped_column(primary_key=True)
    # Unique tag name
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    # Many-to-many relationship: a tag can be associated with multiple photos
    photos: Mapped[List["PhotoORM"]] = relationship(
        "PhotoORM", secondary=photo_tag, back_populates="tags"
    )
