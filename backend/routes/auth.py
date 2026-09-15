from flask import Blueprint, request, jsonify
from database import get_db_connection
from config import JWT_SECRET_KEY
from utils.auth_middleware import token_required
from utils.rate_limiter import limiter

import bcrypt
import jwt
import datetime
import re


auth = Blueprint("auth", __name__)


# ==========================
# Register API
# ==========================

@auth.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    # ==========================================
    # CHECK JSON DATA
    # ==========================================

    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json."
        }), 400

    try:
        data = request.get_json()

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid JSON data."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    # ==========================================
    # GET USER DATA
    # ==========================================

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # ==========================================
    # VALIDATE DATA TYPES
    # ==========================================

    if not isinstance(username, str):
        return jsonify({
            "success": False,
            "message": "Username must be a string."
        }), 400

    if not isinstance(email, str):
        return jsonify({
            "success": False,
            "message": "Email must be a string."
        }), 400

    if not isinstance(password, str):
        return jsonify({
            "success": False,
            "message": "Password must be a string."
        }), 400

    # ==========================================
    # CLEAN INPUT
    # ==========================================

    username = username.strip()
    email = email.strip().lower()

    # IMPORTANT:
    # Do NOT strip the password.
    # Spaces can legitimately be part of a password.

    # ==========================================
    # REQUIRED FIELD VALIDATION
    # ==========================================

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    # Reject passwords containing only spaces
    if not password.strip():
        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400

    # ==========================================
    # USERNAME LENGTH VALIDATION
    # ==========================================

    if len(username) > 100:
        return jsonify({
            "success": False,
            "message": "Username must not exceed 100 characters."
        }), 400

    # ==========================================
    # EMAIL LENGTH VALIDATION
    # ==========================================

    if len(email) > 150:
        return jsonify({
            "success": False,
            "message": "Email must not exceed 150 characters."
        }), 400

    # ==========================================
    # EMAIL FORMAT VALIDATION
    # ==========================================

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    # ==========================================
    # PASSWORD LENGTH VALIDATION
    # ==========================================

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters long."
        }), 400

    # bcrypt has a practical maximum of 72 bytes
    if len(password.encode("utf-8")) > 72:
        return jsonify({
            "success": False,
            "message": "Password is too long."
        }), 400

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        # ======================================
        # CHECK EMAIL ALREADY EXISTS
        # ======================================

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if user:

            return jsonify({
                "success": False,
                "message": "Email already exists."
            }), 409

        # ======================================
        # HASH PASSWORD
        # ======================================

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        # ======================================
        # INSERT USER
        # ======================================

        cursor.execute(
            """
            INSERT INTO users(username, email, password)
            VALUES(%s, %s, %s)
            """,
            (
                username,
                email,
                hashed_password.decode("utf-8")
            )
        )

        connection.commit()

        return jsonify({
            "success": True,
            "message": "User registered successfully."
        }), 201

    except Exception as err:

        print(
            f"❌ Registration Error: {err}"
        )

        connection.rollback()

        return jsonify({
            "success": False,
            "message": "Registration failed."
        }), 500

    finally:

        cursor.close()
        connection.close()


# ==========================
# Login API
# ==========================

@auth.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():

    # ==========================================
    # CHECK JSON DATA
    # ==========================================

    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json."
        }), 400

    try:
        data = request.get_json()

    except Exception:
        return jsonify({
            "success": False,
            "message": "Invalid JSON data."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    # ==========================================
    # GET LOGIN DATA
    # ==========================================

    email = data.get("email")
    password = data.get("password")

    # ==========================================
    # VALIDATE DATA TYPES
    # ==========================================

    if not isinstance(email, str):
        return jsonify({
            "success": False,
            "message": "Email must be a string."
        }), 400

    if not isinstance(password, str):
        return jsonify({
            "success": False,
            "message": "Password must be a string."
        }), 400

    email = email.strip().lower()

    # ==========================================
    # REQUIRED FIELD VALIDATION
    # ==========================================

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required."
        }), 400

    # ==========================================
    # EMAIL FORMAT VALIDATION
    # ==========================================

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(email_pattern, email):
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    # ==========================================
    # CHECK JWT CONFIGURATION
    # ==========================================

    if not JWT_SECRET_KEY:
        return jsonify({
            "success": False,
            "message": "Authentication service is not configured."
        }), 500

    # ==========================================
    # DATABASE CONNECTION
    # ==========================================

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        # ======================================
        # FIND USER
        # ======================================

        cursor.execute(
            """
            SELECT id, username, email, password
            FROM users
            WHERE email=%s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        user_id = user[0]
        username = user[1]
        user_email = user[2]
        hashed_password = user[3]

        # ======================================
        # VERIFY PASSWORD
        # ======================================

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        ):

            return jsonify({
                "success": False,
                "message": "Invalid email or password."
            }), 401

        # ======================================
        # CREATE JWT
        # ======================================

        token = jwt.encode(
            {
                "user_id": user_id,
                "username": username,
                "email": user_email,
                "exp": (
                    datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(hours=1)
                )
            },
            JWT_SECRET_KEY,
            algorithm="HS256"
        )

        # ======================================
        # LOGIN SUCCESS
        # ======================================

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "token": token
        }), 200

    except Exception as err:

        print(
            f"❌ Login Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Login failed."
        }), 500

    finally:

        cursor.close()
        connection.close()


# ==========================
# Protected Profile API
# ==========================

@auth.route("/profile", methods=["GET"])
@token_required
def profile():

    user = request.user

    return jsonify({
        "success": True,
        "message": f"Welcome {user['username']}",
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "email": user["email"]
        }
    }), 200