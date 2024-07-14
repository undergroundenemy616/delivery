from delivery.core.domain.model.courier_aggregate import Courier
from delivery.core.domain.model.order_aggregate import Order
from delivery.utils.ddd_primitives import DomainService


class FindCourierForOrder(DomainService):

    def __call__(self, order: Order, couriers: list[Courier]) -> Courier:
        found_courier, found_time_to_order_location = None, float("-inf")

        for courier in couriers:
            calculated_time_to_order_location = courier.calculate_time_to_order_location(order.location)
            if not found_courier or calculated_time_to_order_location < found_time_to_order_location:
                found_courier, found_time_to_order_location = courier, calculated_time_to_order_location

        return found_courier
