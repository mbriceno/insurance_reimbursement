from api.models import Pet, User
from core.base.repository import BaseRepository


class PetRepository(BaseRepository):
    model = Pet

    def get_by_owner(self, owner: User) -> list[Pet]:
        return self.filter(owner=owner)

    def create_for_owner(self, owner: User, **kwargs) -> Pet:
        return self.create(owner=owner, **kwargs)
