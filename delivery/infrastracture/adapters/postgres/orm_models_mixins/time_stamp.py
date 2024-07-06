from datetime import datetime

from sqlalchemy import Column, DateTime, func


class TimeStampMixin:
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        server_onupdate=func.now(),  # type: ignore
        default=datetime.now,
        nullable=False,
    )
