import re


def analyze_code(code):

    if not code or not code.strip():
        return {
            "lines": 0,
            "characters": 0,
            "functions": 0,
            "classes": 0,
            "imports": 0,
            "loops": 0,
            "conditions": 0,
            "comments": 0,
            "long_functions": 0
        }

    lines = code.splitlines()

    # ==========================================
    # BASIC STATISTICS
    # ==========================================

    line_count = len(
        [line for line in lines if line.strip()]
    )

    character_count = len(code)

    # ==========================================
    # FUNCTIONS
    # ==========================================

    function_matches = re.findall(
        r"\bdef\s+\w+\s*\(",
        code
    )

    python_function_count = len(function_matches)

    # JavaScript functions
    javascript_function_count = len(
        re.findall(
            r"\bfunction\s+\w+\s*\(",
            code
        )
    )

    # Java / C / C++ style methods
    method_count = len(
        re.findall(
            r"\b(public|private|protected)?\s*"
            r"(static\s+)?"
            r"[\w<>\[\]]+\s+"
            r"\w+\s*\([^;{}]*\)\s*\{",
            code
        )
    )

    function_count = (
        python_function_count
        + javascript_function_count
        + method_count
    )

    # ==========================================
    # CLASSES
    # ==========================================

    python_classes = len(
        re.findall(
            r"\bclass\s+\w+",
            code
        )
    )

    java_classes = len(
        re.findall(
            r"\bclass\s+\w+\s*\{",
            code
        )
    )

    class_count = max(
        python_classes,
        java_classes
    )

    # ==========================================
    # IMPORTS
    # ==========================================

    python_imports = len(
        re.findall(
            r"^\s*(import|from)\s+",
            code,
            re.MULTILINE
        )
    )

    java_imports = len(
        re.findall(
            r"^\s*import\s+",
            code,
            re.MULTILINE
        )
    )

    javascript_imports = len(
        re.findall(
            r"^\s*(import\s+.*from|require\s*\()",
            code,
            re.MULTILINE
        )
    )

    import_count = (
        python_imports
        + java_imports
        + javascript_imports
    )

    # ==========================================
    # LOOPS
    # ==========================================

    loop_count = len(
        re.findall(
            r"\b(for|while|do)\b",
            code
        )
    )

    # ==========================================
    # CONDITIONS
    # ==========================================

    condition_count = len(
        re.findall(
            r"\b(if|elif|else|switch|case)\b",
            code
        )
    )

    # ==========================================
    # COMMENTS
    # ==========================================

    comment_count = len(
        re.findall(
            r"^\s*(#|//|/\*|\*)",
            code,
            re.MULTILINE
        )
    )

    # ==========================================
    # LONG FUNCTIONS
    # ==========================================

    long_function_count = 0

    in_function = False
    function_start = 0
    function_indent = 0

    for index, line in enumerate(lines):

        stripped = line.strip()

        if not stripped:
            continue

        # Python function
        if re.match(
            r"^\s*def\s+\w+\s*\(",
            line
        ):

            in_function = True

            function_start = index

            function_indent = (
                len(line)
                - len(line.lstrip())
            )

            continue

        if in_function:

            current_indent = (
                len(line)
                - len(line.lstrip())
            )

            if (
                current_indent <= function_indent
                and stripped
                and not stripped.startswith("#")
            ):

                function_length = (
                    index - function_start
                )

                if function_length > 20:
                    long_function_count += 1

                in_function = False

    # Check function continuing until EOF
    if in_function:

        function_length = (
            len(lines) - function_start
        )

        if function_length > 20:
            long_function_count += 1

    # ==========================================
    # FINAL RESULT
    # ==========================================

    return {

        "lines": line_count,

        "characters": character_count,

        "functions": function_count,

        "classes": class_count,

        "imports": import_count,

        "loops": loop_count,

        "conditions": condition_count,

        "comments": comment_count,

        "long_functions": long_function_count
    }