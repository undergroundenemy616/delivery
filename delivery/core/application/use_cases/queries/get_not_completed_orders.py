from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.infrastracture.adapters.postgres.models import Order
from delivery.utils.application_primitives import Query


class _Location(BaseModel):
    X: int
    Y: int


class _Order(BaseModel):
    id: UUID
    location: _Location


class GetNotCompletedOrdersOutputDTO(BaseModel):
    orders: list[_Order]


class GetNotCompletedOrders(Query):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self):
        query = select(Order).filter(or_(Order.status == OrderStatus.created, Order.status == OrderStatus.assigned))
        result = await self.session.execute(query)
        orders = result.scalars().all()
        return self.construct_dto(orders)

    @staticmethod
    def construct_dto(orders: list[Order]) -> GetNotCompletedOrdersOutputDTO:
        orders = [
            _Order(
                id=order.id,
                location=_Location(X=order.location_x, Y=order.location_y),
            )
            for order in orders
        ]
        return GetNotCompletedOrdersOutputDTO(orders=orders)
