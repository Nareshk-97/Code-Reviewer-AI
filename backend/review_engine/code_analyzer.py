import re


def analyze_code(code, language="Unknown"):

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

    # Python
    python_function_count = len(
        re.findall(
            r"\bdef\s+\w+\s*\(",
            code
        )
    )

    # JavaScript
    javascript_function_count = len(
        re.findall(
            r"\bfunction\s+\w+\s*\(",
            code
        )
    )

    # TypeScript
    typescript_function_count = len(
        re.findall(
            r"\bfunction\s+\w+\s*\(",
            code
        )
    )

    # Swift
    swift_function_count = len(
        re.findall(
            r"\bfunc\s+\w+\s*\(",
            code
        )
    )

    # Kotlin
    kotlin_function_count = len(
        re.findall(
            r"\bfun\s+\w+\s*\(",
            code
        )
    )

    # Go
    go_function_count = len(
        re.findall(
            r"\bfunc\s+\w+\s*\(",
            code
        )
    )

    # Rust
    rust_function_count = len(
        re.findall(
            r"\bfn\s+\w+\s*\(",
            code
        )
    )

    # PHP
    php_function_count = len(
        re.findall(
            r"\bfunction\s+\w+\s*\(",
            code
        )
    )

    # Java / C / C++ / C# methods
    method_count = len(
        re.findall(
            r"\b(?:public|private|protected|static)?\s*"
            r"(?:static\s+)?"
            r"[\w<>\[\]]+\s+"
            r"\w+\s*\([^;{}]*\)\s*\{",
            code
        )
    )

    # Avoid double counting generic functions as methods
    if language in [
        "Python",
        "JavaScript",
        "TypeScript",
        "Swift",
        "Kotlin",
        "Go",
        "Rust",
        "PHP"
    ]:
        method_count = 0

    if language == "Python":
        function_count = python_function_count

    elif language == "JavaScript":
        function_count = javascript_function_count

    elif language == "TypeScript":
        function_count = typescript_function_count

    elif language == "Swift":
        function_count = swift_function_count

    elif language == "Kotlin":
        function_count = kotlin_function_count

    elif language == "Go":
        function_count = go_function_count

    elif language == "Rust":
        function_count = rust_function_count

    elif language == "PHP":
        function_count = php_function_count

    else:
        function_count = method_count

    # ==========================================
    # CLASSES
    # ==========================================

    class_count = len(
        re.findall(
            r"\bclass\s+\w+",
            code
        )
    )

    # ==========================================
    # IMPORTS
    # ==========================================

    import_count = 0

    # Python
    if language == "Python":

        import_count = len(
            re.findall(
                r"^\s*(?:import\s+\w+|from\s+\w+(?:\.\w+)*\s+import)\b",
                code,
                re.MULTILINE
            )
        )

    # Java
    elif language == "Java":

        import_count = len(
            re.findall(
                r"^\s*import\s+(?:static\s+)?[\w.]+\s*;",
                code,
                re.MULTILINE
            )
        )

    # JavaScript
    elif language == "JavaScript":

        import_count = len(
            re.findall(
                r"^\s*import\s+",
                code,
                re.MULTILINE
            )
        )

        import_count += len(
            re.findall(
                r"\brequire\s*\(\s*['\"]",
                code
            )
        )

    # TypeScript
    elif language == "TypeScript":

        import_count = len(
            re.findall(
                r"^\s*import\s+",
                code,
                re.MULTILINE
            )
        )

        import_count += len(
            re.findall(
                r"\brequire\s*\(\s*['\"]",
                code
            )
        )

    # C
    elif language == "C":

        import_count = len(
            re.findall(
                r"^\s*#include\s*[<\"]",
                code,
                re.MULTILINE
            )
        )

    # C++
    elif language == "C++":

        import_count = len(
            re.findall(
                r"^\s*#include\s*[<\"]",
                code,
                re.MULTILINE
            )
        )

    # C#
    elif language == "C#":

        import_count = len(
            re.findall(
                r"^\s*using\s+[\w.]+\s*;",
                code,
                re.MULTILINE
            )
        )

    # Go
    elif language == "Go":

        single_imports = len(
            re.findall(
                r'^\s*import\s+["\']',
                code,
                re.MULTILINE
            )
        )

        import_count = single_imports

        # import (
        if re.search(
            r"^\s*import\s*\(",
            code,
            re.MULTILINE
        ):

            import_block = re.search(
                r"import\s*\((.*?)\)",
                code,
                re.DOTALL
            )

            if import_block:

                import_count = len(
                    re.findall(
                        r'^\s*["\']',
                        import_block.group(1),
                        re.MULTILINE
                    )
                )

    # Rust
    elif language == "Rust":

        import_count = len(
            re.findall(
                r"^\s*(?:use|extern\s+crate)\s+",
                code,
                re.MULTILINE
            )
        )

    # PHP
    elif language == "PHP":

        import_count = len(
            re.findall(
                r"^\s*(?:use|require|require_once|include|include_once)\s+",
                code,
                re.MULTILINE
            )
        )

    # Kotlin
    elif language == "Kotlin":

        import_count = len(
            re.findall(
                r"^\s*import\s+",
                code,
                re.MULTILINE
            )
        )

    # Swift
    elif language == "Swift":

        import_count = len(
            re.findall(
                r"^\s*import\s+\w+",
                code,
                re.MULTILINE
            )
        )

    # HTML
    elif language == "HTML":

        import_count = len(
            re.findall(
                r"<(?:link|script)\b",
                code,
                re.IGNORECASE
            )
        )

    # CSS
    elif language == "CSS":

        import_count = len(
            re.findall(
                r"@import\s+",
                code,
                re.IGNORECASE
            )
        )

    # SQL
    elif language == "SQL":

        import_count = 0

    # ==========================================
    # LOOPS
    # ==========================================

    loop_count = len(
        re.findall(
            r"\b(for|foreach|while|do)\b",
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