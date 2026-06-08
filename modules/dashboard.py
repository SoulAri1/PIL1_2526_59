<<<<<<< Updated upstream
# -*- coding: utf-8 -*-
"""
IFRI MentorLink - Module Dashboard (Adapté au Schema PostgreSQL)
Développé dans le dossier modules/
"""

from flask import Blueprint, render_template, session, redirect
# Importation de la passerelle de connexion créée par le Membre 4
from database.connection import get_db_connection

# Création du Blueprint pour le dashboard
=======
from flask import Blueprint, render_template, session, redirect, url_for
from database.connection import get_db_connection

>>>>>>> Stashed changes
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
<<<<<<< Updated upstream
    # 1. VOS DONNÉES FICTIVES DE BASE (Sécurité et démo)
    stats_plateforme = {
        "total_etudiants": 142,
        "total_mentors": 38,
        "demandes_attente": 15,
        "taux_reussite": "94%"
    }

    recents_suivis = [
        {"etudiant": "Salem PRADA", "filiere": "Intelligence Artificielle", "mentor": "Dr. Lawson", "statut": "Actif"},
        {"etudiant": "Placide PANDORE", "filiere": "Génie Logiciel", "mentor": "Mme. Tossou", "statut": "En attente"},
        {"etudiant": "Dolorès MAHUTIN", "filiere": "Sécurité Réseaux", "mentor": "M. Kodjo", "statut": "Actif"},
    ]

    # 2. CONNEXION ET REQUÊTES SUR VOTRE SCHEMA REEL
    conn = get_db_connection()
    
    if conn:
        cur = conn.cursor()
        try:
            # 📊 REQUÊTE 1 : Compter les étudiants (utilisateurs ayant enregistré des lacunes)
            cur.execute("SELECT COUNT(DISTINCT utilisateur_id) AS total FROM lacunes_mentore;")
            vrai_total_etudiants = cur.fetchone()['total']

            # 📊 REQUÊTE 2 : Compter les mentors (utilisateurs ayant enregistré des compétences)
            cur.execute("SELECT COUNT(DISTINCT utilisateur_id) AS total FROM competences_mentor;")
            vrai_total_mentors = cur.fetchone()['total']

            # 📊 REQUÊTE 3 : Compter les demandes en attente (Annonces de type DEMANDE et toujours ACTIF)
            cur.execute("""
                SELECT COUNT(*) AS total 
                FROM annonces 
                WHERE type_annonce = 'DEMANDE' AND statut = 'ACTIF';
            """)
            vraies_demandes_attente = cur.fetchone()['total']

            # 📋 REQUÊTE 4 : Récupérer les dernières annonces de demandes pour le tableau
            # On fait une jointure (JOIN) avec la table utilisateurs pour récupérer le Nom et Prénom
            cur.execute("""
                SELECT 
                    (u.nom || ' ' || u.prenom) AS etudiant,
                    u.filiere AS filiere,
                    'Non assigné' AS mentor,
                    a.statut AS statut
                FROM annonces a
                JOIN utilisateurs u ON a.utilisateur_id = u.id
                WHERE a.type_annonce = 'DEMANDE'
                ORDER BY a.date_publication DESC
                LIMIT 5;
            """)
            vrais_suivis = cur.fetchall() # Liste de dicts grâce à RealDictCursor

            # --- FUSION DES STRATES DE DONNÉES ---
            stats_plateforme["total_etudiants"] += vrai_total_etudiants
            stats_plateforme["total_mentors"] += vrai_total_mentors
            stats_plateforme["demandes_attente"] += vraies_demandes_attente
            
            if vrais_suivis:
                # Les vraies données de PostgreSQL s'empilent au-dessus des fausses
                recents_suivis = vrais_suivis + recents_suivis

        except Exception as e:
            print(f"⚠️ Erreur lors de l'exécution des requêtes SQL : {e}")
            print("Affichage des données fictives par défaut.")
        finally:
            cur.close()
            conn.close()
    else:
        print("🔌 Base PostgreSQL inaccessible. Mode données fictives activé.")

    # Renvoi des données unifiées au template HTML
    return render_template('dashboard.html', stats=stats_plateforme, suivis=recents_suivis)
=======

    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('auth.login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM utilisateurs WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM matieres")
    matieres = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dashboard.html", user=user, matieres=matieres)
>>>>>>> Stashed changes
