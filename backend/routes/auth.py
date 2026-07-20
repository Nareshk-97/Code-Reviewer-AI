from flask import Blueprint, request, jsonify
from database import get_db_connection
from config import JWT_SECRET_KEY
import bcrypt
import jwt
import datetime

auth = Blueprint("auth", __name__)


# ==========================
# Register API
# ==========================
@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required."
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        cursor.close()
        connection.close()

        return jsonify({
            "success": False,
            "message": "Email already exists."
        }), 409

    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Insert user
    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(%s,%s,%s)
        """,
        (
            username,
            email,
            hashed_password.decode("utf-8")
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "User Registered Successfully"
    }), 201


# ==========================
# Login API
# ==========================
@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and Password are required"
        }), 400

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    # Find user by email
    cursor.execute(
        "SELECT id, username, email, password FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if not user:
        cursor.close()
        connection.close()

        return jsonify({
            "success": False,
            "message": "Invalid Email or Password"
        }), 401

    user_id = user[0]
    username = user[1]
    user_email = user[2]
    hashed_password = user[3]

    # Verify password
    if not bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    ):
        cursor.close()
        connection.close()

        return jsonify({
            "success": False,
            "message": "Invalid Email or Password"
        }), 401

    # Generate JWT Token
    token = jwt.encode(
        {
            "user_id": user_id,
            "username": username,
            "email": user_email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

    cursor.close()
    connection.close()

    return jsonify({
        "success": True,
        "message": "Login Successful",
        "token": token
    }), 200