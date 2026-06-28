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

* This MVP uses username-based login without passwords.
* Database credentials are stored using environment variables.
* The application uses a Railway-hosted PostgreSQL database.

