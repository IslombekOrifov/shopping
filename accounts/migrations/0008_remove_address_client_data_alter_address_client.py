# Generated by Django 4.1.4 on 2023-01-22 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='client_data',
        ),
        migrations.AlterField(
            model_name='address',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]