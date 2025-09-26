from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from src.core.database import Base
from src.models.photo import photo_tag
from src.models.photo import Photo

class Tag(Base):
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
    photos: Mapped[List["Photo"]] = relationship("Photo", secondary=photo_tag, back_populates="tags")
    # String representation for debugging and logging
    def __repr__(self):
        return f"<Tag(name={self.name})>"
