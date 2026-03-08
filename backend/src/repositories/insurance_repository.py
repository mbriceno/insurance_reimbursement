from typing import List, Optional
from core.base.repository import BaseRepository
from models.insurance import PetInsurance
from models.user import User
from models.pet import Pet

class InsuranceRepository(BaseRepository):
    model = PetInsurance

    def get_by_owner(self, owner: User) -> List[PetInsurance]:
        return self.filter(owner=owner)

    def get_by_pet(self, pet: Pet) -> Optional[PetInsurance]:
        return self.get(pet=pet)

    def create_policy(self, owner: User, pet: Pet, coverage_start, **kwargs) -> PetInsurance:
        return self.create(owner=owner, pet=pet, coverage_start=coverage_start, **kwargs)
