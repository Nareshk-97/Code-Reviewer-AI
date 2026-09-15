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
    r"(for|foreach|while)\b",
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

            # Inner loop is more deeply indented
            if inner["indent"] > outer["indent"]:

                nested_loops += 1
                break

            # Returned to same or lower indentation
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

    creates_collection = False

    # ------------------------------------------
    # Python collections
    # ------------------------------------------

    python_patterns = [

        # list(...)
        r"\blist\s*\(",

        # dict(...)
        r"\bdict\s*\(",

        # set(...)
        r"\bset\s*\(",

        # tuple(...)
        r"\btuple\s*\(",

        # list comprehension
        r"\[[^\]]+\s+for\s+\w+\s+in\s+",

        # dictionary comprehension
        r"\{[^{}]*:\s*[^{}]*\s+for\s+\w+\s+in\s+"
    ]

    for pattern in python_patterns:

        if re.search(pattern, code):

            creates_collection = True
            break

    # ------------------------------------------
    # Java / C / C++ / C# arrays
    # ------------------------------------------

    if not creates_collection:

        array_patterns = [

            # new int[10]
            r"\bnew\s+\w+\s*\[[^\]]+\]",

            # new int[size]
            r"\bnew\s+\w+\s*\[\s*\w+\s*\]",

            # int numbers[] = ...
            # But NOT String[] args
            r"\b\w+\s+\w+\s*\[\s*\]\s*=",

            # int[] numbers = ...
            r"\b\w+\s*\[\s*\]\s+\w+\s*=",

            # C/C++ style array with size
            r"\b\w+\s+\w+\s*\[\s*\d+\s*\]\s*="

        ]

        for pattern in array_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break

    # ------------------------------------------
    # C++ vector
    # ------------------------------------------

    if not creates_collection:

        cpp_patterns = [

            r"\bvector\s*<",
            r"\bstd::vector\s*<",

            r"\bmap\s*<",
            r"\bstd::map\s*<",

            r"\bset\s*<",
            r"\bstd::set\s*<",

            r"\bunordered_map\s*<",
            r"\bstd::unordered_map\s*<"

        ]

        for pattern in cpp_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break

    # ------------------------------------------
    # Java collections
    # ------------------------------------------

    if not creates_collection:

        java_patterns = [

            r"\bnew\s+ArrayList\s*<",
            r"\bnew\s+LinkedList\s*<",
            r"\bnew\s+HashMap\s*<",
            r"\bnew\s+HashSet\s*<",

            r"\bArrayList\s*<",
            r"\bLinkedList\s*<",
            r"\bHashMap\s*<",
            r"\bHashSet\s*<"

        ]

        for pattern in java_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break

    # ------------------------------------------
    # JavaScript / TypeScript arrays
    # ------------------------------------------

    if not creates_collection:

        javascript_patterns = [

            # const numbers = [1, 2, 3]
            r"\b(?:const|let|var)\s+\w+\s*=\s*\[[^\]]*\]",

            # new Array(...)
            r"\bnew\s+Array\s*\(",

            # Array(...)
            r"\bArray\s*\("

        ]

        for pattern in javascript_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break
        # ------------------------------------------
    # Go slices
    # ------------------------------------------

    if not creates_collection:

        go_patterns = [

            # numbers := []int{1, 2, 3}
            r":=\s*\[\]\w+\s*\{",

            # numbers := []string{...}
            r":=\s*\[\]\w+\s*\{",

            # var numbers []int
            r"\bvar\s+\w+\s+\[\]\w+"

        ]

        for pattern in go_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break

        # ------------------------------------------
    # Rust collections
    # ------------------------------------------

    if not creates_collection:

        rust_patterns = [

            # let numbers = vec![1, 2, 3]
            r"\bvec!\s*\[",

            # Vec::new()
            r"\bVec\s*::\s*new\s*\(",

            # Vec<T>
            r"\bVec\s*<"

        ]

        for pattern in rust_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break

        # ------------------------------------------
    # PHP arrays
    # ------------------------------------------

    if not creates_collection:

        php_patterns = [

            # $numbers = [1, 2, 3]
            r"\$\w+\s*=\s*\[[^\]]*\]",

            # array(...)
            r"\barray\s*\("

        ]

        for pattern in php_patterns:

            if re.search(pattern, code):

                creates_collection = True
                break
    
    
    

    # ------------------------------------------
    # Python range() is O(1) space
    # ------------------------------------------
    #
    # IMPORTANT:
    # range(n) does NOT mean O(n) space.
    #
    # Example:
    #
    # for i in range(10):
    #     print(i)
    #
    # Space = O(1)

    # ==========================================
    # FINAL SPACE COMPLEXITY
    # ==========================================

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