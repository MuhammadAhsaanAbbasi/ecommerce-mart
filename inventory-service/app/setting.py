from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE-URL", cast=Secret)
TEST_DATABASE_URL = config("TEST-DATABASE-URL", cast=Secret)
SECRET_KEY = config("SECRET-KEY", cast=str)
ALGORITHM = config("ALGORITHM", cast=str)

CLOUDINARY_CLOUD = config("CLOUDINARY-CLOUD", cast=str)
CLOUDINARY_API_KEY = config("CLOUDINARY-API-KEY", cast=str)
CLOUDINARY_API_SECRET = config("CLOUDINARY-API-SECRET", cast=str)

INVENTORY_TOPIC = config("INVENTORY-TOPIC", cast=str)