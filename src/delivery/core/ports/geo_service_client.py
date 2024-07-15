from abc import abstractmethod

from delivery.core.domain.model.shared_kernel.location import Location


class GeoServiceClientInterface:

    @abstractmethod
    async def get_geolocation(self, street: str) -> Location:
        raise NotImplementedError
