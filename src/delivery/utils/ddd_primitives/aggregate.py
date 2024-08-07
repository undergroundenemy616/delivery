from abc import abstractmethod
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Aggregate(BaseModel):
    id: UUID = Field(default_factory=uuid4, frozen=False)

    @classmethod
    @abstractmethod
    def create(cls, *args: Any, **kwargs: Any) -> "Aggregate":
        raise NotImplementedError

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Aggregate):
            return False
        if type(self) != type(other):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
