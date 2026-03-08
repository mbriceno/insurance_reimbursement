# Implementation Plan: Pet Insurance Reimbursement Platform (v2)

**Branch**: `002-pet-reimbursement` | **Date**: 2026-03-08 | **Spec**: /specs/002-pet-reimbursement/spec.md
**Input**: Feature specification from `/specs/002-pet-reimbursement/spec.md`

## Summary
Build a comprehensive Pet Insurance Reimbursement Platform using Clean Architecture (Django Services/Selectors/Repositories) and Vue.js 3. The system will automate claim validation (hash generation and coverage checks) via Celery and enforce strict RBAC for Customers, Support, and Admin users. This iteration introduces polymorphic insurance models (Abstract Base) to support future scalability.

## Technical Context

**Language/Version**: Python 3.12+ (Backend), JavaScript/TypeScript (Frontend - Vue 3)  
**Primary Dependencies**: Django, Django REST Framework (DRF), Celery, Redis, Tailwind CSS, Vue 3 (Composition API)  
**Storage**: PostgreSQL (Relational data), Redis (Broker for Celery)  
**Testing**: Pytest (80% coverage mandatory for business logic)  
**Target Platform**: Dockerized (PostgreSQL, Redis, Celery, Django)
**Project Type**: Web Application (Full-stack)  
**Performance Goals**: Automated claim validation completes within 15 seconds for 95% of uploads.  
**Constraints**: Strict RBAC (CUSTOMER, SUPPORT, ADMIN), polymorphic insurance models, mandatory 365-day coverage rule.  
**Scale/Scope**: MVP for pet insurance claims handling with extensible architecture for other insurance types.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Clean Architecture**: Backend business logic separated into Services, Selectors, and Repositories. (Requirement I)
- [x] **Tech Stack**: Python 3.12+, DRF, Vue 3, Tailwind CSS. (Requirement II)
- [x] **RBAC**: Implementation of CUSTOMER, SUPPORT, ADMIN roles with mandatory ownership checks. (Requirement IV)
- [x] **Quality**: Pytest used with 80% coverage goal on business logic. (Requirement V)
- [x] **Infrastructure**: Docker-ready with docker-compose.yml. (Infrastructure Section)

## Project Structure

### Documentation (this feature)

```text
specs/002-pet-reimbursement/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/             # DRF Views & Serializers
│   ├── models/          # Django Models (including Abstract Base)
│   ├── repositories/    # ORM encapsulations
│   ├── services/        # Business logic (mutations)
│   ├── selectors/       # Optimized queries (reads)
│   └── core/            # Config, Celery setup
└── tests/
    ├── unit/
    ├── integration/
    └── conftest.py

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── services/        # API communication
│   └── assets/          # Tailwind, Icons
└── tests/
```

**Structure Decision**: Option 2 (Web application) selected for full-stack delivery.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Repository Pattern | Decouples ORM from business logic for testability and polymorphic support. | Direct ORM usage makes cross-model logic (like BaseInsurance) harder to manage. |
| Abstract Base Model | Allows sharing core fields (owner, dates) across future insurance types. | Separate models for each type would lead to code duplication and redundant logic. |
| Asynchronous Processing | PDF requirements specify Celery for background validation tasks. | Synchronous validation blocks the user and fails performance goals (SC-001). |

## Phases

### Phase 1: Environment & Base Identity
- Setup Dockerized environment (Django, PostgreSQL, Redis, Celery).
- Implement Custom User model with RBAC (CUSTOMER, SUPPORT, ADMIN).
- Configure Django Admin to expose Pet and Claim models for the ADMIN role.
- Implement Permission Classes (IsAdmin, IsSupport, IsCustomer) for API security.

### Phase 2: Abstract Data Layer
- Create an Abstract 'BaseInsurance' model and a concrete 'PetInsurance' model.
- Implement Claim model with 'date_of_event' and 'file_hash' fields.
- Implement 'Pet' model linked to User.
- Implement 'PetRepository' and 'ClaimRepository' to encapsulate ORM logic.
- Set up 'InsuranceRepository' to handle polymorphic queries and policy creation.

### Phase 3: Domain Logic (Service Layer)
- Develop 'ClaimService' for submission, file hashing, and state management (PROCESSING -> IN_REVIEW/REJECTED).
- Develop 'PolicyService' to handle the 1-year auto-calculation for PetInsurance.
- Implement 'ClaimSelector' for optimized, role-based read queries (filtering by owner or status).

### Phase 4: Async Infrastructure
- Setup Celery for the "Background Task" simulation.
- Implement task to check 'date_of_event' against the 'PetInsurance' coverage period.

### Phase 5: Interface Layer (API & Frontend)
- DRF: Create endpoints using the Services and Selectors.
- Build Vue.js dashboards:
    - Customer: View pets, active insurance policies, and claim history.
    - Support: Queue for pending claim reviews.
- Integrate Django Admin for ADMIN role governance.

### Phase 6: Quality Assurance
- Pytest: Focus on testing the Service layer by mocking the Repository.
- Documentation: Create a README.md justifying the choice of the Repository pattern for scalability.
