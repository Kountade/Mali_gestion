import uuid

from django.db.models import Avg,F
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import AnneeScolaire
from .forms import AnneeScolaireForm, CustomUserCreationForm,ProfesseurForm
from formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect
from .forms import EleveInfoForm, ParentsInfoForm, AutresInfoForm
from .models import Eleve
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from .models import Eleve, Semestre, Matiere, NoteDevoir, NoteComposition
from django.contrib import messages
from .models import AnneeScolaire,Professeur
from .forms import AnneeScolaireForm
# Create your views here.
from django.shortcuts import render
from .models import AnneeScolaire, Eleve, Professeur, Classe, Surveillant

from django.db.models import Avg
from .models import Eleve, AnneeScolaire, Paiement, Professeur, Classe, Surveillant, Matiere, NoteDevoir, NoteComposition
from django.db.models import Count, Q
from django.shortcuts import render
from .models import Eleve, Niveau, AnneeScolaire, Paiement, Professeur

from django.utils.translation import activate
from django.shortcuts import redirect
from django.urls import reverse

from django.shortcuts import render
# application/views.py
from django.shortcuts import redirect
from django.utils.translation import activate
from django.urls import reverse

def set_language(request):
    """
    Vue personnalisée pour changer la langue et rediriger vers la page d'accueil.
    """
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            activate(language)  # Activer la langue sélectionnée
            request.session['django_language'] = language  # Sauvegarder la langue dans la session
    return redirect('home')  # Rediriger vers la page d'accueil
def custom_404_view(request, exception):
    """
    Vue personnalisée pour la page 404.
    """
    return render(request, '404.html', status=404)

def home(request):
    # Récupérer toutes les années scolaires pour le filtre
    annees_scolaires = AnneeScolaire.objects.all()

    # Récupérer l'année scolaire sélectionnée (par défaut, la première)
    annee_scolaire_id = request.GET.get('annee_scolaire')
    annee_scolaire = None
    if annee_scolaire_id:
        annee_scolaire = AnneeScolaire.objects.get(id=annee_scolaire_id)
    else:
        annee_scolaire = annees_scolaires.first()

    # Calculer les statistiques pour l'année scolaire sélectionnée
    eleves = Eleve.objects.filter(classe__annee_scolaire=annee_scolaire)
    nombre_eleves = eleves.count()
    nombre_hommes = eleves.filter(sexe='M').count()
    nombre_femmes = eleves.filter(sexe='F').count()

    # Calculer les pourcentages
    pourcentage_hommes = (nombre_hommes / nombre_eleves) * 100 if nombre_eleves > 0 else 0
    pourcentage_femmes = (nombre_femmes / nombre_eleves) * 100 if nombre_eleves > 0 else 0

    # Calculer le nombre et le pourcentage d'élèves par niveau
    niveaux = Niveau.objects.annotate(
        nombre_eleves=Count('classe__Eleve', filter=Q(classe__annee_scolaire=annee_scolaire))
    ).filter(nombre_eleves__gt=0)

    total_eleves_niveaux = sum(niveau.nombre_eleves for niveau in niveaux)
    for niveau in niveaux:
        niveau.pourcentage = (niveau.nombre_eleves / total_eleves_niveaux) * 100 if total_eleves_niveaux > 0 else 0

    # Récupérer les 10 derniers paiements
    derniers_paiements = Paiement.objects.select_related('eleve').order_by('-date_paiement')[:10]

    # Récupérer les 6 meilleurs élèves de l'année scolaire sélectionnée
    resultats = []
    for eleve in eleves:
        moyenne = calculer_moyenne_eleve(eleve, semestre=1)  # Semestre 1 par défaut
        resultats.append((eleve, moyenne))

    # Classer les élèves par moyenne décroissante
    resultats = sorted(resultats, key=lambda x: x[1], reverse=True)
    meilleurs_eleves = [eleve for eleve, _ in resultats[:6]]  # Prendre les 6 premiers

    # Récupérer les professeurs les plus anciens (triés par date_embauche)
    professeurs_anciens = Professeur.objects.filter(annee_scolaire=annee_scolaire).order_by('date_embauche')[:6]

    # Ajout des statistiques manquantes
    nombre_professeurs = Professeur.objects.filter(annee_scolaire=annee_scolaire).count()
    nombre_classes = Classe.objects.filter(annee_scolaire=annee_scolaire).count()
    nombre_surveillants = Surveillant.objects.filter(annee_scolaire=annee_scolaire).count()

    context = {
        'annees_scolaires': annees_scolaires,
        'annee_scolaire': annee_scolaire,
        'nombre_eleves': nombre_eleves,
        'nombre_hommes': nombre_hommes,
        'nombre_femmes': nombre_femmes,
        'pourcentage_hommes': pourcentage_hommes,
        'pourcentage_femmes': pourcentage_femmes,
        'niveaux': niveaux,  # Ajout des niveaux avec leurs statistiques
        'total_eleves_niveaux': total_eleves_niveaux,  # Total des élèves par niveau
        'derniers_paiements': derniers_paiements,
        'meilleurs_eleves': meilleurs_eleves,
        'professeurs_anciens': professeurs_anciens,
        'nombre_professeurs': nombre_professeurs,  # Nombre de professeurs
        'nombre_classes': nombre_classes,  # Nombre de classes
        'nombre_surveillants': nombre_surveillants,  # Nombre de surveillants
    }

    return render(request, 'index.html', context)



def liste_annees_scolaires(request):
    search_query = request.GET.get('search', '')
    filter_status = request.GET.get('filter_status', '')

    annees = AnneeScolaire.objects.all()

    if search_query:
        annees = annees.filter(reference__icontains=search_query)

    if filter_status:
        annees = annees.filter(statut=filter_status)

    return render(request, 'annees_scolaires/liste.html', {'annees': annees})


# 📌 Détail d'une année scolairefrom django.shortcuts import render, get_object_or_404
from .models import AnneeScolaire, Classe, Professeur, Salle

def detail_annee_scolaire(request, annee_scolaire_id):
    annee_scolaire = get_object_or_404(AnneeScolaire, id=annee_scolaire_id)
    classes = Classe.objects.filter(annee_scolaire=annee_scolaire)
    professeurs = Professeur.objects.filter(annee_scolaire=annee_scolaire)
    salles = Salle.objects.all()  # Ou filtrer selon vos besoins

    context = {
        'annee_scolaire': annee_scolaire,
        'classes': classes,
        'professeurs': professeurs,
        'salles': salles,
    }

    return render(request, 'annees_scolaires/detail_annee_scolaire.html', context)

# 📌 Création d'une année scolaire avec message de confirmation
def creer_annee_scolaire(request):
    if request.method == 'POST':
        form = AnneeScolaireForm(request.POST)
        if form.is_valid():
            annee = form.save()  # Récupération de l'objet sauvegardé
            messages.success(request, f"✅ Année scolaire {annee.reference} ajoutée avec succès !")
            return redirect('liste_annees_scolaires')
        else:
            messages.error(request, "❌ Une erreur est survenue. Veuillez vérifier le formulaire.")
    else:
        form = AnneeScolaireForm()
    
    return render(request, 'annees_scolaires/ajouter_année.html', {'form': form, 'titre': "Créer une année scolaire"})


# 📌 Mise à jour d'une année scolaire avec message
def modifier_annee_scolaire(request, pk):
    annee = get_object_or_404(AnneeScolaire, pk=pk)
    if request.method == 'POST':
        form = AnneeScolaireForm(request.POST, instance=annee)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Année scolaire mise à jour avec succès !")
            return redirect('liste_annees_scolaires')
        else:
            messages.error(request, "❌ Une erreur est survenue lors de la mise à jour.")
    else:
        form = AnneeScolaireForm(instance=annee)
    
    return render(request, 'annees_scolaires/form.html', {'form': form, 'titre': "Modifier une année scolaire"})


