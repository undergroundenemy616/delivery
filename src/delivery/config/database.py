from pydantic import BaseModel


class DBSettings(BaseModel):
    use_ssl: bool = False
    debug_sql: bool = False
    pg_dsn: str = "postgresql+asyncpg://ruby:ruby@0.0.0.0:5432/delivery"
    pg_test_dsn: str = "postgresql+asyncpg://ruby:ruby@0.0.0.0:5433/delivery_test"
