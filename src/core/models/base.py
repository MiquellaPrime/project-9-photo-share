from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, MetaData, String, text
from sqlalchemy.orm import DeclarativeBase, mapped_column

from src.core.config import settings

UTC_NOW_SQL = text("TIMESTAMP('utc', now())")

str_255 = Annotated[str, 255]

timestamp_tz = Annotated[
    datetime,
    mapped_column(server_default=UTC_NOW_SQL),
]


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)
    type_annotation_map = {
        str_255: String(255),
        datetime: TIMESTAMP(timezone=True),
    }
