# Generated by Django 4.0.4 on 2023-04-29 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0027_reservoir'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservoirLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('water', models.IntegerField()),
                ('waste_water', models.IntegerField(blank=True, null=True)),
                ('ro', models.BooleanField(choices=[('yes', 'Yes'), ('no', 'No'), ('mix', 'Mix')], default='yes', max_length=3)),
                ('status', models.CharField(choices=[('refresh', 'Refresh'), ('refill', 'Refill')], max_length=7)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservoir_logs', to='records.log')),
            ],
        ),
        migrations.DeleteModel(
            name='Reservoir',
        ),
    ]