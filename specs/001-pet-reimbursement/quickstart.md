# Quickstart: Pet Insurance Reimbursement Platform

## Setup Environment

### 1. Prerequisite: Docker
Ensure Docker and Docker Compose are installed.

### 2. Launch Services
Run the following from the repository root:
```bash
docker-compose up --build
```
This will start:
- **Backend**: Django (Port 8000)
- **Database**: PostgreSQL
- **Worker**: Celery (handles hashing and validation)
- **Broker**: Redis
- **Frontend**: Vue 3 (Port 5173)

### 3. Initialize Database
Apply migrations and create a superuser:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## API Documentation
Once the server is running, visit:
- **Swagger**: `http://localhost:8000/api/docs/`
- **Django Admin**: `http://localhost:8000/admin/`

## Testing
Run the test suite with coverage:
```bash
docker-compose exec backend pytest --cov=src
```

## Workflow Simulation
1. **Login**: Authenticate as a CUSTOMER.
2. **Register Pet**: `POST /api/pets/` with `coverage_start`.
3. **Submit Claim**: `POST /api/claims/` with a PDF/Image invoice.
4. **Validation**: Observe status transition from `PROCESSING` to `IN_REVIEW` (Check Celery logs).
5. **Review**: Authenticate as a SUPPORT user and `PATCH` the claim to `APPROVED`.
