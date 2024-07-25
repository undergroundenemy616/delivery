from delivery.core.application.domain_event_handlers.order_completed import OrderCompletedDomainEventHandler
from delivery.core.domain.model.order_aggregate.domain_events.order_completed_event import OrderCompletedDomainEvent
from delivery.utils.application_primitives.event_handler import Handler
from delivery.utils.ddd_primitives.domain_event import DomainEvent

DOMAIN_EVENT_HANDLER_MAPPING: dict[type(DomainEvent), type(Handler)] = {
    OrderCompletedDomainEvent: OrderCompletedDomainEventHandler
}