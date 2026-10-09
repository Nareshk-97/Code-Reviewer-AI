def calculate_review_score(
    syntax,
    statistics,
    security,
    complexity
):
    """
    Calculate an overall code quality score.

    Returns a score out of 10 with
    individual category scores.
    """

    # ==========================================
    # SYNTAX SCORE
    # ==========================================

    if syntax.get("valid", False):
        syntax_score = 10
    else:
        syntax_score = 3

    # ==========================================
    # SECURITY SCORE
    # ==========================================

    risk_count = security.get(
        "risk_count",
        0
    )

    if risk_count == 0:
        security_score = 10

    elif risk_count == 1:
        security_score = 8

    elif risk_count == 2:
        security_score = 6

    elif risk_count == 3:
        security_score = 4

    else:
        security_score = 2

    # ==========================================
    # COMPLEXITY SCORE
    # ==========================================

    time_complexity = complexity.get(
        "time_complexity",
        "O(1)"
    )

    if time_complexity == "O(1)":
        complexity_score = 10

    elif time_complexity == "O(n)":
        complexity_score = 9

    elif time_complexity == "O(n^2)":
        complexity_score = 7

    elif time_complexity == "O(n^3)":
        complexity_score = 5

    else:
        complexity_score = 4

    # ==========================================
    # STRUCTURE SCORE
    # ==========================================

    functions = statistics.get(
        "functions",
        0
    )

    classes = statistics.get(
        "classes",
        0
    )

    long_functions = statistics.get(
        "long_functions",
        0
    )

    structure_score = 10

    if long_functions > 0:
        structure_score -= 2

    if functions == 0 and classes == 0:
        structure_score -= 1

    if functions > 20:
        structure_score -= 1

    structure_score = max(
        1,
        structure_score
    )

    # ==========================================
    # MAINTAINABILITY SCORE
    # ==========================================

    comments = statistics.get(
        "comments",
        0
    )

    lines = statistics.get(
        "lines",
        0
    )

    maintainability_score = 10

    if lines > 300:
        maintainability_score -= 2

    elif lines > 150:
        maintainability_score -= 1

    if comments == 0 and lines > 20:
        maintainability_score -= 1

    maintainability_score = max(
        1,
        maintainability_score
    )

    # ==========================================
    # WEIGHTED SCORE
    # ==========================================

    overall_score = (
        syntax_score * 0.20
        + security_score * 0.25
        + complexity_score * 0.20
        + structure_score * 0.20
        + maintainability_score * 0.15
    )

    overall_score = round(
        overall_score,
        1
    )

    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {
        "overall_score": overall_score,
        "syntax_score": syntax_score,
        "security_score": security_score,
        "complexity_score": complexity_score,
        "structure_score": structure_score,
        "maintainability_score": maintainability_score
    }