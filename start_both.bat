@echo off
echo Starting both Todo application servers...

echo Starting Main Todo Application Server...
echo Server will be available at http://localhost:8000
start cmd /k "cd backend && python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload"

echo Starting MCP Server for Todo Chat...
echo Server will be available at http://localhost:8001
start cmd /k "cd backend && python -m uvicorn mcp.server:app --host 0.0.0.0 --port 8001 --reload"

echo Both servers are starting:
echo - Main Todo API: http://localhost:8000
echo - MCP Chat Server: http://localhost:8001
echo.
echo Separate windows should open for each server.

pause