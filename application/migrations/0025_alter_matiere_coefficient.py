# Generated by Django 5.1.3 on 2025-02-06 13:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "application",
            "0024_composition_devoir_moyennesemestre_notecomposition_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="matiere",
            name="coefficient",
            field=models.PositiveIntegerField(
                default=1,
                validators=[django.core.validators.MinValueValidator(1)],
                verbose_name="Coefficient",
            ),
        ),
    ]
