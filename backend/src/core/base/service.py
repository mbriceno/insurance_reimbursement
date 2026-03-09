from typing import Generic, TypeVar

from django.db import transaction

T = TypeVar("T")


class BaseService(Generic[T]):
    """
    Base service class for business logic.
    Provides transaction handling and common utilities.
    """

    @transaction.atomic
    def execute(self, *args, **kwargs) -> T:
        raise NotImplementedError("Service must implement execute method")
