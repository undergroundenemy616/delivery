from delivery.config.dependencies import get_container
from delivery.core.domain.model.order_aggregate.domain_events.order_completed_event import OrderCompletedDomainEvent
from delivery.core.ports.bus_producer_interface import BusProducerInterface
from delivery.utils.application_primitives import Handler


class OrderCompletedDomainEventHandler(Handler):

    def __init__(self):
        self.bus_producer: BusProducerInterface = get_container().resolve(BusProducerInterface)

    async def __call__(self, domain_event: OrderCompletedDomainEvent) -> None:
        await self.bus_producer.publish_order_completed_event(order_completed_event=domain_event)

