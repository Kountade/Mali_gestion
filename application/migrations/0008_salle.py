# Generated by Django 5.1.3 on 2025-02-03 11:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0007_niveau"),
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
                        max_length=20, unique=True, verbose_name="Référence de la salle"
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
    ]
