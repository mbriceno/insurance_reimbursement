# Data Model: Pet Insurance Reimbursement Platform

## Entities

### User (Custom Model)
- **email**: EmailField (Unique ID, primary key)
- **role**: CharField (Choices: CUSTOMER, SUPPORT, ADMIN)
- **is_active**: BooleanField (Default: True)
- **is_staff**: BooleanField (True for ADMIN role)

### Pet
- **owner**: ForeignKey(User, on_delete=CASCADE)
- **name**: CharField
- **species**: CharField (Choices: DOG, CAT, OTHER)
- **birth_date**: DateField
- **coverage_start**: DateField
- **coverage_end**: DateField (Calculated: coverage_start + 365 days)

### Claim
- **user**: ForeignKey(User, on_delete=CASCADE)
- **pet**: ForeignKey(Pet, on_delete=CASCADE)
- **invoice**: FileField (Uploaded document)
- **invoice_date**: DateField (Date of the event/treatment)
- **amount**: DecimalField
- **status**: CharField (Choices: SUBMITTED, PROCESSING, IN_REVIEW, APPROVED, REJECTED)
- **review_notes**: TextField (Optional, filled by SUPPORT)
- **file_hash**: CharField (Unique hash for duplicate checking)

## Relationships
- **User (1) <-> (N) Pet**: One user can have multiple pets.
- **User (1) <-> (N) Claim**: One user can submit multiple claims.
- **Pet (1) <-> (N) Claim**: One pet can have multiple associated claims.

## Validation Rules
1. **Coverage Rule**: `coverage_end` MUST be exactly 365 days after `coverage_start`.
2. **Date of Event**: The `invoice_date` MUST fall within the range `[coverage_start, coverage_end]`.
3. **Duplicate Check**: The `file_hash` MUST be unique across all claims in the system.

## State Transitions (Claim Status)
1. **SUBMITTED** (Initial state via API) -> **PROCESSING** (Automatically set)
2. **PROCESSING** -> **IN_REVIEW** (If hash and date validation pass)
3. **PROCESSING** -> **REJECTED** (If hash or date validation fail)
4. **IN_REVIEW** -> **APPROVED** (Manual transition by SUPPORT)
5. **IN_REVIEW** -> **REJECTED** (Manual transition by SUPPORT)
