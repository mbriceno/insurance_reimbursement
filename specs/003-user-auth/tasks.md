# Tasks: User Management & Authentication

**Input**: Design documents from `/specs/003-user-auth/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency management.

- [x] T001 Create backend project structure and base directories in `backend/src/api/`
- [x] T002 Add `djangorestframework-simplejwt` to `backend/requirements.txt`
- [x] T003 [P] Configure DRF and SimpleJWT authentication settings in `backend/src/core/settings.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Implement Custom `User` model with `role` field choices in `backend/src/api/models/user.py`
- [x] T005 Update `AUTH_USER_MODEL` in `backend/src/core/settings.py`
- [x] T006 Create and run initial migrations for the Custom `User` model
- [x] T007 [P] Implement base Repository/Service/Selector patterns in `backend/src/core/base/` (if missing)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Self-Registration (Priority: P1) 🎯 MVP

**Goal**: Allow guests to create a CUSTOMER account with password and email validation.

**Independent Test**: Use `quickstart.md` curl commands to register a new user and verify it has the 'CUSTOMER' role.

### Tests for User Story 1

- [x] T008 [P] [US1] Create unit tests for user registration and password hashing in `backend/tests/test_user_service.py`
- [x] T009 [P] [US1] Create unit tests for registration serializer validation (email uniqueness, password length) in `backend/tests/test_user_serializers.py`

### Implementation for User Story 1

- [x] T010 [US1] Implement `UserService.create_user` handling hashing and role defaulting in `backend/src/api/services/user_service.py`
- [x] T011 [US1] Implement `UserRegistrationSerializer` with custom `validate_password` in `backend/src/api/serializers.py`
- [x] T012 [US1] Implement `UserRegistrationView` (POST /api/auth/register/) in `backend/src/api/views/user_view.py`
- [x] T013 [US1] Register the registration endpoint in `backend/src/api/urls.py`

**Checkpoint**: User Story 1 (Registration) is fully functional and testable independently.

---

## Phase 4: User Story 2 - Profile View (Priority: P1)

**Goal**: Allow authenticated users to retrieve their own profile details (email, role).

**Independent Test**: Obtain a JWT token using `/api/auth/token/` and call `/api/auth/me/` to verify profile data.

### Tests for User Story 2

- [x] T014 [P] [US2] Create unit tests for profile selector and retrieval logic in `backend/tests/test_user_selector.py`
- [x] T015 [P] [US2] Create integration tests for authenticated profile access in `backend/tests/test_user_api.py`

### Implementation for User Story 2

- [x] T016 [US2] Implement `UserSelector.get_profile` to retrieve current user details in `backend/src/api/selectors/user_selector.py`
- [x] T017 [US2] Create `UserProfileSerializer` for returning email and role in `backend/src/api/serializers.py`
- [x] T018 [US2] Implement `UserProfileView` (GET /api/auth/me/) with `IsAuthenticated` permission in `backend/src/api/views/user_view.py`
- [x] T019 [US2] Register profile and JWT token endpoints in `backend/src/api/urls.py`

**Checkpoint**: User Story 2 (Profile View) and authentication are functional.

---

## Phase 5: User Story 3 - Role Protection (Priority: P2)

**Goal**: Ensure the 'role' field is read-only for users to prevent self-elevation.

**Independent Test**: Attempt a `PUT` or `PATCH` to `/api/auth/me/` with a different role and verify the role remains 'CUSTOMER'.

### Tests for User Story 3

- [x] T020 [P] [US3] Create test case to verify 'role' field is ignored during updates in `backend/tests/test_user_serializers.py`

### Implementation for User Story 3

- [x] T021 [US3] Set `role` as `read_only=True` in `UserProfileSerializer` in `backend/src/api/serializers.py`

**Checkpoint**: Role integrity is enforced at the API level.

---

## Phase 6: User Story 4 - Admin Management (Priority: P2)

**Goal**: Use Django Admin for staff/admin user creation and role assignment.

**Independent Test**: Access Django Admin and create a user with 'SUPPORT' role.

### Implementation for User Story 4

- [x] T022 [US4] Register Custom `User` model in `backend/src/api/admin.py` with role field visibility.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup.

- [ ] T023 [P] Final run of all tests in `backend/tests/` to ensure no regressions.
- [ ] T024 [P] Verify API schema documentation (if applicable) in `backend/src/schema.yml`.
- [ ] T025 Run all steps in `quickstart.md` to validate the entire user auth flow.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Must complete first.
- **Foundational (Phase 2)**: Depends on Phase 1 completion.
- **User Stories (Phase 3+)**: All depend on Phase 2 completion. US1 and US2 can be done in parallel, but US2 depends on US1 for having a user to test with.
- **Polish (Phase 7)**: Depends on all user stories completion.

### Parallel Opportunities

- T003, T007 (Foundational [P] tasks)
- T008, T009 (US1 [P] tests)
- T014, T015 (US2 [P] tests)
- All Phases 3-6 can technically run in parallel once Phase 2 is done, provided team capacity exists.

---

## Parallel Example: User Story 1

```bash
# Launch tests for US1 in parallel:
Task: "Create unit tests for user registration in backend/tests/test_user_service.py"
Task: "Create unit tests for registration serializer in backend/tests/test_user_serializers.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 Only)

1. Complete Phase 1 & 2 (Setup & Foundation).
2. Complete Phase 3 (Self-Registration).
3. Complete Phase 4 (Profile View & Auth).
4. **STOP and VALIDATE**: Verify a user can register and then view their own profile.

### Incremental Delivery

1. Foundation ready.
2. US1 complete -> Guest can become Customer.
3. US2 complete -> Customer can log in and see profile.
4. US3 complete -> Security hardened (Role read-only).
5. US4 complete -> Admin can manage staff.
