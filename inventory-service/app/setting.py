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

CLOUDINARY_CLOUD = config("CLOUDINARY_CLOUD", cast=str)
CLOUDINARY_API_KEY = config("CLOUDINARY_API_KEY", cast=str)
CLOUDINARY_API_SECRET = config("CLOUDINARY_API_SECRET", cast=str)

INVENTORY_TOPIC = config("INVENTORY_TOPIC", cast=str)