def generate_fallback_review(
    code,
    language,
    syntax,
    statistics,
    security,
    complexity,
    score
):
    """
    Generate a local code review when Gemini is unavailable.
    Uses the centralized backend score from review_scorer.py.
    """

    # ==========================================
    # SYNTAX
    # ==========================================

    if syntax.get("valid"):
        errors = "None"
    else:
        errors = syntax.get(
            "error",
            "Unknown syntax error."
        )

    # ==========================================
    # SECURITY
    # ==========================================

    if security.get("risk_count", 0) == 0:

        security_text = "None"

    else:

        security_items = []

        for risk in security.get("risks", []):

            risk_type = risk.get(
                "type",
                "Security Risk"
            )

            message = risk.get(
                "message",
                ""
            )

            security_items.append(
                f"- **{risk_type}:** {message}"
            )

        security_text = "\n".join(
            security_items
        )

    # ==========================================
    # COMPLEXITY
    # ==========================================

    time_complexity = complexity.get(
        "time_complexity",
        "Unknown"
    )

    space_complexity = complexity.get(
        "space_complexity",
        "Unknown"
    )

    # ==========================================
    # BUGS
    # ==========================================

    if not syntax.get("valid"):

        bugs = (
            "The code contains a syntax error "
            "and may not execute correctly."
        )

    else:

        bugs = (
            "No obvious bugs detected by "
            "the local analyzer."
        )

    # ==========================================
    # IMPROVEMENTS
    # ==========================================

    improvements = [
        "- Keep functions focused on a single responsibility.",
        "- Use meaningful variable and function names.",
        "- Add comments where the logic is complex.",
        "- Validate external or user-provided input.",
        "- Handle possible runtime errors appropriately."
    ]

    # ==========================================
    # RATING
    # ==========================================

    # Use the centralized score calculated by
    # scoring/review_scorer.py.
    rating = score.get(
        "overall_score",
        0
    )

    # ==========================================
    # SUMMARY
    # ==========================================

    summary = (
        f"The submitted {language} code contains "
        f"{statistics.get('lines', 0)} lines and "
        f"{statistics.get('functions', 0)} function(s). "
        f"The local analyzer identified "
        f"{security.get('risk_count', 0)} "
        f"security risk(s)."
    )

    # ==========================================
    # FALLBACK REVIEW
    # ==========================================

    review = f"""
# Programming Language

{language}

# Summary

{summary}

# Errors

{errors}

# Bugs

{bugs}

# Improvements

{chr(10).join(improvements)}

# Optimized Code

The optimized code could not be generated automatically
because Gemini AI is currently unavailable.

Please use the original code together with the
improvements above.

# Best Practices

- Follow language-specific coding conventions.
- Keep functions small and readable.
- Use meaningful names.
- Avoid unnecessary complexity.
- Validate input data.
- Handle errors appropriately.
- Never hardcode credentials or secrets.

# Security Checks

{security_text}

# Time Complexity

{time_complexity}

# Space Complexity

{space_complexity}

# Expected Output

The local analyzer does not execute the submitted code.
Therefore, exact runtime output cannot be guaranteed.

# Overall Rating

**{rating}/10**

This rating is calculated by the centralized
Python review scoring engine.

> Gemini AI was unavailable, so this review was generated
> by the local Python review engine.
"""

    return review.strip()