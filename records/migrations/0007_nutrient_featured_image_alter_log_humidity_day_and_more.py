# Generated by Django 4.0.4 on 2023-02-06 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_rename_ph_log_ph_rename_comment_nutrient_detail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutrient',
            name='featured_image',
            field=models.ImageField(blank=True, default='default_fertilizer.jpg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='log',
            name='humidity_day',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='humidity_night',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='irrigation',
            field=models.TextField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='light_height',
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='light_power',
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='nutrientlog',
            name='concentration',
            field=models.IntegerField(),
        ),
    ]