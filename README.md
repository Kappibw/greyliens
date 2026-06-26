# Chat Forum MVP – Flask + PostgreSQL (Railway)

## Overview

This project is a Flask-based chat forum application connected to a PostgreSQL database hosted on Railway.

It demonstrates:

* Secure database connection using environment variables
* Session-based authentication using Flask
* Retrieval of messages using SQL JOIN queries
* Display of database-driven content in a Flask web interface
* Basic relational database structure (users, channels, messages)

---

## Features

* Flask web application
* Railway-hosted PostgreSQL database
* Session-based identity system (guest, logged-in user, logged out)
* Environment variable configuration using `SECRET_KEY` and `DATABASE_URL`
* Relational SQL queries using JOINs
* Dynamic rendering of messages from the database
* Guest login support
* Username-based login (no passwords – MVP)

---

## Project Structure

```
app.py
templates/
    forum.html
schema.md
README.md
screenshots/
```

---

## Database Schema

The database contains three main tables:

* users
* channels
* messages

### Relationships

* A user can create many messages
* A channel can contain many messages
* Each message belongs to one user and one channel

---

## Configuration

This application relies on environment variables and will not run correctly unless they are set.

Flask uses a secret key to manage sessions securely, and the application requires a database connection string to connect to the Railway PostgreSQL database.

### Required Environment Variables

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-railway-postgresql-url
```

* `SECRET_KEY` is used by Flask to securely sign session cookies and manage user sessions.
* `DATABASE_URL` is the PostgreSQL connection string provided by Railway.

---

### Environment Loading in the App

```python
database_url = os.getenv("DATABASE_URL").strip()
secret_key = os.getenv("SECRET_KEY").strip()

app.config["SECRET_KEY"] = secret_key
```

The `.strip()` method removes any accidental spaces from environment variables to prevent connection or authentication issues.

---

## Session System (Identity Model)

The application uses Flask sessions as the **single source of truth** for user identity.

### Identity States

* `logged_out` → no session data exists
* `guest` → temporary session without database user
* `db_user` → authenticated database user

### Session Data Stored

When a user logs in, the session stores:

* `user_id`
* `username`
* `identity_state`

---

## Authentication Routes

### `/login`

* Looks up user by username (no password for MVP)
* Stores user data in session
* Sets identity state to `db_user`

### `/guest-login`

* Creates a guest session
* Sets identity state to `guest`

### `/logout`

* Clears all session data
* Returns user to `logged_out` state

---

## Database Query Logic

Messages are retrieved using SQL JOIN queries:

* `messages` table → message content and timestamps
* `users` table → username
* `channels` table → channel name

This ensures normalized relational data is correctly displayed in the UI.

---

## Setting Up Environment Variables

### Windows (PowerShell)

```powershell
setx SECRET_KEY "your-secret-key"
setx DATABASE_URL "your-railway-postgresql-url"
```

Restart the terminal after setting variables.

---

### Railway Deployment

In Railway dashboard:

1. Open your project
2. Go to **Variables**
3. Add:

   * `SECRET_KEY`
   * `DATABASE_URL`

The app will not start without both variables.

---

## Database Inspection

DBGate was used to:

* Inspect database tables
* Verify relationships
* Confirm inserted records
* Validate SQL JOIN query output

---

## Troubleshooting

### App does not start

* Ensure `SECRET_KEY` is set
* Ensure `DATABASE_URL` is correct

### No messages showing

* Check `messages` table contains data
* Verify JOIN query logic

### Database connection fails

* Confirm Railway PostgreSQL is active
* Check connection string formatting

---

## Notes

* No passwords are used (MVP design choice)
* Session is the only source of truth for authentication
* No credentials are hardcoded in the codebase
* Application assumes a preconfigured Railway PostgreSQL database

---

## Status

The application is fully functional with:

* Railway PostgreSQL integration
* Session-based identity system
* Working login, guest login, and logout
* Dynamic message rendering from database

