# API Contract: Pet Insurance Reimbursement Platform (v2)

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
      "birth_date": "YYYY-MM-DD"
    }
    ```

### 2. Pet Insurance (`/api/insurances/`)
- **GET /api/insurances/**
  - **Description**: List insurance policies owned by the current user.
  - **Roles**: CUSTOMER (own policies), SUPPORT/ADMIN (all policies).
- **POST /api/insurances/**
  - **Description**: Create a new pet insurance policy.
  - **Payload**:
    ```json
    {
      "pet_id": "integer",
      "coverage_start": "YYYY-MM-DD"
    }
    ```
  - **Notes**: `coverage_end` is automatically calculated (+365 days).

### 3. Claims (`/api/claims/`)
- **GET /api/claims/**
  - **Description**: List claims based on role.
  - **CUSTOMER**: Returns only claims linked to the user's policies.
  - **SUPPORT**: Returns all claims with status `IN_REVIEW`.
  - **ADMIN**: Returns all claims.
- **POST /api/claims/**
  - **Description**: Submit a new reimbursement claim.
  - **Payload**: Multipart Form-data
    ```json
    {
      "insurance_id": "integer",
      "invoice": "File",
      "invoice_date": "YYYY-MM-DD",
      "date_of_event": "YYYY-MM-DD",
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

## Authentication & Permissions
- **Method**: JWT or Session-based (default DRF).
- **Authorization**: Custom role-based permission classes (`IsCustomer`, `IsSupport`, `IsAdmin`).
- **Data Filtering**: Views MUST apply ownership filters based on `request.user` for Customers.
