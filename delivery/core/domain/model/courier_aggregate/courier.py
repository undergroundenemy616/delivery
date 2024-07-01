from uuid import UUID

from delivery.core.domain.model.courier_aggregate.courier_status import CourierStatus
from delivery.core.domain.model.courier_aggregate.transport import Transport
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.utils.ddd_primitives.aggregate import Aggregate
from delivery.utils.exceptions.code_exception import CodeExceptionError


class Courier(Aggregate):

    name: str
    transport: Transport
    location: Location
    status: CourierStatus

    @classmethod
    def create(cls, name: str, transport: Transport, location: Location) -> "Courier":
        courier = cls(name=name, transport=transport, location=location, status=CourierStatus.free)
        return courier

    def set_busy(self) -> None:
        if self.status == CourierStatus.busy:
            raise CourierIsAlreadyBusyError(courier_id=self.id)
        self.status = CourierStatus.busy

    def set_free(self) -> None:
        self.status = CourierStatus.free

    def calculate_time_to_order_location(self, order_location: Location) -> float:
        distance_to_order = self.location.distance_to(order_location)
        time_to_order = distance_to_order / self.transport.speed
        return time_to_order

    def move(self, target_location: Location) -> None:
        if self.location == target_location:
            return

        new_x, cruising_range = Location.calculate_new_position(
            self.location.X, target_location.X, self.transport.speed
        )
        self.location = Location(X=new_x, Y=self.location.Y)

        if self.location == target_location:
            return

        new_y, _ = Location.calculate_new_position(self.location.Y, target_location.Y, cruising_range)
        self.location = Location(X=self.location.X, Y=new_y)


class CourierIsAlreadyBusyError(CodeExceptionError):
    code = "courier_is_already_busy_error"

    def __init__(self, courier_id: UUID):
        self.courier_id = courier_id

    def __str__(self) -> str:
        return f"Can not set busy status to Courier with id {self.courier_id} because he is already busy"
