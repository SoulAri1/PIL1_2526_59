# =============================================================
# MODULE : messagerie.py
# Blueprint Flask pour la messagerie instantanée — MentorLink
# Auteur : Membre 7 | Projet IFRI 2025-2026
# =============================================================

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import psycopg2
import psycopg2.extras  # Pour récupérer les résultats sous forme de dictionnaires

# --- Création du Blueprint "messagerie" ---
# Ce blueprint sera enregistré dans app.py via : app.register_blueprint(messagerie_bp)
messagerie_bp = Blueprint('messagerie', __name__)


# --------------------------------------------------------------
# UTILITAIRE : Connexion à la base de données PostgreSQL
# --------------------------------------------------------------
def get_db_connection():
    # On établit la connexion avec les paramètres du projet
    conn = psycopg2.connect(
        host="localhost",
        database="IFRI_MentorLink",   # Nom de la BDD créée par le Membre 4
        user="postgres",              # Adapter selon votre configuration
        password="votre_mot_de_passe" # Adapter selon votre configuration
    )
    # cursor_factory=RealDictCursor permet d'accéder aux colonnes par leur nom
    # Ex: message['contenu'] au lieu de message[1]
    conn.cursor_factory = psycopg2.extras.RealDictCursor
    return conn


# --------------------------------------------------------------
# UTILITAIRE : Vérifier si l'utilisateur est bien connecté
# Retourne True si la session contient un user_id valide
# --------------------------------------------------------------
def utilisateur_connecte():
    return 'user_id' in session and session['user_id'] is not None


# --------------------------------------------------------------
# ROUTE PRINCIPALE : /chat/<destinataire_id>
# GET  → Charge et affiche l'historique de la conversation
# POST → Enregistre un nouveau message et redirige (pattern PRG)
# --------------------------------------------------------------
@messagerie_bp.route('/chat/<int:destinataire_id>', methods=['GET', 'POST'])
def chat(destinataire_id):

    # Sécurité : on vérifie que l'utilisateur est connecté
    # L'id de session est fourni par le Membre 2 lors de la connexion
    if not utilisateur_connecte():
        flash("Veuillez vous connecter pour accéder à la messagerie.", "warning")
        return redirect(url_for('auth.connexion'))

    # On récupère l'identifiant de l'utilisateur actuellement connecté
    expediteur_id = session['user_id']

    # On empêche un utilisateur d'envoyer un message à lui-même
    if expediteur_id == destinataire_id:
        flash("Vous ne pouvez pas vous envoyer un message à vous-même.", "danger")
        return redirect(url_for('annonces.liste'))

    conn = get_db_connection()
    cur = conn.cursor()

    # ---- TRAITEMENT POST : Enregistrement d'un nouveau message ----
    if request.method == 'POST':
        contenu = request.form.get('contenu', '').strip()

        # On n'enregistre que si le message n'est pas vide
        if contenu:
            # Insertion dans la table "messages" du Membre 4
            # date_envoi est automatique grâce à DEFAULT CURRENT_TIMESTAMP
            cur.execute(
                """
                INSERT INTO messages (expediteur_id, destinataire_id, contenu)
                VALUES (%s, %s, %s)
                """,
                (expediteur_id, destinataire_id, contenu)
            )
            conn.commit()  # On valide l'insertion en base de données
        else:
            flash("Le message ne peut pas être vide.", "warning")

        cur.close()
        conn.close()

        # Pattern PRG (Post/Redirect/Get) : on redirige pour éviter
        # la duplication du message si l'utilisateur recharge la page
        return redirect(url_for('messagerie.chat', destinataire_id=destinataire_id))

    # ---- CHARGEMENT GET : Historique et profil du destinataire ----

    # On récupère le profil complet du destinataire (Membre 3 gère ces données)
    cur.execute(
        """
        SELECT id, prenom, nom, filiere, niveau_etudes, photo_profil, bio
        FROM utilisateurs
        WHERE id = %s
        """,
        (destinataire_id,)
    )
    destinataire = cur.fetchone()  # Un seul résultat attendu

    # Si le destinataire n'existe pas dans la base, on renvoie une erreur
    if not destinataire:
        cur.close()
        conn.close()
        flash("Cet utilisateur n'existe pas.", "danger")
        return redirect(url_for('annonces.liste'))

    # On charge l'historique complet de la conversation entre les deux utilisateurs
    # Les messages sont triés du plus ancien au plus récent pour l'affichage
    cur.execute(
        """
        SELECT
            m.id,
            m.contenu,
            m.date_envoi,
            m.expediteur_id,
            u.prenom || ' ' || u.nom AS nom_expediteur,
            u.photo_profil AS photo_expediteur
        FROM messages m
        JOIN utilisateurs u ON u.id = m.expediteur_id
        WHERE
            (m.expediteur_id = %s AND m.destinataire_id = %s)
            OR
            (m.expediteur_id = %s AND m.destinataire_id = %s)
        ORDER BY m.date_envoi ASC
        """,
        (expediteur_id, destinataire_id, destinataire_id, expediteur_id)
    )
    messages = cur.fetchall()  # Liste de tous les messages de la conversation

    cur.close()
    conn.close()

    # On envoie les données au template Jinja2 pour affichage
    return render_template(
        'chat.html',
        messages=messages,              # Historique de la conversation
        destinataire=destinataire,      # Profil du mentor/mentoré en face
        expediteur_id=expediteur_id     # Pour distinguer "mes" messages des autres
    )


# --------------------------------------------------------------
# ROUTE BONUS : /conversations
# Affiche la liste de toutes les conversations de l'utilisateur
# --------------------------------------------------------------
@messagerie_bp.route('/conversations')
def liste_conversations():

    # Sécurité : vérification de la connexion
    if not utilisateur_connecte():
        flash("Veuillez vous connecter.", "warning")
        return redirect(url_for('auth.connexion'))

    user_id = session['user_id']
    conn = get_db_connection()
    cur = conn.cursor()

    # On récupère la liste des personnes avec qui l'utilisateur a échangé
    # On prend le dernier message de chaque conversation pour l'aperçu
    cur.execute(
        """
        SELECT DISTINCT ON (interlocuteur_id)
            interlocuteur_id,
            u.prenom || ' ' || u.nom AS nom_interlocuteur,
            u.photo_profil,
            u.filiere,
            m.contenu AS dernier_message,
            m.date_envoi AS date_dernier_message
        FROM (
            SELECT
                CASE WHEN expediteur_id = %s THEN destinataire_id ELSE expediteur_id END AS interlocuteur_id,
                contenu, date_envoi
            FROM messages
            WHERE expediteur_id = %s OR destinataire_id = %s
        ) m
        JOIN utilisateurs u ON u.id = m.interlocuteur_id
        ORDER BY interlocuteur_id, date_envoi DESC
        """,
        (user_id, user_id, user_id)
    )
    conversations = cur.fetchall()

    cur.close()
    conn.close()

    # On envoie la liste au template de la boîte de réception
    return render_template('conversations.html', conversations=conversations)
