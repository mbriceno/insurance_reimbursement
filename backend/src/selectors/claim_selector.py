from typing import List, Optional, Union
from django.db.models import QuerySet
from core.base.selector import BaseSelector
from models.claim import Claim
from models.user import User

class ClaimSelector(BaseSelector):
    model = Claim

    def get_queryset_for_user(self, user: User) -> QuerySet:
        if user.role == 'ADMIN':
            return self.get_queryset()
        elif user.role == 'SUPPORT':
            return self.get_queryset().filter(status=Claim.Status.IN_REVIEW)
        else:
            # Customer sees only their claims
            return self.get_queryset().filter(insurance__owner=user)
