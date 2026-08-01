from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.review import review
import os

app = Flask(__name__)

# Allow requests from any origin
CORS(app)

# Home route
@app.route("/")
def home():
    return {
        "status": "success",
        "message": "Code Reviewer AI Backend is Running 🚀"
    }

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(review)

print(app.url_map)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)