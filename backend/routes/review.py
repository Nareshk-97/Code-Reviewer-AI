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
You are a Senior Software Engineer, Technical Lead, and Code Reviewer with over 15 years of experience.

Your task is to automatically detect the programming language from the given code and perform a professional code review.

Code:
{code}

Return the review in Markdown using the following sections.

# Programming Language
Detect and mention the programming language.

# Summary
Provide a short summary (2–3 lines) of what the code does.

# Errors
Mention syntax or compilation errors.
If none, write "None".

# Bugs
Mention logical or runtime bugs.
If none, write "None".

# Improvements
Suggest improvements for readability, maintainability, and performance.

# Optimized Code
Provide an improved version of the code in the SAME programming language.

# Best Practices
Suggest clean code practices and coding standards.

# Security Checks
Mention any possible security issues.
If none, write "None".

# Time Complexity
Mention the approximate time complexity.

# Space Complexity
Mention the approximate space complexity.

# Expected Output
Predict the output without executing the program.
If the output depends on user input, explain why.

# Overall Rating
Give a rating out of 10 with a short justification.

Rules:
- You MUST include every section exactly as listed.
- Do NOT skip any section.
- If a section has nothing to report, write "None".
- Detect the programming language automatically.
- Never assume the language is Python.
- Keep the optimized code in the same programming language.
- Do not change the programming language.
- Predict the expected output without executing the code.
- Use proper Markdown headings.
- Return all sections in the specified order.
"""
    result = ask_gemini(prompt)

    return jsonify({
        "success": True,
        "review": result
    }), 200
