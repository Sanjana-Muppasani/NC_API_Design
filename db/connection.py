import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

def get_db_connection():
  
    if os.getenv("ENV") == "test":
        database_url = os.getenv("TEST_DATABASE_URL")
    else:
        database_url = os.getenv("DATABASE_URL")
        
    conn = psycopg2.connect(database_url)
    return conn