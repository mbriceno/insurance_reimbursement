# API Contract: Frontend Application Implementation

## Endpoints

### Authentication

- **POST /api/auth/register/**: Public. Registers a new user.
- **POST /api/token/**: Public. Logins and returns access/refresh tokens.
- **POST /api/token/refresh/**: Public. Refreshes the access token using the refresh token.
- **GET /api/auth/me/**: Authenticated. Returns current user profile data.

### Pet Management

- **GET /api/pets/**: Authenticated. Returns a list of pets owned by the user.
- **POST /api/pets/**: Authenticated. Creates a new pet.
- **GET /api/pets/:id/**: Authenticated. Returns details for a specific pet.

### Insurance Management

- **GET /api/insurance/**: Authenticated. Returns a list of insurance policies.
- **POST /api/insurance/**: Authenticated. Creates a new insurance policy linked to a pet.
- **GET /api/insurance/:id/**: Authenticated. Returns details for a specific policy.

### Claims Management

- **GET /api/claims/**: Authenticated. Returns a list of claims submitted by the user.
- **POST /api/claims/**: Authenticated. Submits a new claim (requires `multipart/form-data` for invoice file).
- **GET /api/claims/:id/**: Authenticated. Returns details for a specific claim.

## Authentication Header
All authenticated requests MUST include the JWT access token in the `Authorization` header:
`Authorization: Bearer <access_token>`
