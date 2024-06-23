from fastapi import UploadFile, HTTPException
import cloudinary # type: ignore
from app.setting import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD
import cloudinary.uploader # type: ignore
import json

# Configuration       
cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET, # Click 'View Credentials' below to copy your API secret
    secure=True
)

def upload_image(image: UploadFile):
    try:
        upload_result = cloudinary.uploader.upload(image.file)
        return upload_result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Occurs during image upload: {e}")