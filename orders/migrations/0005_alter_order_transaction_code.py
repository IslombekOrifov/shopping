# Generated by Django 4.1.4 on 2022-12-26 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_code',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
