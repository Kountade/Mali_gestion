import uuid
from django.contrib import admin


from django.utils.html import format_html

from .models import AnneeScolaire, NoteDevoir,Semestre,Professeur,Matiere,Niveau,Paiement
from .forms import AnneeScolaireForm, PaiementForm

@admin.register(AnneeScolaire)
class AnneeScolaireAdmin(admin.ModelAdmin):
    form = AnneeScolaireForm
    list_display = ('reference', 'debut', 'fin', 'statut', 'nombre_classes', 'nombre_eleves', 'nombre_professeurs', 'nombre_examens', 'nombre_surveillants', 'date_creation')
    list_filter = ('statut', 'debut', 'fin')
    search_fields = ('reference',)
    ordering = ('-debut',)

    readonly_fields = ('nombre_classes', 'nombre_eleves', 'nombre_professeurs', 'nombre_examens', 'nombre_surveillants', 'date_creation')




@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'specialite', 'sexe', 'annee_scolaire', 'date_embauche', 'photo')
    list_filter = ('sexe', 'specialite', 'annee_scolaire')
    search_fields = ('nom', 'prenom', 'email', 'specialite')
    ordering = ('nom', 'prenom')

    # Affichage de l'image du professeur dans l'admin
    def photo(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />', obj.image.url)
        return "Pas d'image"
    
    photo.short_description = "Photo"

    fieldsets = (
        ("Informations personnelles", {
            'fields': ('nom', 'prenom', 'email', 'telephone', 'sexe', 'specialite', 'date_embauche', 'image')
        }),
        ("Informations académiques", {
            'fields': ('annee_scolaire',)
        }),
        ("Autres", {
            'fields': ('date_creation',),
            'classes': ('collapse',)  # Cache la date de création pour éviter toute modification
        }),
    )
    readonly_fields = ('date_creation',)  # Empêche la modification de la date de création



@admin.register(Semestre)
class SemestreAdmin(admin.ModelAdmin):
    list_display = ('nom', 'annee_scolaire', 'debut', 'fin')
    list_filter = ('annee_scolaire',)
    search_fields = ('nom', 'annee_scolaire__reference')
    
    
from django.contrib import admin
from .models import Matiere

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient', 'reference', 'date_creation', 'image_preview')
    search_fields = ('nom', 'reference')
    list_filter = ('coefficient',)
    readonly_fields = ('date_creation', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" style="border-radius: 5px;" />'
        return "Pas d'image"
    image_preview.allow_tags = True
    image_preview.short_description = "Aperçu de l'image"




@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre', 'date_creation')
    search_fields = ('nom',)
    list_filter = ('date_creation',)
    ordering = ('ordre',)


from django.contrib import admin
from .models import Salle

class SalleAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'type_salle', 'capacite')  # ✅ Affichage de la référence
    search_fields = ('nom', 'reference', 'type_salle')  # 🔍 Barre de recherche
    list_filter = ('type_salle',)  # 📌 Ajout de filtres
    readonly_fields = ('reference',)  # 🔒 Champ "reference" non modifiable

    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'nom', 'type_salle', 'capacite', 'description')
        }),
    )

admin.site.register(Salle, SalleAdmin)

from django.contrib import admin
from .models import Eleve

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'sexe', 'date_naissance', 'paiement', 'telephone', 'email')
    list_filter = ('sexe', 'paiement', 'date_inscription')
    search_fields = ('matricule', 'nom', 'prenom', 'telephone', 'email')
    ordering = ('nom', 'prenom')
    readonly_fields = ('date_inscription',)

    fieldsets = (
        ('Informations personnelles', {
            'fields': ('matricule', 'nom', 'prenom', 'date_naissance', 'lieu_naissance', 'sexe','annee_scolaire',  'classe', 'adresse', 'telephone', 'email', 'photo')
        }),
        ('Paiement & Inscription', {
            'fields': ('frais_inscription', 'paiement')
        }),
        ('Informations sur les parents', {
            'fields': ('nom_pere', 'telephone_pere', 'email_pere', 'nom_mere', 'telephone_mere', 'email_mere')
        }),
        ('Santé et Documents', {
            'fields': ('etat_sante', 'aptitude', 'groupe_sanguin', 'maladies_chroniques', 'traitements_en_cours', 'commentaires_etat_general', 'extrait_naissance')
        }),
        ('Autres informations', {
            'fields': ('observations', 'date_inscription')
        }),
    )




