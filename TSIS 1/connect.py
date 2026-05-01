import psycopg2
from db_config import DB_CONFIG
def get_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(e)
        return None
