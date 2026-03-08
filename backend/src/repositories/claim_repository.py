from typing import List, Optional
from core.base.repository import BaseRepository
from models.claim import Claim
from models.insurance import PetInsurance

class ClaimRepository(BaseRepository):
    model = Claim

    def get_by_insurance(self, insurance: PetInsurance) -> List[Claim]:
        return self.filter(insurance=insurance)

    def get_by_status(self, status: str) -> List[Claim]:
        return self.filter(status=status)
