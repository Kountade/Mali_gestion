# Generated by Django 5.1.3 on 2025-02-03 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0014_delete_classe_delete_salle"),
    ]

    operations = [
        migrations.CreateModel(
            name="Salle",
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
                        editable=False,
                        max_length=20,
                        unique=True,
                        verbose_name="Référence de la salle",
                    ),
                ),
                (
                    "nom",
                    models.CharField(
                        max_length=100, unique=True, verbose_name="Nom de la salle"
                    ),
                ),
                (
                    "type_salle",
                    models.CharField(
                        choices=[
                            ("Salle de classe", "Salle de classe"),
                            ("Laboratoire", "Laboratoire"),
                            ("Salle informatique", "Salle informatique"),
                            ("Bibliothèque", "Bibliothèque"),
                            ("Salle des professeurs", "Salle des professeurs"),
                            ("Salle de réunion", "Salle de réunion"),
                            ("Amphithéâtre", "Amphithéâtre"),
                            ("Autre", "Autre"),
                        ],
                        default="Salle de classe",
                        max_length=30,
                        verbose_name="Type de salle",
                    ),
                ),
                (
                    "capacite",
                    models.PositiveIntegerField(verbose_name="Capacité d'accueil"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
            ],
        ),
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
