 HEAD
# 📘 Chat Forum MVP – Flask + PostgreSQL

## 📌 Overview

This project is a Chat Forum MVP backend built using Flask and PostgreSQL (hosted on Railway).

It demonstrates a simple messaging system with:
- Users
- Channels
- Messages

It supports database-driven communication and full CRUD-style operations.

---

## ⚙️ Tech Stack

- Python 3
- Flask
- PostgreSQL (Railway)
- psycopg2
- DBGate

---

## 🗄️ Database Structure

### Users
- id (Primary Key)
- username (Unique)
- created_at

### Channels
- id (Primary Key)
- name (Unique)
- description
- is_private
- created_at
- updated_at

### Messages
- id (Primary Key)
- channel_id (Foreign Key → channels.id)
- author_id (Foreign Key → users.id)
- parent_message_id (Nullable for future replies)
- content
- edited
- created_at
- updated_at

---

## 🔌 Database Connection

The application uses environment variables:

```python
DATABASE_URL = os.getenv("DATABASE_URL")

# Flask Hello World Application

## Overview

This project demonstrates local Flask development setup.

The goal is to allow developers to:

1. Clone the repository
2. Install dependencies
3. Run the Flask app locally
4. Verify localhost works

---


## Clone Repository

```bash
git clone <REPOSITORY_URL>
cd <PROJECT_FOLDER>
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```


## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux


## Install Flask

```bash
pip install flask
```

## Save Dependencies

```bash
pip freeze > requirements.txt
```

---

# Running the Application

```bash
python app.py
```

---

# Verification Step

Open:

http://127.0.0.1:5000

Expected output:

Hello, Flask!

---

# Daily Development Workflow

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

## Run Flask

```bash
python app.py
```

---

# Common Setup Issues

## python not found

Try:

```bash
python3 --version
```

## flask not found

Activate virtual environment first.

Then run:

```bash
pip install -r requirements.txt
```

## Port already in use

Run:

```bash
flask run --port 5001
``
 origin/main
