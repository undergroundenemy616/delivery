from abc import abstractmethod

from core.domain.model.order_aggregate import Order


class OrderRepositoryInterface:

    @abstractmethod
    async def add_order(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_created_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def get_assigned_orders(self) -> list[Order]:
        raise NotImplementedError
