# Generated by Django 5.1.1 on 2024-12-15 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_workerrating_average_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='workerrating',
            name='worker',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='jobs.worker'),
            preserve_default=False,
        ),
    ]
