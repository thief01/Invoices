from django.contrib import admin

import invoices.models

# Register your models here.

admin.site.register(invoices.models.CostInvoice)
admin.site.register(invoices.models.RevenueInvoice)
admin.site.register(invoices.models.InvoiceItem)