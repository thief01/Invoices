from django.contrib.auth.models import User
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
    name = models.CharField(max_length=100)
    vat = models.BooleanField(default=False)
    tax_value = models.DecimalField(max_digits=10, decimal_places=2, default=12)
    company_type = models.CharField(max_length=3, choices=BUSINESS_TYPE_CHOICES, default='BA', verbose_name="Company Type")

