# Tasks: Todo App Multi-Phase Features

**Input**: Design documents from `/specs/001-todo-app-features/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are included as this is a Spec-Driven Development project requiring verification against specifications.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. The project evolves through 5 phases (Console → Web → AI → K8s → Cloud).

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Phase I**: `src/`, `tests/` at repository root (console app)
- **Phase II+**: `backend/src/`, `frontend/src/` (web app)
- **Phase IV+**: `k8s/`, `helm/` (deployment)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for Phase I console application

- [x] T001 Create project structure with src/models/, src/services/, src/cli/, src/lib/, tests/unit/, tests/integration/ directories
- [x] T002 Initialize Python 3.11 project with pyproject.toml and Click dependency
- [x] T003 [P] Configure pytest and pytest-cov in pyproject.toml
- [x] T004 [P] Create .gitignore with Python patterns and .env exclusion
- [x] T005 [P] Create .env.example with placeholder environment variables

**Checkpoint**: Project structure ready for Phase I implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure for Phase I console application - in-memory storage and base models

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create Task model with id, title, description, status, created_at, updated_at in src/models/task.py
- [ ] T007 Create TaskStatus enum (incomplete, complete) in src/models/task.py
- [ ] T008 Implement InMemoryStorage class with CRUD operations in src/lib/storage.py
- [ ] T009 Create custom exceptions (TaskNotFoundError, ValidationError) in src/lib/exceptions.py
- [ ] T010 [P] Create __init__.py files for all packages (src/, src/models/, src/services/, src/cli/, src/lib/)

**Checkpoint**: Foundation ready - User Story 1 implementation can now begin

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Create, view, update, delete, and complete tasks via CLI (Phase I console app)

**Independent Test**: Run `python -m src.cli.main add "Buy groceries"`, then `list`, `update`, `complete`, `delete` commands

### Tests for User Story 1

- [ ] T011 [P] [US1] Create unit tests for Task model validation in tests/unit/test_task_model.py
- [ ] T012 [P] [US1] Create unit tests for TaskService CRUD operations in tests/unit/test_task_service.py
- [ ] T013 [P] [US1] Create integration tests for CLI commands in tests/integration/test_cli.py

### Implementation for User Story 1

- [ ] T014 [US1] Implement TaskService.add_task() with title validation in src/services/task_service.py
- [ ] T015 [US1] Implement TaskService.list_tasks() with optional status filter in src/services/task_service.py
- [ ] T016 [US1] Implement TaskService.get_task() by ID in src/services/task_service.py
- [ ] T017 [US1] Implement TaskService.update_task() for title and description in src/services/task_service.py
- [ ] T018 [US1] Implement TaskService.delete_task() with permanent removal in src/services/task_service.py
- [ ] T019 [US1] Implement TaskService.toggle_status() for complete/incomplete in src/services/task_service.py
- [ ] T020 [US1] Create Click CLI group and add command in src/cli/main.py
- [ ] T021 [US1] Implement CLI list command with status filter option in src/cli/main.py
- [ ] T022 [US1] Implement CLI update command in src/cli/main.py
- [ ] T023 [US1] Implement CLI delete command in src/cli/main.py
- [ ] T024 [US1] Implement CLI complete and incomplete commands in src/cli/main.py
- [ ] T025 [US1] Add user-friendly error messages and help text in src/cli/main.py

**Checkpoint**: Phase I MVP complete - Console Todo app functional with all basic CRUD operations

---

## Phase 4: User Story 2 - User Authentication (Priority: P2)

**Goal**: User registration, login, JWT auth, and task isolation (Phase II web app)

**Independent Test**: Register user, login, create task, logout, login as different user, verify task isolation

### Phase II Setup Tasks

- [ ] T026 [US2] Create backend/ directory structure with src/models/, src/services/, src/api/, src/db/, tests/
- [ ] T027 [US2] Initialize FastAPI project with requirements.txt (fastapi, uvicorn, sqlalchemy, alembic, pyjwt, bcrypt, httpx)
- [ ] T028 [US2] Configure Alembic for database migrations in backend/alembic.ini and backend/alembic/
- [ ] T029 [US2] Create database connection and session management in backend/src/db/database.py
- [ ] T030 [US2] Create SQLAlchemy Base model in backend/src/models/base.py

### Tests for User Story 2

- [ ] T031 [P] [US2] Create unit tests for User model in backend/tests/unit/test_user_model.py
- [ ] T032 [P] [US2] Create unit tests for AuthService in backend/tests/unit/test_auth_service.py
- [ ] T033 [P] [US2] Create contract tests for auth endpoints in backend/tests/contract/test_auth_api.py
- [ ] T034 [P] [US2] Create integration tests for auth flow in backend/tests/integration/test_auth_flow.py

### Implementation for User Story 2

- [ ] T035 [US2] Create User SQLAlchemy model with email, password_hash, created_at in backend/src/models/user.py
- [ ] T036 [US2] Create Task SQLAlchemy model with user_id FK in backend/src/models/task.py
- [ ] T037 [US2] Create initial Alembic migration for User and Task tables in backend/alembic/versions/
- [ ] T038 [US2] Implement password hashing with bcrypt in backend/src/services/auth_service.py
- [ ] T039 [US2] Implement JWT token generation (access + refresh) in backend/src/services/auth_service.py
- [ ] T040 [US2] Implement JWT token validation in backend/src/services/auth_service.py
- [ ] T041 [US2] Implement user registration in backend/src/services/auth_service.py
- [ ] T042 [US2] Implement user login in backend/src/services/auth_service.py
- [ ] T043 [US2] Create JWT auth middleware in backend/src/api/middleware/auth.py
- [ ] T044 [US2] Create Pydantic schemas for auth requests/responses in backend/src/api/schemas/auth.py
- [ ] T045 [US2] Implement POST /auth/register endpoint in backend/src/api/routes/auth.py
- [ ] T046 [US2] Implement POST /auth/login endpoint in backend/src/api/routes/auth.py
- [ ] T047 [US2] Implement POST /auth/logout endpoint in backend/src/api/routes/auth.py
- [ ] T048 [US2] Implement POST /auth/refresh endpoint in backend/src/api/routes/auth.py
- [ ] T049 [US2] Create FastAPI app with CORS and router registration in backend/src/api/main.py
- [ ] T050 [US2] Update TaskService to filter by user_id in backend/src/services/task_service.py

### Frontend Setup Tasks

- [ ] T051 [US2] Initialize React project with Vite and TypeScript in frontend/
- [ ] T052 [US2] Install frontend dependencies (axios, react-router-dom, @tanstack/react-query)
- [ ] T053 [US2] Create API client with auth interceptor in frontend/src/services/api.ts
- [ ] T054 [US2] Create auth context and provider in frontend/src/contexts/AuthContext.tsx
- [ ] T055 [US2] Create Login page component in frontend/src/pages/Login.tsx
- [ ] T056 [US2] Create Register page component in frontend/src/pages/Register.tsx
- [ ] T057 [US2] Create protected route wrapper in frontend/src/components/ProtectedRoute.tsx
- [ ] T058 [US2] Configure React Router with auth routes in frontend/src/App.tsx

**Checkpoint**: Phase II auth complete - Users can register, login, and have isolated task data

---

## Phase 5: User Story 2 Continued - Web Task Management

**Goal**: REST API task endpoints with frontend UI (Phase II continuation)

### Tests for Task API

- [ ] T059 [P] [US2] Create contract tests for task endpoints in backend/tests/contract/test_tasks_api.py
- [ ] T060 [P] [US2] Create integration tests for task operations in backend/tests/integration/test_task_flow.py

### Implementation for Task API

- [ ] T061 [US2] Create Pydantic schemas for task requests/responses in backend/src/api/schemas/task.py
- [ ] T062 [US2] Implement GET /tasks endpoint with filters in backend/src/api/routes/tasks.py
- [ ] T063 [US2] Implement POST /tasks endpoint in backend/src/api/routes/tasks.py
- [ ] T064 [US2] Implement GET /tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [ ] T065 [US2] Implement PUT /tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [ ] T066 [US2] Implement DELETE /tasks/{id} endpoint in backend/src/api/routes/tasks.py
- [ ] T067 [US2] Implement POST /tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py
- [ ] T068 [US2] Implement POST /tasks/{id}/incomplete endpoint in backend/src/api/routes/tasks.py

### Frontend Task UI

- [ ] T069 [US2] Create TaskList component in frontend/src/components/TaskList.tsx
- [ ] T070 [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx
- [ ] T071 [US2] Create TaskForm component for add/edit in frontend/src/components/TaskForm.tsx
- [ ] T072 [US2] Create Home page with task list in frontend/src/pages/Home.tsx
- [ ] T073 [US2] Implement task service with API calls in frontend/src/services/tasks.ts
- [ ] T074 [US2] Add task CRUD functionality with React Query in frontend/src/hooks/useTasks.ts

**Checkpoint**: Phase II complete - Full-stack web app with auth and task management

---

## Phase 6: User Story 4 - AI Chatbot Task Management (Priority: P4)

**Goal**: Natural language task management via chatbot (Phase III)

**Independent Test**: Send "Add a task to buy milk", verify task created; say "Show my tasks", verify list returned

### Tests for User Story 4

- [ ] T075 [P] [US4] Create unit tests for chat tools in backend/tests/unit/test_chat_tools.py
- [ ] T076 [P] [US4] Create integration tests for chat flow in backend/tests/integration/test_chat_flow.py
- [ ] T077 [P] [US4] Create contract tests for chat endpoints in backend/tests/contract/test_chat_api.py

### Implementation for User Story 4

- [ ] T078 [US4] Create Conversation SQLAlchemy model in backend/src/models/conversation.py
- [ ] T079 [US4] Create Message SQLAlchemy model in backend/src/models/message.py
- [ ] T080 [US4] Create Alembic migration for Conversation and Message tables
- [ ] T081 [US4] Implement AddTaskTool for LangChain agent in backend/src/chat/tools.py
- [ ] T082 [US4] Implement ViewTasksTool for LangChain agent in backend/src/chat/tools.py
- [ ] T083 [US4] Implement UpdateTaskTool for LangChain agent in backend/src/chat/tools.py
- [ ] T084 [US4] Implement DeleteTaskTool for LangChain agent in backend/src/chat/tools.py
- [ ] T085 [US4] Implement ToggleCompletionTool for LangChain agent in backend/src/chat/tools.py
- [ ] T086 [US4] Create LangChain agent with Claude and task tools in backend/src/chat/agent.py
- [ ] T087 [US4] Implement ConversationService for persistence in backend/src/services/conversation_service.py
- [ ] T088 [US4] Create WebSocket handler with JWT auth in backend/src/chat/websocket.py
- [ ] T089 [US4] Create Pydantic schemas for chat in backend/src/api/schemas/chat.py
- [ ] T090 [US4] Implement GET /chat/conversations endpoint in backend/src/api/routes/chat.py
- [ ] T091 [US4] Implement POST /chat/conversations endpoint in backend/src/api/routes/chat.py
- [ ] T092 [US4] Implement GET /chat/conversations/{id} endpoint in backend/src/api/routes/chat.py
- [ ] T093 [US4] Implement POST /chat/conversations/{id}/messages endpoint in backend/src/api/routes/chat.py
- [ ] T094 [US4] Register WebSocket route in backend/src/api/main.py

### Frontend Chat UI

- [ ] T095 [US4] Create ChatInterface component in frontend/src/components/Chat/ChatInterface.tsx
- [ ] T096 [US4] Create MessageList component in frontend/src/components/Chat/MessageList.tsx
- [ ] T097 [US4] Create MessageInput component in frontend/src/components/Chat/MessageInput.tsx
- [ ] T098 [US4] Implement WebSocket connection hook in frontend/src/hooks/useWebSocket.ts
- [ ] T099 [US4] Create Chat page in frontend/src/pages/Chat.tsx
- [ ] T100 [US4] Add chat route to router in frontend/src/App.tsx

**Checkpoint**: Phase III complete - AI chatbot manages tasks via natural language

---

## Phase 7: User Story 7 - Kubernetes Deployment (Priority: P7 - Part 1)

**Goal**: Containerize and deploy to local Kubernetes (Phase IV)

**Independent Test**: Run `helm install`, verify pods running, access app via ingress

### Tests for User Story 7

- [ ] T101 [P] [US7] Create health check tests in backend/tests/integration/test_health.py

### Implementation for User Story 7

- [ ] T102 [US7] Implement GET /health endpoint in backend/src/api/routes/health.py
- [ ] T103 [US7] Implement GET /health/ready endpoint in backend/src/api/routes/health.py
- [ ] T104 [US7] Implement GET /health/live endpoint in backend/src/api/routes/health.py
- [ ] T105 [US7] Create backend Dockerfile with multi-stage build in backend/Dockerfile
- [ ] T106 [US7] Create frontend Dockerfile with nginx in frontend/Dockerfile
- [ ] T107 [US7] Create docker-compose.yml for local development
- [ ] T108 [US7] Create Kubernetes deployment manifest in k8s/base/deployment.yaml
- [ ] T109 [US7] Create Kubernetes service manifest in k8s/base/service.yaml
- [ ] T110 [US7] Create Kubernetes configmap in k8s/base/configmap.yaml
- [ ] T111 [US7] Create Kubernetes secret template in k8s/base/secret.yaml
- [ ] T112 [US7] Create Kustomization file in k8s/base/kustomization.yaml
- [ ] T113 [US7] Create dev overlay in k8s/overlays/dev/
- [ ] T114 [US7] Create Helm chart structure in helm/todo-app/
- [ ] T115 [US7] Create Helm values.yaml with configurable parameters
- [ ] T116 [US7] Create Helm deployment template in helm/todo-app/templates/deployment.yaml
- [ ] T117 [US7] Create Helm service template in helm/todo-app/templates/service.yaml
- [ ] T118 [US7] Create Helm ingress template in helm/todo-app/templates/ingress.yaml

**Checkpoint**: Phase IV complete - Application runs on local Kubernetes

---

## Phase 8: User Story 3 - Task Organization (Priority: P3)

**Goal**: Priority, tags, due dates, search, filter, sort (Phase V - Part 1)

**Independent Test**: Create tasks with priorities/tags, filter and sort to verify organization

### Tests for User Story 3

- [ ] T119 [P] [US3] Create unit tests for Tag model in backend/tests/unit/test_tag_model.py
- [ ] T120 [P] [US3] Create contract tests for tag endpoints in backend/tests/contract/test_tags_api.py
- [ ] T121 [P] [US3] Create integration tests for filtering/sorting in backend/tests/integration/test_task_filters.py

### Implementation for User Story 3

- [ ] T122 [US3] Create Tag SQLAlchemy model in backend/src/models/tag.py
- [ ] T123 [US3] Create TaskTag junction model in backend/src/models/task_tag.py
- [ ] T124 [US3] Add priority, due_date fields to Task model in backend/src/models/task.py
- [ ] T125 [US3] Create Alembic migration for Tag, TaskTag, and Task updates
- [ ] T126 [US3] Implement TagService CRUD operations in backend/src/services/tag_service.py
- [ ] T127 [US3] Update TaskService with filter by priority/status/due_date in backend/src/services/task_service.py
- [ ] T128 [US3] Update TaskService with sort by priority/due_date/title in backend/src/services/task_service.py
- [ ] T129 [US3] Implement keyword search in TaskService in backend/src/services/task_service.py
- [ ] T130 [US3] Create Pydantic schemas for tags in backend/src/api/schemas/tag.py
- [ ] T131 [US3] Implement GET /tags endpoint in backend/src/api/routes/tags.py
- [ ] T132 [US3] Implement POST /tags endpoint in backend/src/api/routes/tags.py
- [ ] T133 [US3] Implement DELETE /tags/{id} endpoint in backend/src/api/routes/tags.py
- [ ] T134 [US3] Implement POST /tasks/{id}/tags endpoint in backend/src/api/routes/tasks.py
- [ ] T135 [US3] Implement DELETE /tasks/{id}/tags endpoint in backend/src/api/routes/tasks.py
- [ ] T136 [US3] Update task list endpoint with search/filter/sort params in backend/src/api/routes/tasks.py

### Frontend Organization UI

- [ ] T137 [US3] Create TagSelector component in frontend/src/components/TagSelector.tsx
- [ ] T138 [US3] Create PrioritySelector component in frontend/src/components/PrioritySelector.tsx
- [ ] T139 [US3] Create DatePicker component in frontend/src/components/DatePicker.tsx
- [ ] T140 [US3] Create TaskFilters component in frontend/src/components/TaskFilters.tsx
- [ ] T141 [US3] Update TaskForm with priority/tags/due_date in frontend/src/components/TaskForm.tsx
- [ ] T142 [US3] Update TaskList with filtering and sorting in frontend/src/components/TaskList.tsx

**Checkpoint**: Task organization features complete

---

## Phase 9: User Story 5 - Recurring Tasks (Priority: P5)

**Goal**: Tasks that automatically regenerate on completion (Phase V - Part 2)

**Independent Test**: Create weekly recurring task, complete it, verify new instance created

### Tests for User Story 5

- [ ] T143 [P] [US5] Create unit tests for recurrence logic in backend/tests/unit/test_recurrence.py
- [ ] T144 [P] [US5] Create integration tests for recurring tasks in backend/tests/integration/test_recurring_tasks.py

### Implementation for User Story 5

- [ ] T145 [US5] Add recurrence_pattern field to Task model in backend/src/models/task.py
- [ ] T146 [US5] Create Alembic migration for recurrence_pattern
- [ ] T147 [US5] Implement RecurrenceService.calculate_next_date() in backend/src/services/recurrence_service.py
- [ ] T148 [US5] Implement RecurrenceService.create_next_instance() in backend/src/services/recurrence_service.py
- [ ] T149 [US5] Update task completion to trigger recurrence in backend/src/services/task_service.py
- [ ] T150 [US5] Update Pydantic schemas for recurrence in backend/src/api/schemas/task.py
- [ ] T151 [US5] Add recurrence option to TaskForm in frontend/src/components/TaskForm.tsx

**Checkpoint**: Recurring tasks functional

---

## Phase 10: User Story 6 - Reminder Notifications (Priority: P6)

**Goal**: Scheduled reminders for tasks with due dates (Phase V - Part 3)

**Independent Test**: Set reminder, wait for scheduled time, verify notification sent

### Tests for User Story 6

- [ ] T152 [P] [US6] Create unit tests for Reminder model in backend/tests/unit/test_reminder_model.py
- [ ] T153 [P] [US6] Create integration tests for reminder scheduling in backend/tests/integration/test_reminders.py

### Implementation for User Story 6

- [ ] T154 [US6] Create Reminder SQLAlchemy model in backend/src/models/reminder.py
- [ ] T155 [US6] Create Alembic migration for Reminder table
- [ ] T156 [US6] Implement ReminderService.schedule() in backend/src/services/reminder_service.py
- [ ] T157 [US6] Implement ReminderService.cancel() in backend/src/services/reminder_service.py
- [ ] T158 [US6] Implement ReminderService.process_due_reminders() in backend/src/services/reminder_service.py
- [ ] T159 [US6] Create Pydantic schemas for reminders in backend/src/api/schemas/reminder.py
- [ ] T160 [US6] Implement POST /tasks/{id}/reminder endpoint in backend/src/api/routes/tasks.py
- [ ] T161 [US6] Implement DELETE /tasks/{id}/reminder endpoint in backend/src/api/routes/tasks.py
- [ ] T162 [US6] Add reminder UI to TaskForm in frontend/src/components/TaskForm.tsx

**Checkpoint**: Reminders functional

---

## Phase 11: User Story 7 Continued - Event-Driven Architecture (Priority: P7 - Part 2)

**Goal**: Kafka events and Dapr integration (Phase V - Part 4)

**Independent Test**: Complete task, verify event published to Kafka and processed by subscribers

### Tests for User Story 7 Event-Driven

- [ ] T163 [P] [US7] Create integration tests for event publishing in backend/tests/integration/test_events.py

### Implementation for Event-Driven

- [ ] T164 [US7] Create Dapr pubsub component config in k8s/dapr-components/pubsub.yaml
- [ ] T165 [US7] Create Dapr statestore component config in k8s/dapr-components/statestore.yaml
- [ ] T166 [US7] Create Dapr secretstore component config in k8s/dapr-components/secretstore.yaml
- [ ] T167 [US7] Create Kafka cluster manifest in k8s/kafka-cluster.yaml
- [ ] T168 [US7] Implement EventPublisher with Dapr SDK in backend/src/events/publisher.py
- [ ] T169 [US7] Define TaskEvent schemas (created, updated, completed, deleted) in backend/src/events/schemas.py
- [ ] T170 [US7] Implement NotificationHandler for task events in backend/src/events/handlers/notification.py
- [ ] T171 [US7] Implement AnalyticsHandler for task events in backend/src/events/handlers/analytics.py
- [ ] T172 [US7] Integrate event publishing in TaskService in backend/src/services/task_service.py
- [ ] T173 [US7] Create KEDA ScaledObject for consumer autoscaling in k8s/keda-scaledobject.yaml
- [ ] T174 [US7] Update Helm chart with Dapr annotations in helm/todo-app/templates/deployment.yaml
- [ ] T175 [US7] Create prod overlay with cloud config in k8s/overlays/prod/

**Checkpoint**: Phase V complete - Event-driven cloud-native architecture

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T176 [P] Run full test suite and fix any failures
- [ ] T177 [P] Update README.md with complete setup instructions
- [ ] T178 [P] Create API documentation in docs/api.md
- [ ] T179 Run security scan and address vulnerabilities
- [ ] T180 Validate quickstart.md instructions work end-to-end
- [ ] T181 Performance testing for 100 concurrent users
- [ ] T182 Final code review and cleanup

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) ──────────────────────────────────────────────────────────────▶
         │
         ▼
Phase 2 (Foundational) ───────────────────────────────────────────────────────▶
         │
         ├───────────────────────────────────────────────────────────────────────▶
         │                                                                        │
         ▼                                                                        ▼
Phase 3 (US1: Basic Tasks) ──▶ Phase 4-5 (US2: Auth) ──▶ Phase 6 (US4: Chat)
         │                              │                        │
         │                              ▼                        ▼
         │                     Phase 7 (US7: K8s Part 1) ◀───────┤
         │                              │                        │
         │                              ▼                        │
         │                     Phase 8 (US3: Organization) ◀─────┤
         │                              │                        │
         │                              ▼                        │
         │                     Phase 9 (US5: Recurring) ◀────────┤
         │                              │                        │
         │                              ▼                        │
         │                     Phase 10 (US6: Reminders) ◀───────┤
         │                              │                        │
         │                              ▼                        │
         │                     Phase 11 (US7: Events) ◀──────────┘
         │                              │
         ▼                              ▼
Phase 12 (Polish) ◀─────────────────────┘
```

