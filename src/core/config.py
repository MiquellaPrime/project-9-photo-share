from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseModel):
    """PostgreSQL connection configuration."""

    host: str
    port: int = 5432
    user: str
    password: str
    dbname: str

    @property
    def async_dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class DatabaseConfig(BaseModel):
    """Database engine configuration."""

    postgres: PostgresConfig

    @property
    def url(self) -> str:
        return self.postgres.async_dsn

    echo: bool = False
    pool_size: int = 30
    max_overflow: int = 20
    pool_pre_ping: bool = True
    pool_recycle: int = 3600


class Settings(BaseSettings):
    """Main application settings container."""

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )
    db: DatabaseConfig


settings = Settings()
