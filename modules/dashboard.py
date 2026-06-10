# -*- coding: utf-8 -*-
"""
IFRI MentorLink - Module Dashboard
"""

from flask import Blueprint, render_template
from database.connection import get_db_connection
from modules.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Données par défaut
    stats_plateforme = {
        "total_etudiants": 0,
        "total_mentors": 0,
        "demandes_attente": 0,
        "taux_reussite": "0%"
    }
    recents_suivis = []

    conn = get_db_connection()
    
    if conn:
        cur = conn.cursor()
        try:
            # Total étudiants
            cur.execute("SELECT COUNT(DISTINCT utilisateur_id) AS total FROM lacunes_mentore;")
            result = cur.fetchone()
            stats_plateforme["total_etudiants"] = result['total'] if result else 0

            # Total mentors
            cur.execute("SELECT COUNT(DISTINCT utilisateur_id) AS total FROM competences_mentor;")
            result = cur.fetchone()
            stats_plateforme["total_mentors"] = result['total'] if result else 0

            # Demandes en attente
            cur.execute("SELECT COUNT(*) AS total FROM annonces WHERE type_annonce = 'DEMANDE' AND statut = 'ACTIF';")
            result = cur.fetchone()
            stats_plateforme["demandes_attente"] = result['total'] if result else 0

            # Dernières demandes
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
            recents_suivis = cur.fetchall()

        except Exception as e:
            print(f"[DB] Erreur dashboard: {e}")
        finally:
            cur.close()
            conn.close()
    else:
        print("[DB] Base inaccessible. Mode démo.")

    return render_template('dashboard.html', stats=stats_plateforme, suivis=recents_suivis)