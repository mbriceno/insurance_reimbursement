from typing import Optional
from core.base.service import BaseService
from models.claim import Claim
from models.insurance import PetInsurance
from models.user import User
from repositories.claim_repository import ClaimRepository

class ClaimService(BaseService):
    def __init__(self, claim_repo: ClaimRepository):
        self.claim_repo = claim_repo

    def submit_claim(self, user: User, insurance: PetInsurance, invoice, invoice_date, amount, date_of_event) -> Claim:
        if insurance.owner != user:
            raise PermissionError("User does not own this insurance policy.")

        claim = self.claim_repo.create(
            insurance=insurance,
            invoice=invoice,
            invoice_date=invoice_date,
            amount=amount,
            date_of_event=date_of_event,
            status=Claim.Status.PROCESSING
        )
        
        from tasks.claim_tasks import validate_claim_task
        validate_claim_task.delay(claim.id)
        
        return claim

    def override_claim_status(self, admin_user: User, claim: Claim, new_status: str, notes: str = None) -> Claim:
        if admin_user.role != User.Role.ADMIN:
            raise PermissionError("Only Admins can override claim status.")
        
        if new_status not in Claim.Status.values:
            raise ValueError(f"Invalid status: {new_status}")

        claim.status = new_status
        if notes:
            claim.review_notes = f"ADMIN OVERRIDE: {notes}"
        claim.save()
        return claim
