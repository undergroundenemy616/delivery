from abc import abstractmethod
from uuid import UUID

from delivery.core.domain.model.order_aggregate import Order


class OrderRepositoryInterface:

    @abstractmethod
    async def add_order(self, order_aggregate: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, order_aggregate: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_order_by_id(self, order_id: UUID) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def get_created_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def get_assigned_orders(self) -> list[Order]:
        raise NotImplementedError
