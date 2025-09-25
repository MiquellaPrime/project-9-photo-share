import json

from cloudinary.api import transformation
from fastapi import FastAPI, status, Depends, UploadFile, File, Form, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.photo import Photo
from src.models.tag import Tag
from src.models.users import User
import cloudinary.uploader
from dotenv import load_dotenv
import os
import cloudinary
from typing import List, Optional

from src.create_app import create_app
from src.schemas import HealthResponse

# load environment variables
load_dotenv()

# Configure the Cloudinary photo service.
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_SECRET"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secret=True
)

app = FastAPI()

# Define the photo transformations we allow.
ALLOWED_TRANSFORMATIONS = {
    "resize": [{"width": 800, "height": 600, "crop": "limit"}],
    "grayscale": [{"effect": "grayscale"}],
    "rotate": [{"angle": 90}],
    "thumbnail": [{"width": 150, "height": 150, "crop": "thumb"}],
}

## Core Routes

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(
        url="/docs",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def check_health():
    return JSONResponse(
        content={"status": "ok"},
        status_code=status.HTTP_200_OK,
        headers={"Cache-Control": "no-cache"},
    )

### **Photo Management (CRUD)**

# ------------------------
# GET all photos
# ------------------------
@app.get("/photos")
def read_photos(db: Session = Depends(get_db)):
    """Gets a list of all photos from the database."""
    return db.query(Photo).all()

# ------------------------
# POST a new photo
# ------------------------
@app.post("/photos")
def create_photo(
        file: UploadFile = File(...), # Uploaded photo file
        description: str = Form(None), # Optional photo description
        tags: str = Form(None), # Optional photo description
        transformations: Optional[str] = Form(None),
        db: Session = Depends(get_db),
        user_id: int = 1 # This should be from an authenticated user
):
    transform_list = []
    if transformations:
        try:
            user_transforms = json.loads(transformations)
            for t in user_transforms:
                allowed_t = {k: v for k, v in t.itemss() if k in ALLOWED_TRANSFORMATIONS}
                if allowed_t:
                    transform_list.append(allowed_t)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid transformations format")

    # Upload the file to Cloudinary
    result = cloudinary.uploader.upload(
        file.file,
        transformation=[
            {"width": 800, "height": 600, "crop": "limit"}, {"quality": "auto"}
        ]
    )
    url = result["secure_url"]
    public_id = result["public_id"]
    # Create a new Photo object
    photo = Photo(
        user_id=user_id,
        url=url,
        public_id=public_id,
        description=description
    )
    # Handle tags (max 5)
    if tags:
        tag_names = [t.strip() for t in tags.split(",")][:5]
        for name in tag_names:
            tag = db.query(Tag).filter(Tag.name == name).first()
            if not tag:
                # Create the tag if it does not exist
                tag = Tag(name=name)
                db.add(tag)
                db.commit()
                db.refresh(tag)
            photo.tags.append(tag)

    # Save the photo to the database
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

# ------------------------
# PUT update photo description
# ------------------------
@app.put("/photos/{photo_id}")
def update_photo(photo_id: int, description: str = Form(...), db: Session = Depends(get_db)):
    """Updates the description of an existing photo."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    photo.description = description
    db.commit()
    db.refresh(photo)
    return photo

# ------------------------
# DELETE photo by ID
# ------------------------
@app.delete("/photo/{photo_id}")
def delete_photo(photo_id: int, db:Session = Depends(get_db)):
    """Deletes a photo from the database and from Cloudinary."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    # First, delete from Cloudinary to avoid orphaned files.
    cloudinary.uploader.destroy(photo.public_id)
    db.delete(photo)
    db.commit()
    return {"detail": "Photo delete"}

# ------------------------
# GET photo by public_id
# ------------------------
@app.get("/photo/public/{public_id}")
def get_photo(public_id: str, db: Session = Depends(get_db)):
    """Gets a photo by its unique ID."""
    photo = db.query(Photo).filter(Photo.public_id == public_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

## Transformations and QR Codes

@app.post("/photos/{photos_id}/transform")
def transform_photo(
        photo_id: int,
        transformation: str = Form(...),
        db:Session = Depends(get_db)
):
    """Applies a predefined transformation to a photo and returns the new URL."""
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if transformation not in ALLOWED_TRANSFORMATIONS:
        raise HTTPException(status_code=400, detail=f"Transformation not allowed. Choose one of: {list(ALLOWED_TRANSFORMATIONS.keys())}")
    # Apply the transformation on Cloudinary.
    result = cloudinary.uploader.explicit(
        photo.public_id,
        type="upload",
        eager=ALLOWED_TRANSFORMATIONS[transformation]
    )
    # Get the URL of the transformed photo.
    transformed_url = result["eager"][0]["secure_url"]

    return {"original_url": photo.url, "transformed_url": transformed_url}

### **Generate a QR Code**