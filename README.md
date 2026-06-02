# Chat Forum MVP – Flask + PostgreSQL (Railway)

## Overview

This project is a Flask-based chat forum application connected to a Railway-hosted PostgreSQL database.

It demonstrates:

* Secure database connection using environment variables
* Retrieval of messages from PostgreSQL
* Display of database-driven data in a Flask web interface

---

## Features

* Flask web application
* PostgreSQL database hosted on Railway
* Environment variable configuration (`DATABASE_URL`)
* SQL JOIN queries to combine users, channels, and messages
* Dynamic rendering of database content in the UI

---

## Project Structure

```
app.py
templates/
    forum.html
schema.md
README.md
```

---

## Installation

Install required dependencies:

```bash
pip install flask psycopg2-binary
```

---

## Environment Variables

Set your database connection string:

```bash
DATABASE_URL=your_railway_postgres_connection_string
```

Windows PowerShell:

```bash
setx DATABASE_URL "your_railway_postgres_connection_string"
```

Restart your terminal after setting the variable.

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000/
```

---

## Database Schema

The application uses three tables:

* users
* channels
* messages

These tables are related using foreign keys to support relational queries.

---

## Database Query Logic

Messages are retrieved using SQL JOIN queries that combine:

* messages (content + timestamps)
* users (username)
* channels (channel name)

---

## Database Inspection

DBGate was used to:

* Inspect PostgreSQL tables
* Verify relationships
* Confirm inserted data
* Validate query results

---

## Troubleshooting

### Database not connecting

Ensure `DATABASE_URL` is correctly set.

### No messages appearing

Check that messages exist in the `messages` table.

### Schema errors

Ensure database tables exist in Railway PostgreSQL.

---

## Notes

* No credentials are hardcoded in this project
* All database access uses environment variables
* The `/` route is the main interface for displaying messages

---

## Status

This project is fully connected to a Railway PostgreSQL database and successfully displays dynamic data from the database in a Flask web application.

---


