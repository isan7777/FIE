"""
Unit tests for FIE Verification Engine.
"""

import unittest
from fie.verification.engine import VerificationEngine

class TestVerificationEngine(unittest.TestCase):

    def setUp(self):
        self.verifier = VerificationEngine()

    def test_valid_python_syntax(self):
        code = "def add(a: int, b: int) -> int:\n    return a + b"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["status"], "SYNTAX_PASSED")
        self.assertTrue(result["syntax_valid"])
        self.assertEqual(result["grade"], "A")

    def test_invalid_python_syntax(self):
        code = "def broken(a, b\n    return a +"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["status"], "FAILED")
        self.assertFalse(result["syntax_valid"])
        self.assertEqual(result["grade"], "F")
        self.assertTrue(len(result["issues"]) > 0)

    def test_security_violation_detection(self):
        code = "import os\ndef dangerous(cmd):\n    return eval(cmd)"
        result = self.verifier.verify_python_code(code)
        self.assertEqual(result["grade"], "F")
        has_security_issue = any("[SECURITY]" in iss for iss in result["issues"])
        self.assertTrue(has_security_issue)

    def test_stub_warning_detection(self):
        code = "def calculate_total():\n    # TODO: implement formula\n    pass"
        result = self.verifier.verify_python_code(code)
        self.assertTrue(len(result["warnings"]) > 0)

    def test_dynamic_test_execution(self):
        code = "def multiply(x, y): return x * y"
        test = "assert multiply(3, 4) == 12"
        result = self.verifier.verify_python_code(code, run_test=True, test_code=test)
        self.assertEqual(result["status"], "VERIFIED")
        self.assertTrue(result["test_passed"])
        self.assertEqual(result["grade"], "S")

    def test_text_deliverable_verification(self):
        good_text = (
            "# Executive Architectural Report\n"
            "This report outlines the distributed caching layer and system resilience specifications. "
            "All components comply with high-availability guidelines and zero-downtime rollover protocols."
        )
        res = self.verifier.verify_text_deliverable(good_text, required_keywords=["Executive", "caching"])
        self.assertEqual(res["status"], "VERIFIED")

        bad_text = "Short text {UNRESOLVED_PLACEHOLDER}"
        res_bad = self.verifier.verify_text_deliverable(bad_text)
        self.assertTrue(len(res_bad["warnings"]) > 0 or len(res_bad["issues"]) > 0)

    def test_emoji_sticker_detection(self):
        code_with_emoji = "def greet():\n    # Hello world 🚀\n    return 'ok'"
        res = self.verifier.verify_python_code(code_with_emoji)
        has_emoji_warning = any("[STYLE_POLICY]" in w for w in res["warnings"])
        self.assertTrue(has_emoji_warning)

        text_with_emoji = "Laporan Performa Sistem: Semua modul berjalan dengan baik 👍"
        res_text = self.verifier.verify_text_deliverable(text_with_emoji)
        has_text_emoji = any("[STYLE_POLICY]" in w for w in res_text["warnings"])
        self.assertTrue(has_text_emoji)

if __name__ == "__main__":
    unittest.main()