# 📌 Suppression d'une année scolaire avec message
def supprimer_annee_scolaire(request, pk):
    annee = get_object_or_404(AnneeScolaire, pk=pk)
    if request.method == 'POST':
        reference = annee.reference  # Sauvegarder la référence avant suppression
        annee.delete()
        messages.success(request, f"✅ Année scolaire {reference} supprimée avec succès !")
        return redirect('liste_annees_scolaires')
    else:
        messages.warning(request, "⚠️ Vous êtes sur le point de supprimer une année scolaire.")

    return render(request, 'annees_scolaires/confirmer_suppression.html', {'annee': annee})

#<img src="{{ professeur.image.url }}" alt="Photo de {{ professeur.nom }}" class="img-thumbnail" width="150">


def professeur_list(request):
    query = request.GET.get("q", "")  # Récupérer la recherche par nom
    specialite_filter = request.GET.get("specialite", "")  # Récupérer le filtre de spécialité
    
    professeurs = Professeur.objects.all()

    if query:
        professeurs = professeurs.filter(nom__icontains=query)  # Filtrer par nom (insensible à la casse)
    
    if specialite_filter:
        professeurs = professeurs.filter(specialite=specialite_filter)  # Filtrer par spécialité

    specialites = Professeur.objects.values_list("specialite", flat=True).distinct()  # Obtenir les spécialités uniques
    
    return render(request, "professeurs/liste_professeurs.html", {
        "professeurs": professeurs,
        "query": query,
        "specialites": specialites,
        "specialite_filter": specialite_filter,
    })


def professeur_create(request):
    if request.method == 'POST':
        form = ProfesseurForm(request.POST, request.FILES)
        if form.is_valid():
            professeur = form.save()
            messages.success(request, f"Le professeur {professeur.nom} {professeur.prenom} a été ajouté avec succès !")
            return redirect('professeur_list')
    else:
        form = ProfesseurForm()
    return render(request, 'professeurs/ajouter_professeur.html', {'form': form})

def professeur_detail(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    return render(request, 'professeurs/professeur_detail.html', {'professeur': professeur})

def professeur_update(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    if request.method == 'POST':
        form = ProfesseurForm(request.POST, request.FILES, instance=professeur)
        if form.is_valid():
            professeur = form.save()
            messages.success(request, f"Les informations du professeur {professeur.nom} {professeur.prenom} ont été mises à jour !")
            return redirect('professeur_list')
    else:
        form = ProfesseurForm(instance=professeur)
    return render(request, 'professeur_form.html', {'form': form})

def professeur_delete(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)
    if request.method == 'POST':
        messages.success(request, f"Le professeur {professeur.nom} {professeur.prenom} a été supprimé avec succès !")
        professeur.delete()
        return redirect('professeur_list')
    return render(request, 'professeurs/professeur_confirm_delete.html', {'professeur': professeur})




  
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Matiere
from .forms import MatiereForm

# Liste des matières avec recherche et filtre
def liste_matieres(request):
    query = request.GET.get('q', '')
    matieres = Matiere.objects.all()
    
    if query:
        matieres = matieres.filter(nom__icontains=query)

    return render(request, 'matieres/liste_matieres.html', {'matieres': matieres, 'query': query})


def generer_reference():
    last_matiere = Matiere.objects.order_by('-id').first()
    if last_matiere:
        last_id = int(last_matiere.reference.split('-')[-1])
        new_id = last_id + 1
    else:
        new_id = 1
    return f"RF-M-{new_id:03d}"

def ajouter_matiere(request):
    reference = generer_reference()
    if request.method == "POST":
        form = MatiereForm(request.POST, request.FILES)
        if form.is_valid():
            matiere = form.save(commit=False)
            matiere.reference = reference  # Assigner la référence avant de sauvegarder
            matiere.save()
            messages.success(request, "Matière ajoutée avec succès !")
            return redirect('liste_matieres')
    else:
        form = MatiereForm()

    return render(request, 'matieres/ajouter_matiere.html', {'form': form, 'reference': reference})


# Modifier une matière
def modifier_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == "POST":
        form = MatiereForm(request.POST, request.FILES, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière mise à jour avec succès !")
            return redirect('liste_matieres')
    else:
        form = MatiereForm(instance=matiere)
    
    return render(request, 'matieres/ajouter_matiere.html', {'form': form})

# Supprimer une matière
def supprimer_matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == "POST":
        matiere.delete()
        messages.success(request, "Matière supprimée avec succès !")
        return redirect('liste_matieres')
    
    return render(request, 'matieres/matiere_confirm_delete.html', {'matiere': matiere})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Niveau
from .forms import NiveauForm

def liste_niveaux(request):
    """Affiche la liste des niveaux"""
    niveaux = Niveau.objects.all()
    return render(request, 'niveaux/liste_niveaux.html', {'niveaux': niveaux})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _  # Ajoutez cette ligne
from .forms import NiveauForm

def ajouter_niveau(request):
    """Ajoute un niveau"""
    if request.method == "POST":
        form = NiveauForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Niveau ajouté avec succès !"))  # Traduire le message
            return redirect('liste_niveaux')
    else:
        form = NiveauForm()

    return render(request, 'niveaux/ajouter_niveau.html', {'form': form})

def modifier_niveau(request, id):
    """Modifie un niveau existant"""
    niveau = get_object_or_404(Niveau, id=id)
    if request.method == "POST":
        form = NiveauForm(request.POST, instance=niveau)
        if form.is_valid():
            form.save()
            messages.success(request, "Niveau modifié avec succès !")
            return redirect('liste_niveaux')
    else:
        form = NiveauForm(instance=niveau)

    return render(request, 'niveaux/modifier_niveau.html', {'form': form, 'niveau': niveau})

def supprimer_niveau(request, id):
    """Supprime un niveau"""
    niveau = get_object_or_404(Niveau, id=id)
    if request.method == "POST":
        niveau.delete()
        messages.success(request, "Niveau supprimé avec succès !")
        return redirect('liste_niveaux')

    return render(request, 'niveaux/confirmer_suppression.html', {'niveau': niveau})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Salle
from .forms import SalleForm

# 📌 1. Afficher la liste des salles
def liste_salles(request):
    salles = Salle.objects.all()
    return render(request, 'salles/liste_salles.html', {'salles': salles})

# 📌 2. Ajouter une salle
def ajouter_salle(request):
    reference = f"SAL-{uuid.uuid4().hex[:6].upper()}"  # Générer une référence unique

    if request.method == "POST":
        form = SalleForm(request.POST)
        if form.is_valid():
            salle = form.save(commit=False)
            salle.reference = reference  # Assigner la référence générée
            salle.save()
            messages.success(request, f"Salle {salle.nom} ajoutée avec succès !")
            return redirect('liste_salles')
    else:
        form = SalleForm()

    return render(request, 'salles/ajouter_salle.html', {'form': form, 'reference': reference})


# 📌 3. Modifier une salle
def modifier_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == "POST":
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            messages.success(request, f"Salle {salle.nom} modifiée avec succès !")
            return redirect('liste_salles')
    else:
        form = SalleForm(instance=salle)
    return render(request, 'salles/modifier_salle.html', {'form': form, 'salle': salle})

# 📌 4. Supprimer une salle
def supprimer_salle(request, salle_id):
    salle = get_object_or_404(Salle, id=salle_id)
    if request.method == "POST":
        salle.delete()
        messages.success(request, f"Salle {salle.nom} modifiée avec succès !")
        return redirect('liste_salles')
    return render(request, 'salles/supprimer_salle.html', {'salle': salle})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Classe
from .forms import ClasseForm
import uuid

# 📌 1. Afficher la liste des classes
def liste_classes(request):
    classes = Classe.objects.all()
    return render(request, 'classes/liste_classes.html', {'classes': classes})

# 📌 2. Ajouter une classe
def ajouter_classe(request):
    reference = f"CL-{uuid.uuid4().hex[:6].upper()}"  # Générer une référence unique

    if request.method == "POST":
        form = ClasseForm(request.POST)
        if form.is_valid():
            classe = form.save(commit=False)
            classe.reference = reference  # Assigner la référence générée
            classe.save()
            messages.success(request, f"Classe {classe.nom} ajoutée avec succès !")
            return redirect('liste_classes')
    else:
        form = ClasseForm(initial={'reference': reference, 'effectif': 0})

    return render(request, 'classes/ajouter_classe.html', {'form': form, 'reference': reference})

# 📌 3. Modifier une classe
def modifier_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    if request.method == "POST":
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, f"Classe {classe.nom} modifiée avec succès !")
            return redirect('liste_classes')
    else:
        form = ClasseForm(instance=classe)
    return render(request, 'classes/modifier_classe.html', {'form': form, 'classe': classe})

from django.shortcuts import render, get_object_or_404
from .models import Classe, Eleve, Devoir, Composition, NoteDevoir, NoteComposition

def detail_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe=classe)
    devoirs = Devoir.objects.filter(classe=classe)
    compositions = Composition.objects.filter(classe=classe)
    notes_devoirs = NoteDevoir.objects.filter(devoir__classe=classe)
    notes_compositions = NoteComposition.objects.filter(composition__classe=classe)

    context = {
        'classe': classe,
        'eleves': eleves,
        'devoirs': devoirs,
        'compositions': compositions,
        'notes_devoirs': notes_devoirs,
        'notes_compositions': notes_compositions,
    }

    return render(request,'classes/detail_classe.html', context)



# 📌 4. Supprimer une classe
def supprimer_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    if request.method == "POST":
        classe.delete()
        messages.success(request, f"Classe {classe.nom} supprimée avec succès !")
        return redirect('liste_classes')
    return render(request, 'classes/supprimer_classe.html', {'classe': classe})


from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Classe, Eleve

def liste_eleves_par_classe(request, classe_id):
    # Récupérer la classe spécifique
    classe = get_object_or_404(Classe, id=classe_id)
    
    # Récupérer tous les élèves de cette classe
    eleves = Eleve.objects.filter(classe=classe)
    
    # Passer les données au template
    return render(request, 'classes/liste_eleves_par_classe.html', {
        'classe': classe,
        'eleves': eleves,
    })

def liste_eleves_par_classe_pdf(request, classe_id):
    # Récupérer la classe spécifique
    classe = get_object_or_404(Classe, id=classe_id)
    
    # Récupérer tous les élèves de cette classe
    eleves = Eleve.objects.filter(classe=classe)
    
    # Rendre le template HTML en chaîne de caractères
    html_string = render_to_string('classes/liste_eleves_par_classe_pdf.html', {
        'classe': classe,
        'eleves': eleves,
    })
    
    # Retourner la réponse HTML pour le PDF
    return HttpResponse(html_string)






from django.contrib import messages
from django.shortcuts import redirect
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from .models import Eleve
from .forms import EleveInfoForm, ParentsInfoForm, AutresInfoForm

file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'wizard_uploads'))

