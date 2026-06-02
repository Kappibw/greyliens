
# Chat Forum MVP – Flask + PostgreSQL (Railway)

## Overview

This project is a Flask-based chat forum application connected to a PostgreSQL database hosted on Railway.

It demonstrates:

* Secure database connection using environment variables
* Retrieval of messages using SQL JOIN queries
* Display of database-driven content in a Flask web interface
* Basic relational database structure (users, channels, messages)

---

## Features

* Flask web application
* Railway-hosted PostgreSQL database
* Environment variable configuration using `DATABASE_URL`
* Relational SQL queries using JOINs
* Dynamic rendering of messages from the database

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

## Environment Variables

This project requires a PostgreSQL connection string from Railway.

Set the environment variable:

### Windows (PowerShell)

```
setx DATABASE_URL "your_railway_postgres_connection_string"
```

Then restart your terminal.

---

## Installation

Install dependencies:

```
pip install flask psycopg2-binary
```

---

## Running the Application

Start the Flask server:

```
python app.py
```

Open in browser:

```
http://127.0.0.1:5000/
```

---

## Database Query Logic

The application retrieves messages using SQL JOIN queries:

* messages table (content, timestamps)
* users table (username)
* channels table (channel name)

This ensures normalized relational data is displayed correctly.

---

## Database Inspection

DBGate was used to:

* Inspect database tables
* Verify relationships between entities
* Confirm inserted records
* Validate query output

---

## Screenshots


* DBGate: users table
* DBGate: channels table
* DBGate: messages table
* Flask UI showing messages loaded from database

---

## Troubleshooting

### Database not connecting

Ensure `DATABASE_URL` is correctly set in environment variables.

### No messages displayed

Check that the `messages` table contains data.

### SQL errors

Ensure tables exist and relationships match schema.

---

## Notes

* No credentials are hardcoded in the application
* Database access is handled using environment variables
* The root route `/` displays all messages from the database
* The application assumes a preconfigured Railway PostgreSQL database

---

## Status

The application is fully connected to a Railway PostgreSQL database and successfully renders dynamic data from the database in a Flask web interface.

---



* fix final Git push (so you don’t break again)
* or verify your PR before submission
* or check your screenshots match grading requirements

Just tell me 👍
