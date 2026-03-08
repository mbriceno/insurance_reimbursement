# Data Model: Pet Insurance Reimbursement Platform (v2)

## Entities

### User (Custom Model)
- **email**: EmailField (Unique ID, primary key)
- **role**: CharField (Choices: CUSTOMER, SUPPORT, ADMIN)
- **is_active**: BooleanField (Default: True)
- **is_staff**: BooleanField (True for ADMIN role)

### BaseInsurance (Abstract Model)
- **owner**: ForeignKey(User, on_delete=CASCADE)
- **coverage_start**: DateField
- **coverage_end**: DateField (Calculated: coverage_start + 365 days)
- **status**: CharField (Choices: ACTIVE, EXPIRED)
- **created_at**: DateTimeField (Auto-generated)

### Pet
- **owner**: ForeignKey(User, on_delete=CASCADE)
- **name**: CharField
- **species**: CharField (Choices: DOG, CAT, OTHER)
- **birth_date**: DateField

### PetInsurance (Implements BaseInsurance)
- **pet**: ForeignKey(Pet, on_delete=CASCADE)

### Claim
- **insurance**: ForeignKey(PetInsurance, on_delete=CASCADE)
- **invoice**: FileField (Uploaded document)
- **invoice_date**: DateField
- **amount**: DecimalField
- **status**: CharField (Choices: SUBMITTED, PROCESSING, IN_REVIEW, APPROVED, REJECTED)
- **review_notes**: TextField (Optional, filled by SUPPORT)
- **date_of_event**: DateField (The date the claim event occurred)
- **file_hash**: CharField (Unique hash for duplicate checking)

## Relationships
- **User (1) <-> (N) Pet**: One user can have multiple pets.
- **User (1) <-> (N) Insurance Policies**: One user can own multiple insurance policies.
- **Pet (1) <-> (1) PetInsurance**: A specific pet is covered by a specific policy.
- **PetInsurance (1) <-> (N) Claim**: Multiple claims can be filed against a single insurance policy.

## Validation Rules
1. **365-Day Rule**: `coverage_end` MUST be exactly 365 days after `coverage_start` for `PetInsurance`.
2. **Date of Event Validation**: The `date_of_event` MUST fall within the range `[coverage_start, coverage_end]` of the linked `PetInsurance`.
3. **Duplicate Detection**: The `file_hash` MUST be unique across all system claims.

## State Transitions (Claim Status)
1. **SUBMITTED** (Initial API call) -> **PROCESSING** (Automatically set)
2. **PROCESSING** -> **IN_REVIEW** (If hash and date validation pass via Celery)
3. **PROCESSING** -> **REJECTED** (If hash or date validation fail)
4. **IN_REVIEW** -> **APPROVED** (Manual action by SUPPORT with notes)
5. **IN_REVIEW** -> **REJECTED** (Manual action by SUPPORT with notes)
