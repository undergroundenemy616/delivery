import pytest
from punq import Container
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from delivery.config import settings
from delivery.infrastracture.adapters.postgres.models import Base
from delivery.utils.uow.uow_interface import UnitOfWork


global_engine = None


@pytest.fixture(scope="session")
def engine():
    global global_engine
    engine = create_async_engine(
        settings.db.pg_test_dsn,
        poolclass=NullPool,
    )
    global_engine = engine
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture(autouse=True)
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncSession:
    return AsyncSession(global_engine)


@pytest.fixture
def container() -> Container:
    from delivery.config.dependencies import get_container

    container = get_container()
    container.registrations._Registry__registrations.pop(AsyncSession)
    container.register(AsyncSession, instance=get_session)  # type: ignore[misc]
    return container


@pytest.fixture
async def uow(container):
    return container.resolve(UnitOfWork)


@pytest.fixture
async def session(container, engine):
    async with AsyncSession(engine) as session:
        yield session
