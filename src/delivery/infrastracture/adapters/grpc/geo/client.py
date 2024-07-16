import grpc

from delivery.config import settings
from delivery.core.domain.model.shared_kernel.location import Location
from delivery.core.ports.geo_service_client import GeoServiceClientInterface
from delivery.infrastracture.adapters.grpc.geo.proto import geo_pb2, geo_pb2_grpc


class GeoServiceClientGRPC(GeoServiceClientInterface):

    def __init__(self):
        self.channel = grpc.aio.insecure_channel(f"{settings.geo_service.host}:{settings.geo_service.port}")
        self.stub = geo_pb2_grpc.GeoStub(self.channel)

    async def get_geolocation(self, street: str) -> Location:
        request = geo_pb2.GetGeolocationRequest(Street=street)
        response = await self.stub.GetGeolocation(request)
        location = Location(X=response.Location.x, Y=response.Location.y)
        return location
