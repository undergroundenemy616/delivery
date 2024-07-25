from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select

from delivery.config.dependencies import get_container
from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.infrastracture.adapters.postgres.models import Courier
from delivery.utils.application_primitives import Query
from delivery.core.ports.uow_interface import UnitOfWork


class _Location(BaseModel):
    x: int
    y: int


class GetBusyCouriersOutputDTO(BaseModel):
    id: UUID
    name: str
    location: _Location
    transport_id: int


class GetBusyCouriers(Query):

    def __init__(self):
        self.uow = get_container().resolve(UnitOfWork)

    async def __call__(self):
        async with self.uow:
            query = select(Courier).filter_by(status=CourierStatus.busy.name)
            result = await self.uow.session.execute(query)
            couriers = result.scalars().all()
            return self.construct_dto(couriers)

    @staticmethod
    def construct_dto(couriers: list[Courier]) -> list[GetBusyCouriersOutputDTO]:
        couriers = [
            GetBusyCouriersOutputDTO(
                id=courier.id,
                name=courier.name,
                location=_Location(x=courier.location_x, y=courier.location_y),
                transport_id=courier.transport_id,
            )
            for courier in couriers
        ]
        return couriers
