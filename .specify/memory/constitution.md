<!--
  Sync Impact Report:
  - Version change: 0.0.0 → 1.0.0
  - List of modified principles:
    - [PRINCIPLE_1_NAME] → I. Clean Architecture (Django Services & Selectors)
    - [PRINCIPLE_2_NAME] → II. Technical Stack (Python 3.12, DRF, Vue 3, Tailwind)
    - [PRINCIPLE_3_NAME] → III. Core Engineering Excellence (SOLID, DRY, KISS)
    - [PRINCIPLE_4_NAME] → IV. Security & Role-Based Access Control (RBAC)
    - [PRINCIPLE_5_NAME] → V. Quality Assurance (Pytest & 80% Coverage)
  - Added sections:
    - Infrastructure & Deployment
    - Frontend Design & UX
  - Removed sections: None
  - Templates requiring updates:
    - .specify/templates/plan-template.md (✅ updated) - Checked, aligns.
    - .specify/templates/spec-template.md (✅ updated) - Checked, aligns.
    - .specify/templates/tasks-template.md (✅ updated) - Checked, aligns.
  - Follow-up TODOs: None
-->

# Insurance Reimbursement System Constitution

## Core Principles

### I. Clean Architecture (Django Services & Selectors)
Adhere to Clean Architecture principles. On the backend (Django), separate business logic into Services and Selectors to avoid "Fat Models/Views". Services handle write operations (mutations), while Selectors handle read operations (queries). This ensures a decoupled, testable, and maintainable codebase.

### II. Modern Tech Stack (Python 3.12, DRF, Vue 3)
Backend MUST use Django REST Framework (DRF) with Python 3.12+. Strict type hinting MUST be implemented throughout the entire codebase. Frontend MUST use Vue.js 3 (Composition API) with `<script setup>` and Tailwind CSS for a modern, responsive user interface.

### III. Core Engineering Excellence (SOLID, DRY, KISS)
Apply SOLID, DRY, and KISS principles to all code development. Variable and function names MUST be self-descriptive (Clean Code standards). Code should be readable, maintainable, and avoid unnecessary complexity.

### IV. Security & Role-Based Access Control (RBAC)
Implement strict RBAC for CUSTOMER, SUPPORT, and ADMIN roles. Mandatory ownership checks are REQUIRED for all data access; users MUST only be able to access their own pets and claims, unless elevated permissions are granted via RBAC.

### V. Quality Assurance (Pytest & 80% Coverage)
Use Pytest for all unit and integration tests. A minimum of 80% code coverage on business logic (Services/Selectors) is MANDATORY. Tests MUST verify both happy paths and edge cases to ensure system reliability.

## Infrastructure & Deployment
The project MUST be "Docker-ready" at all times. A `docker-compose.yml` MUST be maintained for local development, including services for PostgreSQL, Redis, and Celery. All infrastructure components should be easily reproducible across environments.

## Frontend Design & UX
The user interface and experience MUST be consistent across the entire application. All new UI components MUST adhere to the established design system. Tailwind CSS MUST be used for responsive and modern styling, ensuring accessibility and performance.

## Governance
This Constitution supersedes all other project documentation and practices. All Pull Requests and design reviews MUST verify compliance with these principles.

### Versioning Policy
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions.
- **MINOR**: New principle/section added or materially expanded guidance.
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements.

### Amendment Procedure
Changes to this Constitution must be documented in the Sync Impact Report and reflected in version number updates. Significant amendments require approval from the architecture lead.

**Version**: 1.0.0 | **Ratified**: 2026-03-08 | **Last Amended**: 2026-03-08
