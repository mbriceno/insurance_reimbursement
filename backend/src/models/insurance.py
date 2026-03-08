from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User
from .pet import Pet
from datetime import timedelta

class BaseInsurance(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('Active')
        EXPIRED = 'EXPIRED', _('Expired')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='policies')
    coverage_start = models.DateField()
    coverage_end = models.DateField(editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.coverage_start and not self.coverage_end:
            self.coverage_end = self.coverage_start + timedelta(days=365)
        super().save(*args, **kwargs)

class PetInsurance(BaseInsurance):
    pet = models.OneToOneField(Pet, on_delete=models.CASCADE, related_name='insurance')

    def __str__(self):
        return f"Policy for {self.pet.name} ({self.status})"
