# Generated by Django 4.1.4 on 2023-01-03 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0008_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='summary_for_message',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]