### User Story Dependencies

- **US1 (P1)**: No dependencies - MVP standalone
- **US2 (P2)**: Depends on US1 completion (tasks exist to authenticate)
- **US3 (P3)**: Depends on US2 (needs auth + db)
- **US4 (P4)**: Depends on US2 (needs auth + db)
- **US5 (P5)**: Depends on US3 (needs due dates)
- **US6 (P6)**: Depends on US3 (needs due dates)
- **US7 (P7)**: Part 1 depends on US4; Part 2 depends on all features

### Within Each User Story

1. Tests (where included) - written first
2. Models - created before services
3. Services - created before API routes
4. API Routes - implement endpoints
5. Frontend - consumes API
6. Integration - verify end-to-end

### Parallel Opportunities

```bash
# Phase 1 parallel tasks:
Task: T003, T004, T005

# Phase 2 parallel tasks:
Task: T010

# Phase 3 (US1) parallel tests:
Task: T011, T012, T013

# Phase 4 (US2) parallel tests:
Task: T031, T032, T033, T034

# Phase 5 (US2 API) parallel tests:
Task: T059, T060

# Phase 6 (US4) parallel tests:
Task: T075, T076, T077

# Phase 7 (US7) parallel test:
Task: T101

# Phase 8 (US3) parallel tests:
Task: T119, T120, T121

# Phase 9 (US5) parallel tests:
Task: T143, T144

# Phase 10 (US6) parallel tests:
Task: T152, T153

# Phase 11 (US7 Events) parallel test:
Task: T163

# Phase 12 parallel tasks:
Task: T176, T177, T178
```

