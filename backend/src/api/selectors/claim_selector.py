from api.models import Claim, User
from core.base.selector import BaseSelector
from django.db.models import QuerySet


class ClaimSelector(BaseSelector):
    model = Claim

    def get_queryset_for_user(self, user: User) -> QuerySet:
        if user.role == "ADMIN":
            return self.get_queryset()
        if user.role == "SUPPORT":
            return self.get_queryset().filter(status=Claim.Status.IN_REVIEW)
        # Customer sees only their claims
        return self.get_queryset().filter(insurance__owner=user)
