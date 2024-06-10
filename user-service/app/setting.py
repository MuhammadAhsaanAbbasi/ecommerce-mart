from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
SECRET_KEY = config("SECRET_KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)
ACCESS_TOKEN_EXPIRE_MINUTES= config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES= config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)

USER_SIGNUP_TOPIC= config("USER_SIGNUP_TOPIC", cast=str)
USER_OTP_TOPIC= config("USER_OTP_TOPIC", cast=str)
USER_SIGNIN_TOPIC= config("USER_SIGNIN_TOPIC", cast=str)
USER_GOOGLE_TOPIC= config("USER_GOOGLE_TOPIC", cast=str)
KONG_TOPIC= config("KONG_TOPIC", cast=str)



REDIRECT_URI = config("REDIRECT_URI", cast=str)
FRONTEND_CLIENT_SUCCESS_URI = config("FRONTEND_CLIENT_SUCCESS_URI", cast=str)
FRONTEND_CLIENT_FAILURE_URI = config("FRONTEND_CLIENT_FAILURE_URI", cast=str)   