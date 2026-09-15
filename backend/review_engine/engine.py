from review_engine.language_detector import detect_language
from review_engine.syntax_checker import check_syntax
from review_engine.code_analyzer import analyze_code
from review_engine.security_checker import check_security
from review_engine.complexity_analyzer import analyze_complexity


def analyze_review(code):
    """
    Run the complete multi-language code review engine.
    """

    if not code or not code.strip():
        raise ValueError("Code is empty.")

    # Detect programming language
    language = detect_language(code)

    # Check syntax
    syntax = check_syntax(code, language)

    # Analyze code structure
    code_statistics = analyze_code(code, language)

    # Check security risks
    security = check_security(code)

    # Analyze complexity
    complexity = analyze_complexity(code)

    return {
        "language": language,
        "syntax": syntax,
        "code_statistics": code_statistics,
        "security": security,
        "complexity": complexity
    }