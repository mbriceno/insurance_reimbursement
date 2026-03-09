# Data Model: Frontend Application Implementation

## Entities

### User
Represents the authenticated user and their current session.
- **id**: UUID (from backend)
- **username**: String
- **email**: String
- **role**: Enum (CUSTOMER, ADMIN, SUPPORT)
- **isAuthenticated**: Boolean (derived from token existence)

### Pet
Represents an animal owned by the user.
- **id**: Integer/UUID
- **name**: String
- **species**: String (e.g., Dog, Cat)
- **owner_id**: Integer/UUID (link to User)

### InsurancePolicy
Represents a coverage plan linked to a pet.
- **id**: Integer/UUID
- **pet_id**: Integer/UUID (link to Pet)
- **policy_number**: String
- **coverage_details**: String
- **is_active**: Boolean

### Claim
Represents a reimbursement request.
- **id**: Integer/UUID
- **pet_id**: Integer/UUID (link to Pet)
- **insurance_id**: Integer/UUID (link to InsurancePolicy)
- **amount**: Decimal
- **description**: String
- **invoice_file**: File/URL (multipart upload)
- **status**: Enum (PENDING, APPROVED, REJECTED)

## State Transitions (Claims)
1. **DRAFT**: Claim is being prepared (local state).
2. **SUBMITTED**: Claim is sent to the backend.
3. **PENDING**: Backend has received and is processing the claim.
4. **FINALIZED**: Claim is either APPROVED or REJECTED.
