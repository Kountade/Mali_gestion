# Generated by Django 5.1.3 on 2025-02-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("application", "0016_alter_salle_reference"),
    ]

    operations = [
        migrations.CreateModel(
            name="Eleve",
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
                    "date_inscription",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date d'inscription"
                    ),
                ),
                (
                    "matricule",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Matricule"
                    ),
                ),
                ("nom", models.CharField(max_length=100, verbose_name="Nom")),
                ("prenom", models.CharField(max_length=100, verbose_name="Prénom")),
                ("date_naissance", models.DateField(verbose_name="Date de naissance")),
                (
                    "lieu_naissance",
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name="Lieu de naissance",
                    ),
                ),
                (
                    "sexe",
                    models.CharField(
                        choices=[("M", "Masculin"), ("F", "Féminin")],
                        max_length=1,
                        verbose_name="Sexe",
                    ),
                ),
                (
                    "nationalite",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Nationalité"
                    ),
                ),
                (
                    "adresse",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Adresse"
                    ),
                ),
                (
                    "telephone",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="Téléphone"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="Email"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True, null=True, upload_to="eleves/", verbose_name="Photo"
                    ),
                ),
                (
                    "frais_inscription",
                    models.CharField(
                        choices=[("P", "Payee")],
                        max_length=20,
                        verbose_name="Frais_inscription",
                    ),
                ),
                (
                    "paiement",
                    models.CharField(
                        choices=[
                            ("Mensuel", "Mensuel"),
                            ("Trimestriel", "Trimestriel"),
                            ("Semestriel", "Semestriel"),
                            ("Annuel", "Annuel"),
                        ],
                        max_length=20,
                        verbose_name="Paiement",
                    ),
                ),
                (
                    "nom_pere",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Nom du père",
                    ),
                ),
                (
                    "telephone_pere",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Téléphone du père",
                    ),
                ),
                (
                    "email_pere",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Email du père",
                    ),
                ),
                (
                    "nom_mere",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Nom de la mère",
                    ),
                ),
                (
                    "telephone_mere",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Téléphone de la mère",
                    ),
                ),
                (
                    "email_mere",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        null=True,
                        verbose_name="Email de la mère",
                    ),
                ),
                (
                    "extrait_naissance",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="eleves/extraits/",
                        verbose_name="Extrait de naissance",
                    ),
                ),
                (
                    "etat_sante",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="État de santé",
                    ),
                ),
                (
                    "aptitude",
                    models.CharField(
                        blank=True,
                        choices=[("Apt", "Apt"), ("Inapte", "Inapte")],
                        max_length=10,
                        null=True,
                        verbose_name="Aptitude",
                    ),
                ),
                (
                    "groupe_sanguin",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Groupe sanguin",
                    ),
                ),
                (
                    "maladies_chroniques",
                    models.TextField(
                        blank=True, null=True, verbose_name="Maladies chroniques"
                    ),
                ),
                (
                    "traitements_en_cours",
                    models.TextField(
                        blank=True, null=True, verbose_name="Traitements en cours"
                    ),
                ),
                (
                    "commentaires_etat_general",
                    models.TextField(
                        blank=True,
                        null=True,
                        verbose_name="Commentaires sur l'état général",
                    ),
                ),
                (
                    "observations",
                    models.TextField(
                        blank=True, null=True, verbose_name="Observations"
                    ),
                ),
            ],
            options={
                "verbose_name": "Élève",
                "verbose_name_plural": "Élèves",
                "ordering": ["nom", "prenom"],
            },
        ),
    ]
