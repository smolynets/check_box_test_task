import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_USER = os.getenv("POSTGRES_USER", "psql_user")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "psql_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "psql_db")

SERVICE_NAME = os.getenv("SERVICE_NAME", "fastapi_boilerplate")
DEBUG = bool(int(os.getenv("DEBUG", "0")))
