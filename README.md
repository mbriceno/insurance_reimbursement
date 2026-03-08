# Pet Insurance Reimbursement Platform

## Overview
A Django-based platform for managing pet insurance claims with automated validation and role-based access control.

## Architecture: Service-Repository-Selector
This project adheres to Clean Architecture principles using the following layers:
- **Models**: Standard Django ORM models defining the data schema.
- **Repositories**: Encapsulate all ORM logic. This decouples the domain logic from the persistence layer, making it easier to swap or mock data sources.
- **Services**: House the business logic and state transitions. Services are the primary way to perform "write" operations (mutations).
- **Selectors**: Centralize optimized "read" queries. Selectors ensure that complex data retrieval is consistent and doesn't clutter views or models.

### Justification for Repository Pattern
- **Testability**: Allows for high-quality unit testing of business logic by mocking the Repository layer without needing a database.
- **Scalability**: Facilitates horizontal scalability by providing a clear boundary for data access, allowing for future optimizations like caching or polyglot persistence without changing the core business logic.
- **Maintainability**: Prevents the "Fat Model" and "Fat View" anti-patterns, keeping the codebase organized as the system grows.

## Setup & Development
Refer to [specs/002-pet-reimbursement/quickstart.md](specs/002-pet-reimbursement/quickstart.md) for detailed setup instructions using Docker.

## Testing
Run tests using Pytest:
```bash
docker-compose exec backend pytest --cov=src
```
Goal: 80%+ coverage on Services and Selectors.
