from fastapi import HTTPException
import requests
from app.setting import KONG_ADMIN_URL

def create_consumer_in_kong(email: str):
    try: 
        response = requests.post(f"http://localhost:8001/consumers/", data={"username": email})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error creating consumer in Kong: {e}")

def create_jwt_credentials_in_kong(email: str, kid: str):
    try:
        response = requests.post(f"http://localhost:8001/consumers/{email}/jwt", data={"key": kid})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error creating JWT credentials in Kong: {e}")