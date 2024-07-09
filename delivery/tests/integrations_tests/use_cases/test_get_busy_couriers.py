from infrastracture.adapters.postgres.repositories.courier_repository import CourierRepository

from delivery.core.application.use_cases.queries.get_busy_couriers import GetBusyCouriers
from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import Transport as TransportEntity
from delivery.core.domain.model.shared_kernel.location import Location


class TestGetBusyCouriersQueryShould:

    async def test_success_return_busy_couriers(self, session, pedestrian_transport):
        courier_aggregate1 = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        courier_aggregate1.set_busy()

        courier_aggregate2 = CourierAggregate.create(
            name="test_name",
            transport=TransportEntity.pedestrian,
            location=Location.create_random(),
        )
        courier_aggregate2.set_busy()
        repository = CourierRepository(session=session)
        await repository.create_courier(courier_aggregate=courier_aggregate1)
        await repository.create_courier(courier_aggregate=courier_aggregate2)
        await session.commit()

        busy_couriers = await GetBusyCouriers(session=session)()

        assert len(busy_couriers.couriers) == 2
