
import os
import psycopg2
from dotenv import load_dotenv

# Load .env from the same folder as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")

print("LOADED DATABASE:", DATABASE_URL)


def get_conn():
    return psycopg2.connect(DATABASE_URL.strip())

