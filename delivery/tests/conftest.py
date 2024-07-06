import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from delivery.infrastracture.adapters.postgres.models import Base
from delivery.settings import settings


@pytest.fixture(scope="session")
def engine():
    engine = create_async_engine(
        settings.db.test_pg_dsn,
        poolclass=NullPool,
    )
    yield engine
    engine.sync_engine.dispose()


@pytest.fixture
async def create(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session(engine, create):
    async with AsyncSession(engine) as session:
        yield session
