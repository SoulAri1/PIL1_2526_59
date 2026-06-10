from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from database.connection import get_db_connection
from modules.auth import login_required

annonces_bp = Blueprint('annonces_module', __name__, url_prefix='/annonces')

@annonces_bp.route('/')
@login_required
def index():
    """Page principale des annonces"""
    user_id = session['user_id']
    conn = get_db_connection()
    
    offres = []
    demandes = []
    
    if conn:
        cur = conn.cursor()
        try:
            # Récupérer les offres actives
            cur.execute("""
                SELECT a.id, a.type_annonce, a.format_mentorat, a.date_publication, a.statut,
                       u.id as utilisateur_id, u.nom, u.prenom, u.filiere, u.photo_profil,
                       array_agg(m.nom_matiere) as matieres
                FROM annonces a
                JOIN utilisateurs u ON a.utilisateur_id = u.id
                LEFT JOIN annonces_matieres am ON a.id = am.annonce_id
                LEFT JOIN matieres m ON am.matiere_id = m.id
                WHERE a.statut = 'ACTIF'
                GROUP BY a.id, u.id, u.nom, u.prenom, u.filiere, u.photo_profil
                ORDER BY a.date_publication DESC
            """)
            all_annonces = cur.fetchall()
            
            offres = [a for a in all_annonces if a['type_annonce'] == 'OFFRE' and a['utilisateur_id'] != user_id]
            demandes = [a for a in all_annonces if a['type_annonce'] == 'DEMANDE' and a['utilisateur_id'] != user_id]
            
            # Mes annonces
            cur.execute("""
                SELECT a.id, a.type_annonce, a.format_mentorat, a.date_publication, a.statut,
                       array_agg(m.nom_matiere) as matieres
                FROM annonces a
                LEFT JOIN annonces_matieres am ON a.id = am.annonce_id
                LEFT JOIN matieres m ON am.matiere_id = m.id
                WHERE a.utilisateur_id = %s
                GROUP BY a.id
                ORDER BY a.date_publication DESC
            """, (user_id,))
            mes_annonces = cur.fetchall()
            
        except Exception as e:
            print(f"[ANNONCES] Erreur: {e}")
            offres, demandes, mes_annonces = [], [], []
        finally:
            cur.close()
            conn.close()
    else:
        offres, demandes, mes_annonces = [], [], []
    
    return render_template('annonces.html', offres=offres, demandes=demandes, mes_annonces=mes_annonces)


@annonces_bp.route('/publier', methods=['POST'])
@login_required
def publier():
    """Publier une nouvelle annonce"""
    user_id = session['user_id']
    type_annonce = request.form.get('type_annonce')
    format_mentorat = request.form.get('format_mentorat')
    matieres = request.form.getlist('matieres')
    
    if not type_annonce or not format_mentorat or not matieres:
        flash('Veuillez remplir tous les champs.', 'danger')
        return redirect(url_for('annonces_module.index'))
    
    conn = get_db_connection()
    if not conn:
        flash('Service indisponible.', 'danger')
        return redirect(url_for('annonces_module.index'))
    
    cur = conn.cursor()
    try:
        # Insérer l'annonce
        cur.execute("""
            INSERT INTO annonces (utilisateur_id, type_annonce, format_mentorat, statut)
            VALUES (%s, %s, %s, 'ACTIF') RETURNING id
        """, (user_id, type_annonce, format_mentorat))
        annonce_id = cur.fetchone()['id']
        
        # Lier les matières
        for matiere_nom in matieres:
            cur.execute("SELECT id FROM matieres WHERE nom_matiere = %s", (matiere_nom,))
            matiere = cur.fetchone()
            if matiere:
                cur.execute("""
                    INSERT INTO annonces_matieres (annonce_id, matiere_id) VALUES (%s, %s)
                """, (annonce_id, matiere['id']))
        
        conn.commit()
        flash('Annonce publiée avec succès !', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ANNONCES] Erreur publication: {e}")
        flash('Erreur lors de la publication.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('annonces_module.index'))


@annonces_bp.route('/supprimer/<int:annonce_id>', methods=['POST'])
@login_required
def supprimer(annonce_id):
    """Supprimer une annonce"""
    user_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        flash('Service indisponible.', 'danger')
        return redirect(url_for('annonces_module.index'))
    
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM annonces WHERE id = %s AND utilisateur_id = %s", (annonce_id, user_id))
        conn.commit()
        flash('Annonce supprimée.', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ANNONCES] Erreur suppression: {e}")
        flash('Erreur lors de la suppression.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('annonces_module.index'))


@annonces_bp.route('/repondre/<int:annonce_id>', methods=['POST'])
@login_required
def repondre(annonce_id):
    """Répondre à une annonce (crée une conversation)"""
    expediteur_id = session['user_id']
    message_perso = request.form.get('message_perso', '').strip()
    
    conn = get_db_connection()
    if not conn:
        flash('Service indisponible.', 'danger')
        return redirect(url_for('annonces_module.index'))
    
    cur = conn.cursor()
    try:
        # Récupérer le propriétaire de l'annonce
        cur.execute("SELECT utilisateur_id FROM annonces WHERE id = %s", (annonce_id,))
        annonce = cur.fetchone()
        
        if not annonce:
            flash('Annonce introuvable.', 'danger')
            return redirect(url_for('annonces_module.index'))
        
        destinataire_id = annonce['utilisateur_id']
        
        if expediteur_id == destinataire_id:
            flash('Vous ne pouvez pas répondre à votre propre annonce.', 'warning')
            return redirect(url_for('annonces_module.index'))
        
        # Créer un message
        prenom_exp = session.get('prenom', 'Un étudiant')
        nom_exp = session.get('nom', '')
        contenu = f"📢 Réponse à votre annonce\nDe : {prenom_exp} {nom_exp}\n\n{message_perso if message_perso else 'Je suis intéressé par votre annonce.'}"
        
        cur.execute("""
            INSERT INTO messages (expediteur_id, destinataire_id, contenu)
            VALUES (%s, %s, %s)
        """, (expediteur_id, destinataire_id, contenu))
        conn.commit()
        
        flash('Votre réponse a été envoyée !', 'success')
    except Exception as e:
        conn.rollback()
        print(f"[ANNONCES] Erreur réponse: {e}")
        flash('Erreur lors de l\'envoi.', 'danger')
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('annonces_module.index'))