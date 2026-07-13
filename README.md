# Chat Forum MVP – Flask + PostgreSQL (Railway)

## Overview

A simple Flask chat forum built with Flask and PostgreSQL hosted on Railway. Users can log in, browse forum messages, and post messages stored in the database.

## Features

* Flask web application
* PostgreSQL database hosted on Railway
* Username-based login (MVP)
* Guest login
* Session-based authentication
* Dynamic forum messages

## Project Structure

```text
app.py
templates/
    forum.html
schema.md
README.md
screenshots/
```

## Installation

1. Clone the repository.

```bash
git clone <repository-url>
cd <repository-folder>
```

2. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install the required packages.

```bash
pip install -r requirements.txt
```

## Environment Variables

This application requires the following environment variables:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-railway-postgresql-url
```

The application reads these values using `os.getenv(...).strip()` before configuring Flask and connecting to the Railway PostgreSQL database.

* `SECRET_KEY` – Used by Flask to manage sessions.
* `DATABASE_URL` – Connection string for the Railway PostgreSQL database.

If deploying on Railway, add both variables in your Railway project's **Variables** tab.

## Running the Application

Start the Flask development server:

```bash
python app.py
```

Then open your browser and visit:

```text
http://127.0.0.1:5000
```

## Database

The application uses the following tables:

* `users`
* `channels`
* `messages`

See `schema.md` for the database schema.

## Notes

* No passwords are used (MVP design choice)
* Session is the only source of truth for authentication
* No credentials are hardcoded in the codebase
* Application assumes a preconfigured Railway PostgreSQL database

---
## Switching from Railway PostgreSQL to Local PostgreSQL

The project was initially developed using a PostgreSQL database hosted on Railway. For local development and testing, the application was moved to a locally hosted PostgreSQL database.

The migration process involved:

* Creating a local PostgreSQL database (`chatforum`).
* Updating the `DATABASE_URL` in the `.env` file to use the local database connection.
* Creating the required database tables locally.
* Testing the application to confirm that Flask was connecting to the local database successfully.

Local database configuration:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/chatforum
```

The application can now be run locally without depending on the Railway database.

## Database Issues Encountered

During development, the application was initially connecting to the wrong PostgreSQL database because an old `DATABASE_URL` was still being loaded. This caused errors because the required tables were not available in the connected database.

### Steps Taken

1. Checked the error message and identified that the `channels` table could not be found.
2. Verified the database connection using pgAdmin.
3. Created the required tables in the local `chatforum` database:

   * `users`
   * `channels`
   * `messages`
4. Updated the environment configuration to point to the local PostgreSQL database.
5. Updated `db.py` to ensure the correct `.env` file was loaded.

### Previous `db.py` Configuration

The application was loading environment variables using:

```python
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

This caused the application to load an outdated database URL.

### Updated `db.py` Configuration

The configuration was changed to explicitly load the `.env` file from the project directory:

```python
import os
import psycopg2
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


def get_conn():
    return psycopg2.connect(DATABASE_URL)
```

### Result

After updating the database configuration, Flask successfully connected to the local PostgreSQL database and was able to access the required tables.

## Status

The application is fully functional with:

* Railway PostgreSQL integration
* Session-based identity system
* Working login, guest login, and logout
* Dynamic message rendering from database