from django.contrib import admin
from django import forms
from .models import NoteDevoir, Devoir, Eleve

from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import NoteDevoir, Devoir, Eleve

class NoteDevoirForm(forms.ModelForm):
    class Meta:
        model = NoteDevoir
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Vérifie si un devoir est sélectionné
        if 'devoir' in self.data:
            try:
                devoir_id = int(self.data.get('devoir'))
                devoir = Devoir.objects.get(id=devoir_id)
                self.fields['eleve'].queryset = Eleve.objects.filter(classe=devoir.classe)
            except (ValueError, TypeError, Devoir.DoesNotExist):
                self.fields['eleve'].queryset = Eleve.objects.none()
        elif self.instance.pk:
            self.fields['eleve'].queryset = Eleve.objects.filter(classe=self.instance.devoir.classe)

class NoteDevoirAdmin(admin.ModelAdmin):
    form = NoteDevoirForm
    list_display = ('devoir', 'eleve', 'note')
    list_filter = ('devoir', 'eleve')
    search_fields = ('devoir__matiere__nom', 'eleve__nom')
    ordering = ('eleve',)

    def save_model(self, request, obj, form, change):
        """Empêche d'enregistrer plusieurs notes pour le même devoir et élève"""
        if not change and NoteDevoir.objects.filter(devoir=obj.devoir, eleve=obj.eleve).exists():
            raise ValidationError("Cet élève a déjà une note pour ce devoir.")
        super().save_model(request, obj, form, change)

admin.site.register(NoteDevoir, NoteDevoirAdmin)



from django.contrib import admin
from .models import Absence


@admin.register(Absence)
class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'classe', 'matiere', 'semestre', 'annee_scolaire', 'date', 'duree', 'justifiee')
    list_filter = ('semestre', 'annee_scolaire', 'classe', 'matiere', 'justifiee')
    search_fields = ('eleve__nom', 'eleve__prenom', 'classe__nom', 'matiere__nom')
    date_hierarchy = 'date'
    ordering = ['-date']


from django.contrib import admin
from .models import Classe

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'niveau', 'annee_scolaire', 'salle', 'effectif')
    list_filter = ('niveau', 'annee_scolaire', 'salle')
    search_fields = ('nom', 'reference')
    ordering = ('annee_scolaire', 'niveau', 'nom')
    fieldsets = (
        ('Informations Générales', {
            'fields': ('reference', 'nom', 'niveau', 'annee_scolaire')
        }),
        ('Détails', {
            'fields': ('salle', 'effectif'),
            'classes': ('collapse',)  # Permet de réduire cette section pour un affichage plus clair
        }),
    )
    readonly_fields = ('reference',)  # La référence est générée automatiquement

    def save_model(self, request, obj, form, change):
        """Génère automatiquement la référence si elle n'est pas définie"""
        if not obj.reference:
            obj.reference = f"SAL-{uuid.uuid4().hex[:6].upper()}"
        obj.save()






@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    form = PaiementForm
    list_display = ('eleve', 'montant', 'statut', 'date_paiement', 'mois_annee')
    list_filter = ('statut', 'plan_paiement')
    search_fields = ('eleve__nom', 'eleve__prenom', 'mois_annee')
    fieldsets = (
        ('Informations de base', {
            'fields': ('eleve', 'montant', 'statut', 'date_paiement')
        }),
        ('Détails du paiement', {
            'fields': ('plan_paiement', 'mois_annee', 'commentaires')
        }),
    )
    


from django.contrib import admin
from .models import Surveillant
from .forms import SurveillantForm

class SurveillantAdmin(admin.ModelAdmin):
    form = SurveillantForm
    list_display = ('nom', 'prenom', 'sexe', 'telephone', 'email', 'annee_scolaire', 'date_embauche')
    list_filter = ('sexe', 'annee_scolaire')
    search_fields = ('nom', 'prenom', 'email')
    ordering = ('nom', 'prenom')

admin.site.register(Surveillant, SurveillantAdmin)
