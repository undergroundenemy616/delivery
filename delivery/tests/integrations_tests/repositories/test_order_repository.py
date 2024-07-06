import uuid

from delivery.core.domain.model.order_aggregate import Order as OrderAggregate
from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.infrastracture.adapters.postgres.models import Order
from delivery.infrastracture.adapters.postgres.repositories.order_repository import OrderRepository


class TestOrderRepositoryShould:

    async def test_success_create_order(self, session, courier):
        order_aggregate = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate.assign(courier)

        repository = OrderRepository(session=session)
        await repository.add_order(order_aggregate=order_aggregate)
        order = await session.get(Order, order_aggregate.id)

        assert order.status == order_aggregate.status.name
        assert order.courier_id == order_aggregate.courier_id
        assert order.location_x == order_aggregate.location.X
        assert order.location_y == order_aggregate.location.Y

    async def test_success_update_order(self, session, courier):
        order_aggregate = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate.assign(courier)
        repository = OrderRepository(session=session)
        await repository.add_order(order_aggregate=order_aggregate)
        order_aggregate.complete()

        await repository.update_order(order_aggregate=order_aggregate)
        order = await session.get(Order, order_aggregate.id)

        assert order.status == OrderStatus.completed.name

    async def test_success_get_created_orders(self, session, pedestrian_transport):
        order_aggregate1 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate2 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate3 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        repository = OrderRepository(session=session)
        await repository.add_order(order_aggregate=order_aggregate1)
        await repository.add_order(order_aggregate=order_aggregate2)
        await repository.add_order(order_aggregate=order_aggregate3)

        couriers = await repository.get_created_orders()

        assert len(couriers) == 3

    async def test_success_get_assigned_orders(self, session, courier):
        order_aggregate1 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate1.assign(courier)

        order_aggregate2 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate2.assign(courier)
        order_aggregate3 = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
        order_aggregate3.assign(courier)
        repository = OrderRepository(session=session)
        await repository.add_order(order_aggregate=order_aggregate1)
        await repository.add_order(order_aggregate=order_aggregate2)
        await repository.add_order(order_aggregate=order_aggregate3)

        couriers = await repository.get_assigned_orders()

        assert len(couriers) == 3
