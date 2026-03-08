# Tasks: Pet Insurance Reimbursement Platform (v2)

**Input**: Design documents from `/specs/002-pet-reimbursement/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Pytest for business logic (Services/Selectors) with 80% coverage goal.

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable (different files, no dependencies)
- **[Story]**: User story mapping (e.g., [US1], [US2], [US3])

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and Docker environment setup

- [x] T001 [P] Create backend/ and frontend/ directory structures per implementation plan
- [x] T002 Initialize Django 5.x project in backend/src with DRF and Celery dependencies
- [x] T003 [P] Initialize Vue 3 project in frontend/src with Vite and Tailwind CSS
- [x] T004 Configure docker-compose.yml with postgres, redis, celery, backend, and frontend services

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure and identity management

**⚠️ CRITICAL**: Must be complete before user story implementation begins

- [x] T005 [P] Implement Custom User model with email ID and Roles (CUSTOMER, SUPPORT, ADMIN) in backend/src/models/user.py
- [x] T006 Implement Base permission classes (IsCustomer, IsSupport, IsAdmin) in backend/src/api/permissions.py
- [x] T007 [P] Setup Celery configuration and Redis broker in backend/src/core/celery.py
- [x] T008 Setup BaseRepository, BaseService, and BaseSelector abstract classes in backend/src/core/base/

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Customer Claim Submission (Priority: P1) 🎯 MVP

**Goal**: Enable customers to register pets, policies, and submit claims with automated validation

**Independent Test**: Register a pet/policy, submit an invoice, and verify Celery transitions status from PROCESSING to IN_REVIEW or REJECTED.

### Implementation for User Story 1

- [x] T009 [P] [US1] Create Pet model in backend/src/models/pet.py
- [x] T010 [P] [US1] Create BaseInsurance (Abstract) and PetInsurance models in backend/src/models/insurance.py
- [x] T011 [US1] Create Claim model with file_hash and status fields in backend/src/models/claim.py
- [x] T012 [P] [US1] Implement PetRepository in backend/src/repositories/pet_repository.py
- [x] T013 [P] [US1] Implement InsuranceRepository in backend/src/repositories/insurance_repository.py
- [x] T014 [US1] Implement ClaimRepository in backend/src/repositories/claim_repository.py
- [x] T015 [US1] Implement PolicyService for 365-day calculation in backend/src/services/policy_service.py
- [x] T016 [US1] Implement ClaimService for submission and file hashing in backend/src/services/claim_service.py
- [x] T017 [US1] Implement Celery task for automated coverage/hash validation in backend/src/tasks/claim_tasks.py
- [x] T018 [US1] Create DRF ViewSets for /api/pets/ and /api/insurances/ in backend/src/api/views/
- [x] T019 [US1] Create DRF ViewSet for /api/claims/ (POST submission) in backend/src/api/views/claim_view.py
- [ ] T020 [US1] Build Customer Dashboard in frontend/src/pages/CustomerDashboard.vue with Pet/Policy/Claim views

**Checkpoint**: User Story 1 is fully functional and testable independently

---

## Phase 4: User Story 2 - Support Review Workflow (Priority: P2)

**Goal**: Enable Support staff to review and transition claims in the queue

**Independent Test**: Login as SUPPORT, view only 'IN_REVIEW' claims, and successfully PATCH a claim to APPROVED with notes.

### Implementation for User Story 2

- [x] T021 [US2] Implement ClaimSelector for optimized, role-based read queries in backend/src/selectors/claim_selector.py
- [x] T022 [US2] Update Claim ViewSet to support GET (filtered by status) and PATCH (review action) in backend/src/api/views/claim_view.py
- [ ] T023 [US2] Build Support Review Queue in frontend/src/pages/SupportDashboard.vue

**Checkpoint**: Support staff can now process claims submitted by customers

---

## Phase 5: User Story 3 - Administrator System Management (Priority: P3)

**Goal**: Full governance and data management via Admin interface

**Independent Test**: Login as ADMIN to Django Admin, promote a user role, and override a claim status.

### Implementation for User Story 3

- [x] T024 [P] [US3] Register User, Pet, Insurance, and Claim models in backend/src/api/admin.py
- [x] T025 [US3] Implement Claim status override logic in backend/src/services/claim_service.py
- [x] T026 [US3] Configure automated Swagger documentation using drf-spectacular in backend/src/core/settings.py

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation and infrastructure validation

- [x] T027 [P] Create root README.md with Repository pattern justification and scalability notes
- [ ] T028 [P] Conduct final Dockerized environment test using quickstart.md steps
- [x] T029 Ensure 80% test coverage for all Services and Selectors in backend/tests/

---

## Dependencies & Execution Order

### Phase Dependencies

1. **Setup (Phase 1)** -> **Foundational (Phase 2)**: Core structure must exist before roles/base classes
2. **Foundational (Phase 2)** -> **User Story 1 (Phase 3)**: Roles and repositories depend on base classes
3. **User Story 1 (Phase 3)** -> **User Story 2 (Phase 4)**: Support reviews claims created in US1
4. **All Stories** -> **Polish (Final Phase)**

### Parallel Opportunities

- T001, T003 can be done in parallel (backend vs frontend init)
- T005, T007 (User model vs Celery setup)
- T009, T010 (Pet vs Insurance models)
- T024 (Admin registration) can be done anytime after models exist

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Setup (Phase 1)
2. Complete Foundational (Phase 2)
3. Complete User Story 1 (Phase 3)
4. **STOP and VALIDATE**: Verify end-to-end claim submission and automated validation

### Incremental Delivery

1. Foundation ready
2. Customer can submit claims (MVP)
3. Support can review claims
4. Admin has full governance
