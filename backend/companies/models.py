from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

from django.db import models

class Company(models.Model):
    BUSINESS_TYPE_CHOICES = [
        ('BA', 'Business activity'),
        ('LLC', 'Limited liability company'),
        ('JSC', 'Joint stock company'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    vat = models.BooleanField(default=False)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=12)
    company_type = models.CharField(max_length=3, choices=BUSINESS_TYPE_CHOICES, default='BA', verbose_name="Company Type")

    def clean(self):
        errors = {}

        if not self.name:
            errors['name'] = 'Name is required'
        elif Company.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            errors['name'] = 'Company with this name already exists'
        if self.tax_value < 0:
            errors['tax_value'] = 'Tax value cannot be negative'
        if self.company_type not in dict(self.BUSINESS_TYPE_CHOICES):
            errors['company_type'] = 'Invalid company type'

        if errors:
            raise ValidationError(errors)