FORMS = [
    ("etape1", EleveInfoForm),
    ("etape2", ParentsInfoForm),
    ("etape3", AutresInfoForm),
]

TEMPLATES = {
    "etape1": "eleves/inscription_etape1.html",
    "etape2": "eleves/inscription_etape2.html",
    "etape3": "eleves/inscription_etape3.html",
}

class EleveInscriptionWizard(SessionWizardView):
    form_list = FORMS
    file_storage = file_storage  # Définir le file_storage ici

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        
        # Créer l'élève avec les données récupérées
        eleve = Eleve.objects.create(**data)

        # Ajouter un message de succès avec le matricule
        messages.success(self.request, f"L'élève {eleve.prenom} {eleve.nom} (Matricule : {eleve.matricule}) a été inscrit avec succès !")

        return redirect('liste_eleves')

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Eleve
from .forms import EleveInfoForm, ParentsInfoForm, AutresInfoForm

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages

from django.db.utils import IntegrityError

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError, transaction
from formtools.wizard.views import SessionWizardView


class EleveModificationWizard(SessionWizardView):
    form_list = FORMS
    file_storage = file_storage

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        """ Pré-remplit les formulaires avec les données de l'élève existant. """
        eleve_id = self.kwargs.get('pk')
        eleve = get_object_or_404(Eleve, pk=eleve_id)

        initial_data = {}

        if step == 'etape1':
            initial_data = {
                'matricule': eleve.matricule,  # Affiché mais non modifiable
                'annee_scolaire': eleve.annee_scolaire,
                'nom': eleve.nom,
                'prenom': eleve.prenom,
                'date_naissance': eleve.date_naissance,
                'lieu_naissance': eleve.lieu_naissance,
                'sexe': eleve.sexe,
                'classe': eleve.classe,
                'adresse': eleve.adresse,
                'telephone': eleve.telephone,
                'email': eleve.email,
                'photo': eleve.photo,
                'frais_inscription': eleve.frais_inscription,
                'paiement': eleve.paiement,
            }
        elif step == 'etape2':
            initial_data = {
                'nom_pere': getattr(eleve, 'nom_pere', ''),  # Vérifie si le champ existe
                'prenom_pere': getattr(eleve, 'prenom_pere', ''),
                'tel_pere': getattr(eleve, 'tel_pere', ''),
                'nom_mere': getattr(eleve, 'nom_mere', ''),
                'prenom_mere': getattr(eleve, 'prenom_mere', ''),
                'tel_mere': getattr(eleve, 'tel_mere', ''),
            }
        elif step == 'etape3':
            initial_data = {
                'activites': getattr(eleve, 'activites', ''),
                'sante': getattr(eleve, 'sante', ''),
            }

        return initial_data

    
    def done(self, form_list, **kwargs):
        """ Enregistre les modifications de l'élève en base de données. """
        eleve_id = self.kwargs.get('pk')
        eleve = get_object_or_404(Eleve, pk=eleve_id)

        try:
            with transaction.atomic():  # Bloque les modifications en cas d'erreur
                for form in form_list:
                    cleaned_data = form.cleaned_data

                    # Vérifier si un autre élève a déjà ce matricule (uniquement si on le modifie)
                    nouveau_matricule = cleaned_data.get("matricule")
                    if nouveau_matricule and nouveau_matricule != eleve.matricule:
                        if Eleve.objects.filter(matricule=nouveau_matricule).exclude(pk=eleve.pk).exists():
                            messages.error(self.request, "Un élève avec ce matricule existe déjà.")
                            return redirect('modifier_eleve', pk=eleve_id)

                    # Appliquer les modifications (sauf le matricule qui ne doit pas être modifié)
                    cleaned_data.pop('matricule', None)
                    for field, value in cleaned_data.items():
                        if hasattr(eleve, field):  # Vérifier que le champ existe
                            setattr(eleve, field, value)

                eleve.save()
                messages.success(self.request, f"L'élève {eleve.prenom} {eleve.nom} a été modifié avec succès !")

        except IntegrityError:
            messages.error(self.request, "Erreur lors de la sauvegarde. Veuillez réessayer.")
            return redirect('modifier_eleve', pk=eleve_id)

        return redirect('liste_eleves')


