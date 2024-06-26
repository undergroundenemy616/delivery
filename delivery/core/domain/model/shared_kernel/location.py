from pydantic import Field
from typing import ClassVar
from delivery.utils.ddd_primitives import ValueObject
import random


class Location(ValueObject):
    min_point_value: ClassVar[int] = 1
    max_point_value: ClassVar[int] = 10

    X: int = Field(..., ge=min_point_value, le=max_point_value)
    Y: int = Field(..., ge=min_point_value, le=max_point_value)

    def distance_to(self, target_location: "Location") -> int:
        distance = abs(target_location.X - self.X) + abs(target_location.Y - self.Y)
        return distance

    @classmethod
    def create_random(cls) -> "Location":
        location = Location(
            X=random.randint(cls.min_point_value, cls.max_point_value),
            Y=random.randint(cls.min_point_value, cls.max_point_value)
        )
        return location
