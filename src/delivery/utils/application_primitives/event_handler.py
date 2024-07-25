from abc import abstractmethod

from delivery.utils.ddd_primitives.domain_event import DomainEvent


class Handler:

    @abstractmethod
    async def __call__(self, domain_event: DomainEvent):
        raise NotImplementedError
