from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base



class User(Base):
    __tablename__ = "users"
    # Primary key ID
    id = Column(Integer, primary_key=True, index=True)
    # Unique username for the user
    username = Column(String, unique=True, nullable=False)
    # Unique email for authentication and communication
    email = Column(String, unique=True, nullable=False)
    # Hashed password for secure storage
    hashed_password = Column(String, nullable=False)
    # User role (e.g., "user", "admin")
    role = Column(String, default="user")
    # Timestamp for account creation
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # One-to-many relationship: a user can have multiple photos
    photos = relationship("Photo", back_populates="user")
    # One-to-many relationship: a user can write multiple comments
    comments = relationship("Comment", back_populates="user")
    # String representation for debugging and logging
    def __repr__(self):
        return f"<User(username={self.username}, email={self.email}, role={self.role})>"