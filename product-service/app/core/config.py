from typing import List
import boto3 # type: ignore
from botocore.exceptions import NoCredentialsError # type: ignore
from fastapi import HTTPException, UploadFile
from app.setting import BUCKET_NAME, AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY


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