from flask import Flask, render_template, request

app = Flask(__name__)

# Simulation d'une base de données
profils = []

@app.route('/')
def accueil():
    return render_template('profil.html')


@app.route('/valider_profil', methods=['POST'])
def valider_profil():

    # Informations personnelles
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    filiere = request.form.get('filiere')

    # Récupération des compétences cochées
    competences = request.form.getlist('competences')

    # Récupération des lacunes cochées
    lacunes = request.form.getlist('lacunes')

    # Transformation en texte lisible
    competences_txt = ", ".join(competences)
    lacunes_txt = ", ".join(lacunes)

    # Création du profil
    profil = {
        "nom": nom,
        "prenom": prenom,
        "filiere": filiere,
        "competences": competences_txt,
        "lacunes": lacunes_txt
    }

    # Sauvegarde
    profils.append(profil)

    return f"""
    <h2>Profil enregistré avec succès</h2>

    <p><b>Nom :</b> {nom}</p>
    <p><b>Prénom :</b> {prenom}</p>
    <p><b>Filière :</b> {filiere}</p>

    <p><b>Compétences :</b> {competences_txt}</p>

    <p><b>Lacunes :</b> {lacunes_txt}</p>
    """


if __name__ == '__main__':
    app.run(debug=True)
