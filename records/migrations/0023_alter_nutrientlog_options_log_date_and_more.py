# Generated by Django 4.0.4 on 2023-03-15 15:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0022_alter_nutrient_nutrient_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nutrientlog',
            options={'ordering': ['nutrient__nutrient_type']},
        ),
        migrations.AddField(
            model_name='log',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cycle',
            name='beginning_phase',
            field=models.CharField(choices=[('seedling', 'Seedling'), ('vegetative', 'Vegetative')], default='vegetative', max_length=15),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='behavioral_response',
            field=models.CharField(blank=True, choices=[('auto-flowering', 'Auto-flowering'), ('photoperiodic', 'Photoperiodic')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='cycle',
            name='seed_type',
            field=models.CharField(blank=True, choices=[('regular', 'Regular'), ('feminized', 'Feminized'), ('clones', 'Clones')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='irrigation',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='nutrient',
            name='nutrient_type',
            field=models.CharField(blank=True, choices=[('medium_conditioner', 'Medium conditioner'), ('base_line', 'Base'), ('root_expander', 'Root expander'), ('bud_strengthener', 'Bud strengthener'), ('bud_enlarger', 'Bud enlarger'), ('bud_taste', 'Bud taste')], max_length=18, null=True),
        ),
    ]