# Research: Pet Insurance Reimbursement Platform (v2)

## Summary
Research focused on implementing a robust, scalable architecture using Django and Vue 3, with a specific emphasis on polymorphic insurance models, the Service-Repository-Selector pattern, and asynchronous validation.

## Decisions & Rationale

### D1: Service-Repository-Selector Pattern
- **Decision**: Implement a full Clean Architecture layers: Repositories for ORM, Services for state changes/logic, and Selectors for optimized reads.
- **Rationale**: Decouples domain logic from Django's framework specifics. Repositories allow for easier unit testing by mocking the persistence layer. Selectors prevent "Fat Models" and "Fat Views" by centralizing query logic.
- **Alternatives Considered**: Direct ORM usage in Views (rejected due to maintainability concerns in a growing system).

### D2: Polymorphic Insurance Models (Abstract Base)
- **Decision**: Use an abstract `BaseInsurance` model and a concrete `PetInsurance` model.
- **Rationale**: Allows for future extension to other insurance types (e.g., Home, Auto) while sharing common fields (owner, dates, status).
- **Alternatives Considered**: Single `Insurance` model with a type field (rejected as it's less extensible and can lead to many null fields).

### D3: Celery + Redis for Background Validation
- **Decision**: Use Celery with Redis as the broker for file hashing and coverage validation.
- **Rationale**: Ensures the API remains responsive. File hashing and complex date calculations should not block the request-response cycle.
- **Alternatives Considered**: Synchronous validation (rejected for UX/performance reasons).

### D4: Vue 3 Dashboards with Tailwind
- **Decision**: Build separate dashboard views for Customers (claims/pets/policies) and Support (review queue) using Vue 3 Composition API.
- **Rationale**: Provides a modern, reactive UX. Tailwind CSS ensures rapid and consistent UI development.
- **Alternatives Considered**: Server-side rendered Django templates (rejected for a more interactive single-page app feel).

## Research Tasks (Phase 0)

1. [x] Research Django Abstract Base Classes for polymorphic models.
2. [x] Research Repository pattern implementation in Python/Django.
3. [x] Research DRF permission classes for role-based filtering (request.user.role).
4. [x] Research Celery task triggering upon model signal or service call.
