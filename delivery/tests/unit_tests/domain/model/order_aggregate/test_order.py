import uuid

import pytest

from delivery.core.domain.model.courier_aggregate import Courier, CourierIsAlreadyBusyError
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.order_aggregate import (
    Order,
    OrderIsAlreadyAssignedError,
    OrderIsAlreadyCompletedError,
    OrderIsNotAssignedError,
    OrderStatus,
)
from delivery.core.domain.model.shared_kernel.location import Location


class TestOrderShould:

    def test_success_create_when_params_is_correct(self) -> None:
        location = Location.create_random()
        id = uuid.uuid4()
        order = Order.create(id=id, location=location)

        assert order.id == id
        assert order.location == location
        assert order.status == OrderStatus.created

    def test_success_assign_with_right_order_status(self) -> None:
        order = Order.create(id=uuid.uuid4(), location=Location.create_random())
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)

        order.assign(courier=courier)

        assert order.courier_id == courier.id
        assert order.status == OrderStatus.assigned

    def test_error_when_assign_to_completed_order(self) -> None:
        order = Order(id=uuid.uuid4(), location=Location.create_random(), status=OrderStatus.completed)
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)

        with pytest.raises(OrderIsAlreadyCompletedError):
            order.assign(courier=courier)

    def test_error_when_assign_to_already_assigned_order(self) -> None:
        order = Order(id=uuid.uuid4(), location=Location.create_random(), status=OrderStatus.assigned)
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)

        with pytest.raises(OrderIsAlreadyAssignedError):
            order.assign(courier=courier)

    def test_error_when_assign_to_already_busy_courier(self) -> None:
        order = Order(id=uuid.uuid4(), location=Location.create_random(), status=OrderStatus.assigned)
        courier = Courier.create(name="name", location=Location.create_random(), transport=Transport.car)
        courier.set_busy()

        with pytest.raises(CourierIsAlreadyBusyError):
            order.assign(courier=courier)

    def test_success_complete_assigned_order(self) -> None:
        order = Order(id=uuid.uuid4(), location=Location.create_random(), status=OrderStatus.assigned)

        order.complete()

        assert order.status == OrderStatus.completed

    def test_error_when_complete_not_assigned_order(self) -> None:
        order = Order(id=uuid.uuid4(), location=Location.create_random(), status=OrderStatus.created)

        with pytest.raises(OrderIsNotAssignedError):
            order.complete()
