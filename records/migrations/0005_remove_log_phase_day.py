# Generated by Django 4.0.4 on 2023-02-06 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_log_phase_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='phase_day',
        ),
    ]
