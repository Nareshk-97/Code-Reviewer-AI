from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.review import review
import os

app = Flask(__name__)

# ==========================
# CORS Configuration
# ==========================

CORS(
    app,
    resources={
        r"/*": {
            "origins": "*"
        }
    },
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)


# ==========================
# Home Route
# ==========================

@app.route("/")
def home():
    return {
        "status": "success",
        "message": "Code Reviewer AI Backend is Running 🚀"
    }


# ==========================
# Register Blueprints
# ==========================

app.register_blueprint(auth)
app.register_blueprint(review)


# ==========================
# Debug Routes
# ==========================

print(app.url_map)


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )