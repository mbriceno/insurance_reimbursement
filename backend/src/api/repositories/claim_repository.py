from api.models import Claim, PetInsurance
from core.base.repository import BaseRepository


class ClaimRepository(BaseRepository):
    model = Claim

    def get_by_insurance(self, insurance: PetInsurance) -> list[Claim]:
        return self.filter(insurance=insurance)

    def get_by_status(self, status: str) -> list[Claim]:
        return self.filter(status=status)
