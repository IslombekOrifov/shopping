# Generated by Django 4.2 on 2025-05-06 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
        ('accounts', '0002_customuser_company_customuser_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='general.currency'),
        ),
    ]
