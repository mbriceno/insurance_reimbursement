import pytest
from unittest.mock import MagicMock
from services.claim_service import ClaimService
from models.claim import Claim
from models.user import User

@pytest.mark.django_db
class TestClaimService:
    def test_submit_claim_success(self, monkeypatch):
        # Mock Repository
        mock_repo = MagicMock()
        mock_repo.create.return_value = MagicMock(id=1, status=Claim.Status.PROCESSING)
        
        # Mock Celery Task
        mock_task = MagicMock()
        monkeypatch.setattr("tasks.claim_tasks.validate_claim_task.delay", mock_task)
        
        service = ClaimService(mock_repo)
        
        user = MagicMock(spec=User)
        insurance = MagicMock()
        insurance.owner = user
        
        claim = service.submit_claim(
            user=user,
            insurance=insurance,
            invoice="invoice.pdf",
            invoice_date="2024-01-01",
            amount=100.00,
            date_of_event="2024-01-01"
        )
        
        assert claim.status == Claim.Status.PROCESSING
        assert mock_repo.create.called
        assert mock_task.called

    def test_submit_claim_permission_denied(self):
        mock_repo = MagicMock()
        service = ClaimService(mock_repo)
        
        user = MagicMock(spec=User)
        other_user = MagicMock(spec=User)
        insurance = MagicMock()
        insurance.owner = other_user
        
        with pytest.raises(PermissionError):
            service.submit_claim(
                user=user,
                insurance=insurance,
                invoice="invoice.pdf",
                invoice_date="2024-01-01",
                amount=100.00,
                date_of_event="2024-01-01"
            )
