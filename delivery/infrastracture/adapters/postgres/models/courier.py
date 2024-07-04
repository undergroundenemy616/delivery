from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import mapped_column, relationship

from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.core.domain.model.courier_aggregate import Transport as TransportEntity
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.infrastracture.adapters.postgres.models import Base
from delivery.infrastracture.adapters.postgres.orm_models_mixins import AggregateMixin, EntityMixin


class Transport(Base, EntityMixin):
    __tablename__ = "transports"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        nullable=False,
    )

    name = Column(String, nullable=False)
    speed = Column(SmallInteger, nullable=False)

    def to_entity(self) -> BaseModel:
        transport = TransportEntity.from_name(name=self.name)
        return transport


class Courier(Base, AggregateMixin):
    __tablename__ = "couriers"

    name: Column = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)
    location_x = Column(SmallInteger, nullable=False)
    location_y = Column(SmallInteger, nullable=False)

    transport_id = mapped_column(ForeignKey("transports.id"), nullable=False, index=True)
    transport = relationship(Transport)

    def to_aggregate(self) -> CourierAggregate:
        transport = self.transport.to_entity()
        location = Location(X=self.location_x, Y=self.location_y)
        status = CourierStatus.from_name(name=self.status)

        courier = CourierAggregate(id=self.id, name=self.name, transport=transport, location=location, status=status)

        return courier
