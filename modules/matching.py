from flask import Blueprint, render_template

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def afficher_matching():
    # Reste ainsi pour l'instant, le temps de lier le HTML et la base de données
    return render_template('matching.html')


def calculer_score_matching(eleve, mentor):
    """ Calcule un score global sur 100 basé sur 3 critères :
    - Matières (40 points)
    - Horaires (30 points)
    - Niveau/Filière (30 points) """
    score_total = 0

    # CRITÈRE 1 : Les Matières / Compétences (Max : 40 points)
   
    besoins_eleve = eleve.get('besoins', [])
    competences_mentor = mentor.get('competences', [])
    
    if len(besoins_eleve) > 0:
        matieres_communes = 0
        for matiere in besoins_eleve:
            if matiere in competences_mentor:
                matieres_communes = matieres_communes + 1
        
        # On calcule les points sur 40
        score_matieres = (matieres_communes / len(besoins_eleve)) * 40
        score_total = score_total + score_matieres


    # CRITÈRE 2 : Les Horaires / Dispos (Max : 30 points)

    dispos_eleve = eleve.get('disponibilites', [])      # Ex: ["Lundi", "Mercredi"]
    dispos_mentor = mentor.get('disponibilites', [])    # Ex: ["Lundi", "Vendredi"]
    
    if len(dispos_eleve) > 0:
        jours_communs = 0
        for jour in dispos_eleve:
            if jour in dispos_mentor:
                jours_communs = jours_communs + 1
                
        # On calcule les points sur 30 (s'ils ont au moins 1 jour en commun)
        if jours_communs > 0:
            score_total = score_total + 30

   
    # CRITÈRE 3 : Filière et Niveau d'études (Max : 30 points)
   
    # Si même filière = 15 points
    if eleve.get('filiere') == mentor.get('filiere'):
        score_total = score_total + 15
        
    # Si le mentor a un niveau supérieur ou égal à l'élève = 15 points
    if mentor.get('niveau_valeur') >= eleve.get('niveau_valeur'):
        score_total = score_total + 15

    # On renvoie le score final arrondi à deux décimales
    return round(score_total, 2)