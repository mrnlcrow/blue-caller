# Generated by Django 5.1.1 on 2024-11-18 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_worker_certificate_file_worker_citizenship_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='appointed',
            field=models.BooleanField(default=False),
        ),
    ]
