from typing import List, Optional
from core.base.repository import BaseRepository
from models.pet import Pet
from models.user import User

class PetRepository(BaseRepository):
    model = Pet

    def get_by_owner(self, owner: User) -> List[Pet]:
        return self.filter(owner=owner)

    def create_for_owner(self, owner: User, **kwargs) -> Pet:
        return self.create(owner=owner, **kwargs)
