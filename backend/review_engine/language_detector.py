import re


def detect_language(code):

    if not code or not code.strip():
        return "Unknown"

    code = code.strip()

    # ==========================================
    # HTML
    # ==========================================

    if (
        re.search(r"<!DOCTYPE\s+html", code, re.IGNORECASE)
        or re.search(r"<html[\s>]", code, re.IGNORECASE)
        or re.search(r"<body[\s>]", code, re.IGNORECASE)
        or re.search(r"<div[\s>]", code, re.IGNORECASE)
    ):
        return "HTML"


    # ==========================================
    # CSS
    # ==========================================

    if (
        re.search(
            r"[.#]?[a-zA-Z][\w-]*\s*\{[^}]*"
            r"(?:color|background|margin|padding|display|font-size)"
            r"\s*:",
            code,
            re.IGNORECASE | re.DOTALL
        )
    ):
        return "CSS"


    # ==========================================
    # SQL
    # ==========================================

    if (
        re.search(r"\bSELECT\b.+\bFROM\b", code, re.IGNORECASE | re.DOTALL)
        or re.search(r"\bINSERT\s+INTO\b", code, re.IGNORECASE)
        or re.search(r"\bUPDATE\s+\w+\s+SET\b", code, re.IGNORECASE)
        or re.search(r"\bDELETE\s+FROM\b", code, re.IGNORECASE)
        or re.search(r"\bCREATE\s+TABLE\b", code, re.IGNORECASE)
        or re.search(r"\bALTER\s+TABLE\b", code, re.IGNORECASE)
        or re.search(r"\bDROP\s+TABLE\b", code, re.IGNORECASE)
    ):
        return "SQL"


    # ==========================================
    # PHP
    # ==========================================

    if (
        re.search(r"<\?php", code, re.IGNORECASE)
        or re.search(r"\becho\s+", code, re.IGNORECASE)
        or re.search(r"\$\w+\s*=", code)
    ):
        return "PHP"


    # ==========================================
    # C++
    # ==========================================

    if (
        re.search(r"#include\s*<iostream>", code)
        or re.search(r"\busing\s+namespace\s+std\b", code)
        or re.search(r"\bcout\s*<<", code)
        or re.search(r"\bcin\s*>>", code)
        or re.search(r"\bstd::", code)
        or re.search(r"\bvector\s*<\s*\w+\s*>", code)
    ):
        return "C++"


    # ==========================================
    # C#
    # ==========================================

    if (
        re.search(r"\busing\s+System\s*;", code)
        or re.search(r"\bConsole\s*\.\s*Write(?:Line)?\s*\(", code)
        or re.search(r"\bnamespace\s+\w+", code)
        or re.search(r"\bpublic\s+class\s+\w+.*\bstatic\s+void\s+Main\b",
                     code, re.DOTALL)
    ):
        return "C#"


    # ==========================================
    # Java
    # ==========================================

    if (
        re.search(r"\bpublic\s+class\s+\w+", code)
        or re.search(
            r"\bpublic\s+static\s+void\s+main\s*\(",
            code
        )
        or re.search(
            r"\bSystem\s*\.\s*out\s*\.\s*println\s*\(",
            code
        )
        or re.search(r"\bimport\s+java\.", code)
    ):
        return "Java"


    # ==========================================
    # C
    # ==========================================

    if (
        re.search(r"#include\s*<stdio\.h>", code)
        or re.search(r"\bprintf\s*\(", code)
        or re.search(r"\bscanf\s*\(", code)
        or re.search(r"\bint\s+main\s*\(\s*(?:void)?\s*\)", code)
    ):
        return "C"


    # ==========================================
    # Go
    # ==========================================

    if (
        re.search(r"\bpackage\s+main\b", code)
        or re.search(r"\bfunc\s+main\s*\(", code)
        or re.search(r"\bfmt\s*\.\s*(?:Println|Printf|Print)\s*\(", code)
        or re.search(r"\bgo\s+func\b", code)
    ):
        return "Go"


    # ==========================================
    # Rust
    # ==========================================

    if (
        re.search(r"\bfn\s+main\s*\(", code)
        or re.search(r"\bprintln!\s*\(", code)
        or re.search(r"\buse\s+std::", code)
        or re.search(r"\blet\s+mut\s+\w+", code)
    ):
        return "Rust"


    # ==========================================
    # Kotlin
    # ==========================================

    if (
        re.search(r"\bfun\s+main\s*\(", code)
        or re.search(r"\bfun\s+\w+\s*\([^)]*\)\s*:", code)
        or re.search(r"\b(?:val|var)\s+\w+\s*:", code)
        or re.search(r"\bprintln\s*\(", code)
    ):
        return "Kotlin"


    # ==========================================
    # Swift
    # ==========================================

    # Swift
    if (
        re.search(
            r"\bimport\s+(?:Foundation|UIKit|SwiftUI)\b",
            code
        )
        or re.search(r"\bfunc\s+\w+\s*\(", code)
        or re.search(r"\blet\s+\w+\s*:\s*[\w\[\]]+", code)
        or re.search(r"\bvar\s+\w+\s*:\s*[\w\[\]]+", code)
    ):
        return "Swift"


    # ==========================================
    # TypeScript
    # ==========================================

    if (
        re.search(r"\binterface\s+\w+\s*\{", code)
        or re.search(r"\btype\s+\w+\s*=", code)
        or re.search(r"\b(?:let|const|var)\s+\w+\s*:\s*[A-Za-z_$][\w<>\[\]| ]*", code)
        or re.search(r"\bfunction\s+\w+\s*\([^)]*\)\s*:\s*[A-Za-z_$][\w<>\[\]| ]*", code)
    ):
        return "TypeScript"


    # ==========================================
    # JavaScript
    # ==========================================

    if (
        re.search(r"\b(?:const|let|var)\s+\w+\s*=", code)
        or re.search(r"\bfunction\s+\w+\s*\(", code)
        or re.search(r"\bconsole\s*\.\s*log\s*\(", code)
        or re.search(r"=>", code)
        or re.search(r"\bexport\s+(?:default\s+)?", code)
        or re.search(r"\bimport\s+.+\s+from\s+['\"]", code)
    ):
        return "JavaScript"


    # ==========================================
    # Python
    # ==========================================

    if (
        re.search(r"\bdef\s+\w+\s*\(", code)
        or re.search(r"\bfrom\s+\w+\s+import\b", code)
        or re.search(r"\bimport\s+\w+", code)
        or re.search(r"\bprint\s*\(", code)
        or re.search(r"\bif\s+.+:", code)
        or re.search(r"\bfor\s+\w+\s+in\s+", code)
    ):
        return "Python"


    # ==========================================
    # Unknown
    # ==========================================

    return "Unknown"