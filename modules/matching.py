# matching.py
from flask import Blueprint, render_template, session, redirect
import mysql.connector

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def faire_le_matching():
    if 'user_id' not in session:
        return redirect('/connexion')
        
    id_eleve = session['user_id']
    
    # Emplacement pour la connexion bdd du groupe
    
    
    
    # Récupération du profil de l'élève connecté.
    cursor.execute("SELECT filiere, niveau, competences_faibles, disponibilites FROM utilisateurs WHERE id_user = %s", (id_eleve,))
    eleve = cursor.fetchone()
    
    # Récupération de tous les mentors enregistrés.
    cursor.execute("SELECT id_user, nom, prenom, filiere, niveau, competences_fortes, disponibilites FROM utilisateurs WHERE role = 'mentor'")
    liste_mentors = cursor.fetchall()
    
    mentors_compatibles = []
    
    # Transformation des textes de la BDD en listes Python.
    besoins_eleve = [b.strip().lower() for b in eleve['competences_faibles'].split(',')]
    dispos_eleve = [d.strip().lower() for d in eleve['disponibilites'].split(',')]
    
    # Algorithme de matching.
    for mentor in liste_mentors:
        score = 0
        
        competences_mentor = [c.strip().lower() for c in mentor['competences_fortes'].split(',')]
        dispos_mentor = [d.strip().lower() for d in mentor['disponibilites'].split(',')]
        
        # Critère 1 : Matières communes.
        matieres_communes = []
        for matiere in besoins_eleve:
            if matiere in competences_mentor:
                score += 3
                matieres_communes.append(matiere)
                
        # Critère 2 & 3 : Filière et Niveau.
        if eleve['filiere'].lower() == mentor['filiere'].lower():
            score += 2
            
        if eleve['niveau'].lower() == mentor['niveau'].lower():
            score += 1
            
        # Critère 4 : Créneaux horaires.
        for temps in dispos_eleve:
            if temps in dispos_mentor:
                score += 1
                
        # Sélection des mentors pertinents uniquement.
        if len(matieres_communes) > 0:
            mentor['score'] = score
            mentor['communes'] = matieres_communes
            mentors_compatibles.append(mentor)
            
    # Tri décroissant selon le score.
    mentors_compatibles = sorted(mentors_compatibles, key=lambda x: x['score'], reverse=True)
    
    cursor.close()
    connex.close()
    
    return render_template('matching.html', mentors=mentors_compatibles)