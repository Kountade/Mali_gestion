from application.models import Eleve, Matiere, NoteDevoir, NoteComposition, MoyenneSemestre
from django.db.models import Avg

from django.db.models import Avg
from .models import NoteDevoir, NoteComposition

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

from django.db.models import Avg
from .models import NoteDevoir, NoteComposition

def calculer_moyenne_matiere(eleve, matiere, semestre):
    # Récupérer la moyenne des notes de devoirs pour la matière et le semestre donnés
    notes_devoirs = NoteDevoir.objects.filter(
        eleve=eleve,
        devoir__matiere=matiere,
        devoir__semestre=semestre
    ).aggregate(Avg('note'))['note__avg'] or 0

    # Récupérer la note de composition pour la matière et le semestre donnés
    note_composition = NoteComposition.objects.filter(
        eleve=eleve,
        composition__matiere=matiere,
        composition__semestre=semestre
    ).aggregate(Avg('note'))['note__avg'] or 0

    # Calculer la moyenne de la matière en pondérant les notes
    # Par exemple, les devoirs comptent pour 40% et la composition pour 60%
    moyenne_matiere = (notes_devoirs * 0.4 + note_composition * 0.6)

    return round(moyenne_matiere, 2)


def attribuer_moyennes_et_rangs(classe, semestre):
    eleves = Eleve.objects.filter(classe=classe)
    resultats = []

    for eleve in eleves:
        moyenne = calculer_moyenne_eleve(eleve, semestre)  # Utilisation de la fonction
        resultats.append((eleve, moyenne))

    # Classement des élèves en fonction de la moyenne
    resultats = sorted(resultats, key=lambda x: x[1], reverse=True)
    rangs = {eleve.id: i + 1 for i, (eleve, _) in enumerate(resultats)}

    return rangs


from django.db.models import Avg
from .models import Eleve, NoteDevoir, NoteComposition

def calculer_rang_matiere(eleve, matiere, semestre):
    # Récupérer tous les élèves de la classe
    eleves_classe = Eleve.objects.filter(classe=eleve.classe)

    # Liste pour stocker les moyennes de chaque élève dans cette matière
    moyennes_eleves = []

    for eleve_classe in eleves_classe:
        # Calculer la moyenne de la matière pour chaque élève
        notes_devoirs = NoteDevoir.objects.filter(
            eleve=eleve_classe,
            devoir__matiere=matiere,
            devoir__semestre=semestre
        ).aggregate(Avg('note'))['note__avg'] or 0

        notes_composition = NoteComposition.objects.filter(
            eleve=eleve_classe,
            composition__matiere=matiere,
            composition__semestre=semestre
        ).aggregate(Avg('note'))['note__avg'] or 0

        moyenne_matiere = (notes_devoirs * 2 + notes_composition * 3) / 5  # Moyenne pondérée
        moyennes_eleves.append((eleve_classe.id, moyenne_matiere))

    # Trier les élèves par moyenne décroissante
    moyennes_eleves.sort(key=lambda x: x[1], reverse=True)

    # Trouver le rang de l'élève
    for i, (id_eleve, moyenne) in enumerate(moyennes_eleves):
        if id_eleve == eleve.id:
            return i + 1  # Rang commence à 1

    return 0  # Si l'élève n'est pas trouvé



def determiner_appreciation(moyenne):
    if moyenne >= 18:
        return "Performance remarquable"
    elif moyenne >= 16:
        return "Excellent niveau"
    elif moyenne >= 14:
        return "Très bon travail"
    elif moyenne >= 12:
        return "Bon travail"
    elif moyenne >= 10:
        return "Résultats satisfaisants"
    elif moyenne >= 8:
        return "Travail passable"
    elif moyenne >= 6:
        return "Des progrès timides"
    elif moyenne >= 4:
        return "Niveau faible"
    elif moyenne >= 2:
        return "Travail très insuffisant"
    else:
        return "Niveau alarmant"