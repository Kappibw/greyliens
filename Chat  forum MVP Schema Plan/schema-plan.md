# Chat Forum MVP Schema Plan

This document defines the minimum database structure required for the Chat Forum MVP. The goal is to support core chat functionality while keeping the schema simple and easy to expand later.

---

## Parent Issue
#1

---

## Define User Behaviors

| User Behavior      | Required Data |
|-------------------|--------------|
| View channels     | Channel name, description |
| Open a channel    | Channel ID |
| Send a message    | Message content, channel reference |
| Edit a message    | Updated timestamp, edited flag |
| Support posting by existing users | Username and user reference |

---

## Define Core Entities

---


### Users Table

| Field       | Type           | Constraints             | Description |
|-------------|---------------|-------------------------|-------------|
| id          | UUID / Integer | Primary Key, Required   | Unique identifier for the user |
| username    | VARCHAR(50)    | Required, Unique        | Username entered when posting |
| created_at  | TIMESTAMP      | Required                | When the user was created |

---
| Field        | Type          | Constraints                     | Description |
|-------------|--------------|--------------------------------|-------------|
| id          | UUID / Integer | Primary Key, Required         | Unique identifier for the channel |
| name        | VARCHAR(50)   | Required, Unique               | Display name of the channel |
| description | TEXT          | Optional                       | Explains the purpose of the channel |
| is_private  | BOOLEAN       | Default = false               | Controls whether the channel is restricted |
| created_at  | TIMESTAMP     | Required                      | When the channel was created |
| updated_at  | TIMESTAMP     | Required                      | Last update time |

---

### Messages Table

| Field       | Type          | Constraints                     | Description |
|-------------|--------------|--------------------------------|-------------|
| id          | UUID / Integer | Primary Key, Required         | Unique identifier for the message |
| channel_id  | Foreign Key   | Required                      | References channels.id |
 | author_id  | Foreign Key   | Required                      | References users.id |                    
| content     | TEXT          | Required                      | Stores message text |
| edited      | BOOLEAN       | Default = false               | Indicates whether the message was edited |
| created_at  | TIMESTAMP     | Required                      | Time the message was sent |
| updated_at  | TIMESTAMP     | Required                      | Time the message was last updated |

---

## Define Relationships

- One channel can contain many messages  
- Each message belongs to exactly one channel  
- One user can create many messages  
- Each message belongs to exactly one user 

---

## Primary Keys
- Users.id  
- Channels.id  
- Messages.id
---

## Foreign Keys

- Messages.channel_id → Channels.id  
- Messages.author_id → Users.id

---

## Add Constraints

- Channel names must be unique  
- Message content is required  
- `channel_id` is required for every message  
- `edited` defaults to `false`  
- `is_private` defaults to `false`
 - `author_id` is required for every message 
- usernames must be unique

---

## Example Rows

### Example Channel Row

| id | name     | description           | is_private | created_at          |
|----|----------|----------------------|------------|---------------------|
| 1  | general  | Main discussion channel | false      | 2026-05-15 10:00    |

---

### Example Message Rows

| id | channel_id | author_id | content            | edited | created_at          |
|----|------------|----------|--------------------|--------|---------------------|
| 1  | 1          | 1        | Hello everyone!      | false  | 2026-05-15 10:05    |
| 2  | 1          | 2        | Welcome to the forum | true   | 2026-05-15 10:07    |

---

## Decision Log

| Decision | Reason |
|----------|--------|
| Simple users table included | Supports posting with existing users |
| Hand-made users for MVP | Keeps implementation simple without full authentication |
| No reactions or threads yet | Outside MVP scope |
| Unique channel names | Prevents duplicate/confusing channels |

---

## Out of Scope for MVP

- Authentication system  
- Reactions  
- Threaded replies  
- File uploads  
- Read receipts  
- Typing indicators  
- Notifications  
- Moderation tools  
