from typing import ClassVar

from delivery.utils.ddd_primitives.value_object import ValueObject


class OrderStatus(ValueObject):
    created: ClassVar["OrderStatus"]
    assigned: ClassVar["OrderStatus"]
    completed: ClassVar["OrderStatus"]

    name: str

    @classmethod
    def from_name(cls, name: str) -> "OrderStatus":
        if name == cls.created.name:
            return cls.created
        if name == cls.assigned.name:
            return cls.assigned
        return cls.completed


OrderStatus.created = OrderStatus(name="created")
OrderStatus.assigned = OrderStatus(name="assigned")
OrderStatus.completed = OrderStatus(name="completed")
