from abc import abstractmethod
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PrivateAttr

from delivery.utils.ddd_primitives.domain_event import DomainEvent


class Aggregate(BaseModel):
    id: UUID = Field(default_factory=uuid4, frozen=False)

    _domain_events: list[DomainEvent] = PrivateAttr(default_factory=list)

    @classmethod
    @abstractmethod
    def create(cls, *args: Any, **kwargs: Any) -> "Aggregate":
        raise NotImplementedError

    def list_domain_events(self):
        return self._domain_events

    def clear_domain_events(self):
        self._domain_events.clear()

    def add_domain_event(self, domain_event: DomainEvent):
        self._domain_events.append(domain_event)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Aggregate):
            return False
        if type(self) != type(other):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
