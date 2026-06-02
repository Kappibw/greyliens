# Chat Forum MVP Schema Plan

This document defines the minimum database structure used in the Chat Forum MVP. The goal is to support core chat functionality while keeping the schema simple and easy to extend later.

This schema is implemented in a Flask application connected to a Railway-hosted PostgreSQL database and inspected using DBGate.

---

## Parent Issue

#1

---

## Define User Behaviors

| User Behavior                     | Required Data                      |
| --------------------------------- | ---------------------------------- |
| View channels                     | Channel name, description          |
| Open a channel                    | Channel ID                         |
| Send a message                    | Message content, channel reference |
| Edit a message                    | Updated timestamp, edited flag     |
| Support posting by existing users | Username and user reference        |

---

## Core Entities (Implemented in PostgreSQL)

---

## Users Table

| Field      | Type        | Constraints      | Description                         |
| ---------- | ----------- | ---------------- | ----------------------------------- |
| id         | integer     | Primary Key      | Unique identifier for the user      |
| username   | varchar(50) | Unique, Required | Username used when posting messages |
| created_at | timestamp   | Required         | User creation time                  |

---

## Channels Table

| Field       | Type        | Constraints      | Description                       |
| ----------- | ----------- | ---------------- | --------------------------------- |
| id          | integer     | Primary Key      | Unique identifier for the channel |
| name        | varchar(50) | Unique, Required | Channel name                      |
| description | text        | Optional         | Channel purpose                   |

---

## Messages Table

| Field             | Type      | Constraints                         | Description           |
| ----------------- | --------- | ----------------------------------- | --------------------- |
| id                | integer   | Primary Key                         | Unique message ID     |
| channel_id        | integer   | Foreign Key → channels.id           | Associated channel    |
| author_id         | integer   | Foreign Key → users.id              | Message author        |
| parent_message_id | integer   | Nullable, Foreign Key → messages.id | Reply support         |
| content           | text      | Required                            | Message text          |
| edited            | boolean   | Default false                       | Edit status           |
| created_at        | timestamp | Required                            | Message creation time |
| updated_at        | timestamp | Optional                            | Last update time      |

---

## Relationships

* One channel contains many messages
* One user can create many messages
* Each message belongs to one user and one channel
* Messages can optionally reference a parent message for replies

---

## Primary Keys

* users.id
* channels.id
* messages.id

---

## Foreign Keys

* messages.channel_id → channels.id
* messages.author_id → users.id
* messages.parent_message_id → messages.id

---

## Constraints

* Channel names must be unique
* Message content is required
* `channel_id` is required for every message
* `author_id` is required for every message
* `edited` defaults to false

---

## Example Data (Verified in DBGate)

### Channels

| id | name    | description             |
| -- | ------- | ----------------------- |
| 1  | general | Main discussion channel |

---

### Messages

| id | channel_id | author_id | parent_message_id | content        | edited | created_at |
| -- | ---------- | --------- | ----------------- | -------------- | ------ | ---------- |
| 1  | 1          | 1         | NULL              | Hello everyone | false  | 2026-05-15 |
| 2  | 1          | 2         | 1                 | I agree        | false  | 2026-05-15 |

---

## Decision Log

| Decision                  | Reason                                |
| ------------------------- | ------------------------------------- |
| Use PostgreSQL (Railway)  | Production-ready hosted database      |
| Use DBGate for inspection | Easier visualization and debugging    |
| Use environment variables | Secure credential handling            |
| Keep MVP schema simple    | Focus on core messaging functionality |
| Include reply support     | Future extensibility                  |

---

## Out of Scope for MVP

* Authentication system
* Reactions
* File uploads
* Read receipts
* Typing indicators
* Notifications
* Moderation tools

---

## Implementation Note

This schema is actively used in a Flask application where:

* Database connection is handled using `DATABASE_URL`
* Data is retrieved using SQL JOIN queries
* Messages are rendered dynamically in the `/` route
* DBGate is used to verify and inspect live database state

---



* fix your README to match this perfectly
* align your Flask code with this schema
* or help you prepare final GitHub submission package

Just tell me 👍


