# Generated by Django 4.0.4 on 2023-05-01 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0031_rename_ro_reservoirlog_reverse_osmosis_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservoirlog',
            old_name='reverse_osmosis',
            new_name='ro',
        ),
    ]