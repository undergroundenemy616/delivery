from typing import ClassVar

from pydantic import Field

from delivery.utils.ddd_primitives.entity import Entity


class Transport(Entity):
    pedestrian: ClassVar["Transport"]
    bicycle: ClassVar["Transport"]
    car: ClassVar["Transport"]

    id: int = Field(frozen=False)
    name: str
    speed: int

    @classmethod
    def from_name(cls, name: str) -> "Transport":
        if name == Transport.pedestrian.name:
            return Transport.pedestrian
        if name == Transport.bicycle:
            return Transport.bicycle
        return Transport.car


Transport.pedestrian = Transport(id=1, name="pedestrian", speed=1)
Transport.bicycle = Transport(id=2, name="bicycle", speed=2)
Transport.car = Transport(id=3, name="car", speed=3)
