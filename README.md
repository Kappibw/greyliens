# 📘 Chat Forum MVP – Flask + PostgreSQL (Railway)

## 📌 Overview

This project is a Chat Forum MVP backend built using Flask and PostgreSQL hosted on Railway.

It demonstrates a simple messaging system with:
- Users
- Channels
- Messages

The system connects Flask to a live PostgreSQL database using environment variables.

---

## ⚙️ Tech Stack

- Python 3
- Flask
- PostgreSQL (Railway)
- psycopg2

---

## 🗄️ Database Structure

### Users
- id (Primary Key)
- username
- created_at

### Channels
- id (Primary Key)
- name
- description
- is_private
- created_at
- updated_at

### Messages
- id (Primary Key)
- channel_id (Foreign Key)
- author_id (Foreign Key)
- content
- created_at

---

## 🔌 Database Connection (Railway)

The app connects to Railway PostgreSQL using environment variables:

```python
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DATABASE_URL)