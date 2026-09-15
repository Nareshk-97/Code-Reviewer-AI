from functools import wraps

from flask import request, jsonify

import jwt

from config import JWT_SECRET_KEY


def token_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # ==========================================
        # CHECK AUTHORIZATION HEADER
        # ==========================================

        auth_header = request.headers.get("Authorization")

        if not auth_header:

            return jsonify({
                "success": False,
                "message": "Token is missing!"
            }), 401

        # ==========================================
        # VALIDATE BEARER FORMAT
        # ==========================================

        parts = auth_header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":

            return jsonify({
                "success": False,
                "message": "Invalid authorization header."
            }), 401

        token = parts[1]

        if not token:

            return jsonify({
                "success": False,
                "message": "Token is missing!"
            }), 401

        # ==========================================
        # CHECK JWT SECRET
        # ==========================================

        if not JWT_SECRET_KEY:

            return jsonify({
                "success": False,
                "message": "Authentication service is not configured."
            }), 500

        # ==========================================
        # VERIFY TOKEN
        # ==========================================

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

        # ==========================================
        # TOKEN VALID
        # ==========================================

        return f(*args, **kwargs)

    return decorated