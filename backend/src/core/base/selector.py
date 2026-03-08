from typing import List, TypeVar, Optional, Any
from django.db import models

T = TypeVar("T", bound=models.Model)

class BaseSelector:
    """
    Base selector class for optimized read queries.
    Focuses on retrieving data efficiently.
    """
    model: Type[T]

    def get_queryset(self) -> models.QuerySet:
        return self.model.objects.all()

    def list(self, filters: dict = None) -> List[T]:
        queryset = self.get_queryset()
        if filters:
            queryset = queryset.filter(**filters)
        return list(queryset)

    def get(self, **kwargs) -> Optional[T]:
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None
