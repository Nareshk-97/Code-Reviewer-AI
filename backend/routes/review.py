from flask import Blueprint, request, jsonify
from ai.gemini import ask_gemini
from utils.auth_middleware import token_required

review = Blueprint("review", __name__)


@review.route("/review", methods=["POST"])
@token_required
def review_code():

    data = request.get_json()

    code = data.get("code")

    if not code:
        return jsonify({
            "success": False,
            "message": "Code is required"
        }), 400

    prompt = f"""
You are an expert software engineer.

Review the following code.

Provide:
1. Errors
2. Bugs
3. Improvements
4. Optimized Code

Code:

{code}
"""

    result = ask_gemini(prompt)

    return jsonify({
        "success": True,
        "review": result
    }), 200