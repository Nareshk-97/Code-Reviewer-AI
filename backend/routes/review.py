from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from ai.gemini import ask_gemini
from utils.auth_middleware import token_required
from utils.rate_limiter import limiter

from review_engine.engine import analyze_review
from review_engine.fallback_reviewer import generate_fallback_review
from scoring.review_scorer import calculate_review_score


review = Blueprint("review", __name__)


# ==========================================
# MAXIMUM CODE SIZE
# ==========================================

MAX_CODE_LENGTH = 100000


# ==========================================
# CODE REVIEW ENDPOINT
# ==========================================

@review.route("/review", methods=["POST"])
@limiter.limit("5 per minute")
@token_required
def review_code():

    # ==========================================
    # GET REQUEST DATA
    # ==========================================

    if not request.is_json:
        return jsonify({
            "success": False,
            "message": "Content-Type must be application/json."
        }), 400

    try:
        data = request.get_json()

    except BadRequest:
        return jsonify({
            "success": False,
            "message": "Invalid JSON."
        }), 400

    if not isinstance(data, dict):
        return jsonify({
            "success": False,
            "message": "Invalid request data."
        }), 400

    code = data.get("code")

    # ==========================================
    # CODE TYPE VALIDATION
    # ==========================================

    if not isinstance(code, str):
        return jsonify({
            "success": False,
            "message": "Code must be a string."
        }), 400

    # ==========================================
    # EMPTY CODE VALIDATION
    # ==========================================

    if not code.strip():
        return jsonify({
            "success": False,
            "message": "Code is required."
        }), 400

    # ==========================================
    # CODE SIZE VALIDATION
    # ==========================================

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({
            "success": False,
            "message": (
                "Code is too large. "
                "Maximum allowed size is 100000 characters."
            )
        }), 413

    # ==========================================
    # LOCAL REVIEW ENGINE
    # ==========================================

    try:

        analysis = analyze_review(code)

        language = analysis["language"]

        syntax_analysis = analysis["syntax"]

        code_analysis = analysis["code_statistics"]

        security_analysis = analysis["security"]

        complexity_analysis = analysis["complexity"]

        # ======================================
        # REVIEW SCORE
        # ======================================

        score = calculate_review_score(
            syntax_analysis,
            code_analysis,
            security_analysis,
            complexity_analysis
        )

    except Exception as err:

        print(
            f"❌ Review Engine Error: {err}"
        )

        return jsonify({
            "success": False,
            "message": "Code analysis failed."
        }), 500

    # ==========================================
    # GEMINI AI PROMPT
    # ==========================================

    prompt = f"""
You are a Senior Software Engineer, Technical Lead,
and Professional Code Reviewer with over 15 years
of software development experience.

Your task is to perform a complete professional
code review.

The programming language must be detected from
the actual source code.

==============================
REVIEW ENGINE DATA
==============================

Detected Language:
{language}

Syntax Analysis:
{syntax_analysis}

Code Statistics:
{code_analysis}

Security Analysis:
{security_analysis}

Complexity Analysis:
{complexity_analysis}

Backend Calculated Score:
{score}

==============================
SOURCE CODE
==============================

{code}

==============================
REVIEW REQUIREMENTS
==============================

Return the review in Markdown.

# Programming Language

Detect and mention the programming language.

# Summary

Provide a short summary of what the code does.

# Errors

Mention syntax or compilation errors.

Use the syntax analysis as additional information.

If none, write:

None

# Bugs

Mention logical or runtime bugs.

If none, write:

None

# Improvements

Suggest improvements for:

- Readability
- Maintainability
- Performance
- Code structure

# Optimized Code

Provide an improved version of the code.

IMPORTANT:

Keep the optimized code in the SAME programming language.

Do NOT change the programming language.

# Best Practices

Suggest clean coding practices
and appropriate coding standards.

# Security Checks

Mention possible security issues.

Use the security analysis as
additional information.

If none, write:

None

# Time Complexity

Mention the approximate time complexity.

Use the complexity analysis as
additional information.

# Space Complexity

Mention the approximate space complexity.

Use the complexity analysis as
additional information.

# Expected Output

Predict the output without executing
the program.

If the output depends on user input,
explain why.

# Overall Rating

Give a rating out of 10 with
a short justification.

==============================
IMPORTANT RULES
==============================

- Include every section.
- Do not skip sections.
- Keep the sections in the exact order.
- Detect the language automatically.
- Never assume the language is Python.
- Keep optimized code in the same language.
- Do not change the programming language.
- Do not execute the code.
- Predict the output without execution.
- Use proper Markdown headings.
"""

    # ==========================================
    # GEMINI AI REVIEW
    # ==========================================

    try:

        result = ask_gemini(prompt)

        ai_available = True

        print(
            "✅ Gemini review generated successfully."
        )

    except Exception as err:

        print(
            f"❌ AI Review Error: {err}"
        )

        print(
            "🛡️ Using local fallback reviewer..."
        )

        # ======================================
        # LOCAL FALLBACK REVIEWER
        # ======================================

        try:

            result = generate_fallback_review(
                code,
                language,
                syntax_analysis,
                code_analysis,
                security_analysis,
                complexity_analysis
            )

            ai_available = False

            print(
                "✅ Local fallback review generated successfully."
            )

        except Exception as fallback_err:

            print(
                f"❌ Fallback Reviewer Error: {fallback_err}"
            )

            return jsonify({
                "success": False,
                "message": "Review generation failed."
            }), 500

    # ==========================================
    # FINAL RESPONSE
    # ==========================================

    return jsonify({

        "success": True,

        "review": result,

        "ai_available": ai_available,

        "score": score,

        # Generic analysis name because the project
        # supports multiple programming languages
        "analysis": {

            "language": language,

            "syntax": syntax_analysis,

            "code_statistics": code_analysis,

            "security": security_analysis,

            "complexity": complexity_analysis

        }

    }), 200