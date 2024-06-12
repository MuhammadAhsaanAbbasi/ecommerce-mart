from fastapi import HTTPException
import requests
from requests.exceptions import HTTPError
from app.setting import SECRET_KEY

KONG_ADMIN_URL = "http://kong:8001"

def create_consumer_in_kong(email: str):
    url = f"{KONG_ADMIN_URL}/consumers/"
    payload = {"username": email}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        if response.status_code == 409:
            print(f"Consumer {email} already exists. Skipping creation.")
        else:
            raise http_err


def create_jwt_credentials_in_kong(email: str, kid: str):
    url = f"{KONG_ADMIN_URL}/consumers/{email}/jwt"
    payload = {
        "key": kid,  # You can generate a unique key
        "secret": SECRET_KEY
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        raise http_err