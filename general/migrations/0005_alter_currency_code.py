# Generated by Django 4.1.4 on 2022-12-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_currency_code_alter_currency_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(max_length=4, unique=True),
        ),
    ]
