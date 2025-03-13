import time
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
import uuid
from django.db import models
from django.db.models import Avg, Sum, F
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _ 


class Niveau(models.Model):
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom du Niveau")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    ordre = models.PositiveIntegerField(unique=True, verbose_name="Ordre d'affichage")

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['ordre']

    def __str__(self):
        return self.nom



class AnneeScolaire(models.Model):
    STATUTS = [
        ('En cours', _('En cours')),
        ('Clôturée', _('Clôturée')),
    ]

    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence de l'année scolaire")
    debut = models.DateField(verbose_name="Date de début")
    fin = models.DateField(verbose_name="Date de fin")
    statut = models.CharField(max_length=20, choices=STATUTS, default='En cours', verbose_name="Statut")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    # Champs pour les statistiques
    nombre_classes = models.PositiveIntegerField(default=0, verbose_name="Nombre de classes")
    nombre_eleves = models.PositiveIntegerField(default=0, verbose_name="Nombre d'élèves")
    nombre_professeurs = models.PositiveIntegerField(default=0, verbose_name="Nombre de professeurs")
    nombre_examens = models.PositiveIntegerField(default=0, verbose_name="Nombre d'examens")
    nombre_surveillants = models.PositiveIntegerField(default=0, verbose_name="Nombre de surveillants")

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"
        ordering = ['-debut']

    def __str__(self):
        return self.reference



import uuid
from django.db import models

class Salle(models.Model):
    """Représente une salle dans l'établissement scolaire"""

    TYPES_SALLE = [
        ('Salle de classe', 'Salle de classe'),
        ('Laboratoire', 'Laboratoire'),
        ('Salle informatique', 'Salle informatique'),
        ('Bibliothèque', 'Bibliothèque'),
        ('Salle des professeurs', 'Salle des professeurs'),
        ('Salle de réunion', 'Salle de réunion'),
        ('Amphithéâtre', 'Amphithéâtre'),
        ('Autre', 'Autre'),
    ]

    reference = models.CharField(
        max_length=20, 
        unique=True, 
        verbose_name="Référence de la salle",
       # 🔒 Rend le champ non modifiable dans les formulaires Django
    )
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la salle")
    type_salle = models.CharField(max_length=30, choices=TYPES_SALLE, default='Salle de classe', verbose_name="Type de salle")
    capacite = models.PositiveIntegerField(verbose_name="Capacité d'accueil")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def save(self, *args, **kwargs):
        """Génère une référence unique pour la salle si elle n'existe pas encore"""
        if not self.reference:
            self.reference = f"SAL-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.type_salle}) - Capacité: {self.capacite} élèves"




class Classe(models.Model):
    """Représente une classe dans un établissement scolaire"""
    
    
    reference = models.CharField(max_length=20, unique=True, verbose_name="Référence de la classe")
    nom = models.CharField(max_length=100, verbose_name="Nom de la classe")
    niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE, verbose_name="Niveau")
    annee_scolaire = models.ForeignKey(AnneeScolaire, on_delete=models.CASCADE, verbose_name="Année Scolaire")
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle attribuée")
    effectif = models.PositiveIntegerField(verbose_name="Effectif", default=0)

    def clean(self):
        """Validation : l'effectif ne peut pas dépasser la capacité de la salle"""
        if self.salle and self.effectif > self.salle.capacite:
            raise ValidationError(f"L'effectif ({self.effectif}) dépasse la capacité maximale de la salle ({self.salle.capacite}).")

    def save(self, *args, **kwargs):
        """Appel de la validation avant l'enregistrement"""
        self.clean()
        super().save(*args, **kwargs)
    
    
    def save(self, *args, **kwargs):
        """Génère une référence unique pour la Classe si elle n'existe pas encore"""
        if not self.reference:
            self.reference = f"SAL-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.niveau.nom}) - {self.annee_scolaire.reference}"




class Professeur(models.Model):
    SEXE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]

    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    specialite = models.CharField(max_length=100, verbose_name="Spécialité")
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    
    annee_scolaire = models.ForeignKey(
        'AnneeScolaire', 
        on_delete=models.CASCADE, 
        related_name="professeurs", 
        verbose_name="Année Scolaire"
    )

    image = models.ImageField(
        upload_to='professeurs/', 
        verbose_name="Photo du Professeur", 
        blank=True, 
        null=True
    )

    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Professeur"
        verbose_name_plural = "Professeurs"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.specialite}"

    def get_image_url(self):
        """ Retourne l'URL de l'image ou une image par défaut si absente """
        if self.image:
            return self.image.url
        return '/media/professeurs/default.jpg'  # Chemin de l'image par défaut

