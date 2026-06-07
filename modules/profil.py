from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# On suppose que get_db_connection est défini dans ton module de configuration de base de données
from database import get_db_connection 

# Instanciation du Blueprint avec le préfixe strict
profil_bp = Blueprint('profil', __name__, url_prefix='/profil')

# Liste officielle des matières enseignées à l'IFRI d'après la fiche de cours
LISTE_MATIERES = [
    "Algorithmique",
    "Développement web",
    "Théorie des bases de données et algèbre relationnelle / SQL",
    "Programmation Python"
]

@profil_bp.route('/modifier', methods=['GET'])
def modifier_profil():
    """
    Route principale (GET) : Extrait les informations de l'étudiant connecté
    et les injecte dans le formulaire d'édition.
    """
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour accéder à cette page.", "danger")
        return redirect(url_for('auth.connexion')) # À adapter selon votre route d'auth

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Extraction de la filière et du niveau de l'étudiant
    cursor.execute("SELECT filiere, niveau FROM users WHERE id = %s;", (user_id,))
    user_data = cursor.fetchone()

    # Si le curseur ne retourne pas de dictionnaire, on gère les index (ex: user_data[0])
    # On initialise un dictionnaire pour faciliter le passage au template Jinja2
    user = {
        'filiere': user_data[0] if user_data else None,
        'niveau': user_data[1] if user_data else None
    }

    # 2. Extraction des compétences acquises (Points Forts) depuis la table pivot
    cursor.execute("SELECT matiere FROM user_competences WHERE user_id = %s;", (user_id,))
    competences = [row[0] for row in cursor.fetchall()]

    # 3. Extraction des lacunes (Matières à améliorer) depuis la table pivot
    cursor.execute("SELECT matiere FROM user_lacunes WHERE user_id = %s;", (user_id,))
    lacunes = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    # On passe toutes les données extraites au template enfant
    return render_template(
        'profil.html', 
        user=user, 
        competences=competences, 
        lacunes=lacunes, 
        liste_matieres=LISTE_MATIERES
    )


@profil_bp.route('/modifier', methods=['POST'])
def mettre_a_jour_profil():
    """
    Route de mise à jour (POST) : Nettoie et met à jour les tables de profils
    et les tables pivots associés à l'utilisateur.
    """
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.connexion'))

    # Récupération des données scalaires du formulaire
    filiere = request.form.get('filiere')
    niveau = request.form.get('niveau')

    # Récupération des listes de choix multiples (notation par tableau côté HTML)
    matieres_fortes = request.form.getlist('matieres_fortes')
    matieres_faibles = request.form.getlist('matieres_faibles')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Mise à jour des informations générales de l'étudiant
        cursor.execute(
            "UPDATE users SET filiere = %s, niveau = %s WHERE id = %s;",
            (filiere, niveau, user_id)
        )

        # 2. NETTOYAGE ET MISE À JOUR DE LA TABLE PIVOT : COMPÉTENCES (Points forts)
        cursor.execute("DELETE FROM user_competences WHERE user_id = %s;", (user_id,))
        for matiere in matieres_fortes:
            cursor.execute(
                "INSERT INTO user_competences (user_id, matiere) VALUES (%s, %s);",
                (user_id, matiere)
            )

        # 3. NETTOYAGE ET MISE À JOUR DE LA TABLE PIVOT : LACUNES (Points faibles)
        cursor.execute("DELETE FROM user_lacunes WHERE user_id = %s;", (user_id,))
        for matiere in matieres_faibles:
            cursor.execute(
                "INSERT INTO user_lacunes (user_id, matiere) VALUES (%s, %s);",
                (user_id, matiere)
            )

        # Validation de la transaction globale
        conn.commit()
        flash("Votre profil a été mis à jour avec succès !", "success")

    except Exception as e:
        # En cas de problème, on annule les modifications pour préserver l'intégrité de la BD
        conn.rollback()
        flash(f"Une erreur système est survenue : {e}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('profil.modifier_profil'))