# Generated by Django 4.2.7 on 2023-11-19 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0010_alter_exercise_repetitions_alter_exercise_sets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='equipment_required',
            field=models.CharField(blank=True, default='None', max_length=50, null=True),
        ),
    ]