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

## Database Issue Encountered

During development, the application was connecting to the wrong PostgreSQL database because an old `DATABASE_URL` was still being loaded.

This caused errors when the application tried to access tables that existed in the correct database but not in the connected one.

The issue was fixed by updating `db.py` to load the `.env` file from the project directory and use the correct `DATABASE_URL`. A check was also added to confirm that the database configuration exists before creating a connection.


## Status

The application is fully functional with:

* Railway PostgreSQL integration
* Session-based identity system
* Working login, guest login, and logout
* Dynamic message rendering from database

