import time

from api.models import Claim
from celery import shared_task


@shared_task
def validate_claim_task(claim_id: int) -> str:
    try:
        claim = Claim.objects.get(id=claim_id)

        # Validate coverage period
        insurance = claim.insurance
        if not (
            insurance.coverage_start
            <= claim.date_of_event
            <= insurance.coverage_end
        ):
            claim.status = Claim.Status.REJECTED
            claim.review_notes = (
                f"Event date {claim.date_of_event} outside "
                f"coverage period ({insurance.coverage_start} "
                f"to {insurance.coverage_end})."
            )
            claim.save()
            return "REJECTED: Outside coverage"

        # If all valid, transition to IN_REVIEW
        claim.status = Claim.Status.IN_REVIEW
        claim.save()

        # @TODO: Some logic to extract data from invoice, maybe implement
        # gemini API to extract data?
        # For now we implement a simple time to simulate this task
        # consume large time period
        time.sleep(30)

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
