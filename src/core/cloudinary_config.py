import os
import cloudinary
from dotenv import load_dotenv


# load environment variables
load_dotenv()

# Configure the Cloudinary photo service.
def init_cloudinary():
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key=os.getenv("CLOUDINARY_API_KEY")
    api_secret=os.getenv("CLOUDINARY_API_SECRET")


    if not all([cloud_name, api_key, api_secret]):
        raise ValueError("Cloudinary environment variables are not set properly.")

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret,
    )




