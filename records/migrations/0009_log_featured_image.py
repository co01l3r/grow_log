# Generated by Django 4.0.4 on 2023-02-06 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_alter_log_light_height_alter_log_light_power'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='featured_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
