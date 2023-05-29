# Generated by Django 4.1.6 on 2023-05-12 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0035_rename_behavioral_response_cycle_reproductive_cycle'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='light_type',
            field=models.CharField(blank=True, choices=[('led', 'Light-Emitting Diode (LED)'), ('hps', 'High pressure sodium vapor (HPS)'), ('cfl', 'Compact fluorescent (CFL)'), ('hid', 'High-intensity discharge (HID)'), ('cmh', 'Ceramic metal halide (CMH)')], default='led', max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='fixture',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]