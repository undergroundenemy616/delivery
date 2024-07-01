from typing import ClassVar

from delivery.utils.ddd_primitives.value_object import ValueObject


class Transport(ValueObject):
    pedestrian: ClassVar["Transport"]
    bicycle: ClassVar["Transport"]
    car: ClassVar["Transport"]

    name: str
    speed: int


Transport.pedestrian = Transport(name="pedestrian", speed=1)
Transport.bicycle = Transport(name="bicycle", speed=2)
Transport.car = Transport(name="car", speed=3)
