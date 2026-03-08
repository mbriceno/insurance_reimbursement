/speckit.constitution Act as a Senior Full Stack Engineer and Software Architect. The project must follow these strict rules:
1. Architecture: Adhere to Clean Architecture principles. On the backend (Django), separate business logic into Services and Selectors to avoid "Fat Models/Views".
2. Backend: Use Django REST Framework (DRF) with Python 3.12+. Implement strict type hinting throughout the codebase.
3. Frontend: Use Vue.js 3 (Composition API) with <script setup> and Tailwind CSS for a modern, responsive UI.
4. Core Principles: Apply SOLID, DRY, and KISS. Variable and function names must be self-descriptive (Clean Code).
5. Security: Implement strict RBAC (Role-Based Access Control) for CUSTOMER, SUPPORT, and ADMIN roles[cite: 19]. Mandatory ownership checks: users must only access their own pets and claims.
6. Docker: The project must be "Docker-ready" with a docker-compose.yml for local development including PostgreSQL, Redis, and Celery.
7. Quality: Use Pytest for unit and integration tests with a minimum 80% coverage on business logic.
8. Frontend: The user interface and experience must be consistent across the entire application. All new UI components must adhere to the established design system.


/speckit.specify Define specifications for a "Pet Insurance Reimbursement Platform":
Core Entities:
- User: Custom User model using email as the unique identifier, password and Roles: CUSTOMER, SUPPORT, ADMIN.
- Base Insurance (Abstract): Common fields for any policy.
    - Fields: owner (FK to User), coverage_start, coverage_end, status (ACTIVE, EXPIRED), created_at.
- Pet: Represents the animal.
    - Fields: name, species (DOG, CAT, OTHER), birth_date.
- PetInsurance (Implements Base Insurance): Connects a Pet to a Policy.
    - Fields: pet (FK to Pet).
    - Business Rule: coverage_end = coverage_start + 365 days.
- Claim Entity:
    - Fields: insurance (FK to PetInsurance), invoice (file), invoice_date, amount, status (SUBMITTED, PROCESSING, IN_REVIEW, APPROVED, REJECTED), date_of_event, file_hash.
- Roles & Permissions :
    - CUSTOMER: Can CRUD their own Pets and create/view their own Claims.
    - SUPPORT: Can view all Claims in 'IN_REVIEW' and transition them to APPROVED/REJECTED.
    - ADMIN: 
        - Full access to the Django Admin site for data management.
        - Ability to manage and promote User roles.
        - Permission to override/reset Claim statuses in case of system errors.
Required Workflow:
1. Upon Claim creation, initial status must be PROCESSING.
2. Implement an asynchronous task (Celery) to:
   - Generate a file hash to prevent duplicate invoice uploads.
   - Validate that the 'date_of_event' falls within the pet's coverage period.
   - Transition status to IN_REVIEW if valid, otherwise REJECTED.
3. SUPPORT role can update status to APPROVED or REJECTED with notes.
4. ADMIN role manages the system via Django Admin.
API Endpoints:
- RESTful endpoints for /api/pets/ and /api/claims/.
- Ownership filters: Customers see only their data; Support sees all pending reviews.
- Automated Swagger documentation.


/speckit.plan
Generate a comprehensive implementation plan for a Clean Architecture (Service-Repository-Selector) approach:
Phase 1: Environment & Base Identity
- Setup Dockerized environment (Django, PostgreSQL, Redis, Celery).
- Implement Custom User model with RBAC (CUSTOMER, SUPPORT, ADMIN).
- Configure Django Admin to expose Pet and Claim models for the ADMIN role.
- Implement Permission Classes (IsAdmin, IsSupport, IsCustomer) to be used across the API.

Phase 2: Abstract Data Layer
- Create an Abstract 'BaseInsurance' model and a concrete 'PetInsurance' model.
- Implement Claim model.
- Implement 'Pet' model as a standalone entity linked to insurance.
- Implement 'PetRepository' and 'ClaimRepository' to encapsulate ORM logic (save, get_by_id, list_by_owner).
- Set up 'InsuranceRepository' to handle polymorphic queries and policy creation.
Phase 3: Domain Logic (Service Layer)
- Develop 'ClaimService' (using the Repository for data access) for submission, file hashing, and state management.
- Develop 'PolicyService' to handle the 1-year auto-calculation for PetInsurance.
- Logic: File hashing, state transitions (PROCESSING -> IN_REVIEW), and 1-year coverage calculation.
- Implement 'ClaimSelector' for optimized, role-based read queries.
Phase 4: Async Infrastructure
- Setup Celery for the "Background Task" simulation required by the PDF.
- Implement task to check 'date_of_event' against the 'PetInsurance' coverage period.
Phase 5: Interface Layer (API & Frontend)
- DRF: Create endpoints using the Services and Selectors.
- Build Vue.js dashboards:
    - Customer: View pets, active insurance policies, and claim history.
    - Support: Queue for pending claim reviews.
- Integrate Django Admin for ADMIN role governance.
Phase 6: Quality Assurance
- Pytest: Focus on testing the Service layer by mocking the Repository.
- Documentation: Create a README.md justifying the choice of the Repository pattern for future horizontal scalability.
