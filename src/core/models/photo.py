from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.core.database import Base
from typing import List


# Association table for many-to-many relationship between Photo and Tag
photo_tag = Table(
    "photo_tag",
    Base.metadata,
    Column("photo_id", ForeignKey("photos.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Photo(Base):
    """
        SQLAlchemy model representing a photo in the database.
        It contains information about the URL, Cloudinary ID, description,
        and relationships to users, tags, and transformations.
        """
    __tablename__ = "photos"

# Primary key ID
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
# Foreign key linking the photo to a specific user
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
# Photo URL
    url: Mapped[str] = mapped_column(String, nullable=False)
# Unique identifier for the photo in external storage
    public_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable= True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
# Relationships
    user: Mapped["User"] = relationship("User", back_populates="photos")
    tags: Mapped[List["Tag"]] = relationship("Tag", secondary=photo_tag, back_populates="photos")
    transformations: Mapped[List["PhotoTransform"]] = relationship(
        "PhotoTransform", back_populates="photo", cascade="all, delete-orphan"
    )

# Method to add tags to a photo (with a max of 5 tags)
    def add_tags(self, tags_list: List["Tag"]) -> None:
        for tag in tags_list[:5]:
            if tag not in self.tags:
                self.tags.append(tag)

    def add_transformation(self, transformation: "PhotoTransform") -> None:
        self.transformations.append(transformation)

    def __repr__(self) -> str:
        return f"<Photo(id={self.id}, url={self.url})>"