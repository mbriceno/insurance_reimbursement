from core.base.selector import BaseSelector
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSelector(BaseSelector):
    @staticmethod
    def get_profile(user: User) -> User:
        # In simple cases, it just returns the user object.
        # Can be used to annotate or select_related in the future.
        return user
