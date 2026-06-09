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
    cursor.execute("SELECT filiere, niveau_etudes, disponibilites FROM utilisateurs WHERE id = %s", (id_eleve,))
    eleve = cursor.fetchone()
    
    # Récupération des ID des matières que l'élève veut travailler (ses lacunes).
    cursor.execute("SELECT matiere_id FROM lacunes_mentore WHERE utilisateur_id = %s", (id_eleve,))
    lacunes_tuples = cursor.fetchall()
    id_lacunes_eleve = [row['matiere_id'] for row in lacunes_tuples]
    
    # Si l'élève n'a enregistré aucune lacune, le matching s'arrête.
    if not id_lacunes_eleve:
        return render_template('matching.html', mentors=[])

    # Récupération de tous les autres utilisateurs pour trouver les mentors.
    cursor.execute("SELECT id, nom, prenom, filiere, niveau_etudes, disponibilites FROM utilisateurs WHERE id != %s", (id_eleve,))
    liste_utilisateurs = cursor.fetchall()
    
    mentors_compatibles = []
    
    # Découpage des disponibilités de l'élève.
    dispos_eleve = [d.strip().lower() for d in eleve['disponibilites'].split(',')] if eleve['disponibilites'] else []
    
    # Algorithme de matching.
    for user in liste_utilisateurs:
        score = 0
        
        # Récupération des compétences de cet utilisateur.
        cursor.execute("SELECT matiere_id FROM competences_mentor WHERE utilisateur_id = %s", (user['id'],))
        competences_tuples = cursor.fetchall()
        id_competences_mentor = [row['matiere_id'] for row in competences_tuples]
        
        # Critère 1 : Matières communes (recherche d'intersections).
        matieres_communes_id = []
        for id_mat in id_lacunes_eleve:
            if id_mat in id_competences_mentor:
                score += 3
                matieres_communes_id.append(id_mat)
                
        # Si cet utilisateur n'a aucune matière correspondant aux besoins, on passe au suivant.
        if not matieres_communes_id:
            continue
            
        # Récupération des vrais noms des matières communes pour l'affichage HTML.
        format_strings = ','.join(['%s'] * len(matieres_communes_id))
        cursor.execute(f"SELECT nom_matiere FROM matieres WHERE id IN ({format_strings})", tuple(matieres_communes_id))
        nom_matieres_tuples = cursor.fetchall()
        noms_communs = [row['nom_matiere'] for row in nom_matieres_tuples]
        
        # Critère 2 : Même filière.
        if eleve['filiere'] and user['filiere'] and eleve['filiere'].lower() == user['filiere'].lower():
            score += 2
            
        # Critère 3 : Même niveau d'études.
        if eleve['niveau_etudes'] and user['niveau_etudes'] and eleve['niveau_etudes'].lower() == user['niveau_etudes'].lower():
            score += 1
            
        # Critère 4 : Créneaux horaires communs.
        if user['disponibilites']:
            dispos_mentor = [d.strip().lower() for d in user['disponibilites'].split(',')]
            for temps in dispos_eleve:
                if temps in dispos_mentor:
                    score += 1
                    
        # Stockage des données du mentor.
        user['score'] = score
        user['communes'] = noms_communs
        mentors_compatibles.append(user)
            
    # Tri décroissant selon le score.
    mentors_compatibles = sorted(mentors_compatibles, key=lambda x: x['score'], reverse=True)
    
    cursor.close()
    connex.close()
    
    return render_template('matching.html', mentors=mentors_compatibles)