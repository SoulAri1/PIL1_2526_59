from flask import Blueprint
profil_bp = Blueprint('profil', __name__)
# Routes de profil a completer
from flask import Flask, render_template, request

app = Flask(__name__)

# Simulation de base de données(inserer la base de donnee)
profils = []

@app.route('/')
def accueil():
    return render_template('profil.html')


@app.route('/valider_profil', methods=['POST'])
def valider_profil():

    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    filiere = request.form.get('filiere')

    competences = request.form.getlist('competences')
    lacunes = request.form.getlist('lacunes')

    profil = {
        "nom": nom,
        "prenom": prenom,
        "filiere": filiere,
        "competences": competences,
        "lacunes": lacunes
    }

    profils.append(profil)

    return render_template(
        'confirmation.html',
        profil=profil
    )


if __name__ == '__main__':
    app.run(debug=True)