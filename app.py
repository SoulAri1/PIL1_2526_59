from flask import Flask, request, render_template_string

app = Flask(__name__)

# 1. ROUTE D'AFFICHAGE (Pour tester ton formulaire sur ton PC)
@app.route('/')
def afficher_formulaire():
    # Petit HTML simple pour simuler l'interface et tester ton code
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Profil - IFRI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f6f9; }
            .form-container { background: white; padding: 25px; max-width: 450px; margin: auto; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h2 { color: #1e3a8a; }
            .btn { background-color: #2563eb; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; }
            .btn:hover { background-color: #1d4ed8; }
            label { display: block; margin-bottom: 10px; cursor: pointer; }
            select { width: 100%; padding: 8px; margin-bottom: 20px; border-radius: 4px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Mon Profil MentorLink</h2>
            <form action="/valider_profil" method="POST">
                
                <p><b>Sélectionne ta filière :</b></p>
                <select name="filiere">
                    <option value="Licence IA">Licence Intelligence Artificielle (IA)</option>
                    <option value="Licence GL">Licence Génie Logiciel (GL)</option>
                    <option value="Licence SI">Licence Systèmes d'Information (SI)</option>
                    <option value="licence SEIOT">licence systeme embarque (SEIOT)</option>
                </select>

                <p><b>Coche tes compétences (matières fortes) :</b></p>
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


# 2. TON CODE BACKEND (TA TÂCHE SPÉCIFIQUE)
@app.route('/valider_profil', methods=['POST'])
def valider_profil():
    # On attrape la filière choisie dans le menu déroulant (ex: Licence IA)
    filiere = request.form.get('filiere') 
    
    # On récupère TOUTES les cases cochées par l'étudiant pour ses compétences.
    # request.form.getlist() rassemble les choix cochés dans une liste Python[cite: 25].
    liste_competences = request.form.getlist('competences')
    
    # On fusionne la liste en une seule phrase textuelle, les éléments séparés par des virgules :
    texte_final = ", ".join(liste_competences)
    
    # --- Code de vérification visuelle (Preuve du bon fonctionnement) ---
    if not liste_competences:
        return "<h3>Erreur : Tu dois cocher au moins une compétence !</h3><a href='/'>Retour</a>"
        
    return f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 25px; border: 2px solid #bbf7d0; background-color: #f0fdf4; border-radius: 8px;">
        <h2 style="color: #166534; margin-top: 0;">Données prêtes à être envoyées en SQL !</h2>
        <p><b>1. Filière récupérée :</b> {filiere}</p>
        <p><b>2. Liste brute reçue du HTML (getlist) :</b> {liste_competences}</p>
        <p><b>3. Chaîne finale nettoyée (prête pour ton SQL) :</b> <code style="background: #e2e8f0; padding: 4px 8px; border-radius: 4px; font-weight: bold;">{texte_final}</code></p>
        <br>
        <a href="/" style="color: #2563eb; text-decoration: none; font-weight: bold;">← Tester à nouveau</a>
    </div>
    """

if __name__ == '__main__':
    # Démarre le serveur local de test
    app.run(debug=True, port=5000)
