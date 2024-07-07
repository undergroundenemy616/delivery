from abc import abstractmethod
from uuid import UUID

from core.domain.model.courier_aggregate import Courier


class CourierRepositoryInterface:

    @abstractmethod
    async def create_courier(self, courier_aggregate: Courier) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_courier(self, courier_aggregate: Courier) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_courier_by_id(self, courier_id: UUID) -> Courier | None:
        raise NotImplementedError

    @abstractmethod
    async def get_free_couriers(self) -> list[Courier]:
        raise NotImplementedError
