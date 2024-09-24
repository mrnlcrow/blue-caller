# Generated by Django 5.1.1 on 2024-09-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_worker_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='certificate_file',
            field=models.FileField(blank=True, null=True, upload_to='certificates/'),
        ),
        migrations.AddField(
            model_name='worker',
            name='citizenship_image',
            field=models.ImageField(blank=True, null=True, upload_to='citizenship/'),
        ),
    ]
