from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.attributes import backref_listeners

from src.database import Base
from src.models.photo import photo_tag

class Tag(Base):
    __tablename__ = "tags"
    # Primary key ID
    id = Column(Integer, primary_key=True, index=True)
    # Unique tag name
    name = Column(String, unique=True, nullable=False)
    # Many-to-many relationship: a tag can be associated with multiple photos
    photos = relationship("Photo", secondary=photo_tag, back_populates="tags")
    # String representation for debugging and logging
    def __repr__(self):
        return f"<Tag(name={self.name})>"
