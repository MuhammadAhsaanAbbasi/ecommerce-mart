from fastapi import HTTPException
import requests
from requests.exceptions import HTTPError
from app.setting import  SECRET_KEY

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
# {"consumer":null,"id":"b55836bd-341a-4a36-9d39-21f02001cd6c","created_at":1718084929,"updated_at":1718206952,"route":{"id":"78c4596b-ab42-414e-801a-68de8315f8f1"},"name":"jwt","protocols":["grpc","grpcs","http","https"],"instance_name":null,"enabled":true,"tags":null,"service":{"id":"18711feb-143c-48c8-8966-c15f630b669f"},"config":{"claims_to_verify":[],"maximum_expiration":0,"run_on_preflight":true,"secret_is_base64":false,"header_names":["authorization"],"uri_param_names":["jwt"],"cookie_names":[],"anonymous":null,"key_claim_name":"iss"}}

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