from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Eleve

from django.shortcuts import get_object_or_404, render
from .models import Eleve

def detail_eleve(request, pk):
    eleve = get_object_or_404(Eleve, pk=pk)  # Renvoie 404 si l'élève n'existe pas
    return render(request, 'eleves/detail_eleve.html', {'eleve': eleve})
def detail_eleveins(request, pk):
    """
    Affiche les détails complets d'un élève inscrit
    """
    eleve = get_object_or_404(Eleve, pk=pk)
    
    context = {
        'eleve': eleve,
        'page_title': f"Détails de l'élève {eleve.prenom} {eleve.nom}",
    }
    
    return render(request, 'eleves/detail_eleve.html', context)

# views.py
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .models import Eleve
from io import BytesIO



from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse

def generer_recu_inscription(request, pk):
    eleve = Eleve.objects.get(pk=pk)
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=100,
        bottomMargin=70
    )

    elements = []
    styles = getSampleStyleSheet()

    # Styles personnalisés
    title_style = ParagraphStyle(name="Title", fontSize=18, alignment=1, spaceAfter=20, textColor=colors.HexColor("#154360"))
    section_title_style = ParagraphStyle(name="SectionTitle", fontSize=12, alignment=1, textColor=colors.HexColor("#1F618D"), backColor=colors.HexColor("#D6EAF8"), spaceAfter=10, spaceBefore=20, leading=14)
    label_style = ParagraphStyle(name="Label", fontSize=10, textColor=colors.HexColor("#34495E"))
    value_style = ParagraphStyle(name="Value", fontSize=10)

    # === En-tête (logo + nom d’école) ===
    elements.append(Paragraph("<b>ÉCOLE SUPÉRIEURE TECHNIQUE</b><br/><i>Formation d'excellence pour l'avenir</i>", title_style))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("REÇU D’INSCRIPTION", ParagraphStyle(name="MainTitle", fontSize=16, alignment=1, textColor=colors.HexColor("#1A5276"), spaceAfter=10)))
    elements.append(Spacer(1, 20))

    # === Section 1 : Informations Administratives ===
    elements.append(Paragraph("1. Informations Administratives", section_title_style))
    admin_data = [
        ["Année scolaire", str(eleve.annee_scolaire)],
        ["Date d'inscription", eleve.date_inscription.strftime("%d/%m/%Y")],
        ["Matricule", eleve.matricule],
        ["Classe", str(eleve.classe)],
        ["Paiement", eleve.paiement],
        ["Frais d'inscription", "Payée" if eleve.frais_inscription == "P" else "Non payée"]
    ]
    elements.append(create_table(admin_data))

    # === Section 2 : Informations Personnelles ===
    elements.append(Paragraph("2. Informations Personnelles", section_title_style))
    perso_data = [
        ["Nom", eleve.nom],
        ["Prénom", eleve.prenom],
        ["Date de naissance", eleve.date_naissance.strftime("%d/%m/%Y")],
        ["Lieu de naissance", eleve.lieu_naissance or "—"],
        ["Sexe", dict(Eleve.SEXE_CHOICES).get(eleve.sexe)],
        ["Adresse", eleve.adresse or "—"],
        ["Téléphone", eleve.telephone or "—"],
        ["Email", eleve.email or "—"]
    ]
    elements.append(create_table(perso_data))

    # === Section 3 : Coordonnées des Parents ===
    elements.append(Paragraph("3. Coordonnées des Parents", section_title_style))
    parent_data = [
        ["Nom du père", eleve.nom_pere or "—"],
        ["Téléphone du père", eleve.telephone_pere or "—"],
        ["Email du père", eleve.email_pere or "—"],
        ["Nom de la mère", eleve.nom_mere or "—"],
        ["Téléphone de la mère", eleve.telephone_mere or "—"],
        ["Email de la mère", eleve.email_mere or "—"]
    ]
    elements.append(create_table(parent_data))

    # === Section 4 : Informations Médicales ===
    elements.append(Paragraph("4. Informations Médicales", section_title_style))
    medical_data = [
        ["État de santé", eleve.etat_sante or "—"],
        ["Aptitude", eleve.aptitude or "—"],
        ["Groupe sanguin", eleve.groupe_sanguin or "—"],
        ["Maladies chroniques", eleve.maladies_chroniques or "—"],
        ["Traitements en cours", eleve.traitements_en_cours or "—"],
        ["Commentaires", eleve.commentaires_etat_general or "—"],
        ["Observations", eleve.observations or "—"]
    ]
    elements.append(create_table(medical_data))

    # === Signature ===
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("Fait à ____________________ le ____ / ____ / _______", label_style))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Signature du Responsable", label_style))
    elements.append(Paragraph("__________________________", label_style))

    # Build avec header et footer
    def add_header_footer(canvas, doc):
        canvas.saveState()

        # Header
        canvas.setFont('Helvetica-Bold', 10)
        canvas.setFillColor(colors.HexColor("#1F618D"))
        canvas.drawString(40, A4[1] - 50, "École Supérieure Technique - Excellence et savoir")

        # Footer
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.grey)
        canvas.drawString(40, 40, "📍 Adresse : 123, Rue de l’Avenir | ☎️ Tél : +212 600 000 000 | ✉️ Email : contact@ecoletech.ma")
        canvas.drawRightString(A4[0] - 40, 40, f"Page {doc.page}")

        canvas.restoreState()

    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="recu_inscription_{eleve.matricule}.pdf"'
    return response


def create_table(data):
    table = Table(data, colWidths=[160, 300])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor("#EBF5FB")]),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table




