from flask import Blueprint, render_template

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def afficher_matching():
    
    # [ ZONE DE DONNÉES SIMULÉES (Mock Data)]
    # Ici on peut modifier les matières ou les jours pour tester l'algo.
    # Plus tard, le Membre 4 (BDA) te dira comment remplacer ça par de vraies requêtes SQL.
    
    mock_eleve = {
        "besoins": ["Python", "Maths"],
        "disponibilites": ["Lundi", "Mercredi"],
        "filiere": "Intelligence Artificielle",
        "niveau_valeur": 1
    }
    
    mock_mentors = [
        {
            "nom": "Ariel Dev",
            "competences": ["Python", "Maths", "SQL"],
            "disponibilites": ["Lundi", "Vendredi"],
            "filiere": "Sécurité Informatique",
            "niveau_valeur": 3
        },
        {
            "nom": "Jean Code",
            "competences": ["Maths", "Physique"],
            "disponibilites": ["Mardi", "Jeudi"],
            "filiere": "Intelligence Artificielle",
            "niveau_valeur": 2
        }
    ]
    
   
    # [ L'Application de l'algo sur chaque mentor ]
   
    resultats = []
    for mentor in mock_mentors:
       # Appel de la fonction exacte écrite juste en dessous
        score = calculer_score_matching(mock_eleve, mentor)
        
        # Dictionnaire propre pour le HTML avec le mentor et son score
        resultats.append({
            "details": mentor,
            "score_match": score
        })
        
    # [💡 ZONE D'AMÉLIORATION PERSO] : Tri automatique du plus grand au plus petit score
    # Si tu l'enlèves, les mentors s'afficheront juste dans l'ordre du tableau.
    resultats = sorted(resultats, key=lambda x: x['score_match'], reverse=True)

    # Envoie de la liste 'resultats' au fichier HTML sous le nom 'matchs'
    return render_template('matching.html', matchs=resultats)


def calculer_score_matching(eleve, mentor):
    
    score_total = 0

    # CRITÈRE 1 : Les Matières / Compétences (Max : 40 points)
    besoins_eleve = eleve.get('besoins', [])
    competences_mentor = mentor.get('competences', [])
    
    if len(besoins_eleve) > 0:
        matieres_communes = 0
        for matiere in besoins_eleve:
            if matiere in competences_mentor:
                matieres_communes = matieres_communes + 1
        
        score_matieres = (matieres_communes / len(besoins_eleve)) * 40
        score_total = score_total + score_matieres

    # CRITÈRE 2 : Les Horaires / Dispos (Max : 30 points)
    dispos_eleve = eleve.get('disponibilites', [])      
    dispos_mentor = mentor.get('disponibilites', [])    
    
    if len(dispos_eleve) > 0:
        jours_communs = 0
        for jour in dispos_eleve:
            if jour in dispos_mentor:
                jours_communs = jours_communs + 1
                
        if jours_communs > 0:
            score_total = score_total + 30

    # CRITÈRE 3 : Filière et Niveau d'études (Max : 30 points)
    if eleve.get('filiere') == mentor.get('filiere'):
        score_total = score_total + 15
        
    if mentor.get('niveau_valeur') >= eleve.get('niveau_valeur'):
        score_total = score_total + 15

    return round(score_total, 2)