from sqlalchemy import UUID, Column


class UUIDAsPkMixin:
    id = Column(
        UUID,
        primary_key=True,
        index=True,
        nullable=False,
    )
