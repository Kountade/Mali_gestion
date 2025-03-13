from django import forms
from .models import Niveau

from django import forms
from .models import Niveau, Paiement

from django import forms
from django.utils.translation import gettext_lazy as _  # Ajoutez cette ligne
from .models import Niveau

class NiveauForm(forms.ModelForm):
    class Meta:
        model = Niveau
        fields = ['nom', 'description', 'ordre']
        labels = {
            'nom': _('Nom du Niveau'),  # Traduire le label
            'description': _('Description'),  # Traduire le label
            'ordre': _("Ordre d'affichage"),  # Traduire le label
        }
        help_texts = {
            'nom': _('Entrez le nom du niveau.'),  # Traduire le help_text
            'description': _('Entrez une description optionnelle.'),  # Traduire le help_text
            'ordre': _("Définissez l'ordre d'affichage du niveau."),  # Traduire le help_text
        }
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from .models import AnneeScolaire

class AnneeScolaireForm(forms.ModelForm):
    class Meta:
        model = AnneeScolaire
        fields = [
            'reference', 'debut', 'fin', 'statut', 'description',
            'nombre_classes', 'nombre_eleves', 'nombre_professeurs',
            'nombre_examens', 'nombre_surveillants'
        ]
        labels = {
            'reference': "Référence de l'année scolaire",
            'debut': "Date de début",
            'fin': "Date de fin",
            'statut': "Statut",
            'description': "Description",
            'nombre_classes': "Nombre de classes",
            'nombre_eleves': "Nombre d'élèves",
            'nombre_professeurs': "Nombre de professeurs",
            'nombre_examens': "Nombre d'examens",
            'nombre_surveillants': "Nombre de surveillants",
        }
        widgets = {
            'reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "EX: 2024-2025.",
                 # Rendre non modifiable
            }),
            'debut': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': "Sélectionnez la date de début de l'année scolaire.",
            }),
            'fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': "Sélectionnez la date de fin de l'année scolaire.",
            }),
            'statut': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': "Sélectionnez le statut de l'année scolaire.",
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': "Ajoutez une description optionnelle.",
            }),
            'nombre_classes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Entrez le nombre de classes pour cette année scolaire.",
                'readonly': 'readonly',  # Rendre non modifiable
            }),
            'nombre_eleves': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Entrez le nombre d'élèves pour cette année scolaire.",
                'readonly': 'readonly',  # Rendre non modifiable
            }),
            'nombre_professeurs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Entrez le nombre de professeurs pour cette année scolaire.",
                'readonly': 'readonly',  # Rendre non modifiable
            }),
            'nombre_examens': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Entrez le nombre d'examens prévus pour cette année scolaire.",
                'readonly': 'readonly',  # Rendre non modifiable
            }),
            'nombre_surveillants': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': "Entrez le nombre de surveillants pour cette année scolaire.",
                'readonly': 'readonly',  # Rendre non modifiable
            }),
        }
        help_texts = {
            'reference': "Entrez une référence unique pour l'année scolaire.",
            'debut': "Sélectionnez la date de début de l'année scolaire.",
            'fin': "Sélectionnez la date de fin de l'année scolaire.",
            'statut': "Sélectionnez le statut de l'année scolaire.",
            'description': "Ajoutez une description optionnelle.",
            'nombre_classes': "Entrez le nombre de classes pour cette année scolaire.",
            'nombre_eleves': "Entrez le nombre d'élèves pour cette année scolaire.",
            'nombre_professeurs': "Entrez le nombre de professeurs pour cette année scolaire.",
            'nombre_examens': "Entrez le nombre d'examens prévus pour cette année scolaire.",
            'nombre_surveillants': "Entrez le nombre de surveillants pour cette année scolaire.",
        }
from django import forms
from .models import Eleve

from django import forms
from .models import Eleve

class EleveInfoForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = [
            'nom', 'prenom', 'date_naissance', 'lieu_naissance', 'sexe',
            'classe', 'adresse', 'telephone', 'email', 'photo',
            'frais_inscription', 'paiement', 'annee_scolaire'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de l\'élève',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom de l\'élève',
            }),
            'date_naissance': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Sélectionnez la date de naissance',
            }),
            'lieu_naissance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le lieu de naissance',
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le sexe',
            }),
            'classe': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez la classe',
            }),
            'adresse': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'adresse de l\'élève',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le numéro de téléphone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'email de l\'élève',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'placeholder': 'Téléversez une photo de l\'élève',
            }),
            'frais_inscription': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez les frais d\'inscription',
            }),
            'paiement': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le plan de paiement',
            }),
            'annee_scolaire': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez l\'année scolaire',
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'date_naissance': 'Date de naissance',
            'lieu_naissance': 'Lieu de naissance',
            'sexe': 'Sexe',
            'classe': 'Classe',
            'adresse': 'Adresse',
            'telephone': 'Téléphone',
            'email': 'Email',
            'photo': 'Photo',
            'frais_inscription': 'Frais d\'inscription',
            'paiement': 'Plan de paiement',
            'annee_scolaire': 'Année Scolaire',
        }

