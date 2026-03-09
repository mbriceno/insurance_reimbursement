from typing import TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class BaseRepository:
    model: type[T]

    def create(self, **kwargs) -> T:
        return self.model.objects.create(**kwargs)

    def get(self, **kwargs) -> T | None:
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def filter(self, **kwargs) -> list[T]:
        return list(self.model.objects.filter(**kwargs))

    def update(self, instance: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        instance.delete()
