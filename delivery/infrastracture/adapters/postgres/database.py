import logging
from collections.abc import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from delivery.settings import settings


logger = logging.getLogger(__name__)


engine: AsyncEngine = create_async_engine(settings.db.pg_dsn, echo=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield async_session
    except SQLAlchemyError as e:
        logger.exception(e)
