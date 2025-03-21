# Generated by Django 5.1.3 on 2025-02-03 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0008_salle"),
    ]

    operations = [
        migrations.CreateModel(
            name="Classe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "reference",
                    models.CharField(
                        max_length=20,
                        unique=True,
                        verbose_name="Référence de la classe",
                    ),
                ),
                (
                    "nom",
                    models.CharField(max_length=100, verbose_name="Nom de la classe"),
                ),
                (
                    "effectif",
                    models.PositiveIntegerField(default=0, verbose_name="Effectif"),
                ),
                (
                    "annee_scolaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.anneescolaire",
                        verbose_name="Année Scolaire",
                    ),
                ),
                (
                    "niveau",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="application.niveau",
                        verbose_name="Niveau",
                    ),
                ),
                (
                    "salle",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="application.salle",
                        verbose_name="Salle attribuée",
                    ),
                ),
            ],
        ),
    ]
