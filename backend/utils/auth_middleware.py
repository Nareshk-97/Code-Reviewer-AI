from functools import wraps
from flask import request, jsonify
import jwt
from config import JWT_SECRET_KEY

def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if "Authorization" in request.headers:

            auth_header = request.headers["Authorization"]

            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({
                "success": False,
                "message": "Token is missing!"
            }), 401

        try:

            data = jwt.decode(
                token,
                JWT_SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = data

        except jwt.ExpiredSignatureError:

            return jsonify({
                "success": False,
                "message": "Token has expired!"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "success": False,
                "message": "Invalid token!"
            }), 401

        return f(*args, **kwargs)

    return decorated