from abc import ABC, abstractmethod

from delivery.core.ports.courier_repository_interface import CourierRepositoryInterface
from delivery.core.ports.order_repository_interface import OrderRepositoryInterface


class UnitOfWork(ABC):
    courier: CourierRepositoryInterface
    order: OrderRepositoryInterface

    @abstractmethod
    async def __aenter__(self): ...

    @abstractmethod
    async def __aexit__(self, *args): ...

    async def commit(self):
        await self._commit()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def _commit(self):
        raise NotImplementedError
