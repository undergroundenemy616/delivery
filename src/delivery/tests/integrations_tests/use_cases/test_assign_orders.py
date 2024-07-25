import uuid

from delivery.core.application.use_cases.commands.assign_orders import AssignOrders
from delivery.core.domain.model.courier_aggregate import Courier as CourierAggregate
from delivery.core.domain.model.courier_aggregate import CourierStatus
from delivery.core.domain.model.courier_aggregate import Transport as TransportEntity
from delivery.core.domain.model.order_aggregate import Order as OrderAggregate
from delivery.core.domain.model.order_aggregate import OrderStatus
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.core.ports.uow_interface import UnitOfWork


class TestAssignOrderCommandShould:

    async def test_success_assign_order_to_courier(self, uow: UnitOfWork, pedestrian_transport):
        async with uow:
            order_aggregate = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
            await uow.order.add_order(order_aggregate=order_aggregate)

            courier_aggregate = CourierAggregate.create(
                name="test_name",
                transport=TransportEntity.pedestrian,
                location=Location.create_random(),
            )
            await uow.courier.create_courier(courier_aggregate=courier_aggregate)
            await uow.commit()

            await AssignOrders()()

            order = await uow.order.get_order_by_id(order_id=order_aggregate.id)
            courier = await uow.courier.get_courier_by_id(courier_id=courier_aggregate.id)

            assert order.status == OrderStatus.assigned
            assert order.courier_id == courier_aggregate.id
            assert courier.status == CourierStatus.busy

    async def test_can_not_assign_order_for_courier_if_free_couriers_not_exist(
        self, uow: UnitOfWork, pedestrian_transport
    ):
        async with uow:
            order_aggregate = OrderAggregate.create(location=Location.create_random(), id=uuid.uuid4())
            await uow.order.add_order(order_aggregate=order_aggregate)
            await uow.commit()

            await AssignOrders()()

            order = await uow.order.get_order_by_id(order_id=order_aggregate.id)

            assert order.status == OrderStatus.created
            assert not order.courier_id