from django import forms
from .models import Eleve

class ParentsInfoForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = [
            'nom_pere', 'telephone_pere', 'email_pere',
            'nom_mere', 'telephone_mere', 'email_mere'
        ]
        widgets = {
            'nom_pere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du père',
            }),
            'telephone_pere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le téléphone du père',
            }),
            'email_pere': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'email du père',
            }),
            'nom_mere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la mère',
            }),
            'telephone_mere': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le téléphone de la mère',
            }),
            'email_mere': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'email de la mère',
            }),
        }
        labels = {
            'nom_pere': 'Nom du père',
            'telephone_pere': 'Téléphone du père',
            'email_pere': 'Email du père',
            'nom_mere': 'Nom de la mère',
            'telephone_mere': 'Téléphone de la mère',
            'email_mere': 'Email de la mère',
        }


from django import forms
from .models import Eleve

class AutresInfoForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = [
            'extrait_naissance', 'etat_sante', 'aptitude', 'groupe_sanguin',
            'maladies_chroniques', 'traitements_en_cours',
            'commentaires_etat_general', 'observations'
        ]
        widgets = {
            'extrait_naissance': forms.ClearableFileInput(attrs={
                'accept': 'application/pdf',
                'class': 'form-control',
                'placeholder': 'Téléversez l\'extrait de naissance'
            }),
            'etat_sante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'état de santé'
            }),
            'aptitude': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'aptitude'
            }),
            'groupe_sanguin': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le groupe sanguin'
            }),
            'maladies_chroniques': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez les maladies chroniques',
                'rows': 3
            }),
            'traitements_en_cours': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez les traitements en cours',
                'rows': 3
            }),
            'commentaires_etat_general': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ajoutez des commentaires sur l\'état général',
                'rows': 3
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ajoutez des observations',
                'rows': 3
            }),
        }
        labels = {
            'extrait_naissance': 'Extrait de naissance',
            'etat_sante': 'État de santé',
            'aptitude': 'Aptitude',
            'groupe_sanguin': 'Groupe sanguin',
            'maladies_chroniques': 'Maladies chroniques',
            'traitements_en_cours': 'Traitements en cours',
            'commentaires_etat_general': 'Commentaires sur l\'état général',
            'observations': 'Observations',
        }


from django import forms
from .models import Professeur

class ProfesseurForm(forms.ModelForm):
    class Meta:
        model = Professeur
        fields = [
            'nom', 'prenom', 'email', 'telephone', 'sexe', 'specialite',
            'date_embauche', 'annee_scolaire', 'image'
        ]
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du professeur',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom du professeur',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'email du professeur',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le téléphone du professeur',
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le sexe',
            }),
            'specialite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la spécialité du professeur',
            }),
            'date_embauche': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Sélectionnez la date d\'embauche',
            }),
            'annee_scolaire': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez l\'année scolaire',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'placeholder': 'Téléversez une photo du professeur',
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'email': 'Email',
            'telephone': 'Téléphone',
            'sexe': 'Sexe',
            'specialite': 'Spécialité',
            'date_embauche': "Date d'embauche",
            'annee_scolaire': "Année Scolaire",
            'image': "Photo du Professeur",
        }
        help_texts = {
            'email': 'Entrez une adresse email unique.',
            'telephone': 'Entrez un numéro de téléphone valide.',
            'specialite': 'Entrez la spécialité du professeur.',
            'date_embauche': "Sélectionnez la date d'embauche du professeur.",
            'image': "Téléversez une photo du professeur (optionnel).",
        }
from django import forms
from django.core.validators import MinValueValidator
from .models import Matiere
from django import forms
from .models import Matiere

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'coefficient', 'description', 'image']
        labels = {
            'nom': 'Nom de la matière',
            'coefficient': 'Coefficient',
            'description': 'Description',
            'image': 'Photo de la matière',
        }
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom de la matière (ex: Mathématiques)',
            }),
            'coefficient': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le coefficient (ex: 3)',
                'min': 1,  # Validation côté client
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ajoutez une description optionnelle (ex: Cours de mathématiques avancées)',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        help_texts = {
            'nom': 'Entrez le nom de la matière (doit être unique).',
            'coefficient': 'Entrez un coefficient supérieur ou égal à 1.',
            'description': 'Ajoutez une description optionnelle.',
            'image': 'Téléversez une image représentative de la matière (optionnel).',
        }

