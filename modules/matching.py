from flask import Blueprint, render_template, jsonify

# Création du module pour l'algo
matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def afficher_matching():
    """Route principale pour afficher les mentors recommandés"""
    # 1. Plus tard, tu récupéreras ici l'ID de l'étudiant connecté
    # 2. Tu appelleras la fonction de calcul
    # 3. Tu renverras les résultats à la page HTML
    return render_template('matching.html')

def calculer_score_matching(besoins_eleve, competences_mentor):
    """
    L'algorithme de matching :
    Compare deux listes et retourne un score sur 100
    """
    if not besoins_eleve:
        return 0
        
    matieres_communes = set(besoins_eleve).intersection(set(competences_mentor))
    score = (len(matieres_communes) / len(besoins_eleve)) * 100
    return round(score, 2)