from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1. Route pour afficher un formulaire de test simple
@app.route('/')
def afficher_formulaire():
    # Ce code HTML permet de tester directement ton code Python
    html_formulaire = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Profil - IFRI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f3f4f6; }
            .card { background: white; padding: 24px; max-width: 500px; margin: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            h2 { color: #1e3a8a; }
            .btn { background-color: #2563eb; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
            .btn:hover { background-color: #1d4ed8; }
            label { display: block; margin-bottom: 8px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Mon Profil MentorLink</h2>
            <form action="/valider_profil" method="POST">
                
                <p><b>1. Choisis ta filière :</b></p>
                <select name="filiere" style="width: 100%; padding: 8px; margin-bottom: 20px;">
                    <option value="Licence IA">Licence Intelligence Artificielle (IA)</option>
                    <option value="Licence GL">Licence Génie Logiciel (GL)</option>
                    <option value="Licence IM">Licence Informatique Médicale (IM)</option>
                </select>

                <p><b>2. Coche tes compétences (matières fortes) :</b></p>
                <label><input type="checkbox" name="competences" value="Algorithmique"> Algorithmique</label>
                <label><input type="checkbox" name="competences" value="Programmation Python"> Programmation Python</label>
                <label><input type="checkbox" name="competences" value="Bases de donnees"> Bases de Données & SQL</label>
                <label><input type="checkbox" name="competences" value="Developpement Web"> Développement Web</label>
                
                <br>
                <button type="submit" class="btn">Valider mon profil</button>
            </form>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_formulaire)


# 2. TON CODE BACKEND (REPRISE ET ENRICHISSEMENT DE TA ROUTE)
@app.route('/valider_profil', methods=['POST'])
def valider_profil():
    # On attrape la filière choisie (ex: Licence IA)
    filiere = request.form.get('filiere') 
    
    # On récupère toutes les cases cochées par l'étudiant pour ses compétences :
    liste_competences = request.form.getlist('competences')
    
    # On fusionne la liste en une seule phrase textuelle séparée par des virgules :
    texte_final = ", ".join(liste_competences)
    
    # --- Code de vérification visuelle pour ton évaluation ---
    if not liste_competences:
        return "<h3>Erreur : Tu dois cocher au moins une compétence !</h3><a href='/'>Retour</a>"
        
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 40px auto; padding: 20px; border: 1px solid #green; background-color: #f0fdf4; border-radius: 8px;">
        <h2 style="color: #166534;">Données prêtes à être envoyées en SQL !</h2>
        <p><b>Filière attrapée :</b> {filiere}</p>
        <p><b>Liste Python brute (getlist) :</b> {liste_competences}</p>
        <p><b>Texte final fusionné (pour ton SQL) :</b> <code style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px;">{texte_final}</code></p>
        <br>
        <a href="/" style="color: #2563eb; text-decoration: none; font-weight: bold;">← Tester à nouveau</a>
    </div>
    """

if __name__ == '__main__':
    # Lance le serveur local sur le port 5000
    app.run(debug=True, port=5000)
