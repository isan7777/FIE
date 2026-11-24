"""
Self-Verification & Quality Engine for Frontier Intelligence Engine (FIE).
Inspects code, markdown with embedded code blocks, and text deliverables across syntax,
completeness, security, natural language style (anti-poetic/anti-brochure), and execution
status to prevent false claims of success.
"""

from typing import Any, Dict, List, Optional
import ast
import re
import subprocess
import sys
import logging

logger = logging.getLogger("fie.verification")

class VerificationEngine:
    """Evaluates deliverables against formal quality rubrics."""

    DANGEROUS_PATTERNS = [
        (r"\beval\s*\(", "Use of 'eval()' is prohibited due to arbitrary code injection risks."),
        (r"\bexec\s*\(", "Use of 'exec()' is prohibited due to security risks."),
        (r"os\.system\s*\(", "Use of 'os.system()' is discouraged; use subprocess with parameterized args."),
        (r"__import__\s*\(", "Direct use of '__import__()' bypasses static security analysis."),
        (r"subprocess\.(?:run|Popen|call|check_output)\s*\([^)]*shell\s*=\s*True", "Subprocess execution with 'shell=True' poses command injection risks."),
        (r"(?:api_key|secret_key|password|access_token)\s*=\s*['\"](?:AIza[0-9A-Za-z\-_]{20,}|sk-[0-9A-Za-z]{20,})['\"]", "Hardcoded secret or API key detected in source code.")
    ]

    STUB_PATTERNS = [
        (r"#\s*TODO\b", "Unfinished TODO comment found."),
        (r"//\s*TODO\b", "Unfinished TODO comment found."),
        (r"#\s*FIXME\b", "Unresolved FIXME comment found."),
        (r"#\s*implement here\b", "Placeholder stub found."),
        (r"/\*\s*add logic here\s*\*/", "Placeholder comment block found."),
        (r"raise\s+NotImplementedError", "Unimplemented method detected.")
    ]

    # Overly poetic, melodramatic brochure AI cliches & translationese patterns
    POETIC_CLICHE_PATTERNS = [
        (r"\bdipilih secara saksama\b", "Translationese 'dipilih secara saksama' detected; use natural wording like 'pilihan' or 'rekomendasi'."),
        (r"\bepisentrum\b", "Overly dramatic metaphor 'episentrum' detected; use 'pusat' or direct factual wording."),
        (r"\bketenangan jiwa\b", "Overly poetic phrase 'ketenangan jiwa' detected; describe the actual atmosphere straightforwardly."),
        (r"\bsitus warisan peradaban\b", "Overly bombastic phrase 'situs warisan peradaban' detected; use 'tempat bersejarah' or 'situs budaya'."),
        (r"\bterbentang\b[^.]{0,60}\bseluas ribuan hektar\b", "Overly poetic brochure phrasing 'terbentang ... seluas ribuan hektar' detected; state area/location naturally."),
        (r"\bharmoni yang memukau\b", "Poetic AI cliche 'harmoni yang memukau' detected; use concrete description."),
        (r"\bsimfoni\b", "Poetic metaphor 'simfoni' in non-musical context detected; use plain language."),
        (r"\bpermata tersembunyi\b", "Translationese cliche 'permata tersembunyi' (hidden gem) detected; use natural description."),
        (r"\bmemanjakan (?:mata|indra|lidah)\b", "Brochure cliche 'memanjakan mata/indra' detected; describe concrete qualities instead."),
        (r"\blanskap digital yang\b", "AI cliche 'lanskap digital yang...' detected; state the technical context directly."),
        (r"\bmenyelami lebih dalam\b", "Translationese cliche 'menyelami lebih dalam' (delving deeper) detected; use 'membahas' or 'memeriksa'.")
    ]

    # Regex pattern to detect emojis and decorative sticker characters
    EMOJI_PATTERN = re.compile(
        r"[\U00010000-\U0010ffff\u2600-\u26ff\u2700-\u27bf\u2300-\u23ff\u2b50-\u2b55\ufe0f]",
        flags=re.UNICODE
    )

    CODE_BLOCK_PATTERN = re.compile(
        r"```(?:python|py)\s*\n(.*?)```",
        flags=re.DOTALL | re.IGNORECASE
    )

    @classmethod
    def extract_python_code_blocks(cls, text: str) -> List[str]:
        """
        Extracts fenced Python code blocks from a markdown deliverable.
        Returns an empty list if no fenced Python blocks are present.
        """
        if not text:
            return []
        matches = cls.CODE_BLOCK_PATTERN.findall(text)
        return [m.strip() for m in matches if m.strip()]

    @classmethod
    def sanitize_emojis(cls, text: str) -> str:
        """Removes all emoji and decorative sticker characters from text or code."""
        if not text:
            return ""
        return cls.EMOJI_PATTERN.sub("", text)

    def check_natural_language_style(self, text: str) -> List[str]:
        """
        Inspects text or code string literals for overly poetic brochure cliches and translationese.
        """
        style_warnings: List[str] = []
        for pattern, msg in self.POETIC_CLICHE_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                style_warnings.append(f"[STYLE_POLICY] {msg}")
        return style_warnings

    def verify_python_code(
        self,
        code_str: str,
        run_test: bool = False,
        test_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validates Python code for syntax, completeness, security, natural language style,
        and optional runtime execution.
        """
        issues: List[str] = []
        warnings: List[str] = []
        status: str = "UNTESTED"

        target_code = code_str.strip()
        fenced_blocks = self.extract_python_code_blocks(target_code)
        if fenced_blocks and target_code.startswith("```"):
            target_code = "\n\n".join(fenced_blocks)

        # 1. AST Syntax Check
        try:
            tree = ast.parse(target_code)
            status = "SYNTAX_PASSED"
        except SyntaxError as e:
            if fenced_blocks:
                combined_blocks = "\n\n".join(fenced_blocks)
                try:
                    tree = ast.parse(combined_blocks)
                    target_code = combined_blocks
                    status = "SYNTAX_PASSED"
                except SyntaxError as inner_e:
                    return {
                        "status": "FAILED",
                        "grade": "F",
                        "syntax_valid": False,
                        "issues": [f"Syntax Error on line {inner_e.lineno}: {inner_e.msg}"],
                        "warnings": []
                    }
            else:
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

        # 4. Style Policies: Zero Emoji & Anti-Poetic Natural Language
        if self.EMOJI_PATTERN.search(code_str):
            warnings.append("[STYLE_POLICY] Emoji/sticker detected in code. Use clean professional text.")

        warnings.extend(self.check_natural_language_style(code_str))

        # AST structural inspections: empty functions and silent bare except handlers
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    warnings.append(f"[COMPLETENESS] Function '{node.name}' contains only 'pass'.")
                elif (
                    len(node.body) == 2
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(getattr(node.body[0], "value", None), ast.Constant)
                    and isinstance(node.body[1], ast.Pass)
                ):
                    warnings.append(f"[COMPLETENESS] Function '{node.name}' contains only a docstring and 'pass'.")
            elif isinstance(node, ast.ExceptHandler):
                if node.type is None and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    warnings.append("[QUALITY] Bare 'except: pass' detected; handle specific exceptions explicitly.")

        # 5. Optional Dynamic Test Execution
        test_passed = False
        if run_test and test_code:
            try:
                full_script = f"{target_code}\n\n# --- TEST RUNNER ---\n{test_code}"
                res = subprocess.run(
                    [sys.executable, "-c", full_script],
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
        Validates non-code deliverables (reports, specifications, UI copy, research notes).
        """
        issues: List[str] = []
        warnings: List[str] = []

        if len(text.strip()) < 50:
            issues.append("Deliverable text is suspiciously short (< 50 characters).")

        # Check for hallucinated placeholder brackets
        placeholders = re.findall(r"\{[A-Z_]{3,}\}", text)
        if placeholders:
            warnings.append(f"Unresolved template placeholders detected: {', '.join(sorted(set(placeholders)))}")

        # Check for emojis/stickers in text
        if self.EMOJI_PATTERN.search(text):
            warnings.append("[STYLE_POLICY] Emoji/sticker detected in deliverable. Use clean editorial text.")

        # Check for overly poetic / brochure AI phrasing
        warnings.extend(self.check_natural_language_style(text))

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

    def verify_deliverable(
        self,
        content: str,
        run_test: bool = False,
        test_code: Optional[str] = None,
        required_keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Unified deliverable verifier that inspects pure Python files, mixed Markdown with
        fenced Python code blocks, or structured text reports.
        """
        stripped = content.strip()
        fenced_blocks = self.extract_python_code_blocks(stripped)

        if fenced_blocks:
            combined_code = "\n\n".join(fenced_blocks)
            code_res = self.verify_python_code(combined_code, run_test=run_test, test_code=test_code)
            text_res = self.verify_text_deliverable(stripped, required_keywords=required_keywords)

            merged_issues = list(dict.fromkeys(code_res["issues"] + text_res["issues"]))
            merged_warnings = list(dict.fromkeys(code_res["warnings"] + text_res["warnings"]))

            if code_res["status"] == "FAILED" or text_res["status"] == "FAILED" or merged_issues:
                status = "FAILED"
                grade = "F"
            elif merged_warnings:
                status = "NEEDS_REVIEW" if code_res["status"] != "SYNTAX_PASSED" else "SYNTAX_PASSED"
                grade = "B"
            else:
                status = code_res["status"]
                grade = code_res["grade"]

            return {
                "status": status,
                "grade": grade,
                "deliverable_type": "markdown_with_python",
                "code_blocks_count": len(fenced_blocks),
                "syntax_valid": code_res["syntax_valid"],
                "test_executed": code_res.get("test_executed", False),
                "test_passed": code_res.get("test_passed", False),
                "issues": merged_issues,
                "warnings": merged_warnings
            }

        looks_like_python = (
            stripped.startswith(("def ", "class ", "import ", "from ", "@", "\"\"\"", "'''"))
            or "\ndef " in stripped
            or "\nclass " in stripped
        )
        if looks_like_python:
            res = self.verify_python_code(stripped, run_test=run_test, test_code=test_code)
            res["deliverable_type"] = "python_code"
            return res

        res = self.verify_text_deliverable(stripped, required_keywords=required_keywords)
        res["deliverable_type"] = "text_report"
        return res
