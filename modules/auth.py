from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        mot_de_passe = request.form.get('mot_de_passe')

        password_hash = generate_password_hash(mot_de_passe)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM utilisateurs WHERE email=%s", (email,))
        exist = cursor.fetchone()

        if exist:
            return render_template("register.html", erreur="Email déjà utilisé")

        cursor.execute("""
            INSERT INTO utilisateurs (nom, prenom, email, telephone, mot_de_passe)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, prenom, email, telephone, password_hash))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM utilisateurs WHERE email=%s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['mot_de_passe'], mot_de_passe):

            session.clear()

            session['user_id'] = user['id']
            session['prenom'] = user['prenom']

            return redirect(url_for('dashboard.dashboard'))

        return render_template("login.html", erreur="Identifiants incorrects")

    return render_template("login.html")


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))