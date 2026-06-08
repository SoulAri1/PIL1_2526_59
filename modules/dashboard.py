# -*- coding: utf-8 -*-
"""
IFRI MentorLink - Module Dashboard
Développé dans le dossier modules/
"""

from flask import Blueprint, render_template, session, redirect

# Création du Blueprint pour le dashboard
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    # Exemple de sécurité : décommenter si vous voulez restreindre l'accès
    # if 'user_id' not in session:
    #     return redirect('/login')

    # Données statiques temporaires (à lier plus tard à la base de données)
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

    return render_template('dashboard.html', stats=stats_plateforme, suivis=recents_suivis)