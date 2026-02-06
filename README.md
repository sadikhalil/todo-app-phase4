# Hackathon Todo Application

## Overview

A modern todo application featuring a chatbot that can manage tasks through natural language processing. The application follows a simplified microservice architecture with a stateless main API server that handles all task operations through a shared service layer.

## Architecture

### Backend Services
- **Main API Server** (Port 8000): Handles chat requests and task operations using shared service layer
- **PostgreSQL/SQLite Database**: Persistent storage for tasks and conversations
- **MCP Server** (Port 8001): Optional HTTP-based tool server for task management

### Tech Stack
- **Backend**: Python 3.11, FastAPI, SQLModel
- **Database**: PostgreSQL or SQLite
- **Frontend**: Next.js 14, React 18, Framer Motion 12

## Project Structure

```
hackathon-todo/
├── backend/                 # Python FastAPI backend
│   ├── main.py              # Main server entry point
│   ├── app/                 # Application modules
│   │   ├── api/             # API routes
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── models/          # Database models
│   │   ├── services/        # Business logic services
│   │   └── db/              # Database configuration
│   ├── mcp/                 # MCP tool server (optional)
│   ├── requirements.txt     # Python dependencies
│   ├── run_main_server.py   # Start main server
│   └── run_mcp_server.py    # Start MCP server
├── frontend/                # Next.js frontend
├── specs/                   # Specification documents
├── docker-compose.yml       # Docker orchestration
├── README.md               # This file
└── .env.example            # Environment variables example
```

## Running the Application

### Prerequisites
- Python 3.11
- Node.js 18+
- PostgreSQL (optional, SQLite is used by default)
- Git

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**

   Create a `.env` file in the backend directory:
   ```env
   # Database Configuration
   DATABASE_URL='sqlite:///./todo_app.db'

   # JWT Configuration
   SECRET_KEY=your-super-secret-and-long-random-string-here-change-this-in-production
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440

   # Application Configuration
   DEBUG=True
   APP_NAME=Todo App API
   VERSION=1.0.0
   HOST=0.0.0.0
   PORT=8000
   ```

4. **Start the main server:**
   ```bash
   python run_main_server.py
   # Main API server runs on http://localhost:8000
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   # Frontend runs on http://localhost:3000
   ```

## API Documentation

### Authentication Endpoints
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user

### Task Endpoints
- `GET /tasks/` - Get all tasks for authenticated user
- `POST /tasks/` - Create a new task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task
- `PATCH /tasks/{id}/status` - Toggle task completion status
- `GET /tasks/stats` - Get task statistics

### Chat Endpoint
- `POST /api/{user_id}/chat` - Send a chat message and receive task-based responses

The chat endpoint supports natural language commands:
- Add tasks: "Add a task to buy groceries"
- List tasks: "Show my tasks"
- Complete tasks: "Complete task 1"
- Delete tasks: "Delete task 2"
- Update tasks: "Update task 1 title to new title"

### Health Checks
- `GET /health` - Health check endpoint

## Deployment

### Environment Variables for Production
```env
# Database Configuration
DATABASE_URL='postgresql://username:password@localhost/todo_db'

# JWT Configuration
SECRET_KEY=your-very-long-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Application Configuration
DEBUG=False
APP_NAME=Todo App API
VERSION=1.0.0
HOST=0.0.0.0
PORT=8000
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Server
Use a production WSGI/ASGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## Features

- **JWT-based Authentication**: Secure user authentication with token-based sessions
- **Natural Language Chatbot**: Add, update, delete, and manage tasks using natural language
- **Real-time Updates**: Dashboard automatically refreshes after chat operations
- **Persistent Storage**: All data stored in database with proper relationships
- **Responsive UI**: Modern, mobile-friendly interface built with Next.js

## Security

- JWT-based authentication with configurable expiration
- User ID validation to prevent unauthorized access
- Input validation for all endpoints
- SQL injection protection through SQLModel ORM

## Development

This project was built for a hackathon with a focus on:
- Clean, modular architecture
- Statelessness for scalability
- Secure inter-service communication
- Modern tech stack compliance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details.