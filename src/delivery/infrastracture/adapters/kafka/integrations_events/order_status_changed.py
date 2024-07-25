from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class OrderStatus(Enum):
    NONE = 0
    CREATED = 1
    ASSIGNED = 2
    COMPLETED = 3


class OrderStatusChangedIntegrationEvent(BaseModel):
    order_id: UUID
    status: OrderStatus
