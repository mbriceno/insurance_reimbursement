# Research: User Management & Authentication

**Status**: Complete  
**Date**: 2026-03-09

## Research Tasks

### RT-001: Implementing read-only 'role' field in DRF

**Decision**: Use `read_only_fields` in the DRF serializer or explicitly set `read_only=True` on the role field in the serializer class.

**Rationale**: DRF serializers provide a built-in mechanism to prevent fields from being updated via API requests while still including them in responses. This directly fulfills the requirement that a CUSTOMER cannot promote themselves.

**Alternatives Considered**:
- Handling in the `update` method of the service: More manual work and less idiomatic DRF.
- Using a separate serializer for updates: Adds complexity and boilerplate.

### RT-002: Secure password hashing in Django/DRF

**Decision**: Use Django's built-in `make_password` and the default `BCrypt` or `Argon2` hasher as configured in `settings.py`.

**Rationale**: Django's password management is highly secure and follows industry standards. Using `make_password` in the service layer before saving the user entity ensures the password is never stored in plain text.

**Alternatives Considered**:
- Custom hashing: Unnecessary and risky.

### RT-003: User Role Management (Groups vs. Custom Field)

**Decision**: Use a custom `role` field on a custom `User` model, with a set of choices (CUSTOMER, SUPPORT, ADMIN).

**Rationale**: The specification mentions a 'role' field specifically and describes it as a property of the user returned in responses. A custom field with choices is more direct and easier to serialize than managing Django Groups for a simple RBAC system.

**Alternatives Considered**:
- Django Groups: More flexible for complex permission sets, but adds overhead for this specific requirement.

### RT-004: Defaulting Role to 'CUSTOMER'

**Decision**: Set the default value for the `role` field in the database model to 'CUSTOMER'.

**Rationale**: Ensures that every user created through any means (unless explicitly specified) defaults to the most restricted role. This provides a safe baseline.

**Alternatives Considered**:
- Assigning in the `UserService.create_user()`: Also valid, but model-level defaults are a stronger guarantee.

## Best Practices & Integration

### DRF Serializer Validation
- Use `UniqueValidator` for the email field.
- Implement a `validate_password` method in the registration serializer to enforce the 8-character minimum length.

### Service-Selector Pattern
- `UserService.create_user(email, password, role='CUSTOMER')` will handle the write logic.
- `UserSelector.get_profile(user)` will handle the read logic (though for `/api/auth/me/`, direct access to `request.user` is more common, the selector could enrich it if needed).

### Authentication
- Use `djangorestframework-simplejwt` for JWT-based authentication, which is the standard for modern DRF APIs.