from django.db import models
from .models import AnneeScolaire

class Surveillant(models.Model):
    SEXE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]

    # Informations de base
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, verbose_name="Sexe")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(unique=True, verbose_name="Email")

    # Lien avec l'année scolaire
    annee_scolaire = models.ForeignKey(
        AnneeScolaire,
        on_delete=models.CASCADE,
        related_name="surveillants",
        verbose_name="Année Scolaire"
    )

    # Informations supplémentaires
    date_embauche = models.DateField(verbose_name="Date d'embauche")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Surveillant"
        verbose_name_plural = "Surveillants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom}"
from django.db import models
from django.utils.text import slugify

class Semestre(models.Model):
    NOM_SEMESTRES = [
        ('Semestre 1', 'Semestre 1'),
        ('Semestre 2', 'Semestre 2'),
    ]

    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence du semestre")
    nom = models.CharField(max_length=20, choices=NOM_SEMESTRES, verbose_name="Nom du semestre")
    annee_scolaire = models.ForeignKey('AnneeScolaire', on_delete=models.CASCADE, related_name='semestres')
    debut = models.DateField(verbose_name="Date de début du semestre")
    fin = models.DateField(verbose_name="Date de fin du semestre")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        unique_together = ('nom', 'annee_scolaire')  # Un même semestre ne peut pas être dupliqué dans une année scolaire
        ordering = ['-debut']

    
    def save(self, *args, **kwargs):
        # Générer la référence automatiquement si elle n'existe pas
        if not self.reference:
            self.reference = f"{self.nom}-{self.annee_scolaire.reference}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nom} ({self.annee_scolaire.reference})"

    
    
class Matiere(models.Model):
    reference = models.CharField(max_length=50, unique=True, verbose_name="Référence de la matière", blank=True)
    nom = models.CharField(max_length=100, unique=True, verbose_name="Nom de la matière")
    coefficient = models.PositiveIntegerField(default=1, verbose_name="Coefficient", validators=[MinValueValidator(1)])
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    image = models.ImageField(upload_to='Matieres/', verbose_name="Photo de la Matière", blank=True, null=True)

    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['nom']

    def save(self, *args, **kwargs):
        if not self.reference:
            last_matiere = Matiere.objects.order_by('-id').first()
            if last_matiere:
                last_id = int(last_matiere.reference.split('-')[-1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.reference = f"RF-M-{new_id:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} (Coeff: {self.coefficient})"




class Eleve(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    PAYEE_CHOICES = [
        ('P', 'Payée'),
    ]
    PLANP_CHOICES = [
        ('Mensuel', 'Mensuel'),
        ('Trimestriel', 'Trimestriel'),
        ('Semestriel', 'Semestriel'),
        ('Annuel', 'Annuel')
    ]

    date_inscription = models.DateTimeField(auto_now_add=True, verbose_name="Date d'inscription")
    annee_scolaire = models.ForeignKey('AnneeScolaire', on_delete=models.CASCADE, related_name='Eleve')
    matricule = models.CharField(max_length=20, unique=False, verbose_name="Matricule", blank=True)
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lieu de naissance")
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name='Eleve')
    adresse = models.CharField(max_length=200, blank=True, null=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    photo = models.ImageField(upload_to='eleves/', blank=True, null=True, verbose_name="Photo")
    frais_inscription = models.CharField(max_length=20, choices=PAYEE_CHOICES, verbose_name="Frais_inscription")
    paiement = models.CharField(max_length=20, choices=PLANP_CHOICES, verbose_name="Paiement")
    
         
    
    # Informations sur les parents
    nom_pere = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom du père")
    telephone_pere = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone du père")
    email_pere = models.EmailField(blank=True, null=True, verbose_name="Email du père")
    nom_mere = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom de la mère")
    telephone_mere = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone de la mère")
    email_mere = models.EmailField(blank=True, null=True, verbose_name="Email de la mère")
    
    # Autres informations complémentaires
  

    extrait_naissance = models.FileField(
        upload_to='eleves/extraits/',
        blank=True,
        null=True,
        verbose_name="Extrait de naissance"
    )
    
    APTITUDE_CHOICES = [
        ('Apt', 'Apt'),
        ('Inapte', 'Inapte'),
    ]
    etat_sante = models.CharField(max_length=100, blank=True, null=True, verbose_name="État de santé")
    aptitude = models.CharField(max_length=10, choices=APTITUDE_CHOICES, blank=True, null=True, verbose_name="Aptitude")
    
    groupe_sanguin = models.CharField(max_length=10, blank=True, null=True, verbose_name="Groupe sanguin")
    maladies_chroniques = models.TextField(blank=True, null=True, verbose_name="Maladies chroniques")
    traitements_en_cours = models.TextField(blank=True, null=True, verbose_name="Traitements en cours")
    commentaires_etat_general = models.TextField(blank=True, null=True, verbose_name="Commentaires sur l'état général")
    observations = models.TextField(blank=True, null=True, verbose_name="Observations")
    
       # Méthodes `save()` et `clean()` après les champs
    def clean(self):
        """ Vérifie l’unicité du matricule uniquement à la création. """
        if not self.pk and Eleve.objects.filter(matricule=self.matricule).exists():
            raise ValidationError({'matricule': "Un élève avec ce matricule existe déjà."})

    def save(self, *args, **kwargs):
        """ Génère un matricule unique seulement si vide. """
        if not self.matricule:
            annee_actuelle = now().year
            dernier_eleve = Eleve.objects.filter(matricule__startswith=f"M-{annee_actuelle}").order_by('-matricule').first()

            if dernier_eleve:
                dernier_numero = int(dernier_eleve.matricule.split('-')[-1]) + 1
            else:
                dernier_numero = 1

            self.matricule = f"M-{annee_actuelle}-{dernier_numero:02d}"

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"

        
        
     

def calculer_moyenne_eleve(eleve, semestre):
    matieres = Matiere.objects.all()
    total_points = 0
    total_coefficients = 0

    for matiere in matieres:
        notes_devoirs = NoteDevoir.objects.filter(eleve=eleve, devoir__matiere=matiere, devoir__semestre=semestre).aggregate(Avg('note'))['note__avg'] or 0
        note_composition = NoteComposition.objects.filter(eleve=eleve, composition__matiere=matiere, composition__semestre=semestre).aggregate(Avg('note'))['note__avg'] or 0

        moyenne_matiere = (notes_devoirs * 2 + note_composition * 3) / 5  # Composition compte plus que les devoirs
        total_points += moyenne_matiere * matiere.coefficient
        total_coefficients += matiere.coefficient

    if total_coefficients == 0:
        return 0

    return round(total_points / total_coefficients, 2)


def attribuer_moyennes_et_rangs(classe, semestre):
    eleves = Eleve.objects.filter(classe=classe)
    resultats = []

    for eleve in eleves:
        moyenne = calculer_moyenne_eleve(eleve, semestre)
        moy_obj, created = MoyenneSemestre.objects.update_or_create(
            eleve=eleve,
            semestre=semestre,
            defaults={'moyenne': moyenne}
        )
        resultats.append((eleve, moyenne))

    # Classement des élèves en fonction de la moyenne
    resultats = sorted(resultats, key=lambda x: x[1], reverse=True)
    rangs = {eleve.id: i + 1 for i, (eleve, _) in enumerate(resultats)}

    return rangs  # Retourne un dictionnaire avec l'ID de l'élève et son rang

     
def __str__(self):
    
    return f"{self.nom} {self.prenom}"


class Devoir(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="devoirs")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="devoirs")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="devoirs")
    date = models.DateField(verbose_name="Date du devoir")

    def __str__(self):
        return f"Devoir de {self.matiere} ({self.classe}) - {self.date}"


class Composition(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="compositions")
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="compositions")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="compositions")
    date = models.DateField(verbose_name="Date de la composition")

    def __str__(self):
        return f"Composition de {self.matiere} ({self.classe}) - {self.date}"


class NoteDevoir(models.Model):
    devoir = models.ForeignKey(Devoir, on_delete=models.CASCADE, related_name="notes")
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="notes_devoirs")
    note = models.FloatField(verbose_name="Note", help_text="Note sur 20")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['devoir', 'eleve'], name='unique_devoir_eleve')
        ]

    def __str__(self):
        return f"{self.eleve} - {self.devoir} : {self.note}"


class NoteComposition(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="notes_compositions")
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name="notes")
    note = models.FloatField(verbose_name="Note", help_text="Note sur 20")

    def __str__(self):
        return f"{self.eleve} - {self.composition} : {self.note}"


class MoyenneSemestre(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name="moyennes")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, related_name="moyennes")
    moyenne = models.FloatField(verbose_name="Moyenne du semestre", help_text="Moyenne sur 20")

    def __str__(self):
        return f"{self.eleve} - {self.semestre} : {self.moyenne}"


class Absence(models.Model):
    """Modèle pour gérer les absences des élèves"""
    
    CHOIX_JUSTIFICATION = [
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]

    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='absences', verbose_name="Élève")
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name='absences', verbose_name="Classe")
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE, related_name='absences', verbose_name="Matière")
    semestre = models.ForeignKey('Semestre', on_delete=models.CASCADE, related_name='absences', verbose_name="Semestre")
    annee_scolaire = models.ForeignKey('AnneeScolaire', on_delete=models.CASCADE, related_name='absences', verbose_name="Année Scolaire")
    date = models.DateField(verbose_name="Date de l'absence")
    duree = models.PositiveIntegerField(verbose_name="Durée (en heures)")
    justifiee = models.CharField(max_length=3, choices=CHOIX_JUSTIFICATION, default='Non', verbose_name="Absence justifiée")
    motif = models.TextField(blank=True, null=True, verbose_name="Motif")

    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"
        ordering = ['-date']

    def __str__(self):
        return f"Absence de {self.eleve.nom} {self.eleve.prenom} - {self.date}"


class Retard(models.Model):
    
    """Modèle pour gérer les retards des élèves"""
    CHOIX_JUSTIFICATION = [
        ('Oui', 'Oui'),
        ('Non', 'Non'),
    ]
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='retards', verbose_name="Élève")
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE, related_name='retards', verbose_name="Classe")
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE, related_name='retards', verbose_name="Matière")
    semestre = models.ForeignKey('Semestre', on_delete=models.CASCADE, related_name='retards', verbose_name="Semestre")
    annee_scolaire = models.ForeignKey('AnneeScolaire', on_delete=models.CASCADE, related_name='retards', verbose_name="Année Scolaire")
    date = models.DateField(verbose_name="Date du retard")
    heure_arrivee = models.TimeField(verbose_name="Heure d'arrivée")
    justifie = models.CharField(max_length=3, choices=CHOIX_JUSTIFICATION, default='Non', verbose_name="Retard justifié")
    raison = models.TextField(blank=True, null=True, verbose_name="Raison du retard")

    class Meta:
        verbose_name = "Retard"
        verbose_name_plural = "Retards"
        ordering = ['-date']

    def __str__(self):
        return f"Retard de {self.eleve.nom} {self.eleve.prenom} - {self.date} à {self.heure_arrivee}"




class Cours(models.Model):
    matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    professeur = models.ForeignKey('Professeur', on_delete=models.CASCADE)
    salle = models.ForeignKey('Salle', on_delete=models.CASCADE)
    date = models.DateField()  # Date du cours
    heure_debut = models.TimeField()  # Heure de début
    heure_fin = models.TimeField()  # Heure de fin
    classe = models.ForeignKey('Classe', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.matiere} - {self.enseignant} - {self.date} {self.heure_debut}-{self.heure_fin}"
    
    
    
    
    from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max

class Paiement(models.Model):
    STATUT_CHOICES = [
        ('P', 'Payé'),
        ('N', 'Non payé'),
        ('R', 'En retard'),
    ]

    reference = models.CharField(max_length=20, unique=True, verbose_name="Référence", editable=False)
    eleve = models.ForeignKey('Eleve', on_delete=models.CASCADE, related_name='paiements', verbose_name="Élève")
    date_paiement = models.DateField(verbose_name="Date de paiement", auto_now_add=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant payé")
    statut = models.CharField(max_length=1, choices=STATUT_CHOICES, default='N', verbose_name="Statut du paiement")
    plan_paiement = models.CharField(max_length=20, choices=Eleve.PLANP_CHOICES, verbose_name="Plan de paiement")
    mois_annee = models.CharField(max_length=7, verbose_name="Mois/Année concerné", help_text="Format : MM/YYYY")
    commentaires = models.TextField(blank=True, null=True, verbose_name="Commentaires")

    def clean(self):
        """ Vérifie que le montant est positif. """
        if self.montant <= 0:
            raise ValidationError({'montant': "Le montant doit être supérieur à zéro."})

    def save(self, *args, **kwargs):
        """ Génère la référence automatiquement avant de sauvegarder. """
        if not self.reference:
            # Récupère le dernier numéro de référence
            dernier_paiement = Paiement.objects.aggregate(Max('id'))['id__max']
            if dernier_paiement is None:
                dernier_paiement = 0
            # Génère la nouvelle référence
            self.reference = f"PAIEMENT-{dernier_paiement + 1:03d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Paiement de {self.eleve.nom} {self.eleve.prenom} - {self.reference}"