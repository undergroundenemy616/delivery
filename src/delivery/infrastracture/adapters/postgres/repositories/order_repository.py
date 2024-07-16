from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.domain.model.order_aggregate import Order as OrderAggregate
from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.core.ports.order_repository_interface import OrderRepositoryInterface
from delivery.infrastracture.adapters.postgres.models import Order


class OrderRepository(OrderRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_order(self, order_aggregate: OrderAggregate) -> None:
        order = Order(
            id=order_aggregate.id,
            status=order_aggregate.status.name,
            location_x=order_aggregate.location.X,
            location_y=order_aggregate.location.Y,
            courier_id=order_aggregate.courier_id,
        )
        self.session.add(order)

    async def update_order(self, order_aggregate: OrderAggregate) -> None:
        stmt = (
            update(Order)
            .filter_by(id=order_aggregate.id)
            .values(
                status=order_aggregate.status.name,
                location_x=order_aggregate.location.X,
                location_y=order_aggregate.location.Y,
                courier_id=order_aggregate.courier_id,
            )
        )
        await self.session.execute(stmt)

    async def get_order_by_id(self, order_id: UUID) -> OrderAggregate | None:
        stmt = select(Order).filter_by(id=order_id)
        result = await self.session.execute(stmt)
        order: Order = result.scalars().one_or_none()
        if order:
            return order.to_aggregate()
        return None

    async def get_created_orders(self) -> list[OrderAggregate]:
        query = select(Order).filter_by(status=OrderStatus.created.name)
        result = await self.session.execute(query)
        orders = result.scalars()
        orders_aggregates = [order.to_aggregate() for order in orders]
        return orders_aggregates

    async def get_assigned_orders(self) -> list[OrderAggregate]:
        query = select(Order).filter_by(status=OrderStatus.assigned.name)
        result = await self.session.execute(query)
        orders = result.scalars()
        orders_aggregates = [order.to_aggregate() for order in orders]
        return orders_aggregates
