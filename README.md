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