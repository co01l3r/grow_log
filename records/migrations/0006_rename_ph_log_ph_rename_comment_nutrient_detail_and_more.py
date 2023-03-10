# Generated by Django 4.0.4 on 2023-02-06 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0005_remove_log_phase_day'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='pH',
            new_name='ph',
        ),
        migrations.RenameField(
            model_name='nutrient',
            old_name='comment',
            new_name='detail',
        ),
        migrations.AlterField(
            model_name='log',
            name='cycle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='records.cycle'),
        ),
        migrations.AlterField(
            model_name='log',
            name='light_power',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
