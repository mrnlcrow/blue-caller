# Generated by Django 5.1.1 on 2024-09-24 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_customer_profile_pic_worker_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
