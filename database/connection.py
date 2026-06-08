import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """
    Établit une connexion temporaire à la base de données PostgreSQL.
    Configure le cursor_factory sur RealDictCursor pour retourner des dictionnaires.
    """
    try:
        # ⚙️ CONFIGURATION TEMPORAIRE (À modifier selon vos configurations locales)
        conn = psycopg2.connect(
            host="localhost",
            database="mentorlink_db",     # Le nom de votre base de données locale
            user="postgres",              # Votre identifiant PostgreSQL
            password="votre_mot_de_passe", # Mettez votre vrai mot de passe ici
            port="5432",
            cursor_factory=RealDictCursor  # ✨ INDISPENSABLE pour la structure de vos Blueprints
        )
        return conn
        
    except Exception as e:
        # En cas d'échec, on affiche l'erreur proprement sans faire crasher Flask
        print(f"🔌 Erreur de connexion PostgreSQL : {e}")
        return None