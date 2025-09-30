import asyncio
from typing import Any
from uuid import UUID

import cloudinary
from cloudinary.uploader import destroy, upload

from src.schemas import UploadImageResult

from .config import settings


class Cloudinary:
    """Async facade over Cloudinary SDK with deterministic public_id."""

    def __init__(
        self,
        cloud_name: str,
        api_key: str,
        api_secret: str,
        secure: bool,
        asset_folder: str,
    ) -> None:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=secure,
        )
        self.asset_folder = asset_folder

    async def upload_image(
        self,
        user_id: int,
        photo_uuid: UUID,
        file: bytes,
    ) -> UploadImageResult:
        """Upload image under public_id=photo_uuid and return upload result."""
        options = {
            "public_id": str(photo_uuid),
            "asset_folder": f"{self.asset_folder}/{user_id}",
            "use_asset_folder_as_public_id_prefix": False,
            "unique_filename": False,
            "resource_type": "image",
            "overwrite": True,
        }
        result: dict[str, Any] = await asyncio.to_thread(upload, file=file, **options)
        return UploadImageResult(**result)

    async def destroy_image(self, photo_uuid: UUID) -> None:
        """Delete image by public_id and invalidate caches."""
        public_id = str(photo_uuid)
        options = {
            "resource_type": "image",
            "type": "upload",
            "invalidate": True,
        }
        await asyncio.to_thread(destroy, public_id=public_id, **options)


cloudinary_cli = Cloudinary(
    cloud_name=settings.cloudinary.cloud_name,
    api_key=settings.cloudinary.api_key,
    api_secret=settings.cloudinary.api_secret,
    secure=settings.cloudinary.secure,
    asset_folder=settings.cloudinary.asset_folder,
)
