from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.core.ports.courier_repository_interface import CourierRepositoryInterface
from delivery.infrastracture.adapters.postgres.models.courier import Courier


class CourierRepository(CourierRepositoryInterface):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_courier(self, courier_aggregate: CourierAggregate) -> None:
        courier = Courier(
            id=courier_aggregate.id,
            name=courier_aggregate.name,
            status=courier_aggregate.status.name,
            location_x=courier_aggregate.location.X,
            location_y=courier_aggregate.location.Y,
            transport_id=courier_aggregate.transport.id,
        )
        self.session.add(courier)

    async def update_courier(self, courier_aggregate: CourierAggregate) -> None:
        stmt = (
            update(Courier)
            .filter_by(id=courier_aggregate.id)
            .values(
                name=courier_aggregate.name,
                status=courier_aggregate.status.name,
                location_x=courier_aggregate.location.X,
                location_y=courier_aggregate.location.Y,
                transport_id=courier_aggregate.transport.id,
            )
        )
        await self.session.execute(stmt)

    async def get_courier_by_id(self, courier_id: UUID) -> CourierAggregate | None:
        stmt = select(Courier).options(joinedload(Courier.transport)).filter_by(id=courier_id)
        result = await self.session.execute(stmt)
        courier: Courier = result.scalars().one_or_none()
        if courier:
            return courier.to_aggregate()
        return None

    async def get_free_couriers(self) -> list[CourierAggregate]:
        query = select(Courier).options(joinedload(Courier.transport)).filter_by(status=CourierStatus.free.name)
        result = await self.session.execute(query)
        couriers = result.scalars()
        couriers_aggregates = [courier.to_aggregate() for courier in couriers]
        return couriers_aggregates