from django import forms
from django.core.exceptions import ValidationError
from .models import Classe, Niveau, AnneeScolaire, Salle

from django import forms
from django.core.exceptions import ValidationError
from .models import Classe

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'niveau', 'annee_scolaire', 'salle', 'effectif']
        labels = {
            'nom': 'Nom de la classe',
            'niveau': 'Niveau',
            'annee_scolaire': 'Année scolaire',
            'salle': 'Salle attribuée',
            'effectif': 'Effectif',
        }
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 6ème A',
            }),
            'niveau': forms.Select(attrs={
                'class': 'form-control',
            }),
            'annee_scolaire': forms.Select(attrs={
                'class': 'form-control',
            }),
            'salle': forms.Select(attrs={
                'class': 'form-control',
            }),
            'effectif': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 30',
                'min': 0,  # Validation côté client
            }),
        }
        help_texts = {
            'nom': 'Entrez le nom de la classe (ex: 6ème A).',
            'niveau': 'Sélectionnez le niveau de la classe.',
            'annee_scolaire': 'Sélectionnez l\'année scolaire.',
            'salle': 'Sélectionnez la salle attribuée à cette classe (optionnel).',
            'effectif': 'Entrez le nombre d\'élèves dans la classe.',
        }

    def clean(self):
        """Validation personnalisée pour vérifier que l'effectif ne dépasse pas la capacité de la salle."""
        cleaned_data = super().clean()
        salle = cleaned_data.get('salle')
        effectif = cleaned_data.get('effectif')

        if salle and effectif and effectif > salle.capacite:
            raise ValidationError(
                f"L'effectif ({effectif}) dépasse la capacité maximale de la salle ({salle.capacite})."
            )

        return cleaned_data
    
from django import forms
from .models import Salle

from django import forms
from .models import Salle

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'type_salle', 'capacite', 'description']
        labels = {
            'nom': 'Nom de la salle',
            'type_salle': 'Type de salle',
            'capacite': 'Capacité d\'accueil',
            'description': 'Description',
        }
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ex: Salle A1'
            }),
            'type_salle': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Salle.TYPES_SALLE),
            'capacite': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 1, 
                'placeholder': 'Ex: 50'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ajoutez une description optionnelle...'
            }),
        }
        help_texts = {
            'nom': 'Entrez un nom unique pour la salle (ex: Salle A1).',
            'type_salle': 'Sélectionnez le type de salle.',
            'capacite': 'Entrez la capacité maximale d\'accueil de la salle.',
            'description': 'Ajoutez une description optionnelle de la salle.',
        }



from django import forms
from .models import Semestre

from django import forms
from .models import Semestre

class SemestreForm(forms.ModelForm):
    reference = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label="Référence du semestre"
    )

    class Meta:
        model = Semestre
        fields = ['reference', 'nom', 'annee_scolaire', 'debut', 'fin', 'description']
        labels = {
            'nom': 'Nom du semestre',
            'annee_scolaire': 'Année scolaire',
            'debut': 'Date de début du semestre',
            'fin': 'Date de fin du semestre',
            'description': 'Description',
        }
        widgets = {
            'nom': forms.Select(attrs={
                'class': 'form-control'
            }, choices=Semestre.NOM_SEMESTRES),
            'annee_scolaire': forms.Select(attrs={
                'class': 'form-control'
            }),
            'debut': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'fin': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Ajoutez une description optionnelle...'
            }),
        }
        help_texts = {
            'nom': 'Sélectionnez le nom du semestre (Semestre 1 ou Semestre 2).',
            'annee_scolaire': 'Sélectionnez l\'année scolaire associée.',
            'debut': 'Sélectionnez la date de début du semestre.',
            'fin': 'Sélectionnez la date de fin du semestre.',
            'description': 'Ajoutez une description optionnelle du semestre.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Générer la référence automatiquement si c'est un nouveau semestre
        if not self.instance.pk:
            nom = self.initial.get('nom', 'Semestre 1')  # Valeur par défaut
            annee_scolaire = self.initial.get('annee_scolaire')
            if annee_scolaire:
                self.initial['reference'] = f"{nom}-{annee_scolaire.reference}"


from django import forms
from .models import Devoir, Semestre, Matiere, Classe
from django import forms
from .models import Devoir

class DevoirForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = ['semestre', 'matiere', 'classe', 'date']
        labels = {
            'semestre': 'Semestre',
            'matiere': 'Matière',
            'classe': 'Classe',
            'date': 'Date du devoir',
        }
        widgets = {
            'semestre': forms.Select(attrs={
                'class': 'form-control',
            }),
            'matiere': forms.Select(attrs={
                'class': 'form-control',
            }),
            'classe': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'placeholder': 'Sélectionnez une date'
            }),
        }
        help_texts = {
            'semestre': 'Sélectionnez le semestre associé au devoir.',
            'matiere': 'Sélectionnez la matière du devoir.',
            'classe': 'Sélectionnez la classe concernée par le devoir.',
            'date': 'Sélectionnez la date du devoir.',
        }


