# Generated by Django 5.2.3 on 2025-06-30 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0009_fix_wrong_company_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='tin',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Tax Identification Number'),
        ),
    ]
