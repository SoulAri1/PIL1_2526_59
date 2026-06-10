from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_socketio import SocketIO, join_room

from modules.auth import auth_bp
from modules.profil import profil_bp
from modules.matching import matching_bp, annonces_bp
from modules.messagerie import messagerie_bp
from modules.dashboard import dashboard_bp
from modules.annonces import annonces_bp as annonces_module_bp

app = Flask(__name__)
app.secret_key = "mentorlink_ifri_2026"   # ← BIEN ÉCRIRE secret_key

# Configuration pour l'upload de fichiers
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=60, ping_interval=25)

# Enregistrement des blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(profil_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(annonces_bp)
app.register_blueprint(messagerie_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(annonces_module_bp)

@app.context_processor
def inject_current_user():
    if session.get('user_id'):
        return {
            'current_user': {
                'id': session['user_id'],
                'prenom': session.get('prenom', ''),
                'nom': session.get('nom', ''),
                'email': session.get('email', ''),
            }
        }
    return {'current_user': None}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposer_avis', methods=['GET', 'POST'])
def deposer_avis():
    if request.method == 'POST':
        nom = request.form.get('nom_complet', '').strip()
        filiere = request.form.get('filiere', '').strip()
        message = request.form.get('message_avis', '').strip()
        if nom and filiere and message:
            flash('Merci pour votre témoignage !', 'success')
        else:
            flash('Veuillez remplir tous les champs.', 'warning')
    return redirect(url_for('index') + '#avis')

@socketio.on('join')
def handle_join(data):
    user_id = data.get('user_id')
    if user_id:
        join_room(str(user_id))
        print(f"[SOCKET] Utilisateur {user_id} a rejoint sa room")

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)