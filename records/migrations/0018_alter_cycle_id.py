# Generated by Django 4.1.6 on 2023-03-07 22:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0017_cycle_is_submitted_alter_cycle_beginning_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]