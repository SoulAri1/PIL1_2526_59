import psycopg2
from psycopg2.extras import RealDictCursor
import urllib.parse
import time

def get_db_connection(max_retries=2, timeout=10):
    raw_password = "#AZERTY1234#123"
    safe_password = urllib.parse.quote_plus(raw_password)   
    
    SUPABASE_URL = f"postgresql://postgres.rptdkboacucrzotrzqvo:{safe_password}@aws-0-eu-west-1.pooler.supabase.com:6543/postgres"
    
    for attempt in range(max_retries + 1):
        try:
            conn = psycopg2.connect(
                SUPABASE_URL,
                cursor_factory=RealDictCursor,
                connect_timeout=timeout
            )
            return conn
        except Exception as e:
            print(f"[DB] Tentative {attempt+1}/{max_retries+1} échouée : {e}")
            if attempt < max_retries:
                time.sleep(1)
            else:
                print(f"[DB] Erreur de connexion à Supabase après {max_retries+1} tentatives : {e}")
                return None
    return None