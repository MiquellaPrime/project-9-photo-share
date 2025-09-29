from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CloudinaryConfig(BaseModel):
    cloud_name: str = Field(..., env="CLOUDINARY_CLOUD_NAME")
    api_key: str = Field(..., env="CLOUDINARY_API_KEY")
    api_secret: str = Field(..., env="CLOUDINARY_API_SECRET")
    secure: bool = True
    asset_folder: str = "photo-share"


class Settings(BaseSettings):
    """Main application settings container."""

    cloudinary: CloudinaryConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore",
    )


settings = Settings()