---

## Implementation Strategy

### MVP First (Phase I Only - User Story 1)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T010)
3. Complete Phase 3: User Story 1 (T011-T025)
4. **STOP and VALIDATE**: Test console app independently
5. Demo Phase I MVP

### Incremental Delivery

1. **Phase I MVP**: Setup + Foundation + US1 → Console Todo App
2. **Phase II**: US2 → Full-stack web app with auth
3. **Phase III**: US4 → AI chatbot integration
4. **Phase IV**: US7 Part 1 → Kubernetes deployment
5. **Phase V**: US3, US5, US6, US7 Part 2 → Advanced features + events

### Agent-Based Implementation (per User Input)

Each Todo operation is handled by a dedicated agent:
- **Add Task Agent**: T014, T020 (Phase I), T063 (Phase II), T081 (Phase III)
- **View Tasks Agent**: T015, T021 (Phase I), T062 (Phase II), T082 (Phase III)
- **Update Task Agent**: T017, T022 (Phase I), T065 (Phase II), T083 (Phase III)
- **Delete Task Agent**: T018, T023 (Phase I), T066 (Phase II), T084 (Phase III)
- **Toggle Completion Agent**: T019, T024 (Phase I), T067-T068 (Phase II), T085 (Phase III)

---

## Task Summary

| Phase | User Story | Task Count | Parallel Tasks |
|-------|------------|------------|----------------|
| 1 | Setup | 5 | 3 |
| 2 | Foundational | 5 | 1 |
| 3 | US1: Basic Tasks | 15 | 3 |
| 4 | US2: Auth Setup | 25 | 4 |
| 5 | US2: Task API | 16 | 2 |
| 6 | US4: AI Chat | 26 | 3 |
| 7 | US7: K8s Part 1 | 18 | 1 |
| 8 | US3: Organization | 24 | 3 |
| 9 | US5: Recurring | 9 | 2 |
| 10 | US6: Reminders | 11 | 2 |
| 11 | US7: Events | 13 | 1 |
| 12 | Polish | 7 | 3 |
| **Total** | | **182** | **28** |

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [USn] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate phase/story independently
- All code generated by Claude Code per constitution R1
- Verify behavior matches specification per constitution DO2
