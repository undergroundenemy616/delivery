from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from delivery.infrastracture.adapters.postgres.orm_models_mixins import TimeStampMixin, UUIDAsPkMixin


metadata = MetaData()

Base = declarative_base(
    metadata=metadata,
    cls=(
        UUIDAsPkMixin,
        TimeStampMixin,
    ),
)

from .courier import Courier, Transport  # noqa: E402
from .order import Order  # noqa: E402


__all__ = ["Courier", "Transport", "Order"]
