from typing import Type, TypeVar, Optional, List, Any
from django.db import models

T = TypeVar("T", bound=models.Model)

class BaseRepository:
    model: Type[T]

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def get(self, **kwargs) -> Optional[T]:
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def filter(self, **kwargs) -> List[T]:
        return list(self.model.objects.filter(**kwargs))

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()
