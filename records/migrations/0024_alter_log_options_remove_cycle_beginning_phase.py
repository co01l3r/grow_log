# Generated by Django 4.1.6 on 2023-03-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0023_alter_nutrientlog_options_log_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'ordering': [models.Case(models.When(phase='seedling', then=models.Value(1)), models.When(phase='vegetative', then=models.Value(2)), models.When(phase='bloom', then=models.Value(3))), 'date', 'id']},
        ),
        migrations.RemoveField(
            model_name='cycle',
            name='beginning_phase',
        ),
    ]