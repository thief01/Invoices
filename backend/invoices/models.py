from django.core.validators import MinValueValidator
from django.db import models
from companies.models import Company
from decimal import Decimal
# Create your models here.


class BaseInvoice(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Szkic'),
        ('sent', 'Wysłana'),
        ('paid', 'Zapłacona'),
        ('overdue', 'Przeterminowana'),
        ('cancelled', 'Anulowana'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='%(class)s_set', verbose_name='Firma')
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name='Numer faktury')
    issue_date = models.DateField(verbose_name='Data wystawienia')
    due_date = models.DateField(verbose_name='Data płatności')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Status')

    net_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Kwota netto')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Kwota VAT')
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Kwota brutto')

    description = models.TextField(blank=True, verbose_name='Opis')
    notes = models.TextField(blank=True, verbose_name='Notatki')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data utworzenia')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data aktualizacji')

    def save(self, *args, **kwargs):
        self.gross_amount = self.net_amount + self.tax_amount
        if self.net_amount < 0 or self.tax_amount < 0 or self.gross_amount < 0:
            raise ValueError("Kwoty nie mogą być ujemne.")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created_at', "-issue_date"]
        verbose_name = 'Faktura'
        verbose_name_plural = 'Faktury'

class CostInvoice(BaseInvoice):
    """
    Model for cost invoices.
    """
    supplier_name = models.CharField(max_length=100, verbose_name='Nazwa dostawcy')
    supplier_tax_id = models.CharField(max_length=20, verbose_name='NIP dostawcy')
    supplier_address = models.CharField(max_length=255, verbose_name='Adres dostawcy')

    class Meta:
        verbose_name = 'Faktura kosztowa'
        verbose_name_plural = 'Faktury kosztowe'

    def __str__(self):
        return f'Faktura kosztowa {self.invoice_number} - {self.supplier_name}'

class RevenueInvoice(BaseInvoice):
    """
    Model for revenue invoices.
    """
    client_name = models.CharField(max_length=100, verbose_name='Nazwa klienta')
    client_tax_id = models.CharField(max_length=20, verbose_name='NIP klienta')
    client_address = models.CharField(max_length=255, verbose_name='Adres klienta')

    class Meta:
        verbose_name = 'Faktura przychodowa'
        verbose_name_plural = 'Faktury przychodowe'

    def __str__(self):
        return f'Faktura przychodowa {self.invoice_number} - {self.client_name}'

class InvoiceItem(models.Model):
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    invoice = GenericForeignKey('content_type', 'object_id')

    description = models.CharField(max_length=255, verbose_name='Opis')
    quantity = models.PositiveIntegerField(verbose_name='Ilość')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Cena jednostkowa')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Cena całkowita')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('23.00'), verbose_name='Stawka VAT')

    @property
    def net_amount(self):
        return self.quantity * self.unit_price

    @property
    def tax_amount(self):
        return self.net_amount * (self.tax_rate / Decimal('100'))

    @property
    def gross_amount(self):
        return self.net_amount + self.tax_amount

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price

        try:
            if hasattr(self.invoice, 'company') and hasattr(self.invoice.company, 'vat_payer'):
                if not self.invoice.company.vat_payer:
                    self.tax_rate = Decimal('0.00')
        except AttributeError:
            pass

        if self.quantity <= 0 or self.unit_price < 0:
            raise ValueError("Ilość musi być większa od 0, cena nie może być ujemna.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.description} - {self.quantity} x {self.unit_price} = {self.total_price}'

    class Meta:
        verbose_name = 'Pozycja faktury'
        verbose_name_plural = 'Pozycje faktur'