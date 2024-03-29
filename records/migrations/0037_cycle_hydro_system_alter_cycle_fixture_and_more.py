# Generated by Django 4.1.6 on 2023-05-12 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0036_cycle_light_type_alter_cycle_fixture'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='hydro_system',
            field=models.CharField(blank=True, choices=[('dwc', 'Deep Water Culture (DWC)'), ('rdwc', 'Recirculating Deep Water Culture (RDWC)'), ('drip', 'Drip Irrigation'), ('rdrip', 'Recirculating Drip Irrigation (RDI)'), ('nft', 'Nutrient Film Technique (NFT)'), ('ebb_and_Flow', 'Ebb and Flow'), ('flood_and_drain', 'Flood and Drain'), ('aeroponics', 'Aeroponics'), ('aquaponics', 'Aquaponics'), ('kratky_method', 'Kratky Method'), ('vertical_farming', 'Vertical Farming')], max_length=37, null=True),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='fixture',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='genetics',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='light_type',
            field=models.CharField(choices=[('led', 'Light-Emitting Diode (LED)'), ('hps', 'High pressure sodium vapor (HPS)'), ('cfl', 'Compact fluorescent (CFL)'), ('hid', 'High-intensity discharge (HID)'), ('cmh', 'Ceramic metal halide (CMH)')], default='led', max_length=32),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='reproductive_cycle',
            field=models.CharField(choices=[('auto-flowering', 'Auto-flowering'), ('photoperiodic', 'Photoperiodic')], default='photoperiodic', max_length=30),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='seed_type',
            field=models.CharField(choices=[('regular', 'Regular'), ('feminized', 'Feminized'), ('clones', 'Clones')], default='feminized', max_length=30),
        ),
    ]
