from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.core.models.photo import PhotoORM


class UserORM(Base):
    """
    SQLAlchemy model representing a user in the database.
    This model contains information for authentication, roles, and
    relationships with other models like photos and comments.
    """

    __tablename__ = "users"

    # Primary key ID
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # Unique email for authentication and communication
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    # Hashed password for secure storage
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    # User role (e.g., "user", "admin")
    role: Mapped[str] = mapped_column(String, default="user")
    # Timestamp for account creation
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # One-to-many relationship: a user can have multiple photos
    photos: Mapped[list["PhotoORM"]] = relationship("PhotoORM", back_populates="user")
    # One-to-many relationship: a user can write multiple comments
