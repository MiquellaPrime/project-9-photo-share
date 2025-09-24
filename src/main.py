from fastapi import FastAPI, status, Depends, UploadFile, File, Form, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.photo import Photo
from src.models.tag import Tag
import cloudinary.uploader
import cloudinary
from src.routes import photos
from typing import List, Optional

from src.create_app import create_app
from src.schemas import HealthResponse
import os

from dotenv import load_dotenv

from src.models.photo import Photo
from src.models.tag import Tag
import cloudinary.uploader
import cloudinary
from src.routes import photos
from typing import List, Optional

app = FastAPI()


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

# load environment variables
load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_SECRET"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secret=True
)

app.include_router(photos.router)

ALLOWED_TRANSFORMATIONS = {} #TODO


# ------------------------
# GET all photos
# ------------------------
@app.get("/photos")
def read_photos(db: Session = Depends(get_db)):
    return db.query(Photo).all()

# ------------------------
# POST a new photo
# ------------------------
@app.post("/photos")
def create_photo(
        file: UploadFile = File(...), # Uploaded photo file
        description: str = Form(None), # Optional photo description
        tags: str = Form(None), # Optional photo description
        db: Session = Depends(get_db),
        user_id: int = 1 # Optional photo description
):
    # Upload the file to Cloudinary
    result = cloudinary.uploader.upload(file.file)
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
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    db.delete(photo)
    db.commit()
    return {"detail": "Photo delete"}


# ------------------------
# GET photo by public_id
# ------------------------
@app.get("/photo/public/{public_id}")
def get_photo(public_id: str, db: Session = Depends(get_db)):
    photo = db.query(Photo).filter(Photo.public_id == public_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

