import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        if connection.is_connected():
            print("✅ Connected to MySQL Database")

        return connection

    except mysql.connector.Error as err:
        print(f"❌ Database Connection Error: {err}")
        return None