
import os
import psycopg2
from dotenv import load_dotenv

# Load .env from the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

# Read the database URL at module import time but validate before use.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


def get_conn():
    """Return a new psycopg2 connection.

    Raises RuntimeError with a clear message when the environment
    variable is missing or empty instead of raising an obscure
    AttributeError on .strip() or letting psycopg2 receive an empty
    string.
    """

    if not DATABASE_URL:
        raise RuntimeError("Environment variable 'DATABASE_URL' is not set")

    db_url = DATABASE_URL.strip()
    if not db_url:
        raise RuntimeError("Environment variable 'DATABASE_URL' is empty")

    return psycopg2.connect(db_url)
