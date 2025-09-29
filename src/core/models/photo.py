from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.models.phototransform import PhotoTransformORM
from src.core.models.tag import TagORM
from src.core.models.users import UserORM

# Association table for many-to-many relationship between Photo and Tag
photo_tag = Table(
    "photo_tag",
    Base.metadata,
    Column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class PhotoORM(Base):
    """
    SQLAlchemy model representing a photo in the database.
    It contains information about the URL, Cloudinary ID, description,
    and relationships to users, tags, and transformations.
    """

    __tablename__ = "photos"

    # Primary key ID
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Foreign key linking the photo to a specific user
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Photo URL
    url: Mapped[str] = mapped_column(String, nullable=False)
    # Unique identifier for the photo in external storage
    public_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # Relationships
    user: Mapped["UserORM"] = relationship("UserORM", back_populates="photos")
    tags: Mapped[List["TagORM"]] = relationship(
        "TagORM", secondary=photo_tag, back_populates="photos"
    )
    transformations: Mapped[List["PhotoTransformORM"]] = relationship(
        "PhotoTransformORM", back_populates="photo", cascade="all, delete-orphan"
    )

    # Method to add tags to a photo (with a max of 5 tags)
    def add_tags(self, tags_list: List["TagORM"]) -> None:
        for tag in tags_list[:5]:
            if tag not in self.tags:
                self.tags.append(tag)

    def add_transformation(self, transformation: "PhotoTransformORM") -> None:
        self.transformations.append(transformation)
