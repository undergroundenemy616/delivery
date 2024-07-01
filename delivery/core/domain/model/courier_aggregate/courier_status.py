from typing import ClassVar

from delivery.utils.ddd_primitives.value_object import ValueObject


class CourierStatus(ValueObject):
    free: ClassVar["CourierStatus"]
    busy: ClassVar["CourierStatus"]

    name: str


CourierStatus.free = CourierStatus(name="free")
CourierStatus.busy = CourierStatus(name="busy")
