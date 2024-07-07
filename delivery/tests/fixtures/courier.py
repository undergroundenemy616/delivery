import pytest

from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import Transport as TransportEntity
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.infrastracture.adapters.postgres.models import Transport
from delivery.infrastracture.adapters.postgres.repositories.courier_repository import CourierRepository


@pytest.fixture
async def pedestrian_transport(session) -> None:
    transport = Transport(
        id=TransportEntity.pedestrian.id, name=TransportEntity.pedestrian.name, speed=TransportEntity.pedestrian.speed
    )
    session.add(transport)
    await session.commit()


@pytest.fixture
async def courier(session, pedestrian_transport) -> CourierAggregate:
    courier_aggregate = CourierAggregate.create(
        name="test_name",
        transport=TransportEntity.pedestrian,
        location=Location.create_random(),
    )
    repository = CourierRepository(session=session)
    await repository.create_courier(courier_aggregate=courier_aggregate)
    return courier_aggregate
