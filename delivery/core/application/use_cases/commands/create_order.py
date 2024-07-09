from uuid import UUID

from core.domain.model.shared_kernel.location import Location
from pydantic import BaseModel

from delivery.core.domain.model.order_aggregate import Order
from delivery.utils.application_primitives import Command
from delivery.utils.uow.uow_interface import UnitOfWork


class CreateOrderDTO(BaseModel):
    basket_id: UUID
    street: str


class CreateOrder(Command):

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self, create_order_dto: CreateOrderDTO):
        async with self.uow:
            order = await self.uow.order.get_order_by_id(order_id=create_order_dto.basket_id)
            if order:
                return

            location = Location.create_random()
            order = Order.create(id=create_order_dto.basket_id, location=location)

            await self.uow.order.add_order(order_aggregate=order)
            await self.uow.commit()
