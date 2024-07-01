from typing import ClassVar

from delivery.utils.ddd_primitives.value_object import ValueObject


class OrderStatus(ValueObject):
    created: ClassVar["OrderStatus"]
    assigned: ClassVar["OrderStatus"]
    completed: ClassVar["OrderStatus"]

    name: str


OrderStatus.created = OrderStatus(name="created")
OrderStatus.assigned = OrderStatus(name="assigned")
OrderStatus.completed = OrderStatus(name="completed")
