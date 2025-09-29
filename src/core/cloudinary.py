from asyncio import to_thread

import cloudinary
from cloudinary.uploader import destroy, upload

from src.core.config import CloudinaryConfig, settings


class CloudinaryClient:
    def __init__(self, config: CloudinaryConfig):
        self.config = config
        cloudinary.config(
            cloud_name=config.cloud_name,
            api_key=config.api_key,
            api_secret=config.api_secret,
            secure=config.secure,
        )

    async def upload_image(self, file_path: str, folder: str | None = None) -> dict:
        target_folder = folder or self.config.asset_folder
        result = await to_thread(upload, file_path, folder=target_folder)
        return result

    async def destroy_image(self, public_id: str) -> dict:
        result = await to_thread(destroy, public_id)
        return result


cloudinary_cli = CloudinaryClient(settings.cloudinary)
