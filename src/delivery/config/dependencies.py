from functools import lru_cache

import punq
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.core.ports.bus_producer_interface import BusProducerInterface
from delivery.core.ports.geo_service_client import GeoServiceClientInterface
from delivery.infrastracture.adapters.grpc.geo.client import GeoServiceClientGRPC
from delivery.infrastracture.adapters.kafka.producer import KafkaBusProducer
from delivery.infrastracture.adapters.postgres.database import get_session
from delivery.infrastracture.adapters.postgres.repositories.uow import SqlAlchemyUnitOfWork
from delivery.core.ports.uow_interface import UnitOfWork


@lru_cache(1)
def get_container() -> punq.Container:
    return _initialize_container()


def _initialize_container() -> punq.Container:
    container = punq.Container()
    container.register(AsyncSession, instance=get_session)
    container.register(UnitOfWork, factory=_get_uow)
    container.register(GeoServiceClientInterface, GeoServiceClientGRPC)
    container.register(BusProducerInterface, KafkaBusProducer)
    return container


def _get_uow() -> UnitOfWork:
    return SqlAlchemyUnitOfWork(get_session=get_container().resolve(AsyncSession))
