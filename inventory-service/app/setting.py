from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("database-urls", cast=Secret)
TEST_DATABASE_URL = config("tests-database-url", cast=Secret)
SECRET_KEY = config("secret-keys", cast=str)
ALGORITHM = config("algorithim", cast=str)

CLOUDINARY_CLOUD = config("cloudinary-clouds", cast=str)
CLOUDINARY_API_KEY = config("cloudinary-api-keys", cast=str)
CLOUDINARY_API_SECRET = config("cloudinary-api-secrets", cast=str)

INVENTORY_TOPIC = config("inventory-topics", cast=str)