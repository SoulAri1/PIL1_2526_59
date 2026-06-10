import re
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from database.connection import get_db_connection
from modules.auth import login_required

matching_bp = Blueprint('matching', __name__, url_prefix='/matching')
annonces_bp = Blueprint('annonces', __name__)

def _parser_disponibilites(texte: str) -> set:
    if not texte:
        return set()
    tokens = re.split(r'[,;\n]', texte)
    return {t.strip().lower() for t in tokens if t.strip()}

def _charger_profil_courant(user_id: int) -> dict | None:
    conn = get_db_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, nom, prenom, filiere, niveau_etudes, bio, photo_profil, disponibilites FROM utilisateurs WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            return None
        profil = dict(row)
        cursor.execute("SELECT m.id, m.nom_matiere FROM competences_mentor cm JOIN matieres m ON cm.matiere_id = m.id WHERE cm.utilisateur_id = %s", (user_id,))
        profil['competences'] = [dict(r) for r in cursor.fetchall()]
        profil['competences_ids'] = {r['id'] for r in profil['competences']}
        cursor.execute("SELECT m.id, m.nom_matiere FROM lacunes_mentore lm JOIN matieres m ON lm.matiere_id = m.id WHERE lm.utilisateur_id = %s", (user_id,))
        profil['lacunes'] = [dict(r) for r in cursor.fetchall()]
        profil['lacunes_ids'] = {r['id'] for r in profil['lacunes']}
        return profil
    except Exception as e:
        print(f'[MATCHING] Erreur: {e}')
        return None
    finally:
        cursor.close()
        conn.close()

def _chercher_mentors(user_id: int, lacunes_ids: set) -> list:
    if not lacunes_ids:
        return []
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.id, u.nom, u.prenom, u.filiere, u.niveau_etudes, u.bio, u.photo_profil, u.disponibilites,
                   m.id AS matiere_id, m.nom_matiere
            FROM utilisateurs u
            JOIN competences_mentor cm ON u.id = cm.utilisateur_id
            JOIN matieres m ON m.id = cm.matiere_id
            WHERE cm.matiere_id = ANY(%s) AND u.id != %s
            ORDER BY u.id, m.nom_matiere
        """, (list(lacunes_ids), user_id))
        rows = cursor.fetchall()
        candidats = {}
        for row in rows:
            uid = row['id']
            if uid not in candidats:
                candidats[uid] = {
                    'id': uid, 'nom': row['nom'], 'prenom': row['prenom'],
                    'filiere': row['filiere'], 'niveau_etudes': row['niveau_etudes'],
                    'bio': row['bio'], 'photo_profil': row['photo_profil'],
                    'disponibilites': row['disponibilites'], 'matieres_communes': []
                }
            candidats[uid]['matieres_communes'].append({'id': row['matiere_id'], 'nom': row['nom_matiere']})
        return list(candidats.values())
    except Exception as e:
        print(f'[MATCHING] Erreur: {e}')
        return []
    finally:
        cursor.close()
        conn.close()

def _chercher_mentores(user_id: int, competences_ids: set) -> list:
    if not competences_ids:
        return []
    conn = get_db_connection()
    if not conn:
        return []
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT u.id, u.nom, u.prenom, u.filiere, u.niveau_etudes, u.bio, u.photo_profil, u.disponibilites,
                   m.id AS matiere_id, m.nom_matiere
            FROM utilisateurs u
            JOIN lacunes_mentore lm ON u.id = lm.utilisateur_id
            JOIN matieres m ON m.id = lm.matiere_id
            WHERE lm.matiere_id = ANY(%s) AND u.id != %s
            ORDER BY u.id, m.nom_matiere
        """, (list(competences_ids), user_id))
        rows = cursor.fetchall()
        candidats = {}
        for row in rows:
            uid = row['id']
            if uid not in candidats:
                candidats[uid] = {
                    'id': uid, 'nom': row['nom'], 'prenom': row['prenom'],
                    'filiere': row['filiere'], 'niveau_etudes': row['niveau_etudes'],
                    'bio': row['bio'], 'photo_profil': row['photo_profil'],
                    'disponibilites': row['disponibilites'], 'matieres_communes': []
                }
            candidats[uid]['matieres_communes'].append({'id': row['matiere_id'], 'nom': row['nom_matiere']})
        return list(candidats.values())
    except Exception as e:
        print(f'[MATCHING] Erreur: {e}')
        return []
    finally:
        cursor.close()
        conn.close()

