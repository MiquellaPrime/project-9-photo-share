from sqlalchemy.orm import Mapped, mapped_column

from .base import UTC_NOW_SQL, timestamp_tz


class TimeMixin:

    created_at: Mapped[timestamp_tz]
    updated_at: Mapped[timestamp_tz] = mapped_column(onupdate=UTC_NOW_SQL)
