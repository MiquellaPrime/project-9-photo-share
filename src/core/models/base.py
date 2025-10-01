from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, MetaData, String, text
from sqlalchemy.orm import DeclarativeBase, mapped_column

from src.core.config import settings

UTC_NOW_SQL = text("TIMEZONE('utc', now())")

str_150 = Annotated[str, 150]
str_255 = Annotated[str, 255]

int_pk = Annotated[int, mapped_column(primary_key=True)]
uuid_pk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
bool_t = Annotated[bool, mapped_column(server_default=text("TRUE"))]
bool_f = Annotated[bool, mapped_column(server_default=text("FALSE"))]
timestamp_tz = Annotated[datetime, mapped_column(server_default=UTC_NOW_SQL)]


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=settings.db.naming_convention)
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
        str_150: String(150),
        str_255: String(255),
    }
