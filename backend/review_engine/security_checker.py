import re


def check_security(code):

    if not code or not code.strip():
        return {
            "risk_count": 0,
            "risks": []
        }

    risks = []

    # ==========================================
    # 1. DANGEROUS FUNCTION - eval()
    # ==========================================

    if re.search(r"\beval\s*\(", code):

        risks.append({
            "type": "Dangerous Function",
            "message": (
                "Use of eval() can execute "
                "untrusted code."
            )
        })

    # ==========================================
    # 2. DANGEROUS FUNCTION - exec()
    # ==========================================

    if re.search(r"\bexec\s*\(", code):

        risks.append({
            "type": "Dangerous Function",
            "message": (
                "Use of exec() can execute "
                "arbitrary code."
            )
        })

    # ==========================================
    # 3. HARDcoded PASSWORD
    # ==========================================

    if re.search(
        r"(password|passwd|pwd)\s*=\s*['\"][^'\"]+['\"]",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Hardcoded Credential",
            "message": (
                "A password appears to be "
                "hardcoded in the source code."
            )
        })

    # ==========================================
    # 4. HARDcoded API KEY / SECRET
    # ==========================================

    if re.search(
        r"(api[\-_]?key|secret[\-_]?key|access[\-_]?token)"
        r"\s*=\s*['\"][^'\"]+['\"]",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Hardcoded Secret",
            "message": (
                "A possible API key, access token, "
                "or secret is hardcoded in the source code."
            )
        })

    # ==========================================
    # 5. SQL STRING CONCATENATION
    # ==========================================

    sql_pattern = (
        r"(SELECT|INSERT|UPDATE|DELETE)"
        r".*(\+|%|\bf['\"]|\.format\s*\()"
    )

    if re.search(
        sql_pattern,
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "SQL Injection Risk",
            "message": (
                "SQL appears to be constructed "
                "using dynamic string formatting or "
                "concatenation. Use parameterized queries."
            )
        })

    # ==========================================
    # 6. OS COMMAND EXECUTION
    # ==========================================

    command_functions = [
        "os.system",
        "os.popen",
        "subprocess.call",
        "subprocess.run",
        "subprocess.Popen"
    ]

    for function in command_functions:

        if re.search(
            rf"\b{re.escape(function)}\s*\(",
            code
        ):

            risks.append({
                "type": "Command Execution",
                "message": (
                    f"Use of {function}() can execute "
                    "system commands. Avoid passing "
                    "untrusted user input to it."
                )
            })

            break

    # ==========================================
    # 7. UNSAFE DESERIALIZATION - pickle
    # ==========================================

    if re.search(
        r"\bpickle\.(load|loads)\s*\(",
        code
    ):

        risks.append({
            "type": "Unsafe Deserialization",
            "message": (
                "pickle.load() or pickle.loads() can "
                "execute malicious code when processing "
                "untrusted serialized data."
            )
        })

    # ==========================================
    # 8. SHELL=True
    # ==========================================

    if re.search(
        r"\bshell\s*=\s*True\b",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Shell Injection Risk",
            "message": (
                "shell=True can make command execution "
                "vulnerable to command injection when "
                "input is not safely controlled."
            )
        })

    # ==========================================
    # 9. DANGEROUS FILE OPERATIONS
    # ==========================================

    if re.search(
        r"\bopen\s*\([^)]*(user_input|request\.|input\s*\()",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Unsafe File Operation",
            "message": (
                "A file path appears to use user-controlled "
                "input. Validate and restrict file paths "
                "to prevent path traversal attacks."
            )
        })

    # ==========================================
    # 10. HARDCODED PRIVATE KEY
    # ==========================================

    if re.search(
        r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH)?\s*PRIVATE KEY-----",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Sensitive Information",
            "message": (
                "A private cryptographic key appears "
                "to be embedded in the source code."
            )
        })

    # ==========================================
    # 11. DEBUG MODE
    # ==========================================

    if re.search(
        r"\bdebug\s*=\s*True\b",
        code,
        re.IGNORECASE
    ):

        risks.append({
            "type": "Debug Configuration",
            "message": (
                "Debug mode is enabled. Disable debug mode "
                "in production because it may expose "
                "sensitive application information."
            )
        })

    # ==========================================
    # FINAL RESULT
    # ==========================================

    return {
        "risk_count": len(risks),
        "risks": risks
    }