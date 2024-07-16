from app.setting import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD
from app.setting import BUCKET_NAME, AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY
from botocore.exceptions import NoCredentialsError # type: ignore
from fastapi import HTTPException, UploadFile
from fastapi import UploadFile, HTTPException
import cloudinary.uploader # type: ignore
import cloudinary # type: ignore
import boto3 # type: ignore
from typing import List
import json


# Configuration       
cloudinary.config( 
    cloud_name = CLOUDINARY_CLOUD, 
    api_key = CLOUDINARY_API_KEY, 
    api_secret = CLOUDINARY_API_SECRET, # Click 'View Credentials' below to copy your API secret
    secure=True
)

async def upload_files_in_s3(file: UploadFile):
    s3_client = boto3.client("s3",
                            aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY
                            )
    try:
        object_name = f"products/{file.filename}"
        print(f"Object Name : {object_name}")
        image_s3 = s3_client.upload_fileobj(
                file.file,
                BUCKET_NAME,
                object_name
            )
        print(image_s3)
        image_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{
                object_name}"
        return image_url
    except NoCredentialsError as nce:
            raise HTTPException(status_code=500, detail=str(nce))


def upload_image(image: UploadFile):
    try:
        upload_result = cloudinary.uploader.upload(image.file)
        return upload_result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error Occurs during image upload: {e}")