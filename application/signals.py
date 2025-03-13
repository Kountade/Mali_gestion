from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import Eleve, AnneeScolaire, Classe

# Signal qui se déclenche après la création ou modification d'un élève
@receiver(post_save, sender=Eleve)
def update_effectif_and_nombre_eleves_on_add(sender, instance, created, **kwargs):
    if created:  # Se déclenche uniquement lors de la création
        # Met à jour le nombre d'élèves pour l'année scolaire
        annee_scolaire = instance.annee_scolaire
        annee_scolaire.nombre_eleves = Eleve.objects.filter(annee_scolaire=annee_scolaire).count()
        annee_scolaire.save()

        # Met à jour l'effectif de la classe
        classe = instance.classe
        classe.effectif = Eleve.objects.filter(classe=classe).count()
        classe.save()

# Signal qui se déclenche avant la suppression d'un élève
@receiver(pre_delete, sender=Eleve)
def update_effectif_and_nombre_eleves_on_delete(sender, instance, **kwargs):
    # Avant la suppression, on met à jour le nombre d'élèves pour l'année scolaire
    annee_scolaire = instance.annee_scolaire
    annee_scolaire.nombre_eleves = Eleve.objects.filter(annee_scolaire=annee_scolaire).count() - 1
    annee_scolaire.save()

    # On met à jour l'effectif de la classe
    classe = instance.classe
    classe.effectif = Eleve.objects.filter(classe=classe).count() - 1
    classe.save()
