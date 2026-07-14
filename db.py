import os
import psycopg2

# Read the database URL at module import time but validate before use.
DATABASE_URL = os.getenv("DATABASE_URL")

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

    print(f"Connecting to database at {db_url}!..")
    return psycopg2.connect(db_url)