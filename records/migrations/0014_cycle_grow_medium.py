# Generated by Django 4.0.4 on 2023-02-20 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0013_alter_cycle_fixture_alter_cycle_genetics'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='grow_medium',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
