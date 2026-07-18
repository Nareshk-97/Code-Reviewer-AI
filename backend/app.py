from flask import Flask
from database import get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    connection = get_db_connection()

    if connection:
        connection.close()
        return {
            "message": "✅ Connected to MySQL Database Successfully!"
        }

    return {
        "message": "❌ Failed to connect to MySQL Database."
    }

if __name__ == "__main__":
    app.run(debug=True)