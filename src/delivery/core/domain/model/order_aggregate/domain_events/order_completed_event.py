from uuid import UUID

from delivery.utils.ddd_primitives.domain_event import DomainEvent


class OrderCompletedDomainEvent(DomainEvent):
    order_id: UUID
