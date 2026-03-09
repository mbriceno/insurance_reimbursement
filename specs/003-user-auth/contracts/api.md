# API Contract: User Management & Authentication

## Endpoints

### User Registration

Create a new CUSTOMER account.

- **URL**: `/api/auth/register/`
- **Method**: `POST`
- **Authentication**: None (Public)
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword123"
  }
  ```
- **Success Response**:
  - **Code**: `201 Created`
  - **Content**:
    ```json
    {
      "email": "user@example.com",
      "role": "CUSTOMER"
    }
    ```
- **Error Responses**:
  - **Code**: `400 Bad Request` (Email already exists, password too short, invalid email format)
  - **Content**:
    ```json
    {
      "email": ["This field must be unique."],
      "password": ["Ensure this field has at least 8 characters."]
    }
    ```

---

### User Profile

Retrieve details of the currently authenticated user.

- **URL**: `/api/auth/me/`
- **Method**: `GET`
- **Authentication**: Required (JWT Bearer Token)
- **Success Response**:
  - **Code**: `200 OK`
  - **Content**:
    ```json
    {
      "email": "user@example.com",
      "role": "CUSTOMER"
    }
    ```
- **Error Responses**:
  - **Code**: `401 Unauthorized` (Token missing or invalid)
  - **Content**:
    ```json
    {
      "detail": "Authentication credentials were not provided."
    }
    ```
