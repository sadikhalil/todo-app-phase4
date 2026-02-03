# Data Model: Todo App Multi-Phase Features

**Feature Branch**: `001-todo-app-features`
**Date**: 2025-12-27
**Database**: PostgreSQL 15

## Entity Relationship Diagram

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │    Task     │       │    Tag      │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │──────<│ user_id(FK) │       │ id (PK)     │
│ email       │       │ id (PK)     │>──────│ user_id(FK) │
│ password    │       │ title       │       │ name        │
│ created_at  │       │ description │       │ created_at  │
└─────────────┘       │ status      │       └─────────────┘
                      │ priority    │              │
                      │ due_date    │              │
                      │ recurrence  │              │
                      │ created_at  │              │
                      │ updated_at  │              │
                      └─────────────┘              │
                             │                    │
                             │    ┌───────────────┘
                             │    │
                      ┌──────┴────┴──┐
                      │  TaskTag     │
                      │ (junction)   │
                      ├──────────────┤
                      │ task_id (FK) │
                      │ tag_id (FK)  │
                      └──────────────┘

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│Conversation │       │  Message    │       │  Reminder   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │──────<│ convo_id(FK)│       │ id (PK)     │
│ user_id(FK) │       │ id (PK)     │       │ task_id(FK) │
│ created_at  │       │ role        │       │ remind_at   │
│ updated_at  │       │ content     │       │ sent        │
└─────────────┘       │ created_at  │       │ created_at  │
                      └─────────────┘       └─────────────┘
```

---

## Entity Definitions

### User (Phase II+)

Represents an authenticated user of the system.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |

**Validation Rules**:
- Email must be valid format (RFC 5322)
- Password minimum 8 characters before hashing
- Email must be unique across all users

**Indexes**:
- `idx_user_email` on `email` (unique)

---

### Task (All Phases)

Represents a to-do item.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, NULL (Phase I) | Owner of the task |
| title | VARCHAR(255) | NOT NULL | Task title |
| description | TEXT | NULL | Optional description |
| status | ENUM | NOT NULL, DEFAULT 'incomplete' | 'complete' or 'incomplete' |
| priority | ENUM | NULL | 'high', 'medium', 'low' (Phase V) |
| due_date | TIMESTAMP | NULL | Optional due date (Phase V) |
| recurrence_pattern | VARCHAR(50) | NULL | 'daily', 'weekly', 'monthly' (Phase V) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update time |

**Validation Rules**:
- Title must not be empty
- Title max length 255 characters
- Description max length 10,000 characters
- Status must be 'complete' or 'incomplete'
- Priority must be 'high', 'medium', or 'low' if set
- Recurrence must be 'daily', 'weekly', or 'monthly' if set
- Due date must be in the future when created

**Indexes**:
- `idx_task_user_id` on `user_id`
- `idx_task_status` on `status`
- `idx_task_due_date` on `due_date`
- `idx_task_priority` on `priority`
- `idx_task_title_search` GIN index on `title` for full-text search

**State Transitions**:
```
incomplete ──[mark complete]──> complete
complete ──[mark incomplete]──> incomplete
```

---

### Tag (Phase V)

Represents a category/tag for organizing tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Owner of the tag |
| name | VARCHAR(50) | NOT NULL | Tag name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |

**Validation Rules**:
- Name must not be empty
- Name max length 50 characters
- Name must be unique per user

**Indexes**:
- `idx_tag_user_id` on `user_id`
- `idx_tag_name_user` UNIQUE on `(user_id, name)`

---

### TaskTag (Phase V)

Junction table for many-to-many Task-Tag relationship.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| task_id | UUID | FK → Task.id, NOT NULL | Task reference |
| tag_id | UUID | FK → Tag.id, NOT NULL | Tag reference |

**Constraints**:
- PK on `(task_id, tag_id)`
- CASCADE DELETE on both foreign keys

---

### Conversation (Phase III+)

Represents a chatbot conversation session.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| user_id | UUID | FK → User.id, NOT NULL | Conversation owner |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Conversation start time |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last message time |

**Indexes**:
- `idx_conversation_user_id` on `user_id`
- `idx_conversation_updated_at` on `updated_at`

---

### Message (Phase III+)

Represents a message in a conversation.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| conversation_id | UUID | FK → Conversation.id, NOT NULL | Parent conversation |
| role | ENUM | NOT NULL | 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Message time |

**Validation Rules**:
- Role must be 'user' or 'assistant'
- Content must not be empty

**Indexes**:
- `idx_message_conversation_id` on `conversation_id`
- `idx_message_created_at` on `created_at`

---

### Reminder (Phase V)

Represents a scheduled notification for a task.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Unique identifier |
| task_id | UUID | FK → Task.id, NOT NULL | Associated task |
| remind_at | TIMESTAMP | NOT NULL | Scheduled reminder time |
| sent | BOOLEAN | NOT NULL, DEFAULT FALSE | Whether reminder was sent |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation time |

**Validation Rules**:
- remind_at must be in the future when created
- One active reminder per task

**Indexes**:
- `idx_reminder_task_id` on `task_id`
- `idx_reminder_remind_at` on `remind_at`
- `idx_reminder_pending` on `(sent, remind_at)` WHERE `sent = FALSE`

---

## Phase-Based Entity Availability

| Entity | Phase I | Phase II | Phase III | Phase IV | Phase V |
|--------|---------|----------|-----------|----------|---------|
| Task | In-memory | PostgreSQL | PostgreSQL | PostgreSQL | PostgreSQL |
| User | N/A | PostgreSQL | PostgreSQL | PostgreSQL | PostgreSQL |
| Tag | N/A | N/A | N/A | N/A | PostgreSQL |
| TaskTag | N/A | N/A | N/A | N/A | PostgreSQL |
| Conversation | N/A | N/A | PostgreSQL | PostgreSQL | PostgreSQL |
| Message | N/A | N/A | PostgreSQL | PostgreSQL | PostgreSQL |
| Reminder | N/A | N/A | N/A | N/A | PostgreSQL |

---

## Enum Definitions

### TaskStatus
```sql
CREATE TYPE task_status AS ENUM ('incomplete', 'complete');
```

### TaskPriority
```sql
CREATE TYPE task_priority AS ENUM ('high', 'medium', 'low');
```

### RecurrencePattern
```sql
CREATE TYPE recurrence_pattern AS ENUM ('daily', 'weekly', 'monthly');
```

### MessageRole
```sql
CREATE TYPE message_role AS ENUM ('user', 'assistant');
```

---

## Migration Strategy

1. **Phase I → Phase II**:
   - Create User, Task tables
   - Add user_id FK to Task (nullable initially)
   - Migrate in-memory tasks to database

2. **Phase II → Phase III**:
   - Create Conversation, Message tables
   - Add pgvector extension for embeddings

3. **Phase III → Phase IV**:
   - No schema changes
   - Database runs in Kubernetes pod

4. **Phase IV → Phase V**:
   - Create Tag, TaskTag, Reminder tables
   - Add priority, due_date, recurrence_pattern to Task
   - Create full-text search indexes
