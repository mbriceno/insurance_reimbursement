# API Contract: Pet Insurance Reimbursement Platform

## Endpoints

### 1. Pets (`/api/pets/`)
- **GET /api/pets/**
  - **Description**: List all pets owned by the current user.
  - **Roles**: CUSTOMER (own pets), SUPPORT/ADMIN (all pets).
- **POST /api/pets/**
  - **Description**: Register a new pet.
  - **Payload**:
    ```json
    {
      "name": "string",
      "species": "DOG|CAT|OTHER",
      "birth_date": "YYYY-MM-DD",
      "coverage_start": "YYYY-MM-DD"
    }
    ```
  - **Notes**: `coverage_end` is automatically calculated (+365 days).

### 2. Claims (`/api/claims/`)
- **GET /api/claims/**
  - **Description**: List claims based on role.
  - **CUSTOMER**: Returns only claims owned by the user.
  - **SUPPORT**: Returns all claims with status `IN_REVIEW`.
  - **ADMIN**: Returns all claims.
- **POST /api/claims/**
  - **Description**: Submit a new reimbursement claim.
  - **Payload**: Multipart Form-data
    ```json
    {
      "pet_id": "integer",
      "invoice": "File",
      "invoice_date": "YYYY-MM-DD",
      "amount": "decimal"
    }
    ```
  - **Response**: Returns 201 Created with status `PROCESSING`.
- **PATCH /api/claims/{id}/**
  - **Description**: Update claim status or add notes.
  - **Roles**: SUPPORT, ADMIN.
  - **Payload**:
    ```json
    {
      "status": "APPROVED|REJECTED",
      "review_notes": "string"
    }
    ```

## Authentication
- **Method**: JWT or Session-based (default DRF).
- **Authorization**: Roles determined by `User.role` field.
