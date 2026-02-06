# Running the Todo App with Logical Server Separation

This project contains two separate servers that can run simultaneously while maintaining logical separation of their persistent directories:

## Server Configuration

### Main Todo API Server
- Port: 8000
- Data Directory: `backend/main_server_data/`
- Database: `backend/main_server_data/main_todo_app.db`

### MCP Chat Server
- Port: 8001
- Data Directory: `backend/mcp_server_data/`
- Database: `backend/mcp_server_data/mcp_todo_app.db`

## Running Both Servers Together

### Recommended Method: Using the Combined Script
```bash
python start_both_separate.py
```
This script:
- Creates separate data directories for each server
- Sets environment variables to ensure logical separation
- Runs both servers simultaneously in separate threads
- Maintains individual persistent states

### Alternative Methods:
1. Individual servers:
   - Main server: `python run_main_server.py`
   - MCP server: `python run_mcp_server.py`

2. Using the shell script:
   ```bash
   ./start_both.sh
   ```

## Persistent Directory Structure

When running with logical separation:
```
backend/
├── main_server_data/       # Main server's persistent data
│   └── main_todo_app.db    # Main server's database
├── mcp_server_data/        # MCP server's persistent data
│   └── mcp_todo_app.db     # MCP server's database
└── src/                    # Shared source code
```

## Benefits of Logical Separation

- Each server maintains its own database and persistent state
- Data isolation prevents conflicts between services
- Independent scaling and maintenance
- Clear separation of concerns
- Easier debugging and monitoring

## Stopping the Servers

Press `Ctrl+C` in the terminal to stop both servers simultaneously.