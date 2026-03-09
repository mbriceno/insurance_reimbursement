from api.models import Pet, PetInsurance, User
from core.base.repository import BaseRepository


class InsuranceRepository(BaseRepository):
    model = PetInsurance

    def get_by_owner(self, owner: User) -> list[PetInsurance]:
        return self.filter(owner=owner)

    def get_by_pet(self, pet: Pet) -> PetInsurance | None:
        return self.get(pet=pet)

    def create_policy(
        self, owner: User, pet: Pet, coverage_start, **kwargs,
    ) -> PetInsurance:
        return self.create(
            owner=owner, pet=pet, coverage_start=coverage_start, **kwargs,
        )
