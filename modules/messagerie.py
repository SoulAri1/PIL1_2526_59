from functools import wraps
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from database.connection import get_db_connection

messagerie_bp = Blueprint('messagerie', __name__, url_prefix='/messagerie')

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter", "warning")
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


# ========== ROUTE 1 : ENVOYER UN MESSAGE ==========
@messagerie_bp.route('/api/envoyer', methods=['POST'])
@login_required
def api_envoyer_message():
    """Envoi de message"""
    try:
        expediteur_id = session['user_id']
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'erreur': 'Données invalides'}), 400
        
        destinataire_id = data.get('destinataire_id')
        contenu = data.get('contenu', '').strip()
        
        if not destinataire_id:
            return jsonify({'success': False, 'erreur': 'Destinataire manquant'}), 400
        
        if not contenu:
            return jsonify({'success': False, 'erreur': 'Message vide'}), 400
        
        if len(contenu) > 2000:
            return jsonify({'success': False, 'erreur': 'Message trop long (max 2000 caractères)'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'erreur': 'Base de données indisponible'}), 500
        
        cur = conn.cursor()
        
        # Vérifier que le destinataire existe
        cur.execute("SELECT id FROM utilisateurs WHERE id = %s", (destinataire_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({'success': False, 'erreur': 'Destinataire introuvable'}), 404
        
        # Insérer le message
        cur.execute("""
            INSERT INTO messages (expediteur_id, destinataire_id, contenu) 
            VALUES (%s, %s, %s) 
            RETURNING id, date_envoi
        """, (expediteur_id, destinataire_id, contenu))
        
        nouveau = cur.fetchone()
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({
            'success': True, 
            'message_id': nouveau['id'],
            'date_envoi': nouveau['date_envoi'].isoformat()
        }), 200
        
    except Exception as e:
        print(f"[MESSAGERIE] Erreur API envoyer: {e}")
        return jsonify({'success': False, 'erreur': str(e)}), 500


# ========== ROUTE 2 : HISTORIQUE DES MESSAGES ==========
@messagerie_bp.route('/api/historique', methods=['GET'])
@login_required
def get_historique():
    """Récupère l'historique des messages avec un utilisateur"""
    expediteur_id = session['user_id']
    avec_id = request.args.get('avec', type=int)
    
    if not avec_id:
        return jsonify({'success': False, 'erreur': 'Paramètre "avec" manquant'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'erreur': 'Base indisponible'}), 500
    
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT m.id, m.contenu, m.date_envoi, m.expediteur_id, m.destinataire_id
            FROM messages m
            WHERE (m.expediteur_id = %s AND m.destinataire_id = %s)
               OR (m.expediteur_id = %s AND m.destinataire_id = %s)
            ORDER BY m.date_envoi ASC
        """, (expediteur_id, avec_id, avec_id, expediteur_id))
        
        messages = cur.fetchall()
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        return jsonify({'success': False, 'erreur': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ========== ROUTE 3 : NOUVEAUX MESSAGES (POLLING) ==========
@messagerie_bp.route('/api/nouveaux_messages', methods=['GET'])
@login_required
def get_nouveaux_messages():
    """Récupère les nouveaux messages depuis un certain ID"""
    expediteur_id = session['user_id']
    depuis = request.args.get('depuis', 0, type=int)
    avec_id = request.args.get('avec', type=int)
    
    if not avec_id:
        return jsonify({'success': False, 'erreur': 'Paramètre "avec" manquant'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'erreur': 'Base indisponible'}), 500
    
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT m.id, m.contenu, m.date_envoi, m.expediteur_id, m.destinataire_id
            FROM messages m
            WHERE m.id > %s
              AND ((m.expediteur_id = %s AND m.destinataire_id = %s)
                OR (m.expediteur_id = %s AND m.destinataire_id = %s))
            ORDER BY m.date_envoi ASC
        """, (depuis, expediteur_id, avec_id, avec_id, expediteur_id))
        
        messages = cur.fetchall()
        return jsonify({'success': True, 'messages': messages})
    except Exception as e:
        return jsonify({'success': False, 'erreur': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# ========== ROUTE 4 : LISTE DES CONVERSATIONS ==========
@messagerie_bp.route('/conversations')
@login_required
def liste_conversations():
    user_id = session['user_id']
    conn = get_db_connection()
    conversations = []
    
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT DISTINCT ON (interlocuteur_id)
                    CASE 
                        WHEN expediteur_id = %s THEN destinataire_id
                        ELSE expediteur_id
                    END AS interlocuteur_id,
                    u.prenom || ' ' || u.nom AS nom_interlocuteur,
                    u.photo_profil,
                    m.contenu AS dernier_message,
                    m.date_envoi
                FROM messages m
                JOIN utilisateurs u ON u.id = (
                    CASE 
                        WHEN m.expediteur_id = %s THEN m.destinataire_id
                        ELSE m.expediteur_id
                    END
                )
                WHERE m.expediteur_id = %s OR m.destinataire_id = %s
                ORDER BY interlocuteur_id, m.date_envoi DESC
            """, (user_id, user_id, user_id, user_id))
            conversations = cur.fetchall()
        except Exception as e:
            print(f"[MESSAGERIE] Erreur conversations: {e}")
        finally:
            cur.close()
            conn.close()
    
    # Si requête AJAX pour la sidebar
    if request.args.get('partial') == '1':
        from flask import render_template_string
        sidebar_html = '''
        <div id="sidebarConversationsList">
        {% for conv in conversations %}
        <a href="{{ url_for('messagerie.chat', destinataire_id=conv.interlocuteur_id) }}" class="conversation-item">
            <div class="conv-meta">
                <div class="conv-name">{{ conv.nom_interlocuteur }}</div>
                <div class="conv-preview">{{ conv.dernier_message[:50] }}</div>
            </div>
        </a>
        {% endfor %}
        </div>
        '''
        return render_template_string(sidebar_html, conversations=conversations)
    
    if conversations:
        return redirect(url_for('messagerie.chat', destinataire_id=conversations[0]['interlocuteur_id']))
    
    flash("Aucune conversation", "info")
    return redirect(url_for('matching.faire_le_matching'))


# ========== ROUTE 5 : PAGE DU CHAT ==========
@messagerie_bp.route('/chat/<int:destinataire_id>')
@login_required
def chat(destinataire_id):
    expediteur_id = session['user_id']
    
    if expediteur_id == destinataire_id:
        flash("Vous ne pouvez pas discuter avec vous-même", "warning")
        return redirect(url_for('messagerie.liste_conversations'))
    
    conn = get_db_connection()
    if not conn:
        flash("Service indisponible", "danger")
        return redirect(url_for('dashboard.dashboard'))
    
    cur = conn.cursor()
    
    # Récupérer le destinataire
    cur.execute("SELECT id, prenom, nom, filiere, photo_profil FROM utilisateurs WHERE id = %s", (destinataire_id,))
    destinataire = cur.fetchone()
    
    if not destinataire:
        cur.close()
        conn.close()
        flash("Utilisateur introuvable", "danger")
        return redirect(url_for('messagerie.liste_conversations'))
    
    # Récupérer les messages
    cur.execute("""
        SELECT m.id, m.contenu, m.date_envoi, m.expediteur_id,
               u.prenom || ' ' || u.nom AS nom_expediteur
        FROM messages m
        JOIN utilisateurs u ON u.id = m.expediteur_id
        WHERE (m.expediteur_id = %s AND m.destinataire_id = %s)
           OR (m.expediteur_id = %s AND m.destinataire_id = %s)
        ORDER BY m.date_envoi ASC
    """, (expediteur_id, destinataire_id, destinataire_id, expediteur_id))
    messages = cur.fetchall()
    
    # Récupérer les conversations pour la sidebar
    cur.execute("""
        SELECT DISTINCT ON (interlocuteur_id)
            CASE 
                WHEN expediteur_id = %s THEN destinataire_id
                ELSE expediteur_id
            END AS interlocuteur_id,
            u.prenom || ' ' || u.nom AS nom_interlocuteur,
            u.photo_profil,
            m.contenu AS dernier_message
        FROM messages m
        JOIN utilisateurs u ON u.id = (
            CASE 
                WHEN m.expediteur_id = %s THEN m.destinataire_id
                ELSE m.expediteur_id
            END
        )
        WHERE m.expediteur_id = %s OR m.destinataire_id = %s
        ORDER BY interlocuteur_id, m.date_envoi DESC
    """, (expediteur_id, expediteur_id, expediteur_id, expediteur_id))
    conversations = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template('chat.html', 
                         messages=messages, 
                         destinataire=destinataire, 
                         expediteur_id=expediteur_id,
                         conversations=conversations)


# ========== ROUTE 6 : TEST ==========
@messagerie_bp.route('/api/test', methods=['GET'])
def test_api():
    """Route de test pour vérifier que l'API fonctionne"""
    return jsonify({'status': 'ok', 'message': 'L\'API messagerie fonctionne correctement'})