def _scorer_et_trier_pourcentage(profil_courant: dict, candidats: list) -> list:
    """
    Calcule un score de compatibilité en POURCENTAGE (0-100%)
    Basé sur : matières communes, même filière, même niveau, disponibilités
    """
    dispos_courant = _parser_disponibilites(profil_courant.get('disponibilites', ''))
    max_points = 0
    
    for candidat in candidats:
        points = 0
        max_possible = 0
        
        # 1. Matières communes (max 60% - 3 points par matière, max 20 matières = 60 points)
        nb_matieres = len(candidat['matieres_communes'])
        points_matieres = nb_matieres * 3
        max_matieres = 60
        points += min(points_matieres, max_matieres)
        max_possible += max_matieres
        
        # 2. Même filière (20%)
        if (profil_courant.get('filiere') or '').strip().lower() == (candidat.get('filiere') or '').strip().lower():
            points += 20
        max_possible += 20
        
        # 3. Même niveau d'études (10%)
        if (profil_courant.get('niveau_etudes') or '').strip().lower() == (candidat.get('niveau_etudes') or '').strip().lower():
            points += 10
        max_possible += 10
        
        # 4. Disponibilités communes (10% - 1 point par créneau, max 10)
        dispos_candidat = _parser_disponibilites(candidat.get('disponibilites', ''))
        creneaux_communs = dispos_courant & dispos_candidat
        points_creneaux = min(len(creneaux_communs), 10)
        points += points_creneaux
        max_possible += 10
        
        # Calcul du pourcentage
        pourcentage = int((points / max_possible) * 100) if max_possible > 0 else 0
        
        candidat['compatibilite'] = pourcentage
        candidat['matieres_communes'] = candidat['matieres_communes']
        candidat['creneaux_communs'] = sorted(creneaux_communs)
        candidat['nb_matieres_communes'] = nb_matieres
    
    return sorted(candidats, key=lambda c: c['compatibilite'], reverse=True)

@matching_bp.route('/')
@login_required
def faire_le_matching():
    user_id = session['user_id']
    profil = _charger_profil_courant(user_id)
    if profil is None:
        flash("Impossible d'accéder à votre profil.", 'danger')
        return render_template('matching.html', profil=None, erreur='db_error', resultats=[], mode=None, peut_etre_mentore=False, peut_etre_mentor=False)
    
    peut_etre_mentore = bool(profil['lacunes_ids'])
    peut_etre_mentor = bool(profil['competences_ids'])
    
    if not peut_etre_mentore and not peut_etre_mentor:
        return render_template('matching.html', profil=profil, erreur='profil_incomplet', resultats=[], mode=None, peut_etre_mentore=False, peut_etre_mentor=False)
    
    mode_defaut = 'mentore' if peut_etre_mentore else 'mentor'
    mode = request.args.get('mode', mode_defaut)
    if mode not in ('mentore', 'mentor'):
        mode = mode_defaut
    
    if mode == 'mentore' and peut_etre_mentore:
        candidats = _chercher_mentors(user_id, profil['lacunes_ids'])
    elif mode == 'mentor' and peut_etre_mentor:
        candidats = _chercher_mentores(user_id, profil['competences_ids'])
    else:
        candidats = []
    
    resultats = _scorer_et_trier_pourcentage(profil, candidats)[:20]
    
    return render_template('matching.html', profil=profil, mode=mode, resultats=resultats, peut_etre_mentore=peut_etre_mentore, peut_etre_mentor=peut_etre_mentor, erreur=None)

@matching_bp.route('/contacter/<int:cible_id>', methods=['POST'])
@login_required
def contacter_utilisateur(cible_id: int):
    expediteur_id = session['user_id']
    if cible_id == expediteur_id:
        flash("Vous ne pouvez pas vous contacter vous-même.", 'warning')
        return redirect(url_for('matching.faire_le_matching'))
    
    message_perso = request.form.get('message_perso', '').strip()
    prenom_exp = session.get('prenom', 'Un étudiant')
    nom_exp = session.get('nom', '')
    intro = f"📚 Demande de mentorat via IFRI MentorLink\nDe : {prenom_exp} {nom_exp}\n\n"
    corps = message_perso if message_perso else "Bonjour, j'ai vu votre profil sur MentorLink et je souhaite vous contacter pour du mentorat."
    contenu = intro + corps
    
    conn = get_db_connection()
    if not conn:
        flash("Service indisponible.", 'danger')
        return redirect(url_for('matching.faire_le_matching'))
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id FROM utilisateurs WHERE id = %s', (cible_id,))
        if not cursor.fetchone():
            flash("Utilisateur introuvable.", 'warning')
            return redirect(url_for('matching.faire_le_matching'))
        
        cursor.execute("INSERT INTO messages (expediteur_id, destinataire_id, contenu) VALUES (%s, %s, %s)", (expediteur_id, cible_id, contenu))
        conn.commit()
        flash("Votre demande de contact a bien été envoyée !", 'success')
    except Exception as e:
        conn.rollback()
        print(f'[MATCHING] Erreur: {e}')
        flash("Erreur lors de l'envoi.", 'danger')
    finally:
        cursor.close()
        conn.close()
    
    return redirect(url_for('matching.faire_le_matching'))

@annonces_bp.route('/annonces')
@login_required
def liste():
    return redirect(url_for('matching.faire_le_matching'))