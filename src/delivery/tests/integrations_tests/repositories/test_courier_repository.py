from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.core.domain.model.courier_aggregate import Transport as TransportEntity
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.infrastracture.adapters.postgres.models import Courier
from delivery.infrastracture.adapters.postgres.repositories.courier_repository import CourierRepository


class TestCourierRepositoryShould:

    async def test_success_create_courier(self, session, pedestrian_transport) -> None:
        courier_aggregate = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )

        repository = CourierRepository(session=session)
        await repository.create_courier(courier_aggregate=courier_aggregate)
        courier = await session.get(Courier, courier_aggregate.id)

        assert courier.status == courier_aggregate.status.name
        assert courier.transport_id == courier_aggregate.transport.id
        assert courier.name == courier_aggregate.name
        assert courier.location_x == courier_aggregate.location.X
        assert courier.location_y == courier_aggregate.location.Y

    async def test_success_update_courier(self, session, pedestrian_transport) -> None:
        courier_aggregate = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        repository = CourierRepository(session=session)
        await repository.create_courier(courier_aggregate=courier_aggregate)
        courier_aggregate.set_busy()

        await repository.update_courier(courier_aggregate=courier_aggregate)
        courier = await session.get(Courier, courier_aggregate.id)

        assert courier.status == CourierStatus.busy.name

    async def test_success_get_courier_by_id(self, session, pedestrian_transport) -> None:
        courier_aggregate = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        repository = CourierRepository(session=session)
        await repository.create_courier(courier_aggregate=courier_aggregate)

        courier = await repository.get_courier_by_id(courier_id=courier_aggregate.id)

        assert courier
        assert courier.status.name == courier_aggregate.status.name
        assert courier.transport == courier_aggregate.transport
        assert courier.name == courier_aggregate.name
        assert courier.location == courier_aggregate.location

    async def test_success_get_free_couriers(self, session, pedestrian_transport) -> None:
        free_courier_aggregate1 = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        free_courier_aggregate2 = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        busy_courier_aggregate = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        busy_courier_aggregate.set_busy()
        repository = CourierRepository(session=session)
        await repository.create_courier(courier_aggregate=free_courier_aggregate1)
        await repository.create_courier(courier_aggregate=free_courier_aggregate2)
        await repository.create_courier(courier_aggregate=busy_courier_aggregate)

        couriers = await repository.get_free_couriers()

        assert len(couriers) == 2
