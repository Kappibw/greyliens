# Chat Forum MVP – Flask + PostgreSQL

## Overview

Chat Forum MVP is a simple forum application built using Flask and PostgreSQL. The application allows users to log in, browse forum messages, and post messages stored in a PostgreSQL database.

The application uses environment variables to configure the database connection, allowing it to run with either a local PostgreSQL database or a hosted PostgreSQL database such as Railway.

---

## Features

* Flask web application
* PostgreSQL database integration
* Support for local and hosted PostgreSQL databases
* Username-based login (MVP)
* Guest login
* Session-based authentication
* Dynamic forum message rendering

---

## Project Structure

```text
app.py
auth.py
db.py
templates/
    forum.html
schema.md
requirements.txt
README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root directory.

The application requires:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-postgresql-connection-string
```

### SECRET_KEY

`SECRET_KEY` is used by Flask to securely manage user sessions.

Example:

```env
SECRET_KEY=my-secret-key
```

---

# Database Configuration

The application connects to PostgreSQL using the `DATABASE_URL` environment variable.

The same code works with both local and hosted databases. Only the value of `DATABASE_URL` needs to change.

---

## Option 1: Local PostgreSQL Database

To run the application locally, create a PostgreSQL database and update your `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/chatforum
```

Make sure the required tables exist:

* users
* channels
* messages

---

## Option 2: Railway PostgreSQL Database

To use Railway PostgreSQL:

1. Create or open your Railway project.
2. Add a PostgreSQL database service.
3. Copy the provided PostgreSQL connection string.
4. Add it to your `.env` file:

```env
DATABASE_URL=your-railway-postgresql-connection-string
```

No code changes are required when switching between local PostgreSQL and Railway PostgreSQL.

---

## Running the Application

Start the Flask development server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## Database

The application uses the following database tables:

* `users`
* `channels`
* `messages`

The database schema is documented in:

```text
schema.md
```

---

## Notes

* Authentication is session-based.
* Password authentication is not implemented because this is an MVP.
* Database credentials should be stored in environment variables and should not be committed to the repository.
* The `.env` file should remain private and be included in `.gitignore`.




