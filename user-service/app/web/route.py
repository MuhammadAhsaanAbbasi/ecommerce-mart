from fastapi import APIRouter, Depends,  Form, Request, HTTPException, status
from fastapi.responses import RedirectResponse, JSONResponse, Response
from ..service.auth import create_user, login_for_access_token, google_user, verify_and_generate_tokens
from ..utils.auth import get_current_active_user, tokens_service, oauth2_scheme, get_current_active_admin_user
from ..setting import USER_GOOGLE_TOPIC, USER_OTP_TOPIC, USER_SIGNIN_TOPIC, USER_SIGNUP_TOPIC
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..model.models import Users, Token, Admin
from ..kafka.user_producer import get_kafka_producer
from aiokafka import AIOKafkaProducer # type: ignore
from aiokafka.errors import KafkaTimeoutError # type: ignore
from typing import Annotated, Any, Optional
from passlib.context import CryptContext
from sqlmodel import Session, select
from ..core.db import get_session
from datetime import timedelta
from app import user_pb2
import os
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Google Import
from google.oauth2 import id_token # type: ignore
from google_auth_oauthlib.flow import Flow # type: ignore
from google.auth.transport import requests as google_requests # type: ignore

# Authentication Import 
from ..setting import FRONTEND_CLIENT_SUCCESS_URI, FRONTEND_CLIENT_FAILURE_URI, REDIRECT_URI

# To avoid error: Exception occurred: (insecure_transport) OAuth 2 MUST utilize https.
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for testing, remove for production

# Load the secrets file
current_file_path = os.path.abspath(__file__)
# print(f"current file: {current_file_path}")

# Get the parent directory of the current file's directory
parent_directory = os.path.dirname(current_file_path)
# print(f"parent file: {parent_directory}")

# Get the parent directory of the parent directory
Child_DIR = os.path.dirname(parent_directory)


# Get the Chlid directory of the parent directory
BASE_DIR = os.path.dirname(Child_DIR)


# Define the path to the client_secret.json file
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'client_secret.json')
# print(f"client file: {CLIENT_SECRET_FILE}")
SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']

# Router
router = APIRouter(prefix="/api/v1")

# Google Login
@router.get("/auth/google/login")
async def login(request:Request):
    flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    
    authorization_url, state = flow.authorization_url(
        # Access type 'offline' so that the token can be refreshed
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true'
    )
    request.session['state'] = state
    return RedirectResponse(authorization_url)

# Google Callback
@router.get("/auth/google/callback")
async def auth(request: Request, session: Annotated[Session, Depends(get_session)]):
    try:
        state = request.session['state']

        if not state or state != request.query_params.get('state'):
            raise HTTPException(status_code=400, detail="State mismatch")

        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE, scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI)

        authorization_response = str(request.url)
        flow.fetch_token(authorization_response=authorization_response)

        credentials: Any = flow.credentials
        # idinfo contains the Google user’s info.
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token, google_requests.Request(), flow.client_config['client_id'])
        # print()
        print(idinfo['name'])
        print(idinfo['email'])
        print(idinfo['picture'])
        
        user_email = idinfo['email']

        user_name = idinfo['name']
        
        user_picture = idinfo['picture']

        # Check if the user exists in your database. If the user doesn't exist, add the user to the database
        new_google_user = await google_user(session, email=user_email, username=user_name, picture=user_picture)
        if new_google_user is None:
            raise HTTPException(status_code=400, detail="User not found")
        
        return new_google_user
    except HTTPException as http_exception:
        # Log the exception for debugging
        print(f"HTTPException occurred: {http_exception.detail}")

        # Append a failure reason to the redirect URL  
        failure_url = f"{FRONTEND_CLIENT_FAILURE_URI}?google_login_failed={http_exception.detail}"
        return RedirectResponse(url=failure_url)

    except Exception as exception:
        # Log the general exception for debugging
        print(f"Exception occurred: {exception}")

        # Append a generic failure message to the redirect URL
        failure_url = f"{FRONTEND_CLIENT_FAILURE_URI}?google_login_failed=error"
        return RedirectResponse(url=failure_url)

# Sign-up Routes
@router.post("/signup")
async def sign_up(user: Users, aio_producer: Annotated[AIOKafkaProducer, Depends(get_kafka_producer)]):
    try:
        user_protobuf = user_pb2.User(username=user.username, email=user.email, hashed_password=user.hashed_password, imageUrl=user.imageUrl, is_active=user.is_active, is_verified=user.is_verified, role=user.role) # type: ignore
        print(f"Todo Protobuf: {user_protobuf}")

        # Serialize the message to a byte string
        serialized_user = user_protobuf.SerializeToString()
        print(f"Serialized data: {serialized_user}")

        # Produce message
        await aio_producer.send_and_wait(topic="signup", value=serialized_user)
    except KafkaTimeoutError as e:
        print(f"Error In Print message...! {e}")
    finally:
        await aio_producer.stop()
        return user
    # users  =  create_user(user, session)
    # return users


@router.post("/signup/verify")
def verify_sign_up_otp(user_otp: str, user: Users, session:Annotated[Session, Depends(get_session)]):
    # Verify OTP
    tokens = verify_and_generate_tokens(user_otp, user, session)
    return tokens


# Login Routes
@router.post("/login", response_model=Token)
async def login_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(get_session)]):
    token = await login_for_access_token(form_data, session)
    return token


# token route
@router.post("/refresh_token", response_model=Token)
async def get_tokens(session: Annotated[Session, Depends(get_session)], refresh_token:Annotated[str, Depends(oauth2_scheme)]): 
    tokens = await tokens_service(refresh_token=refresh_token, session=session)
    return tokens

# user routes
@router.get("/user/me", response_model=Users)
async def read_users_me(current_user: Annotated[Users, Depends(get_current_active_user)]):
    return current_user

# admin routes
@router.get("/user/admin", response_model=Admin)
async def read_users_admin(current_user: Annotated[Admin, Depends(get_current_active_admin_user)]):
    return current_user