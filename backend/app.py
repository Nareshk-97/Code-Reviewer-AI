from flask import Flask, jsonify
from flask_cors import CORS

from config import FRONTEND_URL

from routes.auth import auth
from routes.review import review
from routes.history import history

from utils.rate_limiter import limiter

import os


app = Flask(__name__)


# ==========================================
# RATE LIMITER
# ==========================================

limiter.init_app(app)


# ==========================================
# REQUEST SIZE LIMIT
# ==========================================

# Maximum HTTP request size = 2 MB
#
# The /review endpoint separately limits
# code itself to 100,000 characters.
#
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024


# ==========================================
# CORS CONFIGURATION
# ==========================================

# Allow requests only from the configured
# frontend application.
#
# FRONTEND_URL is loaded from .env
#
CORS(
    app,
    resources={
        r"/*": {
            "origins": FRONTEND_URL
        }
    },
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
)


# ==========================================
# HOME ROUTE
# ==========================================

@app.route("/")
def home():

    return {
        "status": "success",
        "message": "Code Reviewer AI Backend is Running"
    }


# ==========================================
# SAFE API ERROR HANDLERS
# ==========================================

@app.errorhandler(400)
def bad_request(error):

    return jsonify({
        "success": False,
        "message": "Bad request."
    }), 400


@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "success": False,
        "message": "Endpoint not found."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):

    return jsonify({
        "success": False,
        "message": "HTTP method not allowed."
    }), 405


@app.errorhandler(413)
def request_too_large(error):

    return jsonify({
        "success": False,
        "message": "Request payload is too large."
    }), 413


@app.errorhandler(429)
def rate_limit_exceeded(error):

    return jsonify({
        "success": False,
        "message": "Too many requests. Please try again later."
    }), 429


@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({
        "success": False,
        "message": "Internal server error."
    }), 500


# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

app.register_blueprint(auth)
app.register_blueprint(review)
app.register_blueprint(history)





# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )