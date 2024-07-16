from pydantic_settings import BaseSettings, SettingsConfigDict

from .background_jobs_delays import BackGroundJobsDelays
from .database import DBSettings
from .enums import Stand, StorageTypes
from .geo_service import GeoServiceSettings
from .logger import LoggingSettings


class Settings(BaseSettings):
    geo_service: GeoServiceSettings = GeoServiceSettings()
    db: DBSettings = DBSettings()
    redis_url: str = "redis://redis:6379"
    storage: StorageTypes = StorageTypes.postgres
    logging: LoggingSettings = LoggingSettings()
    background_jobs_delays: BackGroundJobsDelays = BackGroundJobsDelays()

    stand: str = Stand.local
    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings()


__all__ = ["settings", "StorageTypes", "Stand", "DBSettings"]
