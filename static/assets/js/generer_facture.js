// Charger la bibliothèque jsPDF
const script = document.createElement('script');
script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
script.onload = function () {
  // Attacher l'événement au bouton "Générer une Facture"
  document.getElementById('generer-facture').addEventListener('click', function () {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Titre de la facture
    doc.setFontSize(18);
    doc.text("Facture de Paiement", 10, 10);

    // Informations de l'élève
    doc.setFontSize(12);
    doc.text(`Élève : ${"{{ paiement.eleve.nom }} {{ paiement.eleve.prenom }}"}`, 10, 20);
    doc.text(`Classe : ${"{{ paiement.eleve.classe.nom }}"}`, 10, 30);

    // Informations du paiement
    doc.text(`Référence : ${"{{ paiement.reference }}"}`, 10, 40);
    doc.text(`Date de Paiement : ${"{{ paiement.date_paiement|date:'d/m/Y' }}"}`, 10, 50);
    doc.text(`Statut : ${"{{ paiement.get_statut_display }}"}`, 10, 60);
    doc.text(`Montant : ${"{{ paiement.montant }} €"}`, 10, 70);
    doc.text(`Plan de Paiement : ${"{{ paiement.get_plan_paiement_display }}"}`, 10, 80);
    doc.text(`Mois/Année : ${"{{ paiement.mois_annee }}"}`, 10, 90);

    // Commentaires
    doc.text(`Commentaires : ${"{{ paiement.commentaires|default:'Aucun commentaire' }}"}`, 10, 100);

    // Enregistrer le PDF
    doc.save(`Facture_{{ paiement.reference }}.pdf`);
  });
};
document.head.appendChild(script);