from django import forms
from .models import Composition, Semestre, Matiere, Classe
from django import forms
from .models import Composition

class CompositionForm(forms.ModelForm):
    class Meta:
        model = Composition
        fields = ['semestre', 'matiere', 'classe', 'date']
        labels = {
            'semestre': 'Semestre',
            'matiere': 'Matière',
            'classe': 'Classe',
            'date': 'Date de la composition',
        }
        widgets = {
            'semestre': forms.Select(attrs={
                'class': 'form-control',
            }),
            'matiere': forms.Select(attrs={
                'class': 'form-control',
            }),
            'classe': forms.Select(attrs={
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date',
                'placeholder': 'Sélectionnez une date'
            }),
        }
        help_texts = {
            'semestre': 'Sélectionnez le semestre associé à la composition.',
            'matiere': 'Sélectionnez la matière de la composition.',
            'classe': 'Sélectionnez la classe concernée par la composition.',
            'date': 'Sélectionnez la date de la composition.',
        }
        

from django import forms
from .models import NoteDevoir, Devoir, Eleve
from django import forms
from .models import NoteDevoir


from django import forms
from .models import NoteDevoir
class NoteDevoirForm(forms.ModelForm):
    class Meta:
        model = NoteDevoir
        fields = ['devoir', 'eleve', 'note']
        widgets = {
            'devoir': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez un devoir',
                'id': 'id_devoir',  # Ajouter un ID pour le champ devoir
            }),
            'eleve': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez un élève',
                'id': 'id_eleve',  # Ajouter un ID pour le champ élève
            }),
            'note': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez la note sur 20',
                'min': 0,
                'max': 20,
                'step': 0.5
            }),
        }
        labels = {
            'devoir': 'Devoir',
            'eleve': 'Élève',
            'note': 'Note',
        }
        help_texts = {
            'note': 'La note doit être comprise entre 0 et 20.',
        }
from django import forms
from .models import NoteComposition, Eleve, Composition
from django import forms
from .models import NoteComposition

class NoteCompositionForm(forms.ModelForm):
    class Meta:
        model = NoteComposition
        fields = ['eleve', 'composition', 'note']
        labels = {
            'eleve': 'Élève',
            'composition': 'Composition',
            'note': 'Note',
        }
        widgets = {
            'eleve': forms.Select(attrs={
                'class': 'form-control',
            }),
            'composition': forms.Select(attrs={
                'class': 'form-control',
            }),
            'note': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0, 
                'max': 20, 
                'step': 0.5,
                'placeholder': 'Ex: 14.5'
            }),
        }
        help_texts = {
            'eleve': 'Sélectionnez l\'élève concerné.',
            'composition': 'Sélectionnez la composition associée.',
            'note': 'Entrez la note sur 20 (ex: 14.5).',
        }

from django import forms
from .models import Absence, Eleve, Classe, Matiere, Semestre, AnneeScolaire
from django import forms
from .models import Absence


from django import forms
from .models import Absence
from django import forms
from .models import Absence, Eleve, Classe, Matiere, Semestre, AnneeScolaire

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = '__all__'
        widgets = {
            'annee_scolaire': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'semestre': forms.Select(attrs={'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'duree': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'justifiee': forms.Select(choices=Absence.CHOIX_JUSTIFICATION, attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrer l'année scolaire pour ne sélectionner que celle avec le statut "En cours"
        self.fields['annee_scolaire'].queryset = AnneeScolaire.objects.filter(statut='En cours')
        
        # Si une année scolaire est sélectionnée, filtrer les classes correspondantes
        if 'annee_scolaire' in self.data:
            try:
                annee_id = int(self.data.get('annee_scolaire'))
                self.fields['classe'].queryset = Classe.objects.filter(annee_scolaire_id=annee_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['classe'].queryset = self.instance.annee_scolaire.classe_set.all()
        
        # Si une classe est sélectionnée, filtrer les élèves correspondants
        if 'classe' in self.data:
            try:
                classe_id = int(self.data.get('classe'))
                self.fields['eleve'].queryset = Eleve.objects.filter(classe_id=classe_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['eleve'].queryset = self.instance.classe.eleve_set.all()

from django import forms
from .models import Retard, Eleve, Classe, Matiere, Semestre, AnneeScolaire
from django import forms
from .models import Retard


class RetardForm(forms.ModelForm):
    class Meta:
        model = Retard
        fields = [
            'eleve', 'classe', 'matiere', 'semestre', 'annee_scolaire',
            'date', 'heure_arrivee', 'justifie', 'raison'
        ]
        labels = {
            'eleve': 'Élève',
            'classe': 'Classe',
            'matiere': 'Matière',
            'semestre': 'Semestre',
            'annee_scolaire': 'Année Scolaire',
            'date': "Date du retard",
            'heure_arrivee': "Heure d'arrivée",
            'justifie': 'Retard justifié',
            'raison': 'Raison du retard',
        }
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'semestre': forms.Select(attrs={'class': 'form-control'}),
            'annee_scolaire': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Sélectionnez une date'
            }),
            'heure_arrivee': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control',
                'placeholder': "Ex: 08:15"
            }),
            'justifie': forms.Select(attrs={'class': 'form-control'}),
            'raison': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Ex: Problème de transport, panne, etc.'
            }),
        }
        help_texts = {
            'eleve': 'Sélectionnez l\'élève concerné.',
            'classe': 'Sélectionnez la classe de l\'élève.',
            'matiere': 'Sélectionnez la matière concernée.',
            'semestre': 'Sélectionnez le semestre concerné.',
            'annee_scolaire': 'Sélectionnez l\'année scolaire concernée.',
            'date': "Sélectionnez la date du retard.",
            'heure_arrivee': "Sélectionnez l'heure d'arrivée de l'élève.",
            'justifie': 'Indiquez si le retard est justifié.',
            'raison': 'Ajoutez une raison optionnelle pour le retard.',
        }

from django import forms
from .models import Cours, Matiere, Professeur, Salle, Classe
from django import forms
from .models import Cours

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = [
            'matiere', 'professeur', 'salle', 'date', 'heure_debut', 'heure_fin', 'classe'
        ]
        labels = {
            'matiere': 'Matière',
            'professeur': 'Professeur',
            'salle': 'Salle',
            'date': 'Date du cours',
            'heure_debut': 'Heure de début',
            'heure_fin': 'Heure de fin',
            'classe': 'Classe',
        }
        widgets = {
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'professeur': forms.Select(attrs={'class': 'form-control'}),
            'salle': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Sélectionnez une date'
            }),
            'heure_debut': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control',
                'placeholder': "Ex: 08:00"
            }),
            'heure_fin': forms.TimeInput(attrs={
                'type': 'time', 
                'class': 'form-control',
                'placeholder': "Ex: 10:00"
            }),
            'classe': forms.Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'matiere': 'Sélectionnez la matière du cours.',
            'professeur': 'Sélectionnez le professeur responsable.',
            'salle': 'Sélectionnez la salle où se déroule le cours.',
            'date': 'Sélectionnez la date du cours.',
            'heure_debut': 'Sélectionnez l\'heure de début du cours.',
            'heure_fin': 'Sélectionnez l\'heure de fin du cours.',
            'classe': 'Sélectionnez la classe concernée.',
        }




from django import forms
from .models import Paiement

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        exclude = ['reference']  # Exclure le champ référence
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'JJ/MM/AAAA'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant payé'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'plan_paiement': forms.Select(attrs={'class': 'form-control'}),
            'mois_annee': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}),
            'commentaires': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Commentaires sur le paiement'}),
        }

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant <= 0:
            raise ValidationError("Le montant doit être supérieur à zéro.")
        return montant
    
    
    



from django import forms
from .models import Surveillant

class SurveillantForm(forms.ModelForm):
    class Meta:
        model = Surveillant
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom du surveillant',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom du surveillant',
            }),
            'sexe': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le sexe',
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le numéro de téléphone',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez l\'adresse email',
            }),
            'annee_scolaire': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez l\'année scolaire',
            }),
            'date_embauche': forms.DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY-MM-DD',
                'type': 'date',  # Pour afficher un sélecteur de date
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap et des placeholders supplémentaires si nécessaire
        for field_name, field in self.fields.items():
            if 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
            if 'placeholder' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['placeholder'] = f'Entrez {field.label.lower()}'
                
                





















from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Entrez une adresse email valide.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}),
    )

    class Meta:
        model = User
        fields = ['username', 'password']





from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']