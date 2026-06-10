import os
from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from database.connection import get_db_connection
from modules.auth import login_required

profil_bp = Blueprint('profil', __name__)
profils = []

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _get_or_create_matiere(cursor, nom_matiere: str):
    nom = nom_matiere.strip() if nom_matiere else ''
    if not nom:
        return None
    cursor.execute('SELECT id FROM matieres WHERE nom_matiere = %s', (nom,))
    row = cursor.fetchone()
    if row:
        return row['id']
    cursor.execute('INSERT INTO matieres (nom_matiere) VALUES (%s) RETURNING id', (nom,))
    return cursor.fetchone()['id']

def _charger_profil_db(user_id: int):
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, nom, prenom, email, telephone, filiere, niveau_etudes, 
                   bio, centres_interet, photo_profil, disponibilites 
            FROM utilisateurs WHERE id = %s
        """, (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        profil = dict(row)
        
        cursor.execute("""
            SELECT m.nom_matiere FROM competences_mentor cm 
            JOIN matieres m ON cm.matiere_id = m.id WHERE cm.utilisateur_id = %s
        """, (user_id,))
        profil['competences'] = [r['nom_matiere'] for r in cursor.fetchall()]
        
        cursor.execute("""
            SELECT m.nom_matiere FROM lacunes_mentore lm 
            JOIN matieres m ON lm.matiere_id = m.id WHERE lm.utilisateur_id = %s
        """, (user_id,))
        profil['lacunes'] = [r['nom_matiere'] for r in cursor.fetchall()]
        
        return profil
    except Exception as e:
        print(f'[PROFIL] Erreur: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

@profil_bp.route('/profil')
@login_required
def accueil():
    return render_template('profil.html', profil=_charger_profil_db(session['user_id']), lecture_seule=False)

@profil_bp.route('/mon_profil')
@login_required
def mon_profil():
    return render_template('profil.html', profil=_charger_profil_db(session['user_id']), lecture_seule=False)

@profil_bp.route('/voir/<int:user_id>')
@login_required
def voir_profil(user_id):
    profil_cible = _charger_profil_db(user_id)
    if not profil_cible:
        return redirect(url_for('matching.faire_le_matching'))
    return render_template('profil.html', profil=profil_cible, lecture_seule=True)

@profil_bp.route('/valider_profil', methods=['POST'])
@login_required
def valider_profil():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    filiere = request.form.get('filiere')
    bio = request.form.get('bio', '')
    centres_interet = request.form.get('centres_interet', '')
    competences = request.form.getlist('competences')
    lacunes = request.form.getlist('lacunes')
    
    # Gestion de la photo de profil
    photo_profil = None
    if 'photo_profil' in request.files:
        file = request.files['photo_profil']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(f"{session['user_id']}_{file.filename}")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            photo_profil = filename
    
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            user_id = session['user_id']
            
            # Mise à jour des infos générales
            if photo_profil:
                cur.execute("""
                    UPDATE utilisateurs 
                    SET nom = %s, prenom = %s, filiere = %s, bio = %s, centres_interet = %s, photo_profil = %s 
                    WHERE id = %s
                """, (nom, prenom, filiere, bio, centres_interet, photo_profil, user_id))
            else:
                cur.execute("""
                    UPDATE utilisateurs 
                    SET nom = %s, prenom = %s, filiere = %s, bio = %s, centres_interet = %s 
                    WHERE id = %s
                """, (nom, prenom, filiere, bio, centres_interet, user_id))
            
            # Compétences
            cur.execute("DELETE FROM competences_mentor WHERE utilisateur_id = %s", (user_id,))
            for comp in competences:
                matiere_id = _get_or_create_matiere(cur, comp)
                if matiere_id:
                    cur.execute("""
                        INSERT INTO competences_mentor (utilisateur_id, matiere_id) 
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (user_id, matiere_id))
            
            # Lacunes
            cur.execute("DELETE FROM lacunes_mentore WHERE utilisateur_id = %s", (user_id,))
            for lac in lacunes:
                matiere_id = _get_or_create_matiere(cur, lac)
                if matiere_id:
                    cur.execute("""
                        INSERT INTO lacunes_mentore (utilisateur_id, matiere_id) 
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (user_id, matiere_id))
            
            conn.commit()
        except Exception as e:
            print(f'[PROFIL] Erreur sauvegarde: {e}')
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    
    return redirect(url_for('matching.faire_le_matching'))