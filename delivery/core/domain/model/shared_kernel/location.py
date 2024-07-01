import random
from typing import ClassVar

from pydantic import Field

from delivery.utils.ddd_primitives import ValueObject


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
            Y=random.randint(cls.min_point_value, cls.max_point_value),
        )
        return location

    @staticmethod
    def calculate_new_position(current_pos: int, target_pos: int, step_size: int) -> tuple[int, int]:
        difference = target_pos - current_pos
        if abs(difference) > step_size:
            step = step_size if difference > 0 else -step_size
            new_position = current_pos + step
            remaining_step = 0
        else:
            new_position = target_pos
            remaining_step = step_size - abs(difference)
        return new_position, remaining_step
