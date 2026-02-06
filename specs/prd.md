# Todo Chatbot Application - PRD

## Overview
A chatbot-enabled todo application that allows users to manage tasks through natural language commands.

## Requirements
- Stateful chatbot that understands natural language commands
- Support for task operations: add, list, complete, delete, update
- Persistent storage for tasks and conversations
- Secure inter-service communication
- Scalable architecture

## Architecture
- Main API server (FastAPI) handles chat requests
- MCP server provides task operation tools
- PostgreSQL database for persistence
- Stateless design for horizontal scaling

## User Stories
1. As a user, I want to add tasks by saying "Add a task to buy milk"
2. As a user, I want to list my tasks by saying "Show my tasks"
3. As a user, I want to complete tasks by saying "Complete task 1"
4. As a user, I want to delete tasks by saying "Delete task 2"

## Technical Specifications
- Python 3.11
- FastAPI framework
- SQLModel ORM
- PostgreSQL database
- HTTP-based inter-service communication
- Internal token authentication