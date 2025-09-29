import json
import os
import tempfile

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import cloudinary_cli
from src.core.models.photo import PhotoORM
from src.core.models.tag import TagORM

# Define the photo transformations we allow.
ALLOWED_TRANSFORMATIONS = {
    "resize": [{"width": 800, "height": 600, "crop": "limit"}],
    "grayscale": [{"effect": "grayscale"}],
    "rotate": [{"angle": 90}],
    "thumbnail": [{"width": 150, "height": 150, "crop": "thumb"}],
}


async def upload_photo(
    file, description, tags, transformations, user_id, db: AsyncSession
):
    transform_list = []
    if transformations:
        try:
            user_transforms = json.loads(transformations)
            for t in user_transforms:
                allowed_t = {k: v for k, v in t.items() if k in ALLOWED_TRANSFORMATIONS}
                if allowed_t:
                    transform_list.append(allowed_t)
        except json.JSONDecodeError:
            raise ValueError("Invalid transformations format")

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    result = await cloudinary_cli.upload_image(temp_path)
    os.remove(temp_path)

    # Create a new Photo object
    photo = PhotoORM(
        user_id=user_id,
        url=result["secure_url"],
        public_id=result["public_id"],
        description=description,
    )
    # Handle tags (max 5)
    tags_objs = []
    if tags:
        tag_names = [t.strip() for t in tags.split(",")][:5]
        for name in tag_names:
            q = await db.execute(select(TagORM).where(TagORM.name == name))
            tag = q.scalar_one_or_none()
            if not tag:
                tag = TagORM(name=name)
                db.add(tag)
                await db.flush()

            tags_objs.append(tag)

    # Save the photo to the database
    photo.tags.extend(tags_objs)

    db.add(photo)
    await db.commit()
    await db.refresh(photo)


async def transform_photo(
    photo: PhotoORM, transformation: str, db: AsyncSession
) -> str:
    if transformation not in ALLOWED_TRANSFORMATIONS:
        raise ValueError(
            f"Transformation not allowed. Choose one of: {list(ALLOWED_TRANSFORMATIONS.keys())}"
        )
    try:
        result = await cloudinary_cli.explicit_image(
            photo.public_id,
            ALLOWED_TRANSFORMATIONS[transformation],
        )
    except Exception as e:
        raise ValueError(f"Cloudinary transformation failed: {str(e)}")

    transformed_url = result["eager"][0]["secure_url"]
    return transformed_url


async def delete_photo(photo: PhotoORM, db: AsyncSession):
    try:
        await cloudinary_cli.destroy_image(photo.public_id)
    except Exception as e:
        raise ValueError(f"Cloudinary deletion failed: {str(e)}")

    await db.delete(photo)
    await db.commit()
