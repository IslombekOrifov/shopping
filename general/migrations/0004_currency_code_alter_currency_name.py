# Generated by Django 4.1.4 on 2022-12-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_alter_currency_price_alter_currency_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='code',
            field=models.CharField(default='USD', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]