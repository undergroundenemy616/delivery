from typing import ClassVar

from delivery.utils.ddd_primitives.value_object import ValueObject


class CourierStatus(ValueObject):
    free: ClassVar["CourierStatus"]
    busy: ClassVar["CourierStatus"]

    name: str

    @classmethod
    def from_name(cls, name: str) -> "CourierStatus":
        if name == cls.free.name:
            return cls.free
        return cls.busy


CourierStatus.free = CourierStatus(name="free")
CourierStatus.busy = CourierStatus(name="busy")
