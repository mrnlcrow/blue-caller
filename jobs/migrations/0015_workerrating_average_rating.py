# Generated by Django 5.1.1 on 2024-12-15 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_remove_workerrating_appointment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerrating',
            name='average_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
