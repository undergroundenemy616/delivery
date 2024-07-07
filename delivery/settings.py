from enum import StrEnum, auto

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class StorageTypes(StrEnum):
    postgres = auto()


class DBSettings(BaseModel):
    use_ssl: bool = False
    debug_sql: bool = False
    pg_dsn: str = "postgresql+asyncpg://ruby:ruby@0.0.0.0:5432/delivery"
    test_pg_dsn: str = "postgresql+asyncpg://ruby:ruby@0.0.0.0:5433/delivery_test"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    storage: StorageTypes = StorageTypes.postgres

    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings()
