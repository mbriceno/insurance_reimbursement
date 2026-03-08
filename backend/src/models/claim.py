from django.db import models
from django.utils.translation import gettext_lazy as _
from .insurance import PetInsurance

class Claim(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', _('Submitted')
        PROCESSING = 'PROCESSING', _('Processing')
        IN_REVIEW = 'IN_REVIEW', _('In Review')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    insurance = models.ForeignKey(PetInsurance, on_delete=models.CASCADE, related_name='claims')
    invoice = models.FileField(upload_to='invoices/')
    invoice_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    review_notes = models.TextField(blank=True, null=True)
    date_of_event = models.DateField()
    file_hash = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Claim #{self.id} - {self.status}"
