# Research: Todo App Multi-Phase Features

**Feature Branch**: `001-todo-app-features`
**Date**: 2025-12-27
**Status**: Complete

## Executive Summary

This document captures technical research decisions for the Todo App evolving from console to cloud-native across 5 phases. All decisions optimize for Spec-Driven Development where code is AI-generated.

---

## Decision 1: Programming Language

**Decision**: Python 3.11+

**Rationale**:
- Strong typing support via type hints (critical for AI-generated code validation)
- Excellent ecosystem for web (FastAPI), AI (LangChain), and deployment (Docker)
- First-class async/await support for concurrent operations
- Well-documented patterns that AI models understand reliably

**Alternatives Considered**:
- **TypeScript/Node.js**: Strong typing, but Python has better AI/ML ecosystem
- **Go**: Better performance, but less flexible for rapid iteration
- **Rust**: Excellent safety, but slower development cycle

---

## Decision 2: Web Framework (Phase II+)

**Decision**: FastAPI

**Rationale**:
- Async-first design: ~2,847 req/s vs Flask (~892) and Django (~743)
- Native WebSocket support via Starlette (essential for Phase III chatbot)
- Automatic OpenAPI documentation from type hints
- Lightweight: ~127MB memory vs Django ~243MB
- JWT authentication well-supported
- Pydantic validation ensures generated code is predictable

**Alternatives Considered**:
- **Flask**: Maximum flexibility but no async, no built-in validation
- **Django**: Built-in admin and ORM, but monolithic and slower

---

## Decision 3: Database (Phase II+)

**Decision**: PostgreSQL

**Rationale**:
- ACID transactions essential for todo state consistency
- Native JSONB indexing for flexible task metadata
- pgvector extension for AI embedding storage (Phase III RAG)
- Proven scalability with read replicas
- Strong regulatory compliance features
- Cost-effective self-hosted or managed options

**Alternatives Considered**:
- **MongoDB**: Flexible schema but ACID only recent (2024), less suited for relational todo data
- **SQLite**: Good for Phase I but not scalable for multi-user

---

## Decision 4: ORM

**Decision**: SQLAlchemy 2.0

**Rationale**:
- Industry-standard Python ORM
- Type hints support for generated code validation
- Alembic for database migrations
- Works seamlessly with FastAPI dependency injection

**Alternatives Considered**:
- **Tortoise ORM**: Async-native but smaller community
- **Prisma**: Good but less mature in Python

---

## Decision 5: Authentication (Phase II+)

**Decision**: JWT (JSON Web Tokens) with PyJWT

**Rationale**:
- Stateless authentication scales horizontally
- Constitution requirement (S1): JWT MUST be enforced
- Standard pattern for API authentication
- Works with WebSocket upgrade for chatbot

**Implementation Pattern**:
- Access tokens: 15-minute expiry
- Refresh tokens: 7-day expiry, stored in database
- Token validation middleware for all protected routes

---

## Decision 6: AI/LLM Integration (Phase III)

**Decision**: LangChain + Anthropic Claude API

**Rationale**:
- LangChain provides standard RAG pipeline patterns
- Tool binding for custom todo operations
- PostgresChatMessageHistory for conversation persistence
- Constitution requirement (AI1, AI2, AI3) alignment

**Architecture Pattern**:
```
User Query (WebSocket)
  → FastAPI WebSocket handler (JWT auth)
    → LangChain retriever (query pgvector for context)
    → Claude API (LLM inference)
    → Streaming response via WebSocket
    → Persist in PostgreSQL
```

**Alternatives Considered**:
- **OpenAI GPT-4**: Proven but higher cost
- **Local Ollama**: Privacy-first but requires GPU resources

---

## Decision 7: Frontend (Phase II+)

**Decision**: React with TypeScript

**Rationale**:
- Component-based architecture aligns with clean architecture
- TypeScript provides type safety for API contracts
- Large ecosystem and AI-friendly patterns
- Vite for fast development builds

**Alternatives Considered**:
- **Vue.js**: Good but smaller ecosystem
- **Svelte**: Modern but less AI training data

---

## Decision 8: Containerization (Phase IV)

**Decision**: Docker with multi-stage builds

**Rationale**:
- Industry standard for Kubernetes deployment
- Multi-stage builds minimize image size
- Reproducible builds across environments

**Image Strategy**:
- Backend: Python slim base, ~150MB final
- Frontend: Node build stage → nginx serve, ~50MB final

---

## Decision 9: Kubernetes Orchestration (Phase IV)

**Decision**: Helm charts for deployment

**Rationale**:
- Constitution requirement (FR-019): Helm charts mandatory
- Templated configurations for environments
- Easy rollback and version control
- GitOps compatible (ArgoCD)

---

## Decision 10: Event-Driven Architecture (Phase V)

**Decision**: Dapr + Kafka + KEDA

**Rationale**:
- **Dapr**: Abstraction layer for pub/sub (swap backends with YAML)
- **Kafka**: Event streaming backbone with partitioning by user_id
- **KEDA**: Auto-scale consumers based on Kafka lag

**Constitution Alignment**:
- FR-029: Kafka for event-driven communication
- FR-030: Dapr for pub/sub, state, secrets, scheduled tasks

**Event Types**:
- `todo.created`, `todo.updated`, `todo.completed`, `todo.deleted`
- Partition key: `user_id` for ordering guarantees

---

## Decision 11: Testing Strategy

**Decision**: pytest + pytest-asyncio + httpx

**Rationale**:
- pytest is Python standard
- Async support for FastAPI testing
- httpx for async HTTP client in tests
- Coverage reporting with pytest-cov

**Test Types**:
- Unit tests: Business logic
- Integration tests: API endpoints + database
- Contract tests: API schema validation
- E2E tests: Full user flows

---

## Decision 12: CI/CD Pipeline

**Decision**: GitHub Actions

**Rationale**:
- Native GitHub integration
- Container registry support
- Kubernetes deployment actions available
- Secret management built-in

---

## Technology Stack Summary

| Phase | Component | Technology |
|-------|-----------|------------|
| I | Console App | Python 3.11 + Click |
| II | Backend API | FastAPI + SQLAlchemy |
| II | Database | PostgreSQL 15 |
| II | Authentication | JWT (PyJWT) |
| II | Frontend | React + TypeScript + Vite |
| III | AI/LLM | LangChain + Anthropic Claude |
| III | Vector Store | pgvector |
| III | Chat Interface | WebSocket |
| IV | Container | Docker |
| IV | Orchestration | Kubernetes + Helm |
| V | Event Streaming | Kafka |
| V | Service Mesh | Dapr |
| V | Autoscaling | KEDA |

---

## Open Items

None - all technical decisions resolved.

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- LangChain RAG Patterns: https://python.langchain.com/docs/tutorials/rag/
- Dapr Documentation: https://docs.dapr.io/
- KEDA Autoscaling: https://keda.sh/
- pgvector Extension: https://github.com/pgvector/pgvector
