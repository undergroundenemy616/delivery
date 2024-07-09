import uuid

from delivery.core.domain.model.courier_aggregate import Courier
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.order_aggregate import Order
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.core.domain.services.find_courier_for_order import FindCourierForOrder


class TestFindCourierForOrderServiceShould:

    def test_success_find_most_optimal_courier_for_order(self):
        order = Order.create(id=uuid.uuid4(), location=Location(X=1, Y=1))
        courier1 = Courier.create(name="name1", location=Location(X=3, Y=1), transport=Transport.pedestrian)
        courier2 = Courier.create(name="name2", location=Location(X=4, Y=1), transport=Transport.car)
        courier3 = Courier.create(name="name3", location=Location(X=10, Y=9), transport=Transport.car)

        found_courier = FindCourierForOrder()(order=order, couriers=[courier1, courier2, courier3])

        assert found_courier == courier2
