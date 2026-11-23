"""
Self-Verification & Quality Engine for Frontier Intelligence Engine (FIE).
Inspects code and text deliverables across syntax, completeness, security,
and execution status to prevent false claims of success.
"""

from typing import Any, Dict, List, Optional
import ast
import re
import subprocess
import logging

logger = logging.getLogger("fie.verification")

class VerificationEngine:
    """Evaluates deliverables against formal quality rubrics."""

    DANGEROUS_PATTERNS = [
        (r"\beval\s*\(", "Use of 'eval()' is prohibited due to arbitrary code injection risks."),
        (r"\bexec\s*\(", "Use of 'exec()' is prohibited due to security risks."),
        (r"os\.system\s*\(", "Use of 'os.system()' is discouraged; use subprocess with parameterized args."),
        (r"__import__\s*\(", "Direct use of '__import__()' bypasses static security analysis.")
    ]

    STUB_PATTERNS = [
        (r"#\s*TODO\b", "Unfinished TODO comment found."),
        (r"//\s*TODO\b", "Unfinished TODO comment found."),
        (r"#\s*implement here\b", "Placeholder stub found."),
        (r"raise\s+NotImplementedError", "Unimplemented method detected.")
    ]

    def verify_python_code(self, code_str: str, run_test: bool = False, test_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Validates Python code for syntax, completeness, security, and optional runtime execution.
        """
        issues: List[str] = []
        warnings: List[str] = []
        status: str = "UNTESTED"

        # 1. AST Syntax Check
        try:
            tree = ast.parse(code_str)
            status = "SYNTAX_PASSED"
        except SyntaxError as e:
            return {
                "status": "FAILED",
                "grade": "F",
                "syntax_valid": False,
                "issues": [f"Syntax Error on line {e.lineno}: {e.msg}"],
                "warnings": []
            }

        # 2. Security Audit
        for pattern, msg in self.DANGEROUS_PATTERNS:
            if re.search(pattern, code_str):
                issues.append(f"[SECURITY] {msg}")

        # 3. Completeness & Stub Detection
        for pattern, msg in self.STUB_PATTERNS:
            if re.search(pattern, code_str, re.IGNORECASE):
                warnings.append(f"[STUB] {msg}")

        # Check for empty functions with only 'pass'
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    warnings.append(f"[COMPLETENESS] Function '{node.name}' contains only 'pass'.")

        # 4. Optional Dynamic Test Execution
        test_passed = False
        if run_test and test_code:
            try:
                full_script = f"{code_str}\n\n# --- TEST RUNNER ---\n{test_code}"
                res = subprocess.run(
                    ["python", "-c", full_script],
                    capture_output=True,
                    text=True,
                    timeout=8
                )
                if res.returncode == 0:
                    status = "VERIFIED"
                    test_passed = True
                else:
                    status = "FAILED"
                    issues.append(f"[RUNTIME TEST FAILED] {res.stderr.strip()[:500]}")
            except Exception as e:
                status = "NEEDS_REVIEW"
                issues.append(f"[TEST RUNNER ERROR] {str(e)}")

        # Calculate Grade
        if status == "FAILED" or any("[SECURITY]" in iss for iss in issues):
            grade = "F"
        elif status == "VERIFIED" and not issues and not warnings:
            grade = "S"
        elif status == "SYNTAX_PASSED" and not issues:
            grade = "A" if not warnings else "B"
        else:
            grade = "B"

        return {
            "status": status,
            "grade": grade,
            "syntax_valid": True,
            "test_executed": run_test,
            "test_passed": test_passed,
            "issues": issues,
            "warnings": warnings
        }

    def verify_text_deliverable(self, text: str, required_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Validates non-code deliverables (reports, specifications, research notes).
        """
        issues: List[str] = []
        warnings: List[str] = []

        if len(text.strip()) < 50:
            issues.append("Deliverable text is suspiciously short (< 50 characters).")

        # Check for hallucinated placeholder brackets
        placeholders = re.findall(r"\{[A-Z_]{3,}\}", text)
        if placeholders:
            warnings.append(f"Unresolved template placeholders detected: {', '.join(set(placeholders))}")

        # Check required keywords
        if required_keywords:
            for kw in required_keywords:
                if kw.lower() not in text.lower():
                    warnings.append(f"Expected keyword/section '{kw}' not found in deliverable.")

        status = "VERIFIED" if not issues and not warnings else ("NEEDS_REVIEW" if not issues else "FAILED")
        grade = "A" if status == "VERIFIED" else ("B" if status == "NEEDS_REVIEW" else "F")

        return {
            "status": status,
            "grade": grade,
            "issues": issues,
            "warnings": warnings,
            "length_characters": len(text)
        }
