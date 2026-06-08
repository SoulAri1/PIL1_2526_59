<<<<<<< Updated upstream
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    try:
        # 🚀 Remplace par ta vraie chaîne URI Supabase (onglet URI dans les paramètres)
        # N'oublie pas d'y inscrire ton mot de passe réel au milieu !
        SUPABASE_URL = "postgresql://postgres:Groupe59@ifri@db.sgsxtkrrsddomjhlehjj.supabase.co:5432/postgres"
        
        conn = psycopg2.connect(
            SUPABASE_URL,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à Supabase : {e}")
        return None
=======
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Miclette2@08",
        database="mentorlink"
    )
>>>>>>> Stashed changes
