from flask import Flask, render_template
from flask_socketio import SocketIO
from modules.auth import auth_bp
from modules.profil import profil_bp
from modules.matching import matching_bp
from modules.messagerie import messagerie_bp
from modules.dashboard import dashboard_bp  # 1. IMPORTATION DU NOUVEAU BLUEPRINT

app = Flask(__name__)
app.secret_key = "mentorlink_ifri_2026"
socketio = SocketIO(app, cors_allowed_origins="*")

# Enregistrement des différents modules (Blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(profil_bp)
app.register_blueprint(matching_bp)
app.register_blueprint(messagerie_bp)
app.register_blueprint(dashboard_bp)  # 2. ENREGISTREMENT DU BLUEPRINT

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)