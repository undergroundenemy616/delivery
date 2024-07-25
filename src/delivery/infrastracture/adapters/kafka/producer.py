from faststream._compat import model_to_json

from delivery.core.domain.model.order_aggregate.domain_events.order_completed_event import OrderCompletedDomainEvent
from delivery.core.ports.bus_producer_interface import BusProducerInterface
from faststream.kafka import KafkaBroker
from delivery.config import settings
from delivery.infrastracture.adapters.kafka.integrations_events.order_status_changed import \
    OrderStatusChangedIntegrationEvent, OrderStatus


class KafkaBusProducer(BusProducerInterface):

    def __init__(self):
        self.broker = KafkaBroker(f"{settings.kafka.host_external}:{settings.kafka.port_external}")

    async def publish_order_completed_event(self, order_completed_event: OrderCompletedDomainEvent) -> None:
        prepared_publisher = self.broker.publisher(topic=settings.kafka.order_status_changed_topic_name)
        integration_event = OrderStatusChangedIntegrationEvent(
            order_id=order_completed_event.order_id,
            status=OrderStatus.COMPLETED
        )

        await self.broker.connect()
        await prepared_publisher.publish(
            key=str(order_completed_event.event_id).encode(),
            message=model_to_json(integration_event),
            headers={"content-type": "application/json"}
        )
        await self.broker.close()
