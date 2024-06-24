from pydantic import Field
from delivery.utils.ddd_primitives import ValueObject
import random


class Location(ValueObject):
    X: int = Field(..., ge=1, le=10)
    Y: int = Field(..., ge=1, le=10)

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
