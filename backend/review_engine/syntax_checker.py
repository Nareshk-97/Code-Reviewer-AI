import ast


def check_syntax(code, language):
    """
    Check basic syntax errors before AI review.
    """

    if not code or not code.strip():
        return {
            "valid": False,
            "error": "Code is empty."
        }

    # ==============================
    # PYTHON SYNTAX CHECK
    # ==============================

    if language == "Python":

        try:
            ast.parse(code)

            return {
                "valid": True,
                "error": None
            }

        except SyntaxError as err:

            return {
                "valid": False,
                "error": f"Line {err.lineno}: {err.msg}"
            }

    # ==============================
    # BASIC BRACKET CHECK
    # ==============================

    brackets = {
        ")": "(",
        "]": "[",
        "}": "{"
    }

    stack = []

    for char in code:

        if char in "([{":
            stack.append(char)

        elif char in ")]}":

            if not stack:
                return {
                    "valid": False,
                    "error": f"Unexpected closing bracket: {char}"
                }

            if stack[-1] != brackets[char]:
                return {
                    "valid": False,
                    "error": f"Mismatched bracket: {char}"
                }

            stack.pop()

    if stack:
        return {
            "valid": False,
            "error": "Missing closing bracket."
        }

    return {
        "valid": True,
        "error": None
    }