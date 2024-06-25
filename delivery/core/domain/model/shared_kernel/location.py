from pydantic import Field
from typing import ClassVar
from delivery.utils.ddd_primitives import ValueObject
import random


class Location(ValueObject):
    min_location: ClassVar[int] = 1
    max_location: ClassVar[int] = 10

    X: int = Field(..., ge=min_location, le=max_location)
    Y: int = Field(..., ge=min_location, le=max_location)

    def distance_to(self, target_location: "Location") -> int:
        distance = abs(target_location.X - self.X) + abs(target_location.Y - self.Y)
        return distance

    @staticmethod
    def create_random() -> "Location":
        location = Location(
            X=random.randint(1, 10),
            Y=random.randint(1, 10)
        )
        return location