def liste_eleves(request):
    eleves = Eleve.objects.all()  # Récupère tous les élèves

    matricule = request.GET.get('matricule', '')
    classe_id = request.GET.get('classe', '')
    annee_scolaire_id = request.GET.get('annee_scolaire', '')

    if matricule:
        eleves = eleves.filter(matricule__icontains=matricule)
    if classe_id:
        eleves = eleves.filter(classe_id=classe_id)
    if annee_scolaire_id:
        eleves = eleves.filter(annee_scolaire_id=annee_scolaire_id)

    classes = Classe.objects.all()
    annees_scolaires = AnneeScolaire.objects.all()

    return render(request, 'eleves/liste_eleves.html', {
        'eleves': eleves,
        'matricule': matricule,
        'classe_id': classe_id,
        'annee_scolaire_id': annee_scolaire_id,
        'classes': classes,
        'annees_scolaires': annees_scolaires,
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Eleve


from django.shortcuts import get_object_or_404, redirect
from .models import Eleve

def eleve_delete(request, pk):
    eleve = get_object_or_404(Eleve, pk=pk)  # Récupère l'élève à supprimer
    if request.method == 'POST':
        # Récupère le nom et le matricule de l'élève
        nom_complet = f"{eleve.prenom} {eleve.nom}"
        matricule = eleve.matricule  # Assurez-vous que l'élève a un attribut 'matricule'
        
        # Supprime l'élève
        eleve.delete()
        
        # Ajoute un message de succès avec le nom et matricule
        messages.success(request, f"L'élève {nom_complet} (Matricule: {matricule}) a été supprimé avec succès.")
        
        # Redirige vers la liste des élèves
        return redirect('liste_eleves')

    # Si ce n'est pas une requête POST, on redirige simplement vers la liste
    return redirect('liste_eleves')




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Semestre
from .forms import SemestreForm

# Liste des semestres
def liste_semestres(request):
    semestres = Semestre.objects.all()
    return render(request, 'semestres/liste_semestres.html', {'semestres': semestres})


# Ajouter un semestre

from .forms import SemestreForm

def ajouter_semestre(request):
    if request.method == 'POST':
        form = SemestreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_semestres')  # Rediriger vers une page de succès
    else:
        form = SemestreForm()
    return render(request, 'semestres/ajouter_semestre.html', {'form': form})

# Modifier un semestre
def modifier_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    if request.method == 'POST':
        form = SemestreForm(request.POST, instance=semestre)
        if form.is_valid():
            form.save()
            messages.success(request, "Le semestre a été modifié avec succès.")
            return redirect('liste_semestres')
    else:
        form = SemestreForm(instance=semestre)

    return render(request, 'semestres/modifier_semestre.html', {'form': form, 'semestre': semestre})

# Supprimer un semestre
def supprimer_semestre(request, semestre_id):
    semestre = get_object_or_404(Semestre, id=semestre_id)
    if request.method == 'POST':
        semestre.delete()
        messages.success(request, "Le semestre a été supprimé avec succès.")
        return redirect('liste_semestres')

    return render(request, 'semestres/supprimer_semestre.html', {'semestre': semestre})






from django.shortcuts import render, get_object_or_404, redirect
from .models import Devoir
from .forms import DevoirForm

# 🔹 Liste des devoirs
def liste_devoirs(request):
    devoirs = Devoir.objects.all()
    return render(request, 'devoirs/liste_devoirs.html', {'devoirs': devoirs})

# 🔹 Ajouter un devoir
def ajouter_devoir(request):
    if request.method == "POST":
        form = DevoirForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_devoirs')  # Redirection vers la liste après l'ajout
    else:
        form = DevoirForm()
    return render(request, 'devoirs/ajouter_devoir.html', {'form': form})

# 🔹 Modifier un devoir
def modifier_devoir(request, pk):
    devoir = get_object_or_404(Devoir, pk=pk)
    if request.method == "POST":
        form = DevoirForm(request.POST, instance=devoir)
        if form.is_valid():
            form.save()
            return redirect('liste_devoirs')
    else:
        form = DevoirForm(instance=devoir)
    return render(request, 'devoirs/modifier_devoir.html', {'form': form})

# 🔹 Supprimer un devoir
def supprimer_devoir(request, pk):
    devoir = get_object_or_404(Devoir, pk=pk)
    if request.method == "POST":
        devoir.delete()
        return redirect('liste_devoirs')
    return render(request, 'devoirs/supprimer_devoir.html', {'devoir': devoir})
from django.shortcuts import render
from .models import Composition

def liste_compositions(request):
    compositions = Composition.objects.all()
    return render(request, 'compositions/liste_compositions.html', {'compositions': compositions})


from django.shortcuts import render, redirect
from .forms import CompositionForm

def ajouter_composition(request):
    if request.method == "POST":
        form = CompositionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_compositions')  # Redirection vers la liste après l'ajout
    else:
        form = CompositionForm()
    return render(request, 'compositions/ajouter_composition.html', {'form': form})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Composition
from .forms import CompositionForm

def modifier_composition(request, pk):
    composition = get_object_or_404(Composition, pk=pk)
    if request.method == "POST":
        form = CompositionForm(request.POST, instance=composition)
        if form.is_valid():
            form.save()
            return redirect('liste_compositions')  # Redirection vers la liste après modification
    else:
        form = CompositionForm(instance=composition)
    return render(request, 'compositions/modifier_composition.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Composition

def supprimer_composition(request, pk):
    composition = get_object_or_404(Composition, pk=pk)
    if request.method == "POST":
        composition.delete()
        return redirect('liste_compositions')  # Redirection vers la liste des compositions après suppression
    return render(request, 'compositions/supprimer_composition.html', {'composition': composition})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import NoteDevoir
from .forms import NoteDevoirForm

# Liste des notes
def liste_notes(request):
    notes = NoteDevoir.objects.all()
    return render(request, 'notes/liste_notes.html', {'notes': notes})

# Ajouter une note

from django.db import IntegrityError

from django.http import JsonResponse
from .models import Devoir, Eleve

from django.shortcuts import render, redirect
from django.db import IntegrityError
from .forms import NoteDevoirForm
from .models import NoteDevoir
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)


from django.shortcuts import render, redirect, get_object_or_404
from .models import NoteDevoir
from .forms import NoteDevoirForm

# Créer une note
def creer_note(request):
    if request.method == 'POST':
        form = NoteDevoirForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_notes')
    else:
        form = NoteDevoirForm()
    return render(request, 'notes/creer_note.html', {'form': form})

# Lister toutes les notes
def lister_notes(request):
    notes = NoteDevoir.objects.all()
    return render(request, 'notes/lister_notes_devoir.html', {'notes': notes})

# Modifier une note
def modifier_note(request, id):
    note = get_object_or_404(NoteDevoir, id=id)
    if request.method == 'POST':
        form = NoteDevoirForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('liste_notes')
    else:
        form = NoteDevoirForm(instance=note)
    return render(request, 'notes/modifier_note_devoir.html', {'form': form})

# Supprimer une note
from django.shortcuts import render, redirect, get_object_or_404
from .models import NoteDevoir

def supprimer_note(request, id):
    note = get_object_or_404(NoteDevoir, id=id)
    if request.method == 'POST':
        note.delete()
        return redirect('liste_notes')
    return render(request, 'notes/supprimer_note.html', {'note': note})

from django.shortcuts import render, get_object_or_404
from .models import Classe, Eleve, Matiere, NoteDevoir

from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Eleve, NoteDevoir, Classe, Semestre

def get_notes_devoirs_par_classe_et_semestre(classe_id, semestre_id):
    """
    Retourne les notes de devoirs des élèves d'une classe pour un semestre donné.
    """
    eleves = Eleve.objects.filter(classe_id=classe_id)
    resultats = []

    for eleve in eleves:
        notes_devoirs = NoteDevoir.objects.filter(
            eleve=eleve,
            devoir__semestre_id=semestre_id
        ).annotate(
            matiere_nom=F('devoir__matiere__nom'),
            date_devoir=F('devoir__date')
        ).values('matiere_nom', 'date_devoir', 'note')

        eleve_data = {
            'eleve_id': eleve.id,
            'nom': eleve.nom,
            'prenom': eleve.prenom,
            'notes_devoirs': list(notes_devoirs)
        }
        resultats.append(eleve_data)

    return resultats

def notes_devoirs_view(request, classe_id):
    """
    Vue pour afficher les notes de devoirs des élèves d'une classe pour tous les semestres.
    """
    # Vérifier que la classe existe
    classe = get_object_or_404(Classe, id=classe_id)

    # Récupérer tous les semestres
    semestres = Semestre.objects.all()

    # Organiser les résultats par semestre
    resultats_par_semestre = []
    for semestre in semestres:
        resultats = get_notes_devoirs_par_classe_et_semestre(classe_id, semestre.id)
        if resultats:  # Ne pas inclure les semestres sans notes
            resultats_par_semestre.append({
                'semestre': semestre,
                'resultats': resultats,
            })

    # Passer les résultats au template
    context = {
        'classe': classe,
        'resultats_par_semestre': resultats_par_semestre,
    }
    return render(request, 'devoirs/notes_par_classe_devoirs.html', context)
def liste_eleves_avec_notes(request, classe_id):
    # Récupérer la classe spécifique
    classe = get_object_or_404(Classe, id=classe_id)
    
    # Récupérer tous les élèves de cette classe
    eleves = Eleve.objects.filter(classe=classe)
    
    # Récupérer toutes les matières
    matieres = Matiere.objects.all()
    
    # Préparer les données pour le template
    data = []
    for eleve in eleves:
        eleve_data = {
            'eleve': eleve,
            'notes_devoirs': []
        }
        
        for matiere in matieres:
            # Récupérer les notes de devoirs pour cette matière
            notes_devoirs = NoteDevoir.objects.filter(
                eleve=eleve, 
                devoir__matiere=matiere
            ).aggregate(Avg('note'))['note__avg'] or 0
            
            eleve_data['notes_devoirs'].append({
                'matiere': matiere.nom,
                'notes_devoirs': notes_devoirs
            })
        
        data.append(eleve_data)
    
    # Passer les données au template
    return render(request, 'notes/liste_eleves_avec_notes.html', {
        'classe': classe,
        'data': data,
        'matieres': matieres  # Passer les matières pour l'en-tête du tableau
    })
    
    
    
    
    
   
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib import messages
from .models import NoteComposition, Composition, Eleve
from .forms import NoteCompositionForm

# Liste des notes de composition
def liste_notes_composition(request):
    notes = NoteComposition.objects.all()
    return render(request, 'notes/liste_notes_composition.html', {'notes': notes})
# Ajouter une note de composition
def ajouter_note_composition(request):
    form = NoteCompositionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        eleve = form.cleaned_data['eleve']
        composition = form.cleaned_data['composition']

        if NoteComposition.objects.filter(eleve=eleve, composition=composition).exists():
            form.add_error(None, "L'élève a déjà une note pour cette composition.")
        else:
            try:
                form.save()
                return redirect('liste_notes_composition')  # Redirection après l'ajout
            except IntegrityError:
                form.add_error(None, "Erreur d'intégrité lors de l'ajout de la note.")

    return render(request, 'notes/ajouter_note_composition.html', {'form': form})

# Récupérer les élèves en fonction de la composition sélectionnée (AJAX)
def get_eleves_by_composition(request):
    composition_id = request.GET.get("composition_id")
    try:
        composition = Composition.objects.get(id=composition_id)
        eleves = Eleve.objects.filter(classe=composition.classe).values("id", "nom")
        return JsonResponse(list(eleves), safe=False)
    except Composition.DoesNotExist:
        return JsonResponse([], safe=False)

# Modifier une note de composition
def modifier_note_composition(request, note_id):
    note_composition = get_object_or_404(NoteComposition, id=note_id)

    if request.method == 'POST':
        form = NoteCompositionForm(request.POST, instance=note_composition)
        if form.is_valid():
            try:
                form.save()
                return redirect('liste_notes_composition')  # Redirection après la modification
            except IntegrityError:
                form.add_error(None, "L'élève a déjà une note pour cette composition.")
    else:
        form = NoteCompositionForm(instance=note_composition)

    return render(request, 'notes/modifier_note_composition.html', {'form': form})

# Supprimer une note de composition
def supprimer_note_composition(request, pk):
    note = get_object_or_404(NoteComposition, pk=pk)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note supprimée avec succès !")
        return redirect("liste_notes_composition")
    return render(request, "notes/confirm_delete.html", {"note": note})



from django.shortcuts import render, get_object_or_404
from .models import Eleve, NoteComposition, Classe, Semestre


from django.shortcuts import render, get_object_or_404
from django.db.models import F
from .models import Eleve, NoteComposition, Classe, Semestre

def get_notes_compositions_par_classe_et_semestre(classe_id, semestre_id):
    """
    Retourne les notes de compositions des élèves d'une classe pour un semestre donné.
    """
    eleves = Eleve.objects.filter(classe_id=classe_id)
    resultats = []

    for eleve in eleves:
        notes_compositions = NoteComposition.objects.filter(
            eleve=eleve,
            composition__semestre_id=semestre_id
        ).annotate(
            matiere_nom=F('composition__matiere__nom'),
            date_composition=F('composition__date')
        ).values('matiere_nom', 'date_composition', 'note')

        eleve_data = {
            'eleve_id': eleve.id,
            'nom': eleve.nom,
            'prenom': eleve.prenom,
            'notes_compositions': list(notes_compositions)
        }
        resultats.append(eleve_data)

    return resultats

def notes_compositions_view(request, classe_id):
    """
    Vue pour afficher les notes de compositions des élèves d'une classe pour tous les semestres.
    """
    # Vérifier que la classe existe
    classe = get_object_or_404(Classe, id=classe_id)

    # Récupérer tous les semestres
    semestres = Semestre.objects.all()

    # Organiser les résultats par semestre
    resultats_par_semestre = []
    for semestre in semestres:
        resultats = get_notes_compositions_par_classe_et_semestre(classe_id, semestre.id)
        if resultats:  # Ne pas inclure les semestres sans notes
            resultats_par_semestre.append({
                'semestre': semestre,
                'resultats': resultats,
            })

    # Passer les résultats au template
    context = {
        'classe': classe,
        'resultats_par_semestre': resultats_par_semestre,
    }
    return render(request, 'compositions/notes_par_classe_compositions.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Eleve, Semestre, Matiere, NoteDevoir, NoteComposition

from application.utils import calculer_moyenne_eleve, attribuer_moyennes_et_rangs,calculer_moyenne_matiere

from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Eleve, Semestre, Matiere, NoteDevoir, NoteComposition

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
        resultats.append((eleve, moyenne))

    # Classement des élèves en fonction de la moyenne
    resultats = sorted(resultats, key=lambda x: x[1], reverse=True)
    rangs = {eleve.id: i + 1 for i, (eleve, _) in enumerate(resultats)}

    return rangs


from django.shortcuts import render, get_object_or_404
from .models import Eleve, Semestre, Matiere, NoteDevoir, NoteComposition
from .utils import calculer_moyenne_matiere, attribuer_moyennes_et_rangs,calculer_rang_matiere,determiner_appreciation

def bulletin(request, pk):
    # Récupérer l'élève
    eleve = get_object_or_404(Eleve, pk=pk)

    # Récupérer la classe de l'élève
    classe = eleve.classe

    # Récupérer le nombre d'élèves dans la classe
    nombre_eleves_classe = Eleve.objects.filter(classe=classe).count()

    # Récupérer tous les semestres de l'année scolaire de l'élève
    semestres = Semestre.objects.filter(annee_scolaire=eleve.annee_scolaire)

    # Liste pour stocker les bulletins de chaque semestre
    bulletins = []

    for semestre in semestres:
        # Récupérer le nombre d'absences de l'élève pour ce semestre
        nombre_absences = Absence.objects.filter(
            eleve=eleve,
            semestre=semestre
        ).count()

        # Récupérer le nombre de retards de l'élève pour ce semestre
        nombre_retards = Retard.objects.filter(
            eleve=eleve,
            semestre=semestre
        ).count()

        # Données du bulletin pour ce semestre
        bulletin_data = {
            'semestre': semestre,
            'matieres': [],
            'moyenne_generale': 0,
            'rang': 0,
            'eleve': eleve,
            'classe': classe,
            'nombre_eleves_classe': nombre_eleves_classe,
            'nombre_absences': nombre_absences,  # Nombre d'absences
            'nombre_retards': nombre_retards,  # Nombre de retards
            'total_coefficients': 0,  # Total des coefficients des matières
            'total_moyenne_absolue': 0,  # Total des moyennes absolues des matières
        }

        total_points = 0
        total_coefficients = 0
        total_moyenne_absolue = 0  # Variable pour stocker la somme des moyennes absolues

        # Récupérer toutes les matières
        matieres = Matiere.objects.all()

        for matiere in matieres:
            # Récupérer les notes de devoirs pour cette matière et ce semestre
            notes_devoirs = NoteDevoir.objects.filter(
                eleve=eleve,
                devoir__matiere=matiere,
                devoir__semestre=semestre
            ).values_list('note', flat=True)

            # Récupérer les notes de composition pour cette matière et ce semestre
            notes_composition = NoteComposition.objects.filter(
                eleve=eleve,
                composition__matiere=matiere,
                composition__semestre=semestre
            ).values_list('note', flat=True)

            # Calculer la moyenne de la matière
            moyenne_matiere = calculer_moyenne_matiere(eleve, matiere, semestre)

            # Calculer la moyenne absolue (moyenne * coefficient)
            moyenne_absolue = moyenne_matiere * matiere.coefficient

            # Ajouter la moyenne absolue au total
            total_moyenne_absolue += moyenne_absolue

            # Calculer le rang de l'élève dans cette matière
            rang_matiere = calculer_rang_matiere(eleve, matiere, semestre)

            # Déterminer l'appréciation en fonction de la moyenne
            appreciation = determiner_appreciation(moyenne_matiere)

            # Ajouter les données de la matière au bulletin
            bulletin_data['matieres'].append({
                'matiere': matiere.nom,
                'devoir': sum(notes_devoirs) / len(notes_devoirs) if notes_devoirs else 0,  # Moyenne des devoirs
                'composition': sum(notes_composition) / len(notes_composition) if notes_composition else 0,  # Moyenne des compositions
                'moyenne': moyenne_matiere,
                'coefficient': matiere.coefficient,
                'moyenne_absolue': moyenne_absolue,  # Ajout de la moyenne absolue
                'rang': rang_matiere,  # Ajout du rang par matière
                'appreciation': appreciation,  # Ajout de l'appréciation
            })

            # Calculer les points totaux pour la moyenne générale
            total_points += moyenne_absolue
            total_coefficients += matiere.coefficient

        # Calculer la moyenne générale pour ce semestre
        if total_coefficients > 0:
            bulletin_data['moyenne_generale'] = round(total_points / total_coefficients, 2)

        # Ajouter le total des coefficients des matières
        bulletin_data['total_coefficients'] = total_coefficients

        # Ajouter le total des moyennes absolues des matières
        bulletin_data['total_moyenne_absolue'] = total_moyenne_absolue

        # Attribuer le rang général de l'élève pour ce semestre
        rangs = attribuer_moyennes_et_rangs(eleve.classe, semestre)
        bulletin_data['rang'] = rangs.get(eleve.id, 0)

        # Ajouter ce bulletin à la liste des bulletins
        bulletins.append(bulletin_data)

    # Passer les données au template
    return render(request, 'bulletin/bulletin.html', {
        'eleve': eleve,
        'bulletins': bulletins,
        'classe': classe,
        'nombre_eleves_classe': nombre_eleves_classe,
    })

    

from django.shortcuts import render, get_object_or_404, redirect
from .models import Absence
from .forms import AbsenceForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Absence
from .forms import AbsenceForm

# Liste des absences
def liste_absences(request):
    absences = Absence.objects.all()
    return render(request, 'absences/liste_absences.html', {'absences': absences})

# Ajouter une absence
def ajouter_absence(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            absence = form.save()
            messages.success(request, f"Absence ajoutée avec succès pour {absence.eleve}.")
            return redirect('liste_absences')
    else:
        form = AbsenceForm()
    return render(request, 'absences/ajouter_absence.html', {'form': form})
from django.http import JsonResponse
from django.shortcuts import render
from .models import Semestre, Eleve

def get_semestres(request):
    annee_id = request.GET.get('annee_id')
    semestres = Semestre.objects.filter(annee_scolaire_id=annee_id)
    return render(request, 'semestre_dropdown_list_options.html', {'semestres': semestres})

def get_eleves(request):
    classe_id = request.GET.get('classe_id')
    eleves = Eleve.objects.filter(classe_id=classe_id)
    return render(request, 'eleve_dropdown_list_options.html', {'eleves': eleves})
from django.http import JsonResponse
from django.shortcuts import render
from .models import Classe, Eleve

def get_classes(request):
    annee_id = request.GET.get('annee_id')
    classes = Classe.objects.filter(annee_scolaire_id=annee_id)
    return render(request, 'classe_dropdown_list_options.html', {'classes': classes})

# Modifier une absence
def modifier_absence(request, absence_id):
    absence = get_object_or_404(Absence, pk=absence_id)
    if request.method == 'POST':
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            absence = form.save()
            messages.success(request, f"L'absence de {absence.eleve} a été mise à jour avec succès.")
            return redirect('liste_absences')
    else:
        form = AbsenceForm(instance=absence)
    return render(request, 'absences/ajouter_absence.html', {'form': form})

# Supprimer une absence
def supprimer_absence(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    if request.method == 'POST':
        messages.success(request, f"L'absence de {absence.eleve} le {absence.date} a été supprimée.")
        absence.delete()
        return redirect('liste_absences')
    return render(request, 'absences/confirmation_suppression_absence.html', {'absence': absence})




from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Retard, Classe, Semestre, Eleve, AnneeScolaire, Matiere
from .forms import RetardForm


from django.shortcuts import render, get_object_or_404, redirect
from .models import Retard
from .forms import RetardForm

def liste_retards(request):
    """Affiche la liste des retards."""
    retards = Retard.objects.all().order_by('-date')
    return render(request, 'retards/liste_retards.html', {'retards': retards})

def detail_retard(request, pk):
    """Affiche les détails d'un retard spécifique."""
    retard = get_object_or_404(Retard, pk=pk)
    return render(request, 'retards/detail_retard.html', {'retard': retard})


def creer_retard(request):
    """Crée un nouveau retard."""
    if request.method == "POST":
        form = RetardForm(request.POST)
        if form.is_valid():
          retard=form.save()
          messages.success(request, f"Le retard de {retard.eleve.nom} {retard.eleve.prenom} a été enregistrer avec succès !")
        return redirect('liste_retards')
    else:
        form = RetardForm()
    return render(request, 'retards/ajouter_retard.html', {'form': form})

def modifier_retard(request, retard_id):
    """Modifie un retard existant."""
    retard = get_object_or_404(Retard, pk=retard_id)
    if request.method == "POST":
        form = RetardForm(request.POST, instance=retard)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le retard de {retard.eleve.nom} {retard.eleve.prenom} a été modifié avec succès !")
            return redirect('detail_retard', pk=retard.pk)
    else:
        form = RetardForm(instance=retard)
    return render(request, 'retards/modifier_retard.html', {'form': form})

def supprimer_retard(request, retard_id):
    """Supprime un retard existant."""
    retard = get_object_or_404(Retard, pk=retard_id)
    if request.method == "POST":
        retard.delete()
        return redirect('liste_retards')
    messages.success(request, f"Le retard de {retard.eleve.nom} {retard.eleve.prenom} a été supprimé avec succès !")
    return render(request, 'retards/supprimer_retard.html', {'retard': retard})


# Récupérer les classes et semestres pour une année scolaire (AJAX)
def get_classes_semestres(request):
    try:
        annee_id = request.GET.get('annee_id')
        classes = list(Classe.objects.filter(annee_scolaire_id=annee_id).values('id', 'nom'))
        semestres = list(Semestre.objects.filter(annee_scolaire_id=annee_id).values('id', 'nom'))
        return JsonResponse({'classes': classes, 'semestres': semestres})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Récupérer les élèves pour une classe (AJAX)
def get_eleves(request):
    try:
        classe_id = request.GET.get('classe_id')
        eleves = list(Eleve.objects.filter(classe_id=classe_id).values('id', 'nom', 'prenom'))
        return JsonResponse({'eleves': eleves})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
    
    

from django.http import JsonResponse
from django.views import View
from .models import Cours
import json

from django.shortcuts import render
from .models import Cours

from django.shortcuts import render
from .models import Cours


from django.shortcuts import render

def calendrier(request):
    return render(request, 'annees_scolaires/calendrier.html')



from django.http import JsonResponse
from .models import Cours

def calendrier_cours(request):
    cours = Cours.objects.all()
    events = []
    for c in cours:
        events.append({
            'title': f"{c.matiere.nom} ({c.classe.nom})",
            'start': f"{c.date}T{c.heure_debut}",
            'end': f"{c.date}T{c.heure_fin}",
            'description': f"Professeur: {c.professeur.nom}, Salle: {c.salle.nom}",
        })
    return JsonResponse(events, safe=False)


from django.shortcuts import render, redirect
from .forms import CoursForm

def ajouter_cours(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendrier')
    else:
        form = CoursForm()
        
    return render(request, 'annees_scolaires/ajouter_cours.html', {'form': form})

from django.shortcuts import render



from django.shortcuts import render, get_object_or_404
from .models import Classe, Eleve

def liste_eleves_par_classe(request, classe_id):
    # Récupérer la classe spécifique
    classe = get_object_or_404(Classe, id=classe_id)
    
    # Récupérer tous les élèves de cette classe
    eleves = Eleve.objects.filter(classe=classe)
    
    # Passer les données au template
    return render(request, 'classes/liste_eleves_par_classe.html', {
        'classe': classe,
        'eleves': eleves,
    })
    
    
    
    
from django.http import JsonResponse
from .models import Eleve

def get_eleves_by_composition(request):
    composition_id = request.GET.get('composition_id')
    eleves = Eleve.objects.filter(composition_id=composition_id).values('id', 'nom')
    return JsonResponse(list(eleves), safe=False)
    
    
    
    
    
    
    
    
class EleveWizard(SessionWizardView):
    # Liste des formulaires à utiliser dans l'ordre
    form_list = [EleveInfoForm, ParentsInfoForm, AutresInfoForm]

    # Template utilisé pour afficher les étapes du formulaire
    template_name = 'eleve_wizard.html'

    def done(self, form_list, **kwargs):
        # Fusionne les données des formulaires
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        
        # Crée une instance de Eleve avec les données fusionnées
        eleve = Eleve(**data)
        eleve.save()
        
        # Redirige vers une vue de liste (ou une autre page)
        return redirect('liste_eleves')
    
    
 
from django.contrib import messages
from .models import Paiement
from .forms import PaiementForm

# Liste des paiements
def liste_paiements(request):
    paiements = Paiement.objects.all().order_by('-date_paiement')
    return render(request, 'paiements/liste_paiements.html', {'paiements': paiements})

# Détails d'un paiement
def details_paiement(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    eleve = paiement.eleve  # Accéder à l'élève associé au paiement
    return render(request, 'paiements/details_paiement.html', {
        'paiement': paiement,
        'eleve': eleve,  # Passer l'élève au template
    })


# Créer un paiement
def creer_paiement(request):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save()
            messages.success(request, f"Le paiement de {paiement.eleve.nom} {paiement.eleve.prenom} a été créé avec succès.")
            return redirect('liste_paiements')
    else:
        form = PaiementForm()
    return render(request, 'paiements/creer_paiement.html', {'form': form})

# Modifier un paiement
def modifier_paiement(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            paiement = form.save()
            messages.success(request, f"Le paiement de {paiement.eleve.nom} {paiement.eleve.prenom} a été modifié avec succès.")
            return redirect('liste_paiements')
    else:
        form = PaiementForm(instance=paiement)
    return render(request, 'paiements/modifier_paiement.html', {'form': form})

# Supprimer un paiement
def supprimer_paiement(request, pk):
    paiement = get_object_or_404(Paiement, pk=pk)
    if request.method == 'POST':
        nom_eleve = f"{paiement.eleve.nom} {paiement.eleve.prenom}"
        paiement.delete()
        messages.success(request, f"Le paiement de {nom_eleve} a été supprimé avec succès.")
        return redirect('liste_paiements')
    return render(request, 'paiements/supprimer_paiement.html', {'paiement': paiement})




def generate_facture_pdf(request, pk):
    # Récupération des données
    paiement = get_object_or_404(Paiement, pk=pk)
    eleve = paiement.eleve
    
    # Calculs supplémentaires si nécessaire
    # ...
    
    return render(request, 'paiements/facture_pdf_template.html', {
        'paiement': paiement,
        'eleve': eleve,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Surveillant
from .forms import SurveillantForm

def liste_surveillants(request):
    """Affiche la liste de tous les surveillants."""
    surveillants = Surveillant.objects.all().order_by('nom', 'prenom')
    return render(request, 'surveillant/liste.html', {'surveillants': surveillants})

def ajouter_surveillant(request):
    """Ajoute un nouveau surveillant."""
    if request.method == 'POST':
        form = SurveillantForm(request.POST)
        if form.is_valid():
            surveillant = form.save()
            messages.success(request, f"Le surveillant {surveillant.nom} {surveillant.prenom} a été ajouté avec succès.")
            return redirect('liste_surveillants')
    else:
        form = SurveillantForm()
    return render(request, 'surveillant/ajouter.html', {'form': form})

def modifier_surveillant(request, id):
    """Modifie les informations d'un surveillant existant."""
    surveillant = get_object_or_404(Surveillant, id=id)
    if request.method == 'POST':
        form = SurveillantForm(request.POST, instance=surveillant)
        if form.is_valid():
            surveillant = form.save()
            messages.success(request, f"Les informations du surveillant {surveillant.nom} {surveillant.prenom} ont été mises à jour avec succès.")
            return redirect('liste_surveillants')
    else:
        form = SurveillantForm(instance=surveillant)
    return render(request, 'surveillant/modifier.html', {'form': form, 'surveillant': surveillant})

def supprimer_surveillant(request, id):
    """Supprime un surveillant."""
    surveillant = get_object_or_404(Surveillant, id=id)
    if request.method == 'POST':
        nom_complet = f"{surveillant.nom} {surveillant.prenom}"
        surveillant.delete()
        messages.success(request, f"Le surveillant {nom_complet} a été supprimé avec succès.")
        return redirect('liste_surveillants')
    return render(request, 'surveillant/supprimer.html', {'surveillant': surveillant})





from django.contrib.auth import authenticate, login,logout

def ajouter_utilisateur(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur créé avec succès !')
            return redirect('login')  # Redirigez vers une page de connexion ou autre
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'utilisateurs/ajouter_utilisateur.html', {'form': form})


from django.contrib.auth import authenticate, login,logout
from .forms import CustomLoginForm

def login_utilisateur(request):
    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Connexion réussie.')
                return redirect('home')  # Redirige après connexion
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')

    return render(request, 'utilisateurs/login.html', {'form': form})

def logout_utilisateur(request):
    
    logout(request)  # Déconnexion de l'utilisateur
    messages.success(request, 'Déconnexion réussie.')
    return redirect('login')  