# Data Model: User Management & Authentication

## Entities

### User

Represents a system user.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `email` | String | Unique email address used for login. | Unique, Required, Email Format |
| `password` | String | Securely hashed password. | Required, Min 8 characters |
| `role` | Enum | User role (CUSTOMER, SUPPORT, ADMIN). | Required, Choices, Read-only via API |

**Relationships**:
- None directly for this feature. Future relationships include Pets and Claims.

**State Transitions & Validation**:
- `role` MUST default to 'CUSTOMER' upon creation via the public API.
- `role` can only be changed by an ADMIN through the Django administration interface.
- `password` MUST be hashed before storage using Django's standard hashers.
