from api.models import BaseInsurance, Pet, PetInsurance, User
from api.repositories.insurance_repository import InsuranceRepository
from core.base.service import BaseService


class PolicyService(BaseService):
    def __init__(self, insurance_repo: InsuranceRepository) -> None:
        self.insurance_repo = insurance_repo

    def create_pet_policy(
        self, user: User, pet: Pet, coverage_start, **kwargs,
    ) -> PetInsurance:
        # Business Rule: Coverage end is auto-calculated in model save,
        # but we can enforce or validate here if needed.
        # The model.save() handles the 365 days logic, so we just
        # delegate creation.

        # Check if pet already has active insurance
        existing_policy = self.insurance_repo.get(
            pet=pet, status=BaseInsurance.Status.ACTIVE,
        )
        if existing_policy:
            raise ValueError(f"Pet {pet.name} already has an active policy.")

        return self.insurance_repo.create_policy(
            owner=user, pet=pet, coverage_start=coverage_start, **kwargs,
        )
