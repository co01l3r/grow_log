# Generated by Django 4.0.4 on 2023-02-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0009_log_featured_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='water',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]