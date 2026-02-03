# Quickstart: Todo App Multi-Phase Features

**Feature Branch**: `001-todo-app-features`
**Date**: 2025-12-27

## Prerequisites

### All Phases
- Python 3.11+
- Git

### Phase II+
- PostgreSQL 15+
- Node.js 18+ (for frontend)

### Phase III+
- Anthropic API key (for Claude)

### Phase IV+
- Docker
- kubectl
- Helm 3
- Minikube or kind (local Kubernetes)

### Phase V+
- Kafka (via Strimzi or Confluent)
- Dapr CLI

---

## Phase I: Console Application

### Setup

```bash
# Clone repository
git clone <repo-url>
cd todo-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install click

# Run console app
python -m src.cli.main
```

### Usage

```bash
# Add a task
todo add "Buy groceries"
todo add "Call mom" --description "Remember to ask about weekend"

# List tasks
todo list

# Update a task
todo update <task-id> --title "Buy groceries and milk"

# Complete a task
todo complete <task-id>

# Mark incomplete
todo incomplete <task-id>

# Delete a task
todo delete <task-id>
```

---

## Phase II: Web Application

### Backend Setup

```bash
# Install backend dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Run database migrations
alembic upgrade head

# Start backend server
uvicorn src.api.main:app --reload --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Environment Variables

```env
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### API Testing

```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Create task (use token from login response)
curl -X POST http://localhost:8000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{"title": "Buy groceries"}'
```

---

## Phase III: AI Chatbot

### Additional Setup

```bash
# Install AI dependencies
pip install langchain langchain-anthropic pgvector

# Add to .env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### WebSocket Chat

Connect to `ws://localhost:8000/api/v1/chat/ws?token=<access_token>`

```javascript
// Example WebSocket client
const ws = new WebSocket('ws://localhost:8000/api/v1/chat/ws?token=' + accessToken);

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Assistant:', data.content);
};

ws.send(JSON.stringify({ content: 'Add a task to buy milk' }));
```

### Chat Commands

Natural language commands supported:
- "Add a task to buy groceries"
- "Show my tasks"
- "Mark buy groceries as done"
- "Delete the buy groceries task"
- "What tasks do I have today?"
- "Set high priority on task X"

---

## Phase IV: Kubernetes Deployment

### Local Kubernetes Setup

```bash
# Start minikube
minikube start --memory=4096 --cpus=2

# Enable ingress
minikube addons enable ingress

# Build Docker images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Load images to minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Deploy with Helm
helm install todo-app ./helm/todo-app \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest
```

### Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get svc

# Port forward to access
kubectl port-forward svc/todo-backend 8000:8000
kubectl port-forward svc/todo-frontend 3000:3000
```

---

## Phase V: Cloud Deployment with Event-Driven Architecture

### Dapr Setup

```bash
# Install Dapr CLI
curl -fsSL https://raw.githubusercontent.com/dapr/cli/master/install/install.sh | bash

# Initialize Dapr in Kubernetes
dapr init -k

# Verify Dapr
dapr status -k
```

### Kafka Setup (via Strimzi)

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka

# Create Kafka cluster
kubectl apply -f ./k8s/kafka-cluster.yaml -n kafka
```

### Deploy with Dapr

```bash
# Deploy Dapr components
kubectl apply -f ./k8s/dapr-components/

# Deploy application with Dapr annotations
helm upgrade todo-app ./helm/todo-app \
  --set dapr.enabled=true \
  --set kafka.enabled=true
```

### KEDA Autoscaling

```bash
# Install KEDA
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace

# Apply ScaledObject
kubectl apply -f ./k8s/keda-scaledobject.yaml
```

---

## Running Tests

```bash
# Unit tests
pytest tests/unit -v

# Integration tests
pytest tests/integration -v

# Contract tests
pytest tests/contract -v

# All tests with coverage
pytest --cov=src --cov-report=html
```

---

## Troubleshooting

### Database Connection Failed
```bash
# Check PostgreSQL is running
pg_isready -h localhost -p 5432

# Verify credentials in .env
```

### JWT Token Expired
```bash
# Use refresh token to get new access token
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token>"}'
```

### Kubernetes Pods Not Starting
```bash
# Check pod logs
kubectl logs <pod-name>

# Check events
kubectl describe pod <pod-name>
```

### Dapr Sidecar Not Injected
```bash
# Verify namespace has annotation
kubectl get namespace default -o yaml | grep dapr

# Check Dapr is running
dapr status -k
```

---

## API Documentation

- OpenAPI Spec: `specs/001-todo-app-features/contracts/openapi.yaml`
- Swagger UI: http://localhost:8000/docs (when backend running)
- ReDoc: http://localhost:8000/redoc
