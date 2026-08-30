import re


def detect_language(code):

    if not code or not code.strip():
        return "Unknown"

    code = code.strip()

    # Python
    if (
        re.search(r"\bdef\s+\w+\s*\(", code)
        or re.search(r"\bimport\s+\w+", code)
        or re.search(r"\bfrom\s+\w+\s+import\b", code)
        or re.search(r"\bprint\s*\(", code)
    ):
        return "Python"

    # Java
    if (
        re.search(r"\bpublic\s+class\s+\w+", code)
        or re.search(
            r"\bpublic\s+static\s+void\s+main\s*\(",
            code
        )
        or re.search(r"\bSystem\.out\.println\s*\(", code)
    ):
        return "Java"

    # JavaScript
    if (
        re.search(r"\bconst\s+\w+\s*=", code)
        or re.search(r"\blet\s+\w+\s*=", code)
        or re.search(r"\bfunction\s+\w+\s*\(", code)
        or "console.log(" in code
    ):
        return "JavaScript"

    # C++
    if (
        "#include <iostream>" in code
        or "using namespace std" in code
        or "cout <<" in code
        or "cin >>" in code
    ):
        return "C++"

    # C
    if (
        "#include <stdio.h>" in code
        or "printf(" in code
        or "scanf(" in code
    ):
        return "C"

    return "Unknown"