import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    db_url = DATABASE_URL.strip()
    print(f"Connecting to database at {db_url}!..")
    return psycopg2.connect(db_url)