from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from .base import Base

photos_tags = Table(
    "photos_tags",
    Base.metadata,
    Column(
        "photo_uuid", UUID(as_uuid=True), ForeignKey("photos.uuid"), primary_key=True
    ),
    Column("tag_uuid", UUID(as_uuid=True), ForeignKey("tags.uuid"), primary_key=True),
)
