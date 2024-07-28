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

USER_SIGNUP_EMAIL_TOPIC = config("USER_SIGNUP_EMAIL_TOPIC", cast=str)

PRODUCT_TOPIC = config("PRODUCT_TOPIC", cast=str)

INVENTORY_TOPIC = config("INVENTORY_TOPIC", cast=str)

DOMAIN_NAME = config("DOMAIN_NAME", cast=str)
AWS_REGION = config("AWS_REGION", cast=str)
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
AWS_SECRET_KEY = config("AWS_SECRET_KEY", cast=str)