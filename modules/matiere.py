from flask import Blueprint, request, redirect, url_for, session
from database.connection import get_db_connection

matiere_bp = Blueprint('matiere', __name__, url_prefix='/matiere')


# =========================
# AJOUT COMPETENCE
# =========================
@matiere_bp.route('/competence/<int:matiere_id>')
def ajouter_competence(matiere_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO competences_mentor (utilisateur_id, matiere_id)
            VALUES (%s, %s)
        """, (user_id, matiere_id))

        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('dashboard.dashboard'))


# =========================
# AJOUT LACUNE
# =========================
@matiere_bp.route('/lacune/<int:matiere_id>')
def ajouter_lacune(matiere_id):

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO lacunes_mentore (utilisateur_id, matiere_id)
            VALUES (%s, %s)
        """, (user_id, matiere_id))

        conn.commit()

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('dashboard.dashboard'))


# =========================
# LISTE MATIERES (OPTIONNEL)
# =========================
@matiere_bp.route('/liste')
def liste_matieres():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM matieres")
    matieres = cursor.fetchall()

    cursor.close()
    conn.close()

    return {"matieres": matieres}