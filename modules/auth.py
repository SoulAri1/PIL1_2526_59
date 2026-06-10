from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import get_db_connection
import secrets
import string
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        prenom = request.form.get('prenom', '').strip()
        email = request.form.get('email', '').strip().lower()
        telephone = request.form.get('telephone', '').strip()
        mot_de_passe = request.form.get('mot_de_passe', '')
        confirm_password = request.form.get('confirm_password', '')
        filiere = request.form.get('filiere', '')
        competences = request.form.getlist('competences')
        lacunes = request.form.getlist('lacunes')

        if not all([nom, prenom, email, telephone, mot_de_passe, confirm_password, filiere]):
            return render_template('register.html', erreur='Veuillez remplir tous les champs obligatoires.')

        if mot_de_passe != confirm_password:
            return render_template('register.html', erreur='Les mots de passe ne correspondent pas.')

        if len(mot_de_passe) < 6:
            return render_template('register.html', erreur='Le mot de passe doit contenir au moins 6 caractères.')

        conn = get_db_connection()
        if not conn:
            return render_template('register.html', erreur='Service temporairement indisponible.')

        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id FROM utilisateurs WHERE email = %s OR telephone = %s', (email, telephone))
            if cursor.fetchone():
                return render_template('register.html', erreur='Cet email ou téléphone est déjà utilisé.')

            password_hash = generate_password_hash(mot_de_passe)
            cursor.execute("""
                INSERT INTO utilisateurs (nom, prenom, email, telephone, mot_de_passe, filiere)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (nom, prenom, email, telephone, password_hash, filiere))
            user_id = cursor.fetchone()['id']

            # Ajout des compétences
            from modules.profil import _get_or_create_matiere
            for comp in competences:
                matiere_id = _get_or_create_matiere(cursor, comp)
                if matiere_id:
                    cursor.execute("""
                        INSERT INTO competences_mentor (utilisateur_id, matiere_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (user_id, matiere_id))

            # Ajout des lacunes
            for lac in lacunes:
                matiere_id = _get_or_create_matiere(cursor, lac)
                if matiere_id:
                    cursor.execute("""
                        INSERT INTO lacunes_mentore (utilisateur_id, matiere_id)
                        VALUES (%s, %s) ON CONFLICT DO NOTHING
                    """, (user_id, matiere_id))

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f'[AUTH] Erreur inscription : {e}')
            return render_template('register.html', erreur='Erreur lors de l\'inscription.')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('auth.login', registered=1))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        mot_de_passe = request.form.get('mot_de_passe', '')

        conn = get_db_connection()
        if not conn:
            return render_template('login.html', erreur='Service temporairement indisponible.')

        cursor = conn.cursor()
        try:
            cursor.execute('SELECT * FROM utilisateurs WHERE email = %s', (email,))
            user = cursor.fetchone()
        except Exception as e:
            print(f'[AUTH] Erreur connexion : {e}')
            return render_template('login.html', erreur='Erreur de connexion.')
        finally:
            cursor.close()
            conn.close()

        if user and check_password_hash(user['mot_de_passe'], mot_de_passe):
            session.clear()
            session['user_id'] = user['id']
            session['prenom'] = user['prenom']
            session['nom'] = user['nom']
            session['email'] = user['email']
            return redirect(url_for('dashboard.dashboard'))

        return render_template('login.html', erreur='Email ou mot de passe incorrect.')

    success = None
    if request.args.get('registered'):
        success = 'Compte créé avec succès. Connectez-vous pour continuer.'
    if request.args.get('logout'):
        success = 'Vous êtes déconnecté. À bientôt sur MentorLink.'
    if request.args.get('reset'):
        success = 'Mot de passe réinitialisé avec succès. Connectez-vous.'

    return render_template('login.html', success=success)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login', logout=1))


# ========== MOT DE PASSE OUBLIÉ ==========
def generate_reset_token():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(50))


@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        conn = get_db_connection()
        if not conn:
            flash('Service temporairement indisponible.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        cursor = conn.cursor()
        try:
            cursor.execute('SELECT id FROM utilisateurs WHERE email = %s', (email,))
            user = cursor.fetchone()

            if user:
                token = generate_reset_token()
                expires = datetime.now() + timedelta(hours=24)

                cursor.execute("""
                    UPDATE utilisateurs SET reset_token = %s, reset_token_expires = %s WHERE id = %s
                """, (token, expires, user['id']))
                conn.commit()

                # Dans une vraie application, envoyer un email
                reset_link = url_for('auth.reset_password', token=token, _external=True)
                flash(f'Lien de réinitialisation (démo) : {reset_link}', 'info')
                print(f"[AUTH] Lien reset pour {email} : {reset_link}")
            else:
                flash('Aucun compte trouvé avec cet email.', 'warning')

        except Exception as e:
            print(f'[AUTH] Erreur forgot_password: {e}')
            flash('Erreur lors de la demande.', 'danger')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('auth.login'))

    return render_template('forgot_password.html')


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_db_connection()
    if not conn:
        flash('Service temporairement indisponible.', 'danger')
        return redirect(url_for('auth.login'))

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id FROM utilisateurs 
            WHERE reset_token = %s AND reset_token_expires > %s
        """, (token, datetime.now()))
        user = cursor.fetchone()

        if not user:
            flash('Lien de réinitialisation invalide ou expiré.', 'danger')
            return redirect(url_for('auth.forgot_password'))

        if request.method == 'POST':
            mot_de_passe = request.form.get('mot_de_passe', '')
            confirm_password = request.form.get('confirm_password', '')

            if not mot_de_passe or len(mot_de_passe) < 6:
                flash('Le mot de passe doit contenir au moins 6 caractères.', 'danger')
                return render_template('reset_password.html', token=token)

            if mot_de_passe != confirm_password:
                flash('Les mots de passe ne correspondent pas.', 'danger')
                return render_template('reset_password.html', token=token)

            password_hash = generate_password_hash(mot_de_passe)
            cursor.execute("""
                UPDATE utilisateurs 
                SET mot_de_passe = %s, reset_token = NULL, reset_token_expires = NULL 
                WHERE id = %s
            """, (password_hash, user['id']))
            conn.commit()

            flash('Mot de passe réinitialisé avec succès !', 'success')
            return redirect(url_for('auth.login', reset=1))

    except Exception as e:
        print(f'[AUTH] Erreur reset_password: {e}')
        flash('Erreur lors de la réinitialisation.', 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('reset_password.html', token=token)