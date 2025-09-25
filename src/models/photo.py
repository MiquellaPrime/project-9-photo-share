from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base


transforms = relationship("PhotoTransform", back_populates="photo", cascade="all, delete")
# Association table for many-to-many relationship between Photo and Tag
photo_tag = Table(
    "photo_tag", Base.metadata,
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
    id = Column(Integer, primary_key=True, index=True)
# Foreign key linking the photo to a specific user
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
# Photo URL
    url = Column(String, nullable=False)
# Unique identifier for the photo in external storage
    public_id = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable= True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="photos")
    tags = relationship("Tag", secondary=photo_tag, back_populates="photos")

# Method to add tags to a photo (with a max of 5 tags)
    def add_tags(self, tags_list):
        for tag in tags_list[:5]:
            self.tags.append(tag)