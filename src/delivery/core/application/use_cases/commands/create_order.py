import uuid
from uuid import UUID

from pydantic import BaseModel

from delivery.config.dependencies import get_container
from delivery.core.domain.model.order_aggregate import Order
from delivery.core.ports.geo_service_client import GeoServiceClientInterface
from delivery.utils.application_primitives import Command
from delivery.core.ports.uow_interface import UnitOfWork


class CreateOrderDTO(BaseModel):
    basket_id: UUID | None = None
    street: str | None = None


class CreateOrder(Command):

    def __init__(self):
        self.uow = get_container().resolve(UnitOfWork)
        self.geo_service_client = get_container().resolve(GeoServiceClientInterface)

    async def __call__(self, create_order_dto: CreateOrderDTO):
        async with self.uow:
            if not create_order_dto.basket_id:
                create_order_dto.basket_id = uuid.uuid4()

            if not create_order_dto.street:
                create_order_dto.street = "fuck"

            order = await self.uow.order.get_order_by_id(order_id=create_order_dto.basket_id)
            if order:
                return

            location = await self.geo_service_client.get_geolocation(street=create_order_dto.street)
            order = Order.create(id=create_order_dto.basket_id, location=location)

            await self.uow.order.add_order(order_aggregate=order)
            await self.uow.commit()
