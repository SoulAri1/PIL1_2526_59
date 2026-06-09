# -*- coding: utf-8 -*-
"""
IFRI MentorLink - Module Profil (Intégration PostgreSQL & Blueprint)
Respecte strictement le travail de formulaire et de template de l'équipe.
"""

from flask import Blueprint, render_template, request, session, redirect
# 🔌 1. Importation de la passerelle de connexion unique (PostgreSQL)
from database.connection import get_db_connection

# 🌐 2. Activation du Blueprint (on utilise profil_bp au lieu de "app")
profil_bp = Blueprint('profil', __name__)  

# Simulation de base de données locale (conservée pour la sécurité de vos tests)
profils = []

@profil_bp.route('/profil')
def accueil():
    # Note : Changé de '/' à '/profil' pour éviter les conflits de routes dans app.py
    return render_template('profil.html')


@profil_bp.route('/valider_profil', methods=['POST'])
def valider_profil():
    # 📥 3. LE TRAVAIL DE TES COLLABORATEURS (Préservé à 100%)
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    filiere = request.form.get('filiere')

    competences = request.form.getlist('competences') # Récupère le tableau des cases cochées
    lacunes = request.form.getlist('lacunes')         # Récupère le tableau des cases cochées

    # Le dictionnaire exact attendu par vos collaborateurs pour 'confirmation.html'
    profil = {
        "nom": nom,
        "prenom": prenom,
        "filiere": filiere,
        "competences": competences,
        "lacunes": lacunes
    }

    # Maintien de leur système de sauvegarde locale temporaire
    profils.append(profil)

    # 🗄️ 4. INTERACTION CHIRURGICALE AVEC POSTGRESQL (Votre schema.sql)
    conn = get_db_connection()
    
    if conn:
        cur = conn.cursor()
        try:
            # Récupération de l'ID de l'étudiant ou mentor actuellement connecté
            user_id = session.get('user_id')

            if user_id:
                # A. Mise à jour des infos générales dans la table 'utilisateurs'
                cur.execute("""
                    UPDATE utilisateurs 
                    SET nom = %s, prenom = %s, filiere = %s 
                    WHERE id = %s;
                """, (nom, prenom, filiere, user_id))

                # B. Sauvegarde des compétences (on nettoie les anciennes avant d'insérer les nouvelles)
                cur.execute("DELETE FROM competences_mentor WHERE utilisateur_id = %s;", (user_id,))
                for comp in competences:
                    cur.execute("""
                        INSERT INTO competences_mentor (utilisateur_id, nom_competence) 
                        VALUES (%s, %s);
                    """, (user_id, comp))

                # C. Sauvegarde des lacunes (on nettoie également pour éviter les doublons)
                cur.execute("DELETE FROM lacunes_mentore WHERE utilisateur_id = %s;", (user_id,))
                for lac in lacunes:
                    cur.execute("""
                        INSERT INTO lacunes_mentore (utilisateur_id, nom_lacune) 
                        VALUES (%s, %s);
                    """, (user_id, lac))

                # ⚠️ Crucial : On valide définitivement les modifications dans PostgreSQL
                conn.commit()
            else:
                print("⚠️ Profil traité en mode démo : aucun utilisateur connecté en session.")

        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde du profil dans PostgreSQL : {e}")
            conn.rollback() # Annule les requêtes en cas de bug pour protéger la base
        finally:
            cur.close()
            conn.close()
    else:
        print("🔌 Base de données injoignable. Passage transparent en mode fictif.")

    # 📤 5. RETOUR DU TEMPLATE INITIAL (Inchangé, vos fichiers HTML ne grinceront pas !)
    return render_template(
        'confirmation.html',
        profil=profil
    )