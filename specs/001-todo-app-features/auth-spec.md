# Authentication and Authorization Specification for Todo App

## Overview
This specification defines the authentication and authorization system for the Todo application. The system will support multiple users with JWT-based authentication and ensure data isolation per user as part of User Story 2 (Priority: P2).

## Requirements
Based on the existing project constitution and specifications, the authentication system must:

1. Support user registration and login
2. Use JWT tokens for authentication
3. Hash passwords securely
4. Include user identity in tokens
5. Require valid tokens for protected API endpoints
6. Isolate user data (each user can only access their own tasks)
7. Return clear error messages for unauthorized access

## System Architecture

### Backend Components
- **User Model**: Stores user information (id, email, password_hash, created_at)
- **Auth Service**: Handles registration, login, password hashing, JWT generation/validation
- **JWT Middleware**: Validates tokens on protected endpoints
- **Task Service**: Filters tasks by user_id for data isolation

### Frontend Components
- **Auth Context**: Manages authentication state
- **Login Page**: Handles user login
- **Register Page**: Handles user registration
- **Protected Routes**: Verify authentication before allowing access

## API Contract

### Authentication Endpoints

#### POST /auth/register
Register a new user
```
Request Body:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response 201 Created:
{
  "message": "User registered successfully",
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}

Error Responses:
400 Bad Request - Invalid input
409 Conflict - Email already exists
```

#### POST /auth/login
Authenticate user and return JWT token
```
Request Body:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response 200 OK:
{
  "access_token": "jwt-token-string",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid-string",
    "email": "user@example.com"
  }
}

Error Responses:
400 Bad Request - Invalid input
401 Unauthorized - Invalid credentials
```

#### POST /auth/logout
Invalidate user session (optional, since JWT is stateless)
```
Request Headers:
Authorization: Bearer {access_token}

Response 200 OK:
{
  "message": "Logged out successfully"
}

Error Responses:
401 Unauthorized - Invalid/expired token
```

### Protected Task Endpoints
All task endpoints require authentication:

#### GET /tasks
Get user's tasks only
```
Request Headers:
Authorization: Bearer {access_token}

Response 200 OK:
{
  "tasks": [
    {
      "id": "uuid",
      "title": "Task title",
      "description": "Task description",
      "status": "incomplete" | "complete",
      "user_id": "user-uuid", // Belongs to requesting user
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  ]
}
```

#### POST /tasks
Create a new task for the authenticated user
```
Request Headers:
Authorization: Bearer {access_token}

Request Body:
{
  "title": "New task",
  "description": "Task description",
  "status": "incomplete" // optional, default
}

Response 201 Created:
{
  "id": "uuid",
  "title": "New task",
  "description": "Task description",
  "status": "incomplete",
  "user_id": "authenticated-user-id", // Auto-populated
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

Similar patterns for GET /tasks/{id}, PUT /tasks/{id}, DELETE /tasks/{id}, etc.

## Authentication Flow

### Registration Flow
1. User submits email and password via registration form
2. Frontend validates input format
3. Frontend sends POST request to /auth/register
4. Backend validates input, hashes password, creates user record
5. Backend returns success response with user info

### Login Flow
1. User submits email and password via login form
2. Frontend validates input format
3. Frontend sends POST request to /auth/login
4. Backend verifies credentials against hashed password
5. Backend generates JWT with user ID and expiration
6. Backend returns JWT token to frontend
7. Frontend stores token (localStorage/sessionStorage)

### Protected Resource Access
1. Frontend retrieves stored JWT token
2. Frontend makes API request with Authorization: Bearer {token}
3. Backend JWT middleware extracts and validates token
4. Backend extracts user ID from token claims
5. Backend authorizes request (ensures user can access requested resource)
6. Backend performs operation filtered by user ID
7. Backend returns response

## Security Implementation Details

### Password Security
- Passwords must be hashed using bcrypt with cost factor 12
- Minimum password length: 8 characters
- Password validation: at least one uppercase, lowercase, number, special character (optional but recommended)

### JWT Configuration
- Algorithm: HS256 or RS256
- Claims:
  - `sub`: user ID (UUID)
  - `exp`: expiration timestamp (1 hour from issue)
  - `iat`: issued at timestamp
  - `jti`: unique token ID (optional for blacklisting)
- Secret key: environment variable, minimum 32 random bytes
- Refresh tokens: optional, with longer expiration (7 days)

### Data Isolation
- All task queries must include `WHERE user_id = :current_user_id` clause
- Task creation automatically assigns `user_id` from authenticated user
- Task update/delete operations verify the task belongs to authenticated user
- Return 404 (not 403) when user tries to access non-existent or foreign resource to prevent user enumeration

## Error Handling

### Authentication Errors
- **400 Bad Request**: Invalid email format, weak password, missing fields
- **401 Unauthorized**: Invalid credentials, expired/invalid token
- **403 Forbidden**: Valid token but insufficient permissions (shouldn't occur with proper isolation)
- **404 Not Found**: User doesn't exist (for login attempts)

### Authorization Errors
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: Attempt to access another user's resource
- **404 Not Found**: Resource doesn't exist OR belongs to another user (to prevent enumeration)

## Frontend Implementation

### Auth Context Structure
```typescript
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}
```

### API Client Configuration
- Automatically attach Authorization header to all requests
- Handle 401 responses by redirecting to login
- Token refresh mechanism (if implemented)

## Database Schema Implications
- Add `user_id` UUID column to `tasks` table (foreign key to `users`)
- Create `users` table with `id`, `email`, `password_hash`, `created_at`
- Add indexes on `tasks.user_id` for efficient querying
- Add unique constraint on `users.email`

## Testing Requirements
- Unit tests for password hashing and verification
- Unit tests for JWT token generation and validation
- Integration tests for registration and login flows
- Integration tests for data isolation (user A can't access user B's tasks)
- Contract tests for authentication API endpoints
- Security tests for common vulnerabilities