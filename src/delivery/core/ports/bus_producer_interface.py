from abc import abstractmethod

from delivery.core.domain.model.order_aggregate.domain_events.order_completed_event import OrderCompletedDomainEvent


class BusProducerInterface:

    @abstractmethod
    async def publish_order_completed_event(self, order_completed_event: OrderCompletedDomainEvent) -> None:
        raise NotImplementedError
