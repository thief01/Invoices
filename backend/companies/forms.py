from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    class Meta:
        model =Company
        fields = ['name', 'tin', 'vat', 'tax_value', 'company_type']