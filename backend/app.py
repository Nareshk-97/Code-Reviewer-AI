from flask import Flask
from flask_cors import CORS
from routes.auth import auth
from routes.review import review
import os

app = Flask(__name__)

# Allow requests from any origin during development.
# Before production, replace "*" with your Vercel frontend URL if you want to restrict access.
CORS(app)

app.register_blueprint(auth)
app.register_blueprint(review)

print(app.url_map)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)