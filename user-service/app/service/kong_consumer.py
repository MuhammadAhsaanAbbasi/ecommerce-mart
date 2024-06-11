from fastapi import HTTPException
import requests
from app.setting import KONG_ADMIN_URL

def create_consumer_in_kong(email:str):
    response = requests.post(f"{KONG_ADMIN_URL}/consumers", data={"username": email})
    if response.status_code != 201:
        raise HTTPException(
            status_code=500, detail="Error creating consumer in Kong")

def create_jwt_credentials_in_kong(email:str, kid:str):
    response = requests.post(f"{KONG_ADMIN_URL}/consumers/{email}/jwt", data={"key": kid})
    if response.status_code != 201:
        raise HTTPException(
            status_code=500, detail="Error creating JWT credentials in Kong")