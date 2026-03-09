import hashlib

from api.models import Claim
from celery import shared_task


@shared_task
def validate_claim_task(claim_id: int) -> str:
    try:
        claim = Claim.objects.get(id=claim_id)

        # 1. Generate file hash
        hasher = hashlib.sha256()
        # Read file chunks to handle large files efficiently
        for chunk in claim.invoice.chunks():
            hasher.update(chunk)
        file_hash = hasher.hexdigest()

        claim.file_hash = file_hash

        # 2. Check for duplicate hash
        # Exclude self from query
        if (
            Claim.objects.filter(file_hash=file_hash)
            .exclude(id=claim.id)
            .exists()
        ):
            claim.status = Claim.Status.REJECTED
            claim.review_notes = "Duplicate invoice upload detected."
            claim.save()
            return "REJECTED: Duplicate claim invoice"

        # 3. Validate coverage period
        insurance = claim.insurance
        if not (
            insurance.coverage_start
            <= claim.date_of_event
            <= insurance.coverage_end
        ):
            claim.status = Claim.Status.REJECTED
            claim.review_notes = f"Event date {claim.date_of_event} outside coverage period ({insurance.coverage_start} to {insurance.coverage_end})."
            claim.save()
            return "REJECTED: Outside coverage"

        # 4. If all valid, transition to IN_REVIEW
        claim.status = Claim.Status.IN_REVIEW
        claim.save()
        return "IN_REVIEW: Validated"

    except Claim.DoesNotExist:
        return f"Claim {claim_id} not found"
    except Exception as e:
        # Handle unexpected errors, maybe mark as REJECTED or leave as PROCESSING for retry?
        # For now, let's log and re-raise or mark as PROCESSING with error note?
        if "claim" in locals():
            claim.review_notes = f"System Error during validation: {e!s}"
            # Maybe keep processing or manual intervention needed?
            # Let's fail safe to REJECTED or PROCESSING?
            # Spec says "Transition status to IN_REVIEW if valid, otherwise REJECTED."
            # System error is not strictly invalid data, but let's fail it for safety.
            claim.status = Claim.Status.REJECTED
            claim.save()
        return f"ERROR: {e!s}"
