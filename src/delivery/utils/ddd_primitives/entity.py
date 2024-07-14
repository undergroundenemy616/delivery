from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Entity(BaseModel):
    id: UUID = Field(default_factory=uuid4, frozen=False)

    @classmethod
    def create(cls, *args: Any, **kwargs: Any) -> "Entity":
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Entity):
            return False
        if type(self) != type(other):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
