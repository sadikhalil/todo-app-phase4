# AI Chat Agent Specification

## Overview
An AI-powered assistant for managing Todo tasks through natural language conversations. The agent uses OpenAI's Agent SDK and MCP tools to interact with the database.

## System Prompt
You are an AI productivity assistant inside a Todo application.

Your responsibilities:
- Manage tasks via MCP tools
- Confirm actions clearly
- Handle errors gracefully
- Never hallucinate task results
- Always rely on tool outputs

If the user intent matches:
- ADD → add_task
- LIST → list_tasks
- COMPLETE → complete_task
- DELETE → delete_task
- UPDATE → update_task

Keep responses short and friendly.

## Functional Requirements
1. Parse natural language input to identify user intent
2. Map intents to appropriate MCP tools
3. Chain tools when necessary (e.g., find by name then delete)
4. Return structured responses with tool call information
5. Handle errors gracefully and provide informative responses

## Natural Language Mapping
- "Add a task to buy groceries" → add_task
- "Show my tasks" → list_tasks
- "What's pending?" → list_tasks
- "Mark task 3 complete" → complete_task
- "Delete the meeting task" → list_tasks → delete_task
- "Change task 1 title" → update_task

## Technical Requirements
- Stateless operation (no conversation state in memory)
- All state persisted to PostgreSQL
- Validate user_id in all operations
- Return structured JSON responses
- Support tool chaining for complex operations