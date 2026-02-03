# MCP Tools Specification

## Overview
MCP (Model Context Protocol) tools for managing Todo tasks. Each tool is stateless and interacts directly with the PostgreSQL database.

## Available Tools

### add_task
**Description**: Creates a new task for a user
**Parameters**:
- user_id (str): The ID of the user creating the task
- title (str): The title of the task
- description (str, optional): Detailed description of the task

**Returns**:
```json
{
  "task_id": 5,
  "status": "created",
  "title": "Buy groceries"
}
```

### list_tasks
**Description**: Lists all tasks for a user
**Parameters**:
- user_id (str): The ID of the user whose tasks to list

**Returns**:
```json
{
  "status": "success",
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Get milk and bread",
      "completed": false
    }
  ]
}
```

### complete_task
**Description**: Marks a task as completed
**Parameters**:
- user_id (str): The ID of the user
- task_id (int): The ID of the task to complete

**Returns**:
```json
{
  "task_id": 5,
  "status": "completed",
  "title": "Buy groceries"
}
```

### delete_task
**Description**: Deletes a task
**Parameters**:
- user_id (str): The ID of the user
- task_id (int): The ID of the task to delete

**Returns**:
```json
{
  "task_id": 5,
  "status": "deleted",
  "title": "Buy groceries"
}
```

### update_task
**Description**: Updates task details
**Parameters**:
- user_id (str): The ID of the user
- task_id (int): The ID of the task to update
- title (str, optional): New title for the task
- description (str, optional): New description for the task
- completed (bool, optional): New completion status

**Returns**:
```json
{
  "task_id": 5,
  "status": "updated",
  "title": "Updated task title"
}
```

## Common Requirements
- All tools are stateless
- All tools read/write from database
- All tools validate user_id
- All tools return structured JSON
- All tools handle errors gracefully
- All tools ensure data integrity