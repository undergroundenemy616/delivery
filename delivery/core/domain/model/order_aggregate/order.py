from uuid import UUID

from delivery.core.domain.model.order_aggregate.order_status import OrderStatus
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.utils.ddd_primitives.aggregate import Aggregate
from delivery.utils.exceptions.code_exception import CodeExceptionError


class Order(Aggregate):

    location: Location
    status: OrderStatus = OrderStatus.created
    courier_id: UUID | None = None

    @classmethod
    def create(cls, id: UUID, location: Location) -> "Order":
        order = cls(id=id, location=location)
        return order

    def assign(self, courier_id: UUID) -> None:
        if self.status == OrderStatus.completed:
            raise OrderIsAlreadyCompletedError(order_id=self.id)
        if self.status == OrderStatus.assigned:
            raise OrderIsAlreadyAssignedError(order_id=self.id)

        self.courier_id = courier_id
        self.status = OrderStatus.assigned

    def complete(self) -> None:
        if self.status != OrderStatus.assigned:
            raise OrderIsNotAssignedError(order_id=self.id)
        self.status = OrderStatus.completed


class OrderIsNotAssignedError(CodeExceptionError):
    code = "order_is_not_assigned_error"

    def __init__(self, order_id: UUID):
        self.order_id = order_id

    def __str__(self) -> str:
        return f"Order with id {self.order_id} can not be completed because it not assigned to courier"


class OrderIsAlreadyCompletedError(CodeExceptionError):
    code = "order_is_already_completed_error"

    def __init__(self, order_id: UUID):
        self.order_id = order_id

    def __str__(self) -> str:
        return f"Order with id {self.order_id} is already completed"


class OrderIsAlreadyAssignedError(CodeExceptionError):
    code = "order_is_already_assigned_error"

    def __init__(self, order_id: UUID):
        self.order_id = order_id

    def __str__(self) -> str:
        return f"Order with id {self.order_id} is already assigned"
