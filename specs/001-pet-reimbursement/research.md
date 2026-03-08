# Research: Pet Insurance Reimbursement Platform

## Summary
Research focused on implementing Clean Architecture in Django, handling asynchronous tasks with Celery, and setting up a secure RBAC environment for both backend and frontend.

## Decisions & Rationale

### D1: Repository-Service-Selector Pattern in Django
- **Decision**: Use `repositories/` for all Django ORM queries, `services/` for business logic and state changes, and `selectors/` for read-only query optimizations.
- **Rationale**: Decouples the domain logic from the framework's persistence layer, enabling easier testing and mockable repositories.
- **Alternatives Considered**: Fat models (rejected due to maintenance difficulty) or fat serializers (rejected as it violates Clean Architecture principles).

### D2: Celery for Asynchronous Validation
- **Decision**: Integrate Celery with Redis as the message broker.
- **Rationale**: Required for non-blocking file hashing and coverage period validation. Ensures the user gets a 'PROCESSING' status immediately.
- **Alternatives Considered**: Synchronous processing (rejected for UX/performance reasons).

### D3: File Hashing for Duplicate Detection
- **Decision**: Use `hashlib` (SHA-256) on the uploaded file content to generate a unique `file_hash`.
- **Rationale**: Efficient and highly reliable for preventing duplicate invoice uploads.
- **Alternatives Considered**: Filename comparison (too fragile).

### D4: DRF Role-Based Access Control (RBAC)
- **Decision**: Custom permission classes (`IsCustomer`, `IsSupport`, `IsAdmin`) and query filtering based on `request.user`.
- **Rationale**: Directly maps to the requirements. `IsCustomer` filters by owner, `IsSupport` allows access to all 'IN_REVIEW' claims.
- **Alternatives Considered**: Django's built-in groups (too heavy for initial MVP, custom roles are more flexible).

### D5: Vue 3 Composition API & Tailwind
- **Decision**: Vite for scaffolding, `<script setup>` for the UI components, and Tailwind for styling.
- **Rationale**: Provides the fastest development cycle and aligns with modern frontend standards.
- **Alternatives Considered**: Options API (rejected as Composition API is preferred for Vue 3).

## Research Tasks (Phase 0)

1. [x] Research Django Custom User Model with email-based identity.
2. [x] Research automated Swagger generation with `drf-spectacular`.
3. [x] Research Pytest-Django configuration for mocking repositories.
4. [x] Research Docker setup for a multi-service Django/Celery app.
