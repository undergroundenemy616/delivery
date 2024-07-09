from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.infrastracture.adapters.postgres.models import Courier
from delivery.utils.application_primitives import Query


class _Location(BaseModel):
    X: int
    Y: int


class _Courier(BaseModel):
    id: UUID
    name: str
    location: _Location
    transport_id: int


class GetBusyCouriersOutputDTO(BaseModel):
    couriers: list[_Courier]


class GetBusyCouriers(Query):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __call__(self):
        query = select(Courier).filter_by(status=CourierStatus.busy.name)
        result = await self.session.execute(query)
        couriers = result.scalars().all()
        return self.construct_dto(couriers)

    @staticmethod
    def construct_dto(couriers: list[Courier]) -> GetBusyCouriersOutputDTO:
        couriers = [
            _Courier(
                id=courier.id,
                name=courier.name,
                location=_Location(X=courier.location_x, Y=courier.location_y),
                transport_id=courier.transport_id,
            )
            for courier in couriers
        ]
        return GetBusyCouriersOutputDTO(couriers=couriers)
