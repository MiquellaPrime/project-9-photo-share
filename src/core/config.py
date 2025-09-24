from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsWithConfig(BaseSettings):
    """Base settings class with common configuration for environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


class Settings(BaseSettingsWithConfig):
    """Main application settings container."""

    pass


settings = Settings()
