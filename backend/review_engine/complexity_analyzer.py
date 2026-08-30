import re


def analyze_complexity(code):

    if not code or not code.strip():
        return {
            "time_complexity": "O(1)",
            "space_complexity": "O(1)",
            "loops": 0,
            "nested_loops": 0
        }

    lines = code.splitlines()

    # ==========================================
    # FIND LOOPS
    # ==========================================

    loop_data = []

    for line_number, line in enumerate(lines):

        stripped = line.lstrip()

        if re.match(
            r"(for|while)\b",
            stripped
        ):

            indentation = (
                len(line) - len(stripped)
            )

            loop_data.append({
                "line": line_number,
                "indent": indentation
            })

    loop_count = len(loop_data)

    # ==========================================
    # FIND NESTED LOOPS
    # ==========================================

    nested_loops = 0

    for i in range(len(loop_data)):

        outer = loop_data[i]

        for j in range(i + 1, len(loop_data)):

            inner = loop_data[j]

            # Inner loop must be more deeply
            # indented than the outer loop.

            if inner["indent"] > outer["indent"]:

                nested_loops += 1

                break

            # Once indentation returns to the
            # same or lower level, this cannot
            # be inside the outer loop.

            if inner["indent"] <= outer["indent"]:

                break

    # ==========================================
    # TIME COMPLEXITY
    # ==========================================

    if nested_loops >= 2:

        time_complexity = "O(n³)"

    elif nested_loops == 1:

        time_complexity = "O(n²)"

    elif loop_count > 0:

        time_complexity = "O(n)"

    else:

        time_complexity = "O(1)"

    # ==========================================
    # ADDITIONAL O(n) OPERATIONS
    # ==========================================

    # Built-in operations that commonly process
    # collections.

    collection_operations = re.findall(
        r"\b(len|sum|max|min|sorted)\s*\(",
        code
    )

    if (
        loop_count == 0
        and len(collection_operations) > 0
    ):

        time_complexity = "O(n)"

    # ==========================================
    # SPACE COMPLEXITY
    # ==========================================

    # Detect common collection creation.

    collection_patterns = [
        r"\[[^\]]*\]",
        r"\blist\s*\(",
        r"\bdict\s*\(",
        r"\bset\s*\(",
        r"\btuple\s*\(",
        r"\brange\s*\("
    ]

    creates_collection = any(
        re.search(pattern, code)
        for pattern in collection_patterns
    )

    if creates_collection:

        space_complexity = "O(n)"

    else:

        space_complexity = "O(1)"

    # ==========================================
    # RETURN RESULT
    # ==========================================

    return {

        "time_complexity": time_complexity,

        "space_complexity": space_complexity,

        "loops": loop_count,

        "nested_loops": nested_loops
    }