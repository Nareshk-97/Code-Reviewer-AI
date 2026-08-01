import psycopg2
from config import DATABASE_URL


def get_db_connection():
    try:
        connection = psycopg2.connect(DATABASE_URL)
        print("✅ Connected to PostgreSQL Database")
        return connection

    except Exception as err:
        print(f"❌ Database Connection Error: {err}")
        return None