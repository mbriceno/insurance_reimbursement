from core.base.service import BaseService
from django.contrib.auth import get_user_model

User = get_user_model()


class UserService(BaseService):
    @staticmethod
    def create_user(
        email: str,
        password: str | None = None,
        role: str = User.Role.CUSTOMER,
        **extra_fields,
    ) -> User:
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            **extra_fields,
        )
        return user
