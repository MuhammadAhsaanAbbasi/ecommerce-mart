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

NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY = config("NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY", cast=str)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", cast=str)

NEXT_PUBLIC_APP_URL = config("NEXT_PUBLIC_APP_URL", cast=str)