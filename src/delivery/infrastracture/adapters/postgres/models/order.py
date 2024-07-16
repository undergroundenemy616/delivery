from sqlalchemy import Column, ForeignKey, SmallInteger, String
from sqlalchemy.orm import mapped_column

from delivery.core.domain.model.order_aggregate import Order as OrderAggregate
from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.infrastracture.adapters.postgres.models import Base
from delivery.infrastracture.adapters.postgres.orm_models_mixins import AggregateMixin


class Order(Base, AggregateMixin):
    __tablename__ = "orders"

    status = Column(String, nullable=False)
    location_x = Column(SmallInteger, nullable=False)
    location_y = Column(SmallInteger, nullable=False)

    courier_id = mapped_column(ForeignKey("couriers.id"), nullable=True, index=True)

    def to_aggregate(self) -> OrderAggregate:
        location = Location(X=self.location_x, Y=self.location_y)
        status = OrderStatus.from_name(name=self.status)

        order = OrderAggregate(id=self.id, status=status, location=location, courier_id=self.courier_id)

        return order
