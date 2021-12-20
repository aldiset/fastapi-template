import os

from .db_dsn import DbDSN
from starlette.config import Config

config = Config(".env")

# DB

DB_DRIVER = config("DB_DRIVER", default="mysql")
DB_USERNAME = config("DB_USERNAME", default="root")
DB_PASSWORD = config("DB_PASSWORD", default="")
DB_SERVER = config("DB_SERVER", default="127.0.0.1")
DB_PORT = config("DB_PORT", default="3306")
DB_NAME = config("DB_NAME", default="db_api")

DB_DSN = DbDSN.build(
    scheme=DB_DRIVER,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=f"{DB_SERVER}:{DB_PORT}",
    path=f"/{DB_NAME}",
)

# General
API_PREFIX = config("API_PREFIX", default="")
API_BASE_URL = config("API_BASE_URL", default="")
PROJECT_NAME = config("PROJECT_NAME", default="My Api")
DEBUG = config("DEBUG", cast=bool, default=True)
VERSION = config("VERSION", default="")
PAGINATION_LIMIT = config("PAGINATION_LIMIT", default=20)
WSO_API_KEY = config("WSO_API_KEY", default="")


