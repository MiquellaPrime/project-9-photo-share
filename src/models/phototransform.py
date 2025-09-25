from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
from src.models.photo import Photo

class PhotoTransform(Base):
    """
        SQLAlchemy model representing a transformation applied to a photo.
        This model stores a unique link to a transformed version of the original photo,
        along with details about the transformation (e.g., resize, filter).
        """
    __tablename__ = "photo_transforms"

    # Primary key ID for the transformation record.
    id = Column(Integer, primary_key=True, index=True)
    photo_id = Column(Integer, ForeignKey("photos.id", ondelete="CASCADE"), nullable=False)
    transformation_type = Column(String, nullable=False)
    transformation_value = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    photo = relationship("Photo", back_populates="transforms")