from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

class Pet(models.Model):
    class Species(models.TextChoices):
        DOG = 'DOG', _('Dog')
        CAT = 'CAT', _('Cat')
        OTHER = 'OTHER', _('Other')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=Species.choices)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.species})"
