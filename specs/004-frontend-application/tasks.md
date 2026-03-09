# Tasks: Frontend Application Implementation

**Input**: Design documents from `/specs/004-frontend-application/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included as per engineering standards for validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/src/`, `frontend/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize Vite project with Vue 3 and TypeScript in `frontend/`
- [X] T002 Install core dependencies: `pinia`, `vue-router`, `axios` in `frontend/package.json`
- [X] T003 [P] Install development dependencies: `tailwindcss`, `postcss`, `autoprefixer`, `vitest`, `@playwright/test` in `frontend/package.json`
- [X] T004 [P] Configure Tailwind CSS in `frontend/tailwind.config.js` and `frontend/src/assets/main.css`
- [X] T005 [P] Configure Vitest in `frontend/vitest.config.ts`
- [X] T006 [P] Configure Playwright in `frontend/playwright.config.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create base types and interfaces in `frontend/src/types/index.ts` (based on data-model.md)
- [X] T008 [P] Implement base Axios instances (public/auth) in `frontend/src/services/api.ts`
- [X] T009 [P] Setup Pinia root store in `frontend/src/main.ts`
- [X] T010 [P] Setup Vue Router base configuration in `frontend/src/router/index.ts`
- [X] T011 [P] Create `PublicLayout.vue` and `AppLayout.vue` in `frontend/src/layouts/`
- [X] T012 Implement global notification state in `frontend/src/store/notification.ts`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication & Session Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to register, login, and maintain a session.

**Independent Test**: Successfully register a new user, log in, and see user profile data synced from `/api/auth/me/`.

### Tests for User Story 1

- [X] T013 [P] [US1] Create unit tests for `auth` store in `frontend/src/store/__tests__/auth.spec.ts`
- [X] T014 [P] [US1] Create E2E tests for Login/Register flow in `frontend/tests/e2e/auth.spec.ts`

### Implementation for User Story 1

- [X] T015 [US1] Implement `auth` store with login/register/logout/refresh actions in `frontend/src/store/auth.ts`
- [X] T016 [US1] Add JWT interceptors to Axios auth instance in `frontend/src/services/api.ts`
- [X] T017 [US1] Create `RegisterView.vue` with form validation in `frontend/src/pages/RegisterView.vue`
- [X] T018 [US1] Create `LoginView.vue` with form validation in `frontend/src/pages/LoginView.vue`
- [X] T019 [US1] Implement `isAuthenticated` router guard in `frontend/src/router/index.ts`

**Checkpoint**: User Story 1 is functional. Users can authenticate and sessions are managed.

---

## Phase 4: User Story 2 - Pet and Insurance Management (Priority: P1)

**Goal**: Allow users to list and manage their pets and associated insurance policies.

**Independent Test**: Create a pet, then create an insurance policy selecting that pet from the dropdown. Verify both appear in the respective lists.

### Tests for User Story 2

- [X] T020 [P] [US2] Create unit tests for `pet` and `insurance` services in `frontend/src/services/__tests__/resource.spec.ts`
- [X] T021 [P] [US2] Create E2E tests for Pet/Insurance management in `frontend/tests/e2e/resources.spec.ts`

### Implementation for User Story 2

- [X] T022 [P] [US2] Implement `petService` for CRUD operations in `frontend/src/services/petService.ts`
- [X] T023 [P] [US2] Implement `insuranceService` for CRUD operations in `frontend/src/services/insuranceService.ts`
- [X] T024 [US2] Create `PetsListView.vue` and `PetDetailView.vue` in `frontend/src/pages/`
- [X] T025 [US2] Create `InsuranceCreateView.vue` with pet selection logic in `frontend/src/pages/InsuranceCreateView.vue`
- [X] T026 [US2] Integrate pet/insurance views into the router in `frontend/src/router/index.ts`

**Checkpoint**: User Story 2 is functional. Users can manage their pets and insurance.

---

## Phase 5: User Story 3 - Claim Submission with Invoice Upload (Priority: P2)

**Goal**: Enable users to submit reimbursement claims with file uploads.

**Independent Test**: Submit a claim with a valid invoice file and verify success notification and API call payload.

### Tests for User Story 3

- [X] T027 [P] [US3] Create unit tests for `claimService` in `frontend/src/services/__tests__/claim.spec.ts`
- [X] T028 [P] [US3] Create E2E tests for Claim submission in `frontend/tests/e2e/claims.spec.ts`

### Implementation for User Story 3

- [X] T029 [US3] Implement `claimService` with `multipart/form-data` support in `frontend/src/services/claimService.ts`
- [X] T030 [US3] Create `ClaimSubmissionView.vue` with file upload and pet/policy selection in `frontend/src/pages/ClaimSubmissionView.vue`
- [X] T031 [US3] Add claim routes to `frontend/src/router/index.ts`

**Checkpoint**: User Story 3 is functional. Users can submit claims with invoices.

---

## Phase 6: User Story 4 - Navigation & Global Error Handling (Priority: P2)

**Goal**: Provide a consistent navigation experience and global error feedback.

**Independent Test**: Trigger a 401/400 error and verify global notification appears. Verify navbar links change on login/logout.

### Tests for User Story 4

- [X] T032 [P] [US4] Create unit tests for `Notification` component in `frontend/src/components/__tests__/Notification.spec.ts`
- [X] T033 [P] [US4] Create E2E tests for Navigation visibility in `frontend/tests/e2e/navigation.spec.ts`

### Implementation for User Story 4

- [X] T034 [US4] Create `Navbar.vue` with conditional links in `frontend/src/components/Navbar.vue`
- [X] T035 [US4] Create `GlobalNotification.vue` component in `frontend/src/components/GlobalNotification.vue`
- [X] T036 [US4] Implement global error handling interceptor in `frontend/src/services/api.ts` to trigger notifications.
- [X] T037 [US4] Implement `isAdmin` router guard in `frontend/src/router/index.ts`

**Checkpoint**: User Story 4 is functional. Navigation and error handling are polished.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, styling, and optimization.

- [X] T038 Apply consistent Tailwind styling across all views in `frontend/src/assets/main.css`
- [X] T039 Implement loading states for all async operations in components
- [X] T040 Final code cleanup and removal of console logs

---

## Implementation Strategy

1. **MVP First**: Complete Phase 1 & 2, then Phase 3 (US1). This provides a functional, authenticated application.
2. **Incremental Delivery**: Phases 4 and 5 can be worked on in parallel once US1 is stable.
3. **Fail Fast**: Write test cases before implementation to ensure requirements are met.

## Dependencies

1. **Setup (Phase 1)** -> **Foundational (Phase 2)**
2. **Foundational (Phase 2)** -> **US1 (Phase 3)**
3. **US1 (Phase 3)** -> **US2, US3, US4**
4. **All User Stories** -> **Polish (Phase 7)**

## Parallel Execution Opportunities

- T003, T004, T005, T006 (Setup configs)
- T008, T009, T010, T011 (Foundational components)
- T013, T014 (US1 Tests)
- T020, T021, T022, T023 (US2 Service/Test components)
