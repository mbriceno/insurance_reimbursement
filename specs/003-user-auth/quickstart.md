# Quickstart: User Management & Authentication

## Testing User Registration

1. **Register a new user**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"email": "testuser@example.com", "password": "password123"}'
   ```
   **Expected Output**: `201 Created` with email and CUSTOMER role.

2. **Attempt to register with existing email**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"email": "testuser@example.com", "password": "password123"}'
   ```
   **Expected Output**: `400 Bad Request` with uniqueness error.

3. **Attempt registration with weak password**:
   ```bash
   curl -X POST http://localhost:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{"email": "newuser@example.com", "password": "abc"}'
   ```
   **Expected Output**: `400 Bad Request` with length error.

## Testing User Profile Retrieval

1. **Obtain a JWT token** (assumes login endpoint exists):
   ```bash
   curl -X POST http://localhost:8000/api/auth/token/ \
     -H "Content-Type: application/json" \
     -d '{"email": "testuser@example.com", "password": "password123"}'
   ```
   Capture the `access` token.

2. **Retrieve profile**:
   ```bash
   curl -X GET http://localhost:8000/api/auth/me/ \
     -H "Authorization: Bearer <access_token>"
   ```
   **Expected Output**: `200 OK` with profile details.

3. **Attempt access without token**:
   ```bash
   curl -X GET http://localhost:8000/api/auth/me/
   ```
   **Expected Output**: `401 Unauthorized`.
