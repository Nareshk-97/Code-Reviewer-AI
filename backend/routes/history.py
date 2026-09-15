from flask import Blueprint, request, jsonify

from database import get_db_connection
from utils.auth_middleware import token_required


history = Blueprint("history", __name__)


# ============================================================
# SAVE REVIEW HISTORY
# ============================================================

@history.route("/history", methods=["POST"])
@token_required
def save_history():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    language = data.get("language")
    code = data.get("code")
    review = data.get("review")
    score = data.get("score")

    if not language:
        return jsonify({
            "success": False,
            "message": "Language is required."
        }), 400

    if not code:
        return jsonify({
            "success": False,
            "message": "Code is required."
        }), 400

    if not review:
        return jsonify({
            "success": False,
            "message": "Review is required."
        }), 400

    if not isinstance(score, dict):
        score = {}

    user_id = request.user["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO review_history (
                user_id,
                language,
                code,
                review,
                overall_score,
                syntax_score,
                security_score,
                complexity_score,
                structure_score,
                maintainability_score
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                user_id,
                language,
                code,
                review,
                score.get("overall_score"),
                score.get("syntax_score"),
                score.get("security_score"),
                score.get("complexity_score"),
                score.get("structure_score"),
                score.get("maintainability_score")
            )
        )

        connection.commit()

        history_id = cursor.lastrowid

        return jsonify({
            "success": True,
            "message": "Review saved successfully.",
            "history_id": history_id
        }), 201

    except Exception as err:

        connection.rollback()

        print(
            f"❌ Save History Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Failed to save review history."
        }), 500

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET USER REVIEW HISTORY
# ============================================================

@history.route("/history", methods=["GET"])
@token_required
def get_history():

    user_id = request.user["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor(dictionary=True)

    try:

        cursor.execute(
            """
            SELECT
                id,
                language,
                code,
                review,
                overall_score,
                syntax_score,
                security_score,
                complexity_score,
                structure_score,
                maintainability_score,
                created_at
            FROM review_history
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        reviews = cursor.fetchall()

        return jsonify({
            "success": True,
            "history": reviews
        }), 200

    except Exception as err:

        print(
            f"❌ Get History Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Failed to fetch review history."
        }), 500

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DELETE ONE REVIEW
# ============================================================

@history.route("/history/<int:history_id>", methods=["DELETE"])
@token_required
def delete_history(history_id):

    user_id = request.user["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM review_history
            WHERE id = %s
            AND user_id = %s
            """,
            (
                history_id,
                user_id
            )
        )

        connection.commit()

        if cursor.rowcount == 0:

            return jsonify({
                "success": False,
                "message": "Review not found."
            }), 404

        return jsonify({
            "success": True,
            "message": "Review deleted successfully."
        }), 200

    except Exception as err:

        connection.rollback()

        print(
            f"❌ Delete History Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Failed to delete review."
        }), 500

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DELETE ALL USER REVIEW HISTORY
# ============================================================

@history.route("/history", methods=["DELETE"])
@token_required
def clear_history():

    user_id = request.user["user_id"]

    connection = get_db_connection()

    if connection is None:
        return jsonify({
            "success": False,
            "message": "Database connection failed."
        }), 500

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            DELETE FROM review_history
            WHERE user_id = %s
            """,
            (user_id,)
        )

        deleted_count = cursor.rowcount

        connection.commit()

        return jsonify({
            "success": True,
            "message": "Review history cleared successfully.",
            "deleted_count": deleted_count
        }), 200

    except Exception as err:

        connection.rollback()

        print(
            f"❌ Clear History Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Failed to clear review history."
        }), 500

    finally:

        cursor.close()
        connection.close()