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

BUCKET_NAME = config("BUCKET_NAME", cast=str)
AWS_REGION = config("AWS_REGION", cast=str)
AWS_ACCESS_KEY = config("AWS_ACCESS_KEY", cast=str)
AWS_SECRET_KEY = config("AWS_SECRET_KEY", cast=str)

PRODUCT_TOPIC = config("PRODUCT_TOPIC", cast=str)