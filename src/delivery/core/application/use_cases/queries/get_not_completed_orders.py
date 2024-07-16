from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import or_, select

from delivery.config.dependencies import get_container
from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.infrastracture.adapters.postgres.models import Order
from delivery.utils.application_primitives import Query
from delivery.utils.uow.uow_interface import UnitOfWork


class _Location(BaseModel):
    x: int
    y: int


class GetNotCompletedOrdersOutputDTO(BaseModel):
    id: UUID
    location: _Location


class GetNotCompletedOrders(Query):

    def __init__(self):
        self.uow = get_container().resolve(UnitOfWork)

    async def __call__(self):
        async with self.uow:
            query = select(Order).filter(
                or_(Order.status == OrderStatus.created.name, Order.status == OrderStatus.assigned.name)
            )
            result = await self.uow.session.execute(query)
            orders = result.scalars().all()
            return self.construct_dto(orders)

    @staticmethod
    def construct_dto(orders: list[Order]) -> list[GetNotCompletedOrdersOutputDTO]:
        orders = [
            GetNotCompletedOrdersOutputDTO(
                id=order.id,
                location=_Location(x=order.location_x, y=order.location_y),
            )
            for order in orders
        ]
        return orders
