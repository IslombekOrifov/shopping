# Generated by Django 4.1.4 on 2023-01-08 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_order_options_order_slug_alter_order_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]
