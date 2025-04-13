from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import EleveInscriptionWizard, FORMS
from .views import EleveModificationWizard, FORMS
from . import views


urlpatterns = [
   
    path('liste_annees_scolaires/', views.liste_annees_scolaires, name='liste_annees_scolaires'),
    path('liste_annees_scolaires/ajouter/', views.creer_annee_scolaire, name='creer_annee_scolaire'),
    path('annee-scolaire/<int:annee_scolaire_id>/', views.detail_annee_scolaire, name='detail_annee_scolaire'),
    path('liste_annees_scolaires/<int:pk>/modifier/', views.modifier_annee_scolaire, name='modifier_annee_scolaire'),
    path('liste_annees_scolaires/<int:pk>/supprimer/', views.supprimer_annee_scolaire, name='supprimer_annee_scolaire'),
    
    
    path('professeurs/',views.professeur_list, name='professeur_list'),
    path('professeurs/<int:pk>/', views.professeur_detail, name='professeur_detail'),
    path('professeurs/ajouter/', views.professeur_create, name='ajouter_professeur'),
    path('professeurs/<int:pk>/modifier/', views.professeur_update, name='modifier_professeur'),
    path('professeurs/<int:pk>/supprimer/', views.professeur_delete, name='supprimer_professeur'),
    
     # Liste des surveillants
    path('surveillant/', views.liste_surveillants, name='liste_surveillants'),
    # Ajouter un surveillant
    path('surveillant/ajouter/', views.ajouter_surveillant, name='ajouter_surveillant'),
    # Modifier un surveillant
    path('surveillant/modifier/<int:id>/', views.modifier_surveillant, name='modifier_surveillant'),
    # Supprimer un surveillant
    path('surveillant/supprimer/<int:id>/', views.supprimer_surveillant, name='supprimer_surveillant'),
    
    
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', views.ajouter_matiere, name='ajouter_matiere'),
    path('matieres/modifier/<int:pk>/', views.modifier_matiere, name='modifier_matiere'),
    path('matieres/supprimer/<int:pk>/', views.supprimer_matiere, name='supprimer_matiere'),
    

    path('niveaux/',  views.liste_niveaux, name='liste_niveaux'),
    path('niveaux/ajouter/',  views.ajouter_niveau, name='ajouter_niveau'),
    path('niveaux/modifier/<int:id>/',  views.modifier_niveau, name='modifier_niveau'),
    path('niveaux/supprimer/<int:id>/',  views.supprimer_niveau, name='supprimer_niveau'),
    
 
    path('salles/',  views.liste_salles, name='liste_salles'),
    path('salles/ajouter/',  views.ajouter_salle, name='ajouter_salle'),
    path('salles/modifier/<int:salle_id>/',  views.modifier_salle, name='modifier_salle'),
    path('salles/supprimer/<int:salle_id>/',  views.supprimer_salle, name='supprimer_salle'),


 
    path('classes/',  views.liste_classes, name='liste_classes'),
    path('classes/ajouter/',  views.ajouter_classe, name='ajouter_classe'),
    path('classes/modifier/<int:classe_id>/',  views.modifier_classe, name='modifier_classe'),
    path('classes/supprimer/<int:classe_id>/',  views.supprimer_classe, name='supprimer_classe'),
    path('classes/<int:classe_id>/eleves/', views.liste_eleves_par_classe, name='liste_eleves_par_classe'),
    path('classe/<int:classe_id>/pdf/', views.liste_eleves_par_classe_pdf, name='liste_eleves_par_classe_pdf'),
    path('classe/<int:classe_id>/', views.detail_classe, name='detail_classe'),
 

    path('eleves/inscription/', EleveInscriptionWizard.as_view(FORMS), name='inscription_eleve'),
    path('eleves/modifier-eleve/<int:pk>/', EleveModificationWizard.as_view(FORMS), name='modifier_eleve'),
    path('eleves/',  views.liste_eleves, name='liste_eleves'),
    path('eleve/<int:pk>/', views.eleve_delete, name='eleve_delete'),
    # path('eleves/<int:pk>/',  views.detail_eleve, name='detail_eleve'),
    # path('eleves/modifier/<int:pk>/',  views.modifier_eleve, name='modifier_eleve'),
    # path('eleves/supprimer/<int:pk>/',  views.supprimer_eleve, name='supprimer_eleve'),
    path('eleves/<int:pk>/', views.bulletin, name='detail_eleve'),
   
   
    path('semestres/',  views.liste_semestres, name='liste_semestres'),
    path('semestres/ajouter/',  views.ajouter_semestre, name='ajouter_semestre'),
    path('semestres/modifier/<int:semestre_id>/',  views.modifier_semestre, name='modifier_semestre'),
    path('semestres/supprimer/<int:semestre_id>/',  views.supprimer_semestre, name='supprimer_semestre'),
   
    path('devoirs/',  views.liste_devoirs, name='liste_devoirs'),
    path('devoirs/ajouter/',  views.ajouter_devoir, name='ajouter_devoir'),
    path('devoirs/modifier/<int:pk>/',  views.modifier_devoir, name='modifier_devoir'),
    path('devoirs/supprimer/<int:pk>/',  views.supprimer_devoir, name='supprimer_devoir'),
    
    

    path('notes/creer/', views.creer_note, name='creer_note'),
    path('notes/', views.lister_notes, name='liste_notes'),
    path('notes/modifier/<int:id>/', views.modifier_note, name='modifier_note'),
    path('notes/supprimer/<int:id>/', views.supprimer_note, name='supprimer_note'),
  
 
    #path('classes/<int:classe_id>/eleves-avec-notes/', views.liste_eleves_avec_notes, name='liste_eleves_avec_notes'),
    path('classe/<int:classe_id>/', views.notes_devoirs_view, name='notes_devoirs_classe'),
   
   # Gestion des notes de composition
   
    path('compositions/', views.liste_compositions, name='liste_compositions'),
    path('compositions/ajouter/', views.ajouter_composition, name='ajouter_composition'),
    path('compositions/modifier/<int:pk>/', views.modifier_composition, name='modifier_composition'),
    path('compositions/supprimer/<int:pk>/', views.supprimer_composition, name='supprimer_composition'),
   
   
    path('notes-composition/', views.liste_notes_composition, name='liste_notes_composition'),
    path('notes-composition/ajouter/', views.ajouter_note_composition, name='ajouter_note_composition'),
    path('notes-composition/modifier/<int:note_id>/', views.modifier_note_composition, name='modifier_note_composition'),
    path('notes-composition/supprimer/<int:pk>/', views.supprimer_note_composition, name='supprimer_note_composition'),
    path('notes-composition/get-eleves/', views.get_eleves_by_composition, name='get_eleves_by_composition'),
    path('notes-compositions/<int:classe_id>/',  views.notes_compositions_view, name='notes_compositions'),
     
     
    path('absences/', views.liste_absences, name='liste_absences'),
    path('absences/nouvelle/', views.ajouter_absence, name='ajouter_absence'),
    path('absences/<int:absence_id>/modifier/', views.modifier_absence, name='modifier_absence'),
    path('absences/<int:absence_id>/supprimer/', views.supprimer_absence, name='supprimer_absence'),
    path('get-semestres/', views.get_semestres, name='get_semestres'),
    path('get-eleves/', views.get_eleves, name='get_eleves'),
    
    path('ajax/get_classes_semestres/', views.get_classes_semestres, name='get_classes_semestres'),
    path('ajax/get_eleves/', views.get_eleves, name='get_eleves'),
    path('get-classes/', views.get_classes, name='get_classes'),
 
     

     
    path('retards', views.liste_retards, name='liste_retards'),
    path('retards/ajouter/', views.creer_retard, name='ajouter_retard'),
    path('retards/<int:retard_id>/modifier/', views.modifier_retard, name='modifier_retard'),
    path('retards/<int:retard_id>/supprimer/', views.supprimer_retard, name='supprimer_retard'),
    #path('ajax/get_classes_semestres/', views.get_classes_semestres, name='get_classes_semestres'),
    #path('ajax/get_eleves/', views.get_eleves, name='get_eleves'),
     
     
    
    

    path('ajouter-cours/', views.ajouter_cours, name='ajouter_cours'),
    path('calendrier/', views.calendrier, name='calendrier'),
    path('calendrier-cours/', views.calendrier_cours, name='calendrier_cours'),
    
   
    path('paiements/', views.liste_paiements, name='liste_paiements'),
    path('paiements/<int:pk>/', views.details_paiement, name='details_paiement'),
    path('paiements/creer/', views.creer_paiement, name='creer_paiement'),
    path('paiements/<int:pk>/modifier/', views.modifier_paiement, name='modifier_paiement'),
    path('paiements/<int:pk>/supprimer/', views.supprimer_paiement, name='supprimer_paiement'),
    path('paiements/<int:pk>/facture/', views.generate_facture_pdf, name='facture_pdf'),

    
    
     path('utilisateur/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
   # path('utilisateur/<int:pk>/supprimer/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
   
    
     path('Logout', views.logout_utilisateur, name='Logout'),
     
   path("home", views.home, name="home"),
    path('', views.login_utilisateur, name='login'),
    path('set_language/', views.set_language, name='set_language'),  # Ajoutez cette ligne
]





                                